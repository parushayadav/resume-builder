# Job Posting Streaming Job - Documentation

## Overview

The **Job Posting Streaming Job** is a powerful automation tool that monitors your Gmail inbox for job postings, automatically detects data engineering roles, matches them against your profile, and generates tailored resumes specifically customized for each matching opportunity.

## Features

✅ **Real-time Email Monitoring**: Continuously monitors Gmail for new emails  
✅ **Smart Job Detection**: Identifies job postings with high accuracy  
✅ **Data Engineering Focus**: Automatically filters for data engineering roles  
✅ **Profile Matching**: Compares job requirements against your skills and experience  
✅ **Automatic Resume Generation**: Creates tailored resumes in Word format  
✅ **Smart Customization**: Highlights relevant skills and experience for each role  
✅ **Local Output**: Saves generated resumes to your machine

## Architecture

```
Email Stream (Gmail)
        ↓
Job Posting Detector
        ↓
Data Engineering Filter
        ↓
Profile Matcher
        ↓
Resume Personalizer
        ↓
Word Document Export (.docx)
```

## Components

### 1. Gmail Integration (`gmail_integration.py`)

**GmailStreamingService**: Handles Gmail API authentication and email streaming
- Authenticates with Gmail using OAuth2
- Retrieves emails from your inbox
- Streams new emails continuously
- Extracts email headers and body content

**EmailJobPostingDetector**: Identifies job postings and data engineering roles
- Detects if email is a job posting (keyword matching)
- Determines if role is data engineering related
- Extracts key metadata (job title, company, location, skills, experience requirements)

### 2. Profile Matching (`profile_matcher.py`)

**ProfileMatcher**: Compares job requirements with user profile
- Matches skills against requirements
- Verifies years of experience requirement
- Identifies skill gaps
- Calculates overall match percentage

**ProfileLoader**: Loads user profile from resume template
- Parses resume text to extract structured data
- Creates Resume object with all information
- Handles multiple date formats
- Extracts skills, experience, education, certifications

### 3. Resume Generation

**WordDocumentExporter** (`word_exporter.py`): Exports personalized resumes to .docx
- Formats resume in professional Word document style
- Includes job matching score
- Organizes content by section (summary, skills, experience, education)
- Applies consistent formatting

**ResumeBuilder Enhancement**: Extended to return PersonalizedResume objects
- Parses job descriptions
- Personalizes resume based on job requirements
- Prioritizes relevant experience
- Highlights matched skills

### 4. Main Orchestrator (`job_streaming.py`)

**JobPostingStreamingJob**: Main orchestrator that ties everything together
- Loads user profile from resume template
- Monitors Gmail inbox
- Processes emails end-to-end
- Generates tailored resumes
- Saves files to local directory

## Setup Guide

### 1. Prerequisites

```bash
pip install -r requirements.txt
```

This installs:
- `google-auth-oauthlib` - Gmail API OAuth
- `google-api-python-client` - Gmail API client
- `python-docx` - Word document generation
- `pydantic` - Data validation
- `python-dotenv` - Environment variables

### 2. Gmail API Setup

#### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API

#### Step 2: Create OAuth2 Credentials
1. Go to "Credentials" in the left menu
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Select "Desktop application"
4. Download the JSON file and save as `credentials.json` in your project root

#### Step 3: Grant Permissions
- First run will prompt you to authorize the app
- Grant permission to access Gmail (read-only)
- Token will be saved for future use

### 3. Create Resume Template

Save your resume as a text file (e.g., `my_resume.txt`):

```
YOUR NAME
email@example.com | +1 XXXXXXXXXX | LinkedIn URL

PROFESSIONAL SUMMARY
[Your professional summary]

TECHNICAL SKILLS
Programming Languages – Python, Java, SQL
Big Data Platforms – Spark, Hadoop, Kafka
Cloud Platform – AWS (S3, EMR, Glue), Azure (ADF, Synapse)
Databases - SQL Server, Snowflake, MongoDB

PROFESSIONAL EXPERIENCE

Data Engineer/Analyst | Company Name | Date1 to Date2
[Job responsibilities and achievements]

EDUCATION
Master's Degree | University Name | Year

CERTIFICATIONS
AWS Certified Data Engineer – Associate
```

### 4. Set Output Directory

```python
output_directory = os.path.expanduser('~/Resume_Generator_Output')
# This creates a folder in your home directory for generated resumes
```

## Usage

### Basic Usage

```python
from resume_builder.job_streaming import JobPostingStreamingJob

# Initialize the streaming job
job = JobPostingStreamingJob(
    resume_template_path='/path/to/my_resume.txt',
    output_directory='/path/to/output',
    gmail_credentials_path='credentials.json'
)

# Start monitoring Gmail for job postings
job.start_streaming(poll_interval=60)  # Check every 60 seconds
```

### Process Single Email (Testing)

```python
result = job.process_single_email_text(
    subject="Data Engineer Position - NYC",
    body="Full job description text...",
    from_address="recruiter@company.com"
)

# Result contains:
# - is_job_posting: bool
# - is_data_engineering: bool
# - matches_profile: bool
# - match_details: dict with skill percentages
# - resume_path: path to generated resume (if match found)
```

### Example Script

Run the included example:

```bash
python examples/streaming_job_example.py
```

This demonstrates:
1. Loading a resume template
2. Processing a sample job posting email
3. Generating a tailored resume
4. Saving to Word document

## Workflow

### When an Email Arrives

1. **Detection**: Checks if email is a job posting
   - Looks for keywords like "hiring", "position", "requirements"
   - Scores based on keyword frequency

2. **Classification**: Determines if it's a data engineering role
   - Looks for data engineering keywords: "Spark", "Python", "SQL", "Data Pipeline", etc.
   - Skips if not data engineering related

3. **Metadata Extraction**: Pulls key information
   - Job title
   - Company name
   - Location
   - Years of experience required
   - Required skills

4. **Profile Matching**: Compares against your skills
   - Calculates skill match percentage
   - Checks if you meet experience requirements
   - Identifies skill gaps

5. **Resume Generation** (if match is good):
   - Uses job requirements to personalize resume
   - Highlights relevant skills and experience
   - Creates professional Word document
   - Saves with timestamp and company name

## Generated Resume Format

Each generated resume:
- **Filename**: `Resume_{Company}_{JobTitle}_{Timestamp}.docx`
- **Location**: `~/Resume_Generator_Output/`
- **Content**:
  - Name and target job title
  - Job match score (percentage)
  - Contact information
  - Customized professional summary
  - Matched technical skills (highlighted)
  - Prioritized work experience
  - Education
  - Certifications

## Configuration

### Matching Thresholds

Adjust matching sensitivity in `ProfileMatcher`:

```python
matcher = ProfileMatcher()
matcher.min_skill_match_threshold = 0.6  # 60% minimum skill match
```

### Email Polling Interval

Change frequency of Gmail checks:

```python
job.start_streaming(poll_interval=300)  # Check every 5 minutes
```

### Job Posting Detection

Customize detection in `EmailJobPostingDetector`:

```python
detector = EmailJobPostingDetector(job_posting_threshold=0.5)
```

## Output Example

When a matching job is found:

```
=============================================================
Processing email from: saurabhkp@clifyx.com
Subject: Lead Data Engineer/Architect - Sunnyvale, CA

Job posting detection: True (confidence: 75.0%)
Data engineering role detection: True (confidence: 82.0%)

Profile matching:
  - Skill match: 87.5%
  - Experience match: True
  - Years requirement: True
  - Overall match: True

📄 Generating personalized resume...
✓ Resume saved to: ~/Resume_Generator_Output/Resume_ClifyX_Lead_Data_Engineer_20260116_143025.docx
=============================================================
```

## Troubleshooting

### Gmail Authentication Issues

**Problem**: "Authentication required" error
- **Solution**: Delete `token.pickle` and run again to re-authenticate

**Problem**: "gmail-readonly scope not granted"
- **Solution**: Check that OAuth credentials were granted Gmail read permission

### Resume Generation Issues

**Problem**: "Resume template file not found"
- **Solution**: Verify the path to resume template is correct and file exists

**Problem**: No emails detected
- **Solution**: 
  - Check email has "from" and "subject" fields
  - May be filtered by Gmail's spam filter
  - Try with subject line containing clear job-related keywords

### Matching Issues

**Problem**: Resumes not being generated for matching jobs
- **Solution**: 
  - Lower `min_skill_match_threshold` if too strict
  - Check resume template has required skills
  - Review skill gaps in the matching report

## Advanced Usage

### Custom Email Query

Only process emails from specific senders:

```python
for email in gmail_service.stream_job_posting_emails(
    query='from:recruiter@company.com'
):
    job.process_email(email)
```

### Batch Processing

Process multiple stored emails:

```python
emails = gmail_service.get_recent_emails(max_results=20)
results = []
for email in emails:
    result = job.process_email(email)
    results.append(result)
```

### Customize Resume Format

Extend `WordDocumentExporter` for custom formatting:

```python
class CustomResumeExporter(WordDocumentExporter):
    def _add_header(self, resume, personalized_resume):
        # Custom header logic
        pass
```

## Performance Considerations

- **Email Processing**: ~2-3 seconds per email
- **Resume Generation**: ~1-2 seconds
- **Gmail API Rate Limits**: 1 billion per day (plenty for daily use)
- **Recommended Poll Interval**: 60-300 seconds (1-5 minutes)

## Security

- **OAuth Token**: Stored locally in `token.pickle`
- **Credentials**: Keep `credentials.json` in project root only
- **Never**: Commit credentials or token files to version control
- **Add to .gitignore**:
  ```
  credentials.json
  token.pickle
  Resume_Generator_Output/
  ```

## Feature Roadmap

Future enhancements:
- [ ] Multi-job postings per email
- [ ] LinkedIn profile integration
- [ ] Skill gap recommendations
- [ ] Email notification of matches
- [ ] Dashboard for tracking applications
- [ ] Custom resume templates
- [ ] Multiple output formats (PDF, ATS-optimized)
- [ ] Interview prep suggestions

## Support & Issues

For issues or feature requests:
1. Check troubleshooting section above
2. Review example script usage
3. Enable debug logging for detailed information

## License

This feature is part of the Resume Builder project.

---

**Ready to start automating your job search?** 🚀

Run your first example:
```bash
python examples/streaming_job_example.py
```
