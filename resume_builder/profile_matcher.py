"""
Profile Matcher - Matches job requirements with user profile
Profile Loader - Loads user profile from resume template
"""
from typing import Dict, List, Set, Tuple
from .models import Resume, Skill, Experience, Education
import re


class ProfileMatcher:
    """Matches job requirements with user profile"""
    
    def __init__(self):
        self.min_skill_match_threshold = 0.6  # 60% of required skills
    
    def match_profile_to_job(self, 
                            resume: Resume,
                            job_metadata: Dict,
                            job_description: str) -> Dict:
        """
        Compare job requirements with user profile
        
        Args:
            resume: User's resume
            job_metadata: Extracted job metadata
            job_description: Full job description text
            
        Returns:
            Dictionary with matching results
        """
        results = {
            'overall_match': False,
            'skill_match_percentage': 0,
            'experience_match': False,
            'years_match': False,
            'matched_skills': [],
            'missing_skills': [],
            'matched_experience': [],
            'gaps': []
        }
        
        # Extract required skills from metadata and job description
        required_skills = self._extract_required_skills(job_metadata, job_description)
        
        # Match skills
        skill_match = self._match_skills(resume, required_skills)
        results['matched_skills'] = skill_match['matched']
        results['missing_skills'] = skill_match['missing']
        results['skill_match_percentage'] = skill_match['percentage']
        
        # Check experience level
        years_required = job_metadata.get('years_required', 0)
        experience_match = self._match_experience(resume, years_required)
        results['years_match'] = experience_match['meets_requirement']
        results['experience_match'] = experience_match['has_relevant_experience']
        
        # Identify gaps
        results['gaps'] = self._identify_gaps(resume, job_metadata, job_description)
        
        # Calculate overall match
        results['overall_match'] = (
            results['skill_match_percentage'] >= self.min_skill_match_threshold and
            results['experience_match'] and
            results['years_match']
        )
        
        return results
    
    def _extract_required_skills(self, job_metadata: Dict, job_description: str) -> List[str]:
        """Extract required skills from metadata and job description"""
        required_skills = []
        
        # From metadata
        if 'required_skills' in job_metadata:
            required_skills.extend(job_metadata['required_skills'])
        
        # From job description
        skills_patterns = [
            r'(?:top \d+ required skills?|must have skills?|technical skills?)[\s:]*([^\n]+)',
            r'(?:required skills?|must have)[\s:]*([^\n]+)',
        ]
        
        for pattern in skills_patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                skills_text = match.group(1)
                # Split by comma and/or bullet points
                skills = []
                for s in skills_text.split(','):
                    s = s.strip().lstrip('•-').strip()
                    # Clean up any special characters at the end
                    s = re.sub(r'[^\w\s+#\-]$', '', s)
                    if s and len(s) > 2:
                        skills.append(s.lower())
                required_skills.extend(skills)
        
        # Remove duplicates and clean
        return list(set([s.lower() for s in required_skills if s.strip() and len(s) > 2]))
    
    def _match_skills(self, resume: Resume, required_skills: List[str]) -> Dict:
        """Match resume skills with required skills"""
        resume_skill_names = {s.name.lower() for s in resume.skills}
        required_skills_lower = {s.lower() for s in required_skills}
        
        matched_skills = resume_skill_names.intersection(required_skills_lower)
        missing_skills = required_skills_lower - resume_skill_names
        
        match_percentage = len(matched_skills) / len(required_skills_lower) if required_skills_lower else 0
        
        return {
            'matched': list(matched_skills),
            'missing': list(missing_skills),
            'percentage': match_percentage * 100
        }
    
    def _match_experience(self, resume: Resume, years_required: int) -> Dict:
        """Check if resume has required years of experience"""
        # Calculate total years from experience
        total_years = 0
        relevant_experiences = []
        
        for exp in resume.experience:
            years = self._calculate_duration(exp.start_date, exp.end_date)
            total_years += years
            relevant_experiences.append(exp)
        
        return {
            'meets_requirement': total_years >= years_required,
            'total_years': total_years,
            'years_required': years_required,
            'has_relevant_experience': len(relevant_experiences) > 0
        }
    
    def _calculate_duration(self, start_date: str, end_date: str) -> float:
        """Calculate duration between two dates in years"""
        from datetime import datetime
        
        date_formats = ['%B %Y', '%b %Y', '%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d']
        
        def parse_date(date_str):
            if not date_str or date_str.lower() == 'present':
                return datetime.now()
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            return None
        
        start = parse_date(start_date)
        end = parse_date(end_date) if end_date else datetime.now()
        
        if start and end:
            # Handle case where end date is before start date (typo in resume)
            if end < start:
                end = datetime.now()
            delta = end - start
            years = delta.days / 365.25
            return max(0, years)  # Ensure non-negative
        return 0
    
    def _identify_gaps(self, resume: Resume, job_metadata: Dict, job_description: str) -> List[str]:
        """Identify skill and experience gaps"""
        gaps = []
        
        # Check years requirement
        years_required = job_metadata.get('years_required', 0)
        total_years = sum(
            self._calculate_duration(exp.start_date, exp.end_date) 
            for exp in resume.experience
        )
        
        if total_years < years_required:
            gaps.append(f"Missing {years_required - total_years:.1f} years of experience (need {years_required}, have {total_years:.1f})")
        
        # Check specific skills
        required_skills = self._extract_required_skills(job_metadata, job_description)
        resume_skills = {s.name.lower() for s in resume.skills}
        
        missing = [s for s in required_skills if s.lower() not in resume_skills]
        if missing:
            gaps.append(f"Missing key skills: {', '.join(missing[:3])}")
        
        return gaps


class ProfileLoader:
    """Load user profile from resume template"""
    
    @staticmethod
    def load_profile_from_text(resume_text: str) -> Resume:
        """
        Parse resume text and create Resume object
        
        Args:
            resume_text: Full resume text
            
        Returns:
            Resume object with parsed information
        """
        # Extract contact info
        name = ProfileLoader._extract_name(resume_text)
        email = ProfileLoader._extract_email(resume_text)
        phone = ProfileLoader._extract_phone(resume_text)
        location = ProfileLoader._extract_location(resume_text)
        
        # Extract sections
        professional_summary = ProfileLoader._extract_section(resume_text, 'PROFESSIONAL SUMMARY')
        technical_skills_text = ProfileLoader._extract_section(resume_text, 'TECHNICAL SKILLS')
        
        # Parse skills
        skills = ProfileLoader._parse_skills(technical_skills_text)
        
        # Parse experience
        experience = ProfileLoader._parse_experience(resume_text)
        
        # Parse education
        education = ProfileLoader._parse_education(resume_text)
        
        # Parse certifications
        certifications = ProfileLoader._parse_certifications(resume_text)
        
        return Resume(
            name=name,
            email=email,
            phone=phone,
            location=location,
            professional_summary=professional_summary,
            skills=skills,
            experience=experience,
            education=education,
            certifications=certifications
        )
    
    @staticmethod
    def _extract_name(text: str) -> str:
        """Extract name from resume"""
        lines = text.split('\n')
        if lines:
            return lines[0].strip()
        return "Unknown"
    
    @staticmethod
    def _extract_email(text: str) -> str:
        """Extract email from resume"""
        pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        match = re.search(pattern, text)
        return match.group(0) if match else ""
    
    @staticmethod
    def _extract_phone(text: str) -> str:
        """Extract phone number from resume"""
        pattern = r'\+?1?\s*\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})'
        match = re.search(pattern, text)
        if match:
            return f"+1 {match.group(1)}{match.group(2)}{match.group(3)}"
        return ""
    
    @staticmethod
    def _extract_location(text: str) -> str:
        """Extract location from resume"""
        lines = text.split('\n')
        for line in lines[:5]:
            if 'location' in line.lower() or ',' in line:
                # Try to extract city, state format
                match = re.search(r'([A-Z][a-z]+),\s*([A-Z]{2})', line)
                if match:
                    return f"{match.group(1)}, {match.group(2)}"
        return ""
    
    @staticmethod
    def _extract_section(text: str, section_name: str) -> str:
        """Extract a section of the resume"""
        pattern = f"{section_name}\\s*([\\s\\S]*?)(?=\\n[A-Z][A-Z ]+|$)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match and match.group(1):
            return match.group(1).strip()
        return ""
    
    @staticmethod
    def _parse_skills(skills_text: str) -> List[Skill]:
        """Parse technical skills section"""
        skills = []
        
        lines = skills_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('–') or line.startswith('-'):
                continue
            
            # Handle format like "Programming Languages – Python, Java, SQL"
            if ' – ' in line or ' - ' in line:
                # Split by separator (– or -)
                separator = ' – ' if ' – ' in line else ' - '
                parts = line.split(separator)
                if len(parts) == 2:
                    category = parts[0].strip()
                    skills_str = parts[1]
                else:
                    category = "Technical"
                    skills_str = line
            else:
                category = "Technical"
                skills_str = line
            
            # Split skills by comma
            if ',' in skills_str:
                individual_skills = skills_str.split(',')
            else:
                individual_skills = [skills_str]
            
            for skill_name in individual_skills:
                skill_name = skill_name.strip()
                if skill_name:
                    skills.append(Skill(
                        name=skill_name,
                        proficiency_level="Advanced",
                        category=category
                    ))
        
        return skills
    
    @staticmethod
    def _parse_experience(text: str) -> List[Experience]:
        """Parse professional experience section"""
        experiences = []
        
        # Find experience section
        experience_section = ProfileLoader._extract_section(text, 'PROFESSIONAL EXPERIENCE|WORK EXPERIENCE|EXPERIENCE')
        
        # Split by job entries (typically marked by bold/date patterns)
        job_blocks = re.split(r'\n(?=[A-Z][^|]*?\||\n•|\n-)', experience_section)
        
        for block in job_blocks:
            if not block.strip():
                continue
            
            # Extract job title and company
            title_match = re.search(r'([A-Za-z].*?)\|', block)
            if title_match:
                job_title = title_match.group(1).strip()
                
                # Extract company and dates
                company_match = re.search(r'\|\s*([^|]+?)\s*\|?\s*(.*?)(?:\n|$)', block)
                if company_match:
                    company = company_match.group(1).strip()
                    dates = company_match.group(2).strip()
                    
                    # Extract start and end dates
                    date_parts = dates.split('-') if dates else []
                    start_date = date_parts[0].strip() if date_parts else ""
                    end_date = date_parts[1].strip() if len(date_parts) > 1 else ""
                    
                    # Extract achievements/bullet points
                    achievements = []
                    for line in block.split('\n'):
                        if line.strip().startswith('•') or line.strip().startswith('-'):
                            achievement = line.strip().lstrip('•-').strip()
                            if achievement:
                                achievements.append(achievement)
                    
                    experiences.append(Experience(
                        job_title=job_title,
                        company=company,
                        start_date=start_date,
                        end_date=end_date,
                        achievements=achievements
                    ))
        
        return experiences
    
    @staticmethod
    def _parse_education(text: str) -> List[Education]:
        """Parse education section"""
        educations = []
        
        education_section = ProfileLoader._extract_section(text, 'EDUCATION')
        
        # Split by degree entries
        degree_blocks = re.split(r'\n(?=[A-Z])', education_section)
        
        for block in degree_blocks:
            if not block.strip():
                continue
            
            lines = block.strip().split('\n')
            if lines:
                degree_line = lines[0]
                
                # Extract degree and field
                match = re.search(r"(Master's|Bachelor's|PhD|M\.S\.|B\.S\.|MBA)(?:\s+(?:of|in))?\s+(.+?)(?:\s+in\s+(.+))?$", degree_line)
                if match:
                    degree = match.group(1)
                    field = match.group(3) or match.group(2)
                    
                    # Extract institution and year
                    institution = ""
                    graduation_year = 0
                    
                    if len(lines) > 1:
                        inst_line = lines[1]
                        institution = inst_line.split(',')[0].strip() if ',' in inst_line else inst_line
                        
                        # Extract year
                        year_match = re.search(r'(\d{4})', inst_line)
                        if year_match:
                            graduation_year = int(year_match.group(1))
                    
                    educations.append(Education(
                        degree=degree,
                        field_of_study=field,
                        institution=institution,
                        graduation_year=graduation_year
                    ))
        
        return educations
    
    @staticmethod
    def _parse_certifications(text: str) -> List[str]:
        """Parse certifications section"""
        certifications = []
        
        cert_section = ProfileLoader._extract_section(text, 'CERTIFICATIONS|CERTIFICATES')
        
        for line in cert_section.split('\n'):
            line = line.strip()
            if line and not line.startswith('–') and not line.startswith('-'):
                if line.startswith('•'):
                    line = line[1:].strip()
                certifications.append(line)
        
        return certifications
