"""
Gmail Integration - Monitors Gmail account for job postings
Handles Gmail API authentication and email streaming
"""
import base64
import re
from typing import List, Dict, Optional, Generator
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle
import os


class GmailStreamingService:
    """Handles Gmail API integration for monitoring job postings"""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, credentials_path: str = 'credentials.json', token_path: str = 'token.pickle'):
        """
        Initialize Gmail API client
        
        Args:
            credentials_path: Path to OAuth2 credentials file
            token_path: Path to store OAuth2 token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token_file:
                creds = pickle.load(token_file)
        
        # Create new token if needed
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save token for future use
            with open(self.token_path, 'wb') as token_file:
                pickle.dump(creds, token_file)
        
        return build('gmail', 'v1', credentials=creds)
    
    def get_recent_emails(self, max_results: int = 10, query: str = '') -> List[Dict]:
        """
        Retrieve recent emails
        
        Args:
            max_results: Maximum number of emails to retrieve
            query: Gmail search query filter
            
        Returns:
            List of email dictionaries
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                email_data = self._get_email_details(message['id'])
                if email_data:
                    emails.append(email_data)
            
            return emails
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    def stream_job_posting_emails(self, query: str = '', poll_interval: int = 60) -> Generator:
        """
        Stream job posting emails continuously
        
        Args:
            query: Gmail search query (e.g., 'from:recruiters@example.com')
            poll_interval: Poll interval in seconds
            
        Yields:
            Email dictionaries as they arrive
        """
        import time
        last_check_timestamp = None
        
        while True:
            try:
                search_query = query
                if last_check_timestamp:
                    # Only get new emails since last check
                    search_query += f' after:{last_check_timestamp}'
                
                emails = self.get_recent_emails(max_results=5, query=search_query)
                
                for email in emails:
                    yield email
                    last_check_timestamp = email.get('timestamp', int(time.time()))
                
                time.sleep(poll_interval)
            
            except Exception as e:
                print(f'Error in email streaming: {e}')
                time.sleep(poll_interval)
    
    def _get_email_details(self, message_id: str) -> Optional[Dict]:
        """Extract email content and metadata"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            email_data = {
                'id': message_id,
                'timestamp': int(message['internalDate']) // 1000
            }
            
            # Extract header information
            for header in headers:
                if header['name'] == 'From':
                    email_data['from'] = header['value']
                elif header['name'] == 'Subject':
                    email_data['subject'] = header['value']
                elif header['name'] == 'Date':
                    email_data['date'] = header['value']
            
            # Extract body
            body_content = self._get_email_body(message['payload'])
            email_data['body'] = body_content
            
            return email_data
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
    
    def _get_email_body(self, payload: Dict) -> str:
        """Extract email body from payload"""
        if 'parts' in payload:
            # Multipart message
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        data = part['body']['data']
                        return base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            # Simple message
            if 'body' in payload and 'data' in payload['body']:
                data = payload['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
        
        return ''


class EmailJobPostingDetector:
    """Detects if an email is a job posting"""
    
    # Keywords commonly found in job postings
    JOB_POSTING_KEYWORDS = {
        'job posting', 'job opening', 'job opportunity', 'we are hiring',
        'hiring', 'position', 'job title', 'job description', 'apply now',
        'requirements', 'responsibilities', 'qualifications', 'salary',
        'work location', 'employment type', 'urgently hiring', 'vacancy',
        'opportunity for', 'role:', 'title:', 'looking for', 'seeking',
        'technical skills', 'required skills', 'must have', 'must haves',
        'years of experience', 'experience required', 'we are looking for',
        'job posting', 'technical hiring', 'contract', 'minimum years',
        'work location with zip', 'kindly respond', 'speed up the interview'
    }
    
    # Data engineering related keywords
    DATA_ENGINEERING_KEYWORDS = {
        'data engineer', 'data architect', 'etl', 'data pipeline',
        'spark', 'hadoop', 'kafka', 'airflow', 'snowflake', 'redshift',
        'bigquery', 'sql', 'python', 'scala', 'data warehouse',
        'data lake', 'pyspark', 'dbt', 'luigi', 'tableau',
        'power bi', 'databricks', 'aws glue', 'azure data factory',
        'data modeling', 'database design', 'etl pipeline', 'streaming',
        'batch processing', 'data integration', 'data migration',
        'lead data engineer', 'senior data engineer', 'architect',
        'big data', 'hdfs', 'hive', 'cassandra', 'mongodb'
    }
    
    def __init__(self, job_posting_threshold: float = 0.3):
        """
        Initialize detector
        
        Args:
            job_posting_threshold: Confidence threshold for job posting detection
        """
        self.job_posting_threshold = job_posting_threshold
    
    def is_job_posting(self, email_subject: str, email_body: str) -> tuple[bool, float]:
        """
        Determine if email is a job posting
        
        Args:
            email_subject: Email subject line
            email_body: Email body content
            
        Returns:
            Tuple of (is_job_posting, confidence_score)
        """
        combined_text = (email_subject + ' ' + email_body).lower()
        
        # Count job posting keywords
        job_keyword_count = sum(
            1 for keyword in self.JOB_POSTING_KEYWORDS 
            if keyword in combined_text
        )
        
        # Calculate confidence - normalize by total keywords
        confidence = job_keyword_count / max(len(self.JOB_POSTING_KEYWORDS), 1)
        
        is_posting = confidence >= self.job_posting_threshold or job_keyword_count >= 3
        
        return is_posting, confidence * 100
    
    def is_data_engineering_role(self, email_subject: str, email_body: str) -> tuple[bool, float]:
        """
        Determine if job posting is for data engineering role
        
        Args:
            email_subject: Email subject line
            email_body: Email body content
            
        Returns:
            Tuple of (is_data_engineering, confidence_score)
        """
        combined_text = (email_subject + ' ' + email_body).lower()
        
        # Count data engineering keywords
        de_keyword_count = sum(
            1 for keyword in self.DATA_ENGINEERING_KEYWORDS 
            if keyword in combined_text
        )
        
        # Calculate confidence
        confidence = de_keyword_count / max(len(self.DATA_ENGINEERING_KEYWORDS), 1)
        
        return de_keyword_count >= 2 or confidence > 0.1, confidence * 100
    
    def extract_job_metadata(self, email_subject: str, email_body: str) -> Dict:
        """
        Extract key metadata from job posting email
        
        Args:
            email_subject: Email subject line
            email_body: Email body content
            
        Returns:
            Dictionary with extracted metadata
        """
        text = email_subject + ' ' + email_body
        metadata = {}
        
        # Extract job title from subject or body
        job_title_patterns = [
            r'(?:job title|title|position)[\s:]*([^\n]+)',
            r'(?:lead|senior|junior)?\s*(data engineer|data architect|architect)[^\n]*'
        ]
        for pattern in job_title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metadata['job_title'] = match.group(1).strip()
                break
        
        # Extract company from subject or body
        company_patterns = [
            r'from\s+([A-Z][^\n]+?)(?:\s+\(|$)',
            r'at\s+([A-Z][^\n]+?)(?:\s+|$)'
        ]
        for pattern in company_patterns:
            match = re.search(pattern, text)
            if match:
                metadata['company'] = match.group(1).strip()
                break
        
        # Extract work location
        location_pattern = r'(?:location|city|zip)[\s:]*([^\n]+)'
        match = re.search(location_pattern, text, re.IGNORECASE)
        if match:
            metadata['location'] = match.group(1).strip()
        
        # Extract years of experience requirement
        exp_pattern = r'(\d+)\s*\+?\s*years?\s+of\s+experience'
        match = re.search(exp_pattern, text, re.IGNORECASE)
        if match:
            metadata['years_required'] = int(match.group(1))
        
        # Extract key skills/technologies
        skills_pattern = r'(?:required skills?|must have|top \d+ skills?)[\s:]*([^\n]+?)(?=\n|$)'
        match = re.search(skills_pattern, text, re.IGNORECASE)
        if match:
            skills_text = match.group(1)
            metadata['required_skills'] = [s.strip() for s in skills_text.split(',')]
        
        return metadata
