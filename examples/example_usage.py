"""
Example usage of Resume Builder
Demonstrates how to use the system with sample data
"""
from resume_builder import ResumeBuilder
from resume_builder.models import Resume, Skill, Experience, Education


def create_sample_resume() -> Resume:
    """Create a sample data engineer resume"""
    
    skills = [
        Skill(
            name="Python",
            proficiency_level="Expert",
            years_of_experience=5,
            keywords=["pandas", "numpy", "scipy"],
            category="Technical"
        ),
        Skill(
            name="SQL",
            proficiency_level="Advanced",
            years_of_experience=6,
            keywords=["PostgreSQL", "optimization", "window functions"],
            category="Technical"
        ),
        Skill(
            name="Apache Spark",
            proficiency_level="Advanced",
            years_of_experience=3,
            keywords=["PySpark", "distributed computing", "RDD"],
            category="Technical"
        ),
        Skill(
            name="AWS",
            proficiency_level="Intermediate",
            years_of_experience=2,
            keywords=["S3", "EC2", "Lambda", "Glue"],
            category="Technical"
        ),
        Skill(
            name="Airflow",
            proficiency_level="Advanced",
            years_of_experience=3,
            keywords=["DAG", "task scheduling", "monitoring"],
            category="Technical"
        ),
        Skill(
            name="Snowflake",
            proficiency_level="Intermediate",
            years_of_experience=1.5,
            keywords=["data warehouse", "schema", "streams"],
            category="Technical"
        ),
        Skill(
            name="Docker",
            proficiency_level="Intermediate",
            years_of_experience=2,
            keywords=["containerization", "image build"],
            category="Technical"
        ),
        Skill(
            name="Git",
            proficiency_level="Advanced",
            years_of_experience=5,
            keywords=["version control", "CI/CD"],
            category="Technical"
        ),
        Skill(
            name="Team Leadership",
            proficiency_level="Intermediate",
            years_of_experience=1,
            keywords=["mentoring", "code review"],
            category="Soft"
        ),
        Skill(
            name="Communication",
            proficiency_level="Advanced",
            years_of_experience=5,
            keywords=["documentation", "stakeholder management"],
            category="Soft"
        ),
    ]
    
    experience = [
        Experience(
            job_title="Senior Data Engineer",
            company="TechCorp Solutions",
            start_date="2022-01",
            end_date=None,
            is_current=True,
            description="Led data engineering initiatives for enterprise data platform processing 500GB+ daily",
            achievements=[
                "Reduced ETL pipeline latency by 60% through Apache Spark optimization",
                "Built automated data ingestion framework handling 15+ data sources",
                "Mentored 3 junior engineers and established code review practices",
                "Designed Snowflake data warehouse architecture serving 100+ analytics queries/day",
            ],
            skills_used=["Python", "Spark", "SQL", "Airflow", "Snowflake", "AWS"]
        ),
        Experience(
            job_title="Data Engineer",
            company="DataFlow Inc.",
            start_date="2019-06",
            end_date="2021-12",
            is_current=False,
            description="Developed ETL pipelines and data infrastructure for financial services",
            achievements=[
                "Implemented 20+ production ETL pipelines using Python and SQL",
                "Optimized database queries improving report generation time by 40%",
                "Migrated legacy systems to cloud-based architecture on AWS",
                "Automated data quality checks reducing manual validation by 70%",
            ],
            skills_used=["Python", "SQL", "Airflow", "AWS", "Docker"]
        ),
        Experience(
            job_title="Junior Data Engineer",
            company="AnalyticsHub",
            start_date="2018-03",
            end_date="2019-05",
            is_current=False,
            description="Built and maintained data pipelines for business intelligence",
            achievements=[
                "Created automated data pipelines processing 50M+ records daily",
                "Developed SQL scripts for complex data transformations",
                "Implemented monitoring and alerting for data quality",
            ],
            skills_used=["Python", "SQL", "Airflow"]
        ),
    ]
    
    education = [
        Education(
            degree="Bachelor of Science",
            field_of_study="Computer Science",
            institution="State University",
            graduation_year=2018,
            gpa=3.7,
            relevant_coursework=["Database Systems", "Distributed Computing", "Algorithms"]
        ),
    ]
    
    resume = Resume(
        name="Alex Morgan",
        email="alex.morgan@example.com",
        phone="+1-555-123-4567",
        location="San Francisco, CA",
        professional_summary="Experienced Data Engineer with 5+ years building scalable data infrastructure",
        skills=skills,
        experience=experience,
        education=education,
        certifications=[
            "AWS Certified Solutions Architect",
            "Snowflake Certified Data Engineer"
        ],
        portfolio_links={
            "GitHub": "https://github.com/alexmorgan",
            "Medium": "https://medium.com/@alexmorgan"
        }
    )
    
    return resume


def create_sample_job_description() -> str:
    """Sample job description for Senior Data Engineer role"""
    return """
    Senior Data Engineer - Seattle, WA
    Company: CloudScale Technologies
    
    About the Role:
    We're looking for an experienced Senior Data Engineer to join our growing data platform team. 
    You'll be responsible for designing and implementing scalable data pipelines and infrastructure 
    that power our analytics and machine learning initiatives.
    
    Responsibilities:
    - Design and build fault-tolerant, scalable data pipelines processing terabytes of data daily
    - Collaborate with data scientists and analytics teams to understand data requirements
    - Optimize database performance and query execution
    - Establish data quality standards and implement monitoring solutions
    - Mentor junior engineers and drive engineering best practices
    
    Required Skills:
    - 5+ years of data engineering experience
    - Expert proficiency in Python and SQL
    - Deep experience with Apache Spark or similar distributed computing frameworks
    - Strong knowledge of cloud platforms (AWS, GCP, or Azure)
    - Experience with workflow orchestration tools (Airflow, Dagster)
    - Proficiency with data warehouse solutions (Snowflake, BigQuery, Redshift)
    - Experience with containerization (Docker, Kubernetes)
    - Strong understanding of data modeling and database design
    
    Preferred Skills:
    - Experience with machine learning pipelines
    - Knowledge of Apache Kafka for streaming data
    - Familiarity with dbt for data transformation
    - Experience with Scala
    - AWS certification
    - Open source contributions
    
    Nice to Have:
    - Experience leading technical teams
    - Knowledge of data governance and compliance (GDPR, HIPAA)
    - Experience with real-time data processing
    
    We Offer:
    - Competitive salary ($180k-$240k)
    - Remote-first work environment
    - Professional development budget
    - Stock options
    - Comprehensive health insurance
    """


def main():
    """Main example execution"""
    print("=" * 80)
    print("RESUME BUILDER - PERSONALIZATION EXAMPLE".center(80))
    print("=" * 80 + "\n")
    
    # Initialize builder
    builder = ResumeBuilder()
    
    # Create sample data
    resume = create_sample_resume()
    job_description = create_sample_job_description()
    
    print(f"Original Resume: {resume.name}")
    print(f"Skills: {len(resume.skills)} | Experience: {len(resume.experience)} roles\n")
    
    # Build personalized resume
    print("Processing job description and personalizing resume...\n")
    
    # Get analysis metrics
    metrics = builder.get_analysis_metrics(
        resume=resume,
        job_title="Senior Data Engineer",
        company="CloudScale Technologies",
        job_description=job_description
    )
    
    # Print analysis
    print("-" * 80)
    print("ANALYSIS RESULTS")
    print("-" * 80)
    analysis = metrics['analysis']
    print(f"Relevance Score: {analysis['relevance_score']:.1f}%")
    print(f"Skill Match: {analysis['skill_match_percentage']}")
    print(f"Recommendation: {analysis['recommendation']}\n")
    
    print("Matched Skills:")
    for skill in analysis['matched_skills']:
        print(f"  ✓ {skill}")
    
    if analysis['missing_skills']:
        print(f"\nMissing Skills (to develop):")
        for skill in analysis['missing_skills'][:5]:
            print(f"  ✗ {skill}")
    
    print(f"\nTop Matching Experiences:")
    for exp in analysis['top_matching_experience']:
        print(f"  • {exp}")
    
    print("\n" + "-" * 80)
    print("PERSONALIZED RESUME (MARKDOWN FORMAT)".center(80))
    print("-" * 80 + "\n")
    
    # Generate markdown resume
    markdown_resume = builder.build_personalized_resume(
        resume=resume,
        job_title="Senior Data Engineer",
        company="CloudScale Technologies",
        job_description=job_description,
        output_format='markdown'
    )
    
    print(markdown_resume)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE".center(80))
    print("=" * 80)


if __name__ == "__main__":
    main()
