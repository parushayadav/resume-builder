"""
Unit tests for Resume Builder components
Tests parser, rules engine, and formatters
"""
import unittest
from resume_builder.models import Resume, Skill, Experience, Education, JobDescription
from resume_builder.parser import JobDescriptionParser
from resume_builder.rules_engine import ResumeRulesEngine
from resume_builder.formatters import MarkdownFormatter, JSONFormatter


class TestJobDescriptionParser(unittest.TestCase):
    """Test job description parsing"""
    
    def setUp(self):
        self.parser = JobDescriptionParser()
    
    def test_extract_required_skills(self):
        """Test extraction of required skills"""
        job_text = """
        Required Skills:
        - Python
        - SQL
        - Apache Spark
        - AWS
        """
        job = self.parser.parse("Data Engineer", "TestCorp", job_text)
        
        self.assertIn('python', job.required_skills)
        self.assertIn('sql', job.required_skills)
        self.assertIn('apache spark', [s.lower() for s in job.required_skills])
    
    def test_extract_experience_level(self):
        """Test experience level extraction"""
        job_text = "Looking for a Senior Data Engineer with 5+ years experience"
        job = self.parser.parse("Data Engineer", "TestCorp", job_text)
        
        self.assertEqual(job.experience_level, 'senior')
    
    def test_extract_years_of_experience(self):
        """Test years of experience extraction"""
        job_text = "We require 5+ years of data engineering experience"
        job = self.parser.parse("Data Engineer", "TestCorp", job_text)
        
        self.assertEqual(job.years_of_experience_required, 5)


class TestResumeRulesEngine(unittest.TestCase):
    """Test resume personalization rules"""
    
    def setUp(self):
        self.engine = ResumeRulesEngine()
        self.resume = self._create_test_resume()
        self.job = self._create_test_job()
    
    def _create_test_resume(self) -> Resume:
        """Create test resume"""
        return Resume(
            name="Test User",
            email="test@example.com",
            phone="555-1234",
            location="Test City",
            skills=[
                Skill(name="Python", proficiency_level="Expert"),
                Skill(name="SQL", proficiency_level="Advanced"),
                Skill(name="Apache Spark", proficiency_level="Advanced"),
                Skill(name="AWS", proficiency_level="Intermediate"),
            ],
            experience=[
                Experience(
                    job_title="Data Engineer",
                    company="TestCorp",
                    start_date="2020-01",
                    skills_used=["Python", "SQL", "Spark"],
                    achievements=["Built ETL pipeline", "Optimized queries"]
                )
            ]
        )
    
    def _create_test_job(self) -> JobDescription:
        """Create test job description"""
        return JobDescription(
            job_title="Senior Data Engineer",
            company="TestCorp",
            description="Test job",
            required_skills=["Python", "SQL", "Apache Spark"],
            key_technologies=["AWS", "Airflow"]
        )
    
    def test_skill_matching(self):
        """Test skill matching"""
        personalized = self.engine.personalize(self.resume, self.job)
        
        self.assertGreater(personalized.relevance_score, 0)
        self.assertGreater(len(personalized.matched_skills), 0)
    
    def test_relevance_score_calculation(self):
        """Test relevance score is within bounds"""
        personalized = self.engine.personalize(self.resume, self.job)
        
        self.assertGreaterEqual(personalized.relevance_score, 0)
        self.assertLessEqual(personalized.relevance_score, 100)
    
    def test_missing_skills_identification(self):
        """Test identification of missing skills"""
        personalized = self.engine.personalize(self.resume, self.job)
        
        # Airflow is in job tech but not in resume
        self.assertIn('airflow', personalized.missing_skills)


class TestFormatters(unittest.TestCase):
    """Test output formatters"""
    
    def setUp(self):
        self.engine = ResumeRulesEngine()
        self.markdown_formatter = MarkdownFormatter()
        self.json_formatter = JSONFormatter()
        
        self.resume = Resume(
            name="Test User",
            email="test@example.com",
            phone="555-1234",
            location="Test City",
            skills=[Skill(name="Python", proficiency_level="Expert")],
            experience=[
                Experience(
                    job_title="Data Engineer",
                    company="TestCorp",
                    start_date="2020-01",
                    achievements=["Achievement 1"]
                )
            ]
        )
        
        self.job = JobDescription(
            job_title="Senior Data Engineer",
            company="TestCorp",
            description="Test job",
            required_skills=["Python"]
        )
    
    def test_markdown_format_output(self):
        """Test markdown formatting produces valid output"""
        personalized = self.engine.personalize(self.resume, self.job)
        output = self.markdown_formatter.format(personalized)
        
        self.assertIn("# Test User", output)
        self.assertIn("Senior Data Engineer", output)
        self.assertIn("Data Engineer", output)
    
    def test_json_format_output(self):
        """Test JSON formatting produces valid output"""
        personalized = self.engine.personalize(self.resume, self.job)
        output = self.json_formatter.format(personalized)
        
        self.assertIn("Test User", output)
        self.assertIn("Data Engineer", output)


if __name__ == '__main__':
    unittest.main()
