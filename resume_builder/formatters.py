"""
Resume Formatters - Output resume in different formats
Supports JSON, Markdown, and plain text formats
"""
import json
from typing import Dict, Any
from .models import PersonalizedResume, Resume


class ResumeFormatter:
    """Base formatter class"""
    
    def format(self, resume: PersonalizedResume) -> str:
        raise NotImplementedError


class JSONFormatter(ResumeFormatter):
    """Format resume as JSON"""
    
    def format(self, resume: PersonalizedResume) -> str:
        """Convert resume to JSON string"""
        return json.dumps(resume.to_dict(), indent=2)


class MarkdownFormatter(ResumeFormatter):
    """Format resume as Markdown"""
    
    def format(self, resume: PersonalizedResume) -> str:
        """Convert resume to Markdown format"""
        lines = []
        
        # Header
        r = resume.original_resume
        lines.append(f"# {r.name}")
        lines.append(f"\n**{resume.target_job.job_title}** @ {resume.target_job.company}")
        lines.append(f"\nRelevance Score: **{resume.relevance_score:.1f}%**\n")
        
        # Contact Info
        lines.append("## Contact Information")
        lines.append(f"- Email: {r.email}")
        lines.append(f"- Phone: {r.phone}")
        lines.append(f"- Location: {r.location}")
        
        # Personalized Summary
        if resume.personalized_summary:
            lines.append("\n## Professional Summary")
            lines.append(resume.personalized_summary)
        
        # Matched Skills
        if resume.matched_skills:
            lines.append("\n## Key Skills (Matched to Job)")
            for skill in resume.matched_skills:
                lines.append(f"- **{skill.name}** ({skill.proficiency_level})")
        
        # Missing Skills (for awareness)
        if resume.missing_skills:
            lines.append("\n## Skills to Develop")
            for skill in resume.missing_skills[:5]:
                lines.append(f"- {skill}")
        
        # Prioritized Experience
        if resume.prioritized_experience:
            lines.append("\n## Work Experience")
            for exp in resume.prioritized_experience:
                lines.append(f"\n### {exp.job_title}")
                lines.append(f"**{exp.company}** | {exp.start_date} - {exp.end_date or 'Present'}")
                if exp.description:
                    lines.append(f"\n{exp.description}\n")
                
                if exp.achievements:
                    lines.append("**Achievements:**")
                    for achievement in exp.achievements:
                        lines.append(f"- {achievement}")
        
        # Education
        if r.education:
            lines.append("\n## Education")
            for edu in r.education:
                lines.append(f"- **{edu.degree}** in {edu.field_of_study}")
                lines.append(f"  - {edu.institution}, {edu.graduation_year}")
        
        # Certifications
        if r.certifications:
            lines.append("\n## Certifications")
            for cert in r.certifications:
                lines.append(f"- {cert}")
        
        # Portfolio
        if r.portfolio_links:
            lines.append("\n## Portfolio & Projects")
            for name, link in r.portfolio_links.items():
                lines.append(f"- [{name}]({link})")
        
        # Highlighted Achievements
        if resume.highlighted_achievements:
            lines.append("\n## Key Achievements for This Role")
            for achievement in resume.highlighted_achievements:
                lines.append(f"- {achievement}")
        
        return "\n".join(lines)


class PlainTextFormatter(ResumeFormatter):
    """Format resume as plain text"""
    
    def format(self, resume: PersonalizedResume) -> str:
        """Convert resume to plain text format"""
        lines = []
        
        r = resume.original_resume
        
        # Header
        lines.append("=" * 80)
        lines.append(r.name.center(80))
        lines.append("=" * 80)
        
        # Job context
        lines.append(f"\nTARGET POSITION: {resume.target_job.job_title} @ {resume.target_job.company}")
        lines.append(f"RELEVANCE SCORE: {resume.relevance_score:.1f}%\n")
        
        # Contact
        lines.append("-" * 80)
        lines.append("CONTACT INFORMATION")
        lines.append("-" * 80)
        lines.append(f"Email: {r.email}")
        lines.append(f"Phone: {r.phone}")
        lines.append(f"Location: {r.location}\n")
        
        # Summary
        if resume.personalized_summary:
            lines.append("-" * 80)
            lines.append("PROFESSIONAL SUMMARY")
            lines.append("-" * 80)
            lines.append(resume.personalized_summary)
            lines.append()
        
        # Skills
        if resume.matched_skills:
            lines.append("-" * 80)
            lines.append("KEY SKILLS (MATCHED TO JOB)")
            lines.append("-" * 80)
            for skill in resume.matched_skills:
                lines.append(f"  • {skill.name:<30} ({skill.proficiency_level})")
            lines.append()
        
        # Experience
        if resume.prioritized_experience:
            lines.append("-" * 80)
            lines.append("WORK EXPERIENCE")
            lines.append("-" * 80)
            for exp in resume.prioritized_experience:
                lines.append(f"\n{exp.job_title}")
                lines.append(f"{exp.company} | {exp.start_date} - {exp.end_date or 'Present'}")
                if exp.description:
                    lines.append(f"\n{exp.description}\n")
                if exp.achievements:
                    for achievement in exp.achievements:
                        lines.append(f"  • {achievement}")
        
        # Education
        if r.education:
            lines.append("\n" + "-" * 80)
            lines.append("EDUCATION")
            lines.append("-" * 80)
            for edu in r.education:
                lines.append(f"{edu.degree} in {edu.field_of_study}")
                lines.append(f"{edu.institution}, {edu.graduation_year}")
        
        return "\n".join(lines)


class AggregateReportFormatter(ResumeFormatter):
    """Format comprehensive analysis report"""
    
    def format(self, resume: PersonalizedResume, report_data: Dict[str, Any]) -> str:
        """Generate detailed report"""
        lines = []
        
        lines.append("\n" + "=" * 80)
        lines.append("RESUME PERSONALIZATION ANALYSIS REPORT".center(80))
        lines.append("=" * 80 + "\n")
        
        r = resume.original_resume
        j = resume.target_job
        
        lines.append(f"Candidate: {r.name}")
        lines.append(f"Target Position: {j.job_title} @ {j.company}")
        lines.append(f"Analysis Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Score Summary
        lines.append("-" * 80)
        lines.append("RELEVANCE ANALYSIS")
        lines.append("-" * 80)
        lines.append(f"Overall Relevance Score: {report_data['relevance_score']:.1f}%")
        lines.append(f"Skill Match: {report_data['skill_match_percentage']}")
        lines.append(f"Recommendation: {report_data['recommendation']}\n")
        
        # Matched Skills
        lines.append("-" * 80)
        lines.append("SKILL ALIGNMENT")
        lines.append("-" * 80)
        lines.append(f"Matched Skills ({len(report_data['matched_skills'])}):")
        for skill in report_data['matched_skills']:
            lines.append(f"  ✓ {skill}")
        
        if report_data['missing_skills']:
            lines.append(f"\nMissing Required Skills ({len(report_data['missing_skills'])}):")
            for skill in report_data['missing_skills']:
                lines.append(f"  ✗ {skill}")
        
        # Recommendations
        lines.append("\n" + "-" * 80)
        lines.append("RECOMMENDATIONS FOR IMPROVEMENT")
        lines.append("-" * 80)
        for i, rec in enumerate(report_data['recommended_improvements'], 1):
            lines.append(f"{i}. {rec}")
        
        # Top Experiences
        if report_data['top_matching_experience']:
            lines.append("\n" + "-" * 80)
            lines.append("TOP RELEVANT EXPERIENCES")
            lines.append("-" * 80)
            for exp in report_data['top_matching_experience']:
                lines.append(f"  • {exp}")
        
        lines.append("\n" + "=" * 80 + "\n")
        
        return "\n".join(lines)
