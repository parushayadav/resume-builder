"""
Data models for Resume Builder
Defines structures for Resume, JobDescription, Skills, and Experience
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class Skill:
    """Represents a single skill"""
    name: str
    proficiency_level: str  # Beginner, Intermediate, Advanced, Expert
    years_of_experience: float = 0
    keywords: List[str] = field(default_factory=list)
    category: str = ""  # Technical, Soft, Domain
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "proficiency_level": self.proficiency_level,
            "years_of_experience": self.years_of_experience,
            "keywords": self.keywords,
            "category": self.category
        }


@dataclass
class Experience:
    """Represents work experience or project"""
    job_title: str
    company: str
    start_date: str
    end_date: Optional[str] = None
    description: str = ""
    achievements: List[str] = field(default_factory=list)
    skills_used: List[str] = field(default_factory=list)
    is_current: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "job_title": self.job_title,
            "company": self.company,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "achievements": self.achievements,
            "skills_used": self.skills_used,
            "is_current": self.is_current
        }


@dataclass
class Education:
    """Represents educational background"""
    degree: str
    field_of_study: str
    institution: str
    graduation_year: int
    gpa: Optional[float] = None
    relevant_coursework: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "degree": self.degree,
            "field_of_study": self.field_of_study,
            "institution": self.institution,
            "graduation_year": self.graduation_year,
            "gpa": self.gpa,
            "relevant_coursework": self.relevant_coursework
        }


@dataclass
class Resume:
    """Complete resume structure"""
    name: str
    email: str
    phone: str
    location: str
    professional_summary: str = ""
    skills: List[Skill] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    portfolio_links: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "professional_summary": self.professional_summary,
            "skills": [s.to_dict() for s in self.skills],
            "experience": [e.to_dict() for e in self.experience],
            "education": [ed.to_dict() for ed in self.education],
            "certifications": self.certifications,
            "portfolio_links": self.portfolio_links
        }


@dataclass
class JobDescription:
    """Parsed job description"""
    job_title: str
    company: str
    description: str
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    experience_level: str = "Mid-level"  # Entry-level, Mid-level, Senior
    years_of_experience_required: int = 0
    responsibilities: List[str] = field(default_factory=list)
    key_technologies: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "job_title": self.job_title,
            "company": self.company,
            "description": self.description,
            "required_skills": self.required_skills,
            "preferred_skills": self.preferred_skills,
            "experience_level": self.experience_level,
            "years_of_experience_required": self.years_of_experience_required,
            "responsibilities": self.responsibilities,
            "key_technologies": self.key_technologies
        }


@dataclass
class PersonalizedResume:
    """Resume customized for a specific job"""
    original_resume: Resume
    target_job: JobDescription
    personalized_summary: str = ""
    prioritized_experience: List[Experience] = field(default_factory=list)
    matched_skills: List[Skill] = field(default_factory=list)
    relevance_score: float = 0.0  # 0-100
    missing_skills: List[str] = field(default_factory=list)
    highlighted_achievements: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "original_resume": self.original_resume.to_dict(),
            "target_job": self.target_job.to_dict(),
            "personalized_summary": self.personalized_summary,
            "prioritized_experience": [e.to_dict() for e in self.prioritized_experience],
            "matched_skills": [s.to_dict() for s in self.matched_skills],
            "relevance_score": self.relevance_score,
            "missing_skills": self.missing_skills,
            "highlighted_achievements": self.highlighted_achievements
        }
