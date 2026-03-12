"""
Job Posting Streaming Job - Main orchestrator
Combines all components to monitor emails and generate tailored resumes
"""
import os
from typing import Dict, Optional
from datetime import datetime
from .models import Resume
from .gmail_integration import GmailStreamingService, EmailJobPostingDetector
from .profile_matcher import ProfileMatcher, ProfileLoader
from .word_exporter import create_tailored_resume_word
from . import ResumeBuilder


class JobPostingStreamingJob:
    """Main job that orchestrates the entire process"""
    
    def __init__(self, 
                 resume_template_path: str,
                 output_directory: str = None,
                 gmail_credentials_path: str = 'credentials.json'):
        """
        Initialize the streaming job
        
        Args:
            resume_template_path: Path to the resume template text file
            output_directory: Directory to save generated resumes (default: current directory)
            gmail_credentials_path: Path to Gmail API credentials
        """
        self.resume_template_path = resume_template_path
        self.output_directory = output_directory or os.path.expanduser('~/Resume_Generator_Output')
        self.gmail_credentials_path = gmail_credentials_path
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_directory, exist_ok=True)
        
        # Initialize components
        self.resume_builder = ResumeBuilder()
        self.profile_matcher = ProfileMatcher()
        self.detector = EmailJobPostingDetector()
        
        # Load user profile from template
        self.user_profile = self._load_user_profile()
        
        print(f"✓ Initialized streaming job for {self.user_profile.name}")
        print(f"✓ Output directory: {self.output_directory}")
    
    def _load_user_profile(self) -> Resume:
        """Load user profile from resume template"""
        print(f"Loading resume template from {self.resume_template_path}...")
        
        with open(self.resume_template_path, 'r', encoding='utf-8') as f:
            resume_text = f.read()
        
        profile = ProfileLoader.load_profile_from_text(resume_text)
        print(f"✓ Loaded profile: {profile.name} with {len(profile.skills)} skills")
        return profile
    
    def start_streaming(self, poll_interval: int = 60):
        """
        Start streaming job postings from Gmail
        
        Args:
            poll_interval: Polling interval in seconds
        """
        print(f"\nStarting email streaming (polling every {poll_interval}s)...")
        
        try:
            gmail_service = GmailStreamingService(self.gmail_credentials_path)
            
            for email in gmail_service.stream_job_posting_emails(poll_interval=poll_interval):
                self.process_email(email)
        
        except Exception as e:
            print(f"Error in streaming job: {e}")
            raise
    
    def process_email(self, email: Dict) -> Optional[Dict]:
        """
        Process a single email and generate resume if it's a matching job posting
        
        Args:
            email: Email dictionary with 'from', 'subject', and 'body' keys
            
        Returns:
            Processing result dictionary or None
        """
        print(f"\n{'='*60}")
        print(f"Processing email from: {email.get('from', 'Unknown')}")
        print(f"Subject: {email.get('subject', 'No subject')}")
        
        result = {
            'email': email,
            'timestamp': datetime.now().isoformat(),
            'is_job_posting': False,
            'is_data_engineering': False,
            'matches_profile': False,
            'resume_path': None
        }
        
        # Check if it's a job posting
        is_posting, posting_confidence = self.detector.is_job_posting(
            email.get('subject', ''),
            email.get('body', '')
        )
        
        print(f"Job posting detection: {is_posting} (confidence: {posting_confidence:.1%})")
        result['is_job_posting'] = is_posting
        
        if not is_posting:
            print("❌ Not a job posting, skipping...")
            return result
        
        # Check if it's data engineering related
        is_de_role, de_confidence = self.detector.is_data_engineering_role(
            email.get('subject', ''),
            email.get('body', '')
        )
        
        print(f"Data engineering role detection: {is_de_role} (confidence: {de_confidence:.1%})")
        result['is_data_engineering'] = is_de_role
        
        if not is_de_role:
            print("⚠ Not a data engineering role, skipping...")
            return result
        
        # Extract job metadata
        job_metadata = self.detector.extract_job_metadata(
            email.get('subject', ''),
            email.get('body', '')
        )
        
        print(f"Extracted job details:")
        print(f"  - Job Title: {job_metadata.get('job_title', 'Unknown')}")
        print(f"  - Company: {job_metadata.get('company', 'Unknown')}")
        print(f"  - Location: {job_metadata.get('location', 'Unknown')}")
        print(f"  - Years Required: {job_metadata.get('years_required', 'Unknown')}")
        
        # Match with profile
        match_result = self.profile_matcher.match_profile_to_job(
            self.user_profile,
            job_metadata,
            email.get('body', '')
        )
        
        print(f"\nProfile matching:")
        print(f"  - Skill match: {match_result['skill_match_percentage']:.1f}%")
        print(f"  - Experience match: {match_result['experience_match']}")
        print(f"  - Years requirement: {match_result['years_match']}")
        print(f"  - Overall match: {match_result['overall_match']}")
        
        if match_result['gaps']:
            print(f"  - Gaps: {', '.join(match_result['gaps'])}")
        
        result['matches_profile'] = match_result['overall_match']
        result['match_details'] = match_result
        
        if not match_result['overall_match']:
            print("⚠ Profile doesn't meet minimum requirements, skipping...")
            return result
        
        # Generate personalized resume
        print(f"\n📄 Generating personalized resume...")
        try:
            resume_path = self._generate_resume(
                email,
                job_metadata,
                match_result
            )
            
            result['resume_path'] = resume_path
            print(f"✓ Resume saved to: {resume_path}")
        
        except Exception as e:
            print(f"❌ Error generating resume: {e}")
            result['error'] = str(e)
        
        return result
    
    def _generate_resume(self, 
                        email: Dict,
                        job_metadata: Dict,
                        match_result: Dict) -> str:
        """
        Generate a personalized resume for the job posting
        
        Args:
            email: Email dictionary
            job_metadata: Extracted job metadata
            match_result: Profile matching results
            
        Returns:
            Path to the generated resume file
        """
        job_title = job_metadata.get('job_title', 'Data Engineer')
        company = job_metadata.get('company', 'Unknown Company')
        job_description = email.get('body', '')
        
        # Use resume builder to personalize
        personalized_resume = self.resume_builder.personalize(
            self.user_profile,
            job_description,
            job_title,
            company
        )
        
        # Generate filename with timestamp and company name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"Resume_{company}_{job_title}_{timestamp}.docx"
        filename = filename.replace(' ', '_').replace('/', '_')
        
        output_path = os.path.join(self.output_directory, filename)
        
        # Export to Word document
        create_tailored_resume_word(
            personalized_resume,
            output_path,
            include_matching_score=True
        )
        
        return output_path
    
    def process_single_email_text(self, 
                                  subject: str,
                                  body: str,
                                  from_address: str = 'test@example.com') -> Dict:
        """
        Process a single email from text (useful for testing)
        
        Args:
            subject: Email subject
            body: Email body
            from_address: Sender email address
            
        Returns:
            Processing result dictionary
        """
        email = {
            'from': from_address,
            'subject': subject,
            'body': body
        }
        
        return self.process_email(email)


def create_job_streaming_instance(resume_template_path: str,
                                  output_directory: str = None,
                                  gmail_credentials_path: str = 'credentials.json') -> JobPostingStreamingJob:
    """
    Convenience function to create a job streaming instance
    
    Args:
        resume_template_path: Path to resume template
        output_directory: Output directory for resumes
        gmail_credentials_path: Path to Gmail credentials
        
    Returns:
        JobPostingStreamingJob instance
    """
    return JobPostingStreamingJob(
        resume_template_path=resume_template_path,
        output_directory=output_directory,
        gmail_credentials_path=gmail_credentials_path
    )
