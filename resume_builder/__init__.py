"""
Main application entry point for Resume Builder
Orchestrates parsing, personalization, and formatting
"""
from .models import Resume, JobDescription, PersonalizedResume
from .parser import JobDescriptionParser
from .rules_engine import ResumeRulesEngine
from .formatters import (
    JSONFormatter, 
    MarkdownFormatter, 
    PlainTextFormatter,
    AggregateReportFormatter
)


class ResumeBuilder:
    """Main class for resume personalization"""
    
    def __init__(self):
        self.parser = JobDescriptionParser()
        self.rules_engine = ResumeRulesEngine()
        self.formatters = {
            'json': JSONFormatter(),
            'markdown': MarkdownFormatter(),
            'text': PlainTextFormatter(),
            'report': AggregateReportFormatter()
        }
    
    def build_personalized_resume(self,
                                 resume: Resume,
                                 job_title: str,
                                 company: str,
                                 job_description: str,
                                 output_format: str = 'markdown') -> str:
        """
        Complete workflow: Parse job, personalize resume, format output
        
        Args:
            resume: User's original resume
            job_title: Position title
            company: Company name
            job_description: Full job description text
            output_format: 'json', 'markdown', 'text', 'report'
            
        Returns:
            Formatted personalized resume
        """
        # Parse job description
        parsed_job = self.parser.parse(job_title, company, job_description)
        
        # Personalize resume
        personalized = self.rules_engine.personalize(resume, parsed_job)
        
        # Format output
        formatter = self.formatters.get(output_format.lower(), self.formatters['markdown'])
        
        if output_format.lower() == 'report':
            report_data = self.rules_engine.get_recommendation_report(personalized)
            return formatter.format(personalized, report_data)
        else:
            return formatter.format(personalized)
    
    def get_analysis_metrics(self,
                            resume: Resume,
                            job_title: str,
                            company: str,
                            job_description: str) -> dict:
        """
        Get detailed analysis metrics without formatting
        
        Returns analysis data for API/programmatic use
        """
        parsed_job = self.parser.parse(job_title, company, job_description)
        personalized = self.rules_engine.personalize(resume, parsed_job)
        report = self.rules_engine.get_recommendation_report(personalized)
        
        return {
            'job': parsed_job.to_dict(),
            'personalization': personalized.to_dict(),
            'analysis': report
        }
