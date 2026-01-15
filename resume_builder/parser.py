"""
Job Description Parser - Extracts key information from job postings
Parses requirements, skills, technologies, and responsibilities
"""
import re
from typing import List, Dict, Tuple
from .models import JobDescription


class JobDescriptionParser:
    """Parses job descriptions to extract structured data"""
    
    # Common data engineering skills and technologies
    COMMON_DE_SKILLS = {
        'python', 'sql', 'spark', 'hadoop', 'etl', 'java', 'scala',
        'airflow', 'kafka', 'flink', 'aws', 'gcp', 'azure',
        'snowflake', 'bigquery', 'redshift', 'postgresql', 'mongodb',
        'docker', 'kubernetes', 'git', 'jenkins', 'tableau', 'looker',
        'pandas', 'numpy', 'airflow', 'luigi', 'dbt', 'databricks',
        'delta lake', 'parquet', 'json', 'protobuf', 'avro',
        'ci/cd', 'terraform', 'linux', 'bash', 'scala', 'hive'
    }
    
    EXPERIENCE_LEVELS = ['entry-level', 'junior', 'mid-level', 'senior', 'lead', 'principal']
    
    def __init__(self):
        self.extracted_skills: List[str] = []
        self.extracted_technologies: List[str] = []
    
    def parse(self, 
              job_title: str,
              company: str,
              description: str) -> JobDescription:
        """
        Parse job description and extract structured information
        
        Args:
            job_title: Title of the position
            company: Company name
            description: Full job description text
            
        Returns:
            JobDescription object with extracted data
        """
        required_skills = self._extract_required_skills(description)
        preferred_skills = self._extract_preferred_skills(description)
        key_technologies = self._extract_technologies(description)
        responsibilities = self._extract_responsibilities(description)
        experience_level = self._extract_experience_level(description)
        years_required = self._extract_years_of_experience(description)
        
        return JobDescription(
            job_title=job_title,
            company=company,
            description=description,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            key_technologies=key_technologies,
            responsibilities=responsibilities,
            experience_level=experience_level,
            years_of_experience_required=years_required
        )
    
    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract skills listed as required"""
        required_patterns = [
            r'must have[\s\S]*?:(.+?)(?=\n\n|(?i:preferred|nice to have))',
            r'required skills?[\s\S]*?:(.+?)(?=\n\n|(?i:preferred|nice to have))',
            r'what we\'re looking for[\s\S]*?:(.+?)(?=\n\n|(?i:preferred|nice to have))',
        ]
        
        skills = []
        for pattern in required_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                skills_text = match.group(1)
                skills.extend(self._parse_skill_list(skills_text))
        
        # If no explicit required section, extract all mentioned skills
        if not skills:
            skills = self._extract_mentioned_skills(text)
        
        return list(set([s.lower() for s in skills]))
    
    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract skills listed as preferred or nice-to-have"""
        preferred_patterns = [
            r'(?i:preferred|nice to have)[\s\S]*?:(.+?)(?=\n\n|(?i:responsibilities|about|requirements))',
            r'(?i:nice to have skills?)[\s\S]*?:(.+?)(?=\n\n)',
        ]
        
        skills = []
        for pattern in preferred_patterns:
            match = re.search(pattern, text)
            if match:
                skills_text = match.group(1)
                skills.extend(self._parse_skill_list(skills_text))
        
        return list(set([s.lower() for s in skills]))
    
    def _extract_mentioned_skills(self, text: str) -> List[str]:
        """Extract skills mentioned anywhere in the text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.COMMON_DE_SKILLS:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _parse_skill_list(self, text: str) -> List[str]:
        """Parse a comma or bullet separated list of skills"""
        # Remove bullets and extra whitespace
        text = re.sub(r'^[\s\-\•]*', '', text, flags=re.MULTILINE)
        
        # Split by comma or newline
        items = re.split(r'[,\n]', text)
        
        skills = []
        for item in items:
            # Clean up
            skill = item.strip()
            skill = re.sub(r'^[\-\•]*', '', skill).strip()
            
            # Extract just the skill name (before parentheses or additional info)
            skill = re.split(r'[\(\[]', skill)[0].strip()
            
            if skill and len(skill) > 2:
                skills.append(skill)
        
        return skills
    
    def _extract_technologies(self, text: str) -> List[str]:
        """Extract technology stack mentioned"""
        tech_keywords = {
            'spark', 'hadoop', 'kafka', 'flink', 'airflow', 'luigi', 'dbt',
            'snowflake', 'bigquery', 'redshift', 'databricks', 'delta',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'python', 'scala', 'java', 'sql', 'bash',
            'postgresql', 'mongodb', 'cassandra', 'hbase',
            'tableau', 'looker', 'power bi', 'grafana',
            'jenkins', 'terraform', 'git', 'gitlab', 'github'
        }
        
        text_lower = text.lower()
        found_tech = []
        
        for tech in tech_keywords:
            if tech in text_lower:
                found_tech.append(tech)
        
        return found_tech
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract key responsibilities"""
        responsibility_patterns = [
            r'(?i:responsibilities?)[\s\S]*?:(.+?)(?=\n\n|(?i:requirements|qualifications))',
            r'(?i:you will?)[\s\S]*?:?(.+?)(?=\n\n|(?i:requirements))',
        ]
        
        responsibilities = []
        for pattern in responsibility_patterns:
            match = re.search(pattern, text)
            if match:
                resp_text = match.group(1)
                items = re.split(r'[\n]', resp_text)
                for item in items:
                    item = re.sub(r'^[\s\-\•]*', '', item).strip()
                    if item and len(item) > 10:
                        responsibilities.append(item)
        
        return responsibilities[:5]  # Limit to top 5
    
    def _extract_experience_level(self, text: str) -> str:
        """Determine experience level required"""
        text_lower = text.lower()
        
        for level in ['principal', 'lead', 'senior', 'mid-level', 'intermediate', 'junior', 'entry-level']:
            if level in text_lower:
                return level.replace('intermediate', 'mid-level')
        
        return 'mid-level'  # Default
    
    def _extract_years_of_experience(self, text: str) -> int:
        """Extract years of experience required"""
        # Look for patterns like "3+ years", "3-5 years", etc.
        patterns = [
            r'(\d+)\s*\+?\s*years?\s+of\s+(?:experience|working)',
            r'(\d+)\s*-\s*(\d+)\s+years?\s+of',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    return int(match.group(1))  # Return the minimum
                else:
                    return int(match.group(1))
        
        return 0  # Default
