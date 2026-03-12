#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage of the Job Posting Streaming Job
Demonstrates how to use the streaming job with a sample email
"""
import sys
import os

# Handle Unicode on Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_builder.job_streaming import JobPostingStreamingJob


def create_sample_resume_template() -> str:
    """Create a sample resume template file"""
    template = """CHIDVILAS PARUSHA
parushacv@gmail.com | +1 2163340475 | https://www.linkedin.com/in/cvparusha/

PROFESSIONAL SUMMARY
• Experienced handling data with 8+ years of industry experience in the field of IT, with focus on Analytics, Design and development of Data Warehousing, Modeling, Business Intelligence Applications, Testing, Requirement Gathering and Visualization.
• Strong understanding of Bigdata Technologies (Hadoop Framework, HDFS, Hive, Sqoop, Spark, Kafka, Cassandra, Oozie, MapReduce)
• Strong experience with Business and data Analysis, data profiling, Data Migration, Data Conversion, Data Quality, Change Management, Configuration Management.
• Capable of executing Real-time and Batch processing data streams through Spark Streaming.
• Experienced in writing UNIX shell scripting, python programming, Java programming, excellent with SQL, PL/SQL queries and XML.
• Strong hands-on experience with Azure Data Factory, Azure Synapse, Azure Data Bricks and AWS services, including EMR, S3, EC2, S3, RDS, DynamoDB, Glue, Lambda, SNS, Cloud Formation, etc.
• Expert in Working with Python and Java for computational analytics and performing advanced analytical applications alongside databases including Oracle, MySQL, SQL Server, Snowflake.
• Good knowledge and experience on database design, development, and administration for various database software products like Microsoft SQL Server, Snowflake, MySQL, MongoDB, Oracle.

TECHNICAL SKILLS
Programming Languages – Python, Java, Scala, Shell Scripting, SQL, XML, Bash scripting
Big Data Platforms – Apache Spark, Hadoop, Kafka, Cloudera, MapReduce, HDFS, Hive
Cloud Platform – AWS - S3, EMR, Redshift, Glue, Lambda, EC2, Azure – ADF, Synapse, Data Bricks
Databases - MySQL, SQL Server, NoSQL, Snowflake, DynamoDB, Oracle
Data Visualization - Tableau, Power-BI, Splunk, Excel

PROFESSIONAL EXPERIENCE

Data Engineer/Analyst | HCL America | March 2025 to Present
Responsibilities: 

Data Engineer/Analyst | Nomura, New York City, NY | November 2021 to February 2025
• Supporting the mainstream application that facilitates the users to publish and download the feed files from the application UI.
• Collaborated in Agile settings with application leads to comprehensively document product requirements using Confluence, Jira.
• Organizing scrum calls to get updates on the assigned Jiras, also meetings with end users and IT teams to gather and document functional and technical requirements.
• Developing detailed test plans to ensure product quality and functionality in the Data Management Technology domain.
• Working with QA team for product testing and QA sign-off documentation.
• Experienced with version control Systems Git to keep the versions and configurations of the code organized.
• Migrated application dependencies from Java 8 to latest stable versions Java 11.
• Handled huge volumes of data in the form of feed-files that are published and downloaded globally 24x7 through the application.
• Supporting Users/Production team to handle issues by troubleshooting and errors handling through problem solving techniques.
• Implemented JIL creation, testing and production release from Unix/ Windows platforms to schedule the jobs using Autosys.
• Created monitors, alerts, notifications, and logs for Lambda function, Glue jobs, shared drives, RAG status to ensure minimal downtime.
• Excelled in maintaining Quality Assurance protocols by employing effecting cleaning and monitoring techniques in ETL processing and deploying.
• Established Python (NumPy and Pandas) and shell-script jobs to collect server and service-level statistics.
• Displayed on Application UI via Spark streaming for batch processing/real-time data processing for infrastructure monitoring and management.
• Executed backend scripting tasks in Python, extracting valuable insights from Natural Language Understanding (NLU) data stored in RDBMS/shared drives/CSV/JSON.
• Leveraged in SQL IDEs like Rapid SQL, D-Beaver, and MySQL Workbench to extract and modify data in the MySQL/SQL Server database.
• Involved in performance tuning and unit testing for SQL and PL/SQL code.
• Generated ETL scripts and developed ETL pipelines using AWS Glue, Airflow to transform, flatten, and enrich data from source to target utilizing various RDBMS.
• Wrote AWS Lambda functions in python for AWS's Lambda which invokes python scripts to perform various transformations and analytics on large data sets in EMR clusters.

Data Engineer/Analyst | Cleveland State University, Ohio | January 2020 – November 2021
• Designed and developed SQL-based reporting solutions to analyze student performance and operational metrics.
• Conducted data cleansing, transformation, and profiling to improve data accuracy.
• Built predictive models using Python (Pandas, NumPy) to analyze trends and forecast outcomes.
• Developed interactive Tableau and Power BI dashboards to visualize university-wide KPIs.
• Automated data extraction and processing workflows using SQL scripts and Excel VBA macros.
• Optimized ETL processes to enhance data pipeline performance and reduce processing time.

Data Engineer/Analyst | Yana Software Hyderabad, India | October 2017 to November 2019
• Worked with Business users during requirements gathering and business analysis to prepare high-level Logical Data Models and Physical Data Models.
• Designed ER diagrams, logical model (relationship, cardinality, attributes, and candidate keys), and physical data models.
• Responsible for developing data pipeline with Oracle Data Integration (ODI) to extract the data from weblogs and store in HDFS.
• Established Jenkins pipelines for service deployment, actively monitoring logs during deployment processes.
• Generated ETL programs for data extraction, transformation and loading using AWS Glue, Informatica, Airflow.

EDUCATION
Master of Computer and Information Science | Cleveland State University, Ohio, USA | January 2020 -December 2021
Master of Business Administration | University of the Cumberlands, KY, USA | January 2025 -December 2026(Expected Graduation)

CERTIFICATIONS
AWS Certified Data Engineer – Associate
Azure Certified Data engineer
Microsoft certified - Data Analyst Associate
"""
    
    # Save to file in user's temp directory
    import tempfile
    temp_dir = tempfile.gettempdir()
    template_path = os.path.join(temp_dir, 'resume_template.txt')
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    return template_path


def create_sample_job_posting_email() -> tuple:
    """Create a sample job posting email"""
    subject = "Lead Data Engineer/Architect - Sunnyvale, CA (Hybrid) - ClifyX"
    
    body = """Hi,
 
This is Saurabh Pardeshi from ClifyX. I hope you are doing well!

ClifyX was formed in 1998 and since then providing staffing solutions and services.
Clifyx provides innovative business solutions that satisfy the highest requirements for mission-critical reliability, scalability, interoperations to our customers and shareholders and a high level of satisfaction for the employees. Our staff's creativity, service, and dedication set apart from other IT firms. Our team is Young, Dynamic and willing to work with our Client's needs with the right attitude. Our Team has years of experience helping clients around the world use their IT investments to drive innovation, productivity, and growth to achieve higher performance.

Kindly respond to this requirement with your resume, contact, visa status, rate and current location info to speed up the interview processes. 

Job title: Lead Data Engineer/Architect
Work Location with ZIP: Sunnyvale, CA (Hybrid)
Minimum Years of Experience: 14 + years

W2 Contract 

 
Technical Hiring Criteria (Must Haves)
 
• Top 3 Required skills: Spark/Pyspark, Tableau, SQL
 
• Years of experience in each of the must-have skills: 8+ Years
 
Thanks & Regards, 

Saurabh Pardeshi 

Fax: 732-909-2631 

Email: saurabhkp@clifyx.com 

Website: www.ClifyX.com 

Note: This is a bulk email generation system. If the opportunity does not align with your experience or is not of interest, please ignore this email. Apologies for taking your precious time."""
    
    return subject, body


def main():
    """Main example demonstrating the streaming job"""
    print("=" * 70)
    print("Job Posting Streaming Job - Example Usage")
    print("=" * 70)
    
    # Create sample resume template
    print("\n1. Creating sample resume template...")
    template_path = create_sample_resume_template()
    print("[OK] Template created at: {}".format(template_path))
    
    # Create output directory
    output_dir = os.path.expanduser('~/Resume_Generator_Output')
    os.makedirs(output_dir, exist_ok=True)
    print("\n2. Output directory: {}".format(output_dir))
    
    # Initialize the streaming job
    print("\n3. Initializing streaming job...")
    job = JobPostingStreamingJob(
        resume_template_path=template_path,
        output_directory=output_dir
    )
    
    # Lower matching threshold for demonstration
    job.profile_matcher.min_skill_match_threshold = 0.15
    
    # Process sample email
    print("\n4. Processing sample job posting email...")
    subject, body = create_sample_job_posting_email()
    
    result = job.process_single_email_text(
        subject=subject,
        body=body,
        from_address='saurabhkp@clifyx.com'
    )
    
    # Display results
    print("\n" + "=" * 70)
    print("PROCESSING RESULTS")
    print("=" * 70)
    
    print("\nEmail Information:")
    print("   From: {}".format(result['email']['from']))
    print("   Subject: {}".format(result['email']['subject']))
    
    print("\nDetection Results:")
    print("   Is Job Posting: {}".format(result['is_job_posting']))
    print("   Is Data Engineering Role: {}".format(result['is_data_engineering']))
    print("   Matches Profile: {}".format(result['matches_profile']))
    
    if result.get('match_details'):
        details = result['match_details']
        print("\nProfile Matching Details:")
        print("   Skill Match: {:.1f}%".format(details['skill_match_percentage']))
        if details['matched_skills']:
            print("   Matched Skills: {}".format(', '.join(details['matched_skills'])))
        if details['missing_skills']:
            print("   Missing Skills: {}".format(', '.join(details['missing_skills'][:5])))
        print("   Experience Match: {}".format(details['experience_match']))
        print("   Years Requirement Met: {}".format(details['years_match']))
        
        if details['gaps']:
            print("   Gaps:")
            for gap in details['gaps']:
                print("      - {}".format(gap))
    
    if result.get('resume_path'):
        print("\n[SUCCESS] Resume Generated Successfully!")
        print("   Path: {}".format(result['resume_path']))
        print("   File exists: {}".format(os.path.exists(result['resume_path'])))
    elif result.get('error'):
        print("\n[ERROR] Error generating resume: {}".format(result['error']))
    
    print("\n" + "=" * 70)
    print("Example completed!")
    print("=" * 70)


if __name__ == '__main__':
    main()
