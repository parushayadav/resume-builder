# Resume Builder

A personalized resume generation tool for data engineers that customizes resumes based on job descriptions.

**Version**: 1.0.0 | **Status**: ✅ Production Ready | **Date**: January 15, 2026

---

## Table of Contents

- [Quick Start](#quick-start)
- [Overview](#overview)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Scoring System](#scoring-system)
- [Rules Engine](#rules-engine)
- [Architecture](#architecture)
- [Examples](#examples)
- [Data Models](#data-models)
- [Configuration](#configuration)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

---

## Quick Start

### 5-Minute Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run example
python examples/example_usage.py

# 3. Verify tests pass
python -m pytest tests/ -v
```

### Basic Usage

```python
from resume_builder import ResumeBuilder
from resume_builder.models import Resume, Skill, Experience

# Create resume
resume = Resume(
    name="Your Name",
    email="your@email.com",
    phone="+1-555-1234",
    location="City, State",
    skills=[Skill(name="Python", proficiency_level="Expert")],
    experience=[Experience(job_title="Data Engineer", company="TechCorp", start_date="2022-01")]
)

# Analyze job
builder = ResumeBuilder()
metrics = builder.get_analysis_metrics(
    resume=resume,
    job_title="Senior Data Engineer",
    company="Company",
    job_description="... full job posting ..."
)

# Get results
print(f"Match: {metrics['analysis']['relevance_score']}%")
print(f"Missing Skills: {metrics['analysis']['missing_skills']}")

# Generate personalized resume
personalized = builder.build_personalized_resume(
    resume=resume,
    job_title="Senior Data Engineer",
    company="Company",
    job_description="... full job posting ...",
    output_format='markdown'
)
```

---

## Overview

**Resume Builder** is an intelligent resume personalization system that:

- **Parses job descriptions** to extract requirements, skills, and technologies
- **Analyzes your resume** to identify relevant experiences and skills
- **Calculates relevance scores** to measure fit with job requirements (0-100%)
- **Personalizes content** including summary, experience order, and highlighted achievements
- **Outputs in multiple formats** (Markdown, JSON, Plain Text, Detailed Report)

### Key Features

✅ **Smart Job Parsing** - Extracts skills, technologies, experience level from any job posting
✅ **Intelligent Matching** - Maps skills, experience, and technologies with proficiency consideration
✅ **Accurate Scoring** - 0-100% relevance score using weighted algorithm
✅ **Personalization** - Generates tailored summaries, prioritizes experiences, highlights achievements
✅ **Multiple Formats** - JSON, Markdown, Plain Text, and detailed analysis reports
✅ **50+ Data Engineering Skills** - Pre-configured skill database
✅ **Highly Customizable** - Adjust weights, thresholds, and add custom rules
✅ **Production Ready** - Full test suite, type hints, comprehensive documentation

---

## How It Works

### 3-Step Process

```
INPUT: Your Resume + Job Description
    ↓
STEP 1: PARSE JOB
    → Extract skills, technologies, experience level, responsibilities
    → Result: Structured JobDescription object
    ↓
STEP 2: MATCH & SCORE
    → Match skills against requirements
    → Score experience relevance
    → Calculate overall fit (0-100%)
    → Identify skill gaps
    → Result: PersonalizedResume with scores
    ↓
STEP 3: FORMAT & OUTPUT
    → Generate tailored summary
    → Prioritize experiences by relevance
    → Highlight matching achievements
    → Format as JSON/Markdown/Text/Report
    → Result: Personalized resume ready to use
```

### Example Calculation

```
Job: Senior Data Engineer
Requirements: Python, SQL, Spark, AWS, Airflow (5 required)
Technologies: Spark, AWS, Airflow, Snowflake (4 total)

Your Resume:
✓ Matched Skills: Python, SQL, Spark, AWS (4/5 = 80%)
✓ Matched Tech: Spark, AWS (2/4 = 50%)
✓ Relevant Experiences: 2 roles (50%)

Score Calculation:
  Skill Score:       80 × 0.40 = 32
  Experience Score:  50 × 0.35 = 17.5
  Technology Score:  50 × 0.25 = 12.5
  
  TOTAL: 62% ← GOOD MATCH!
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

```bash
# Navigate to project directory
cd resume-builder

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "from resume_builder import ResumeBuilder; print('✓ Success')"
```

---

## Usage

### Create Your Resume

```python
from resume_builder.models import Resume, Skill, Experience, Education

skills = [
    Skill(
        name="Python",
        proficiency_level="Expert",
        years_of_experience=5,
        keywords=["pandas", "numpy"],
        category="Technical"
    ),
    Skill(name="SQL", proficiency_level="Advanced", years_of_experience=6),
    Skill(name="Apache Spark", proficiency_level="Advanced", years_of_experience=3),
    # ... add more skills
]

experience = [
    Experience(
        job_title="Data Engineer",
        company="TechCorp",
        start_date="2022-01",
        end_date=None,
        is_current=True,
        description="Built data pipelines",
        achievements=[
            "Reduced ETL latency by 60% through optimization",
            "Built automated ingestion framework for 15+ data sources",
        ],
        skills_used=["Python", "Spark", "SQL"]
    ),
    # ... add more experiences
]

education = [
    Education(
        degree="Bachelor of Science",
        field_of_study="Computer Science",
        institution="State University",
        graduation_year=2018,
    ),
]

resume = Resume(
    name="Your Name",
    email="your@email.com",
    phone="+1-555-XXXX",
    location="City, State",
    professional_summary="Experienced Data Engineer",
    skills=skills,
    experience=experience,
    education=education,
    certifications=["AWS Certified Solutions Architect"],
    portfolio_links={"GitHub": "https://github.com/yourname"}
)
```

### Get Analysis Metrics

```python
builder = ResumeBuilder()

# Get detailed analysis without generating resume
metrics = builder.get_analysis_metrics(
    resume=resume,
    job_title="Senior Data Engineer",
    company="Company Name",
    job_description="... full job description text ..."
)

# Access analysis
analysis = metrics['analysis']
print(f"Relevance Score: {analysis['relevance_score']}%")
print(f"Matched Skills: {analysis['matched_skills']}")
print(f"Missing Skills: {analysis['missing_skills']}")
print(f"Recommendation: {analysis['recommendation']}")
```

### Generate Personalized Resume

```python
# Generate in Markdown format (default)
personalized = builder.build_personalized_resume(
    resume=resume,
    job_title="Senior Data Engineer",
    company="Company Name",
    job_description="... full job description ...",
    output_format='markdown'  # or 'json', 'text', 'report'
)

# Save to file
with open('resume_personalized.md', 'w') as f:
    f.write(personalized)

# Or use other formats
json_resume = builder.build_personalized_resume(..., output_format='json')
text_resume = builder.build_personalized_resume(..., output_format='text')
report = builder.build_personalized_resume(..., output_format='report')
```

### Analyze Multiple Jobs

```python
jobs = [
    {"title": "Senior Data Engineer", "company": "Company1", "desc": "..."},
    {"title": "Data Engineer", "company": "Company2", "desc": "..."},
    {"title": "Analytics Engineer", "company": "Company3", "desc": "..."},
]

results = {}
for job in jobs:
    metrics = builder.get_analysis_metrics(
        resume=resume,
        job_title=job["title"],
        company=job["company"],
        job_description=job["desc"]
    )
    results[job["company"]] = metrics["analysis"]["relevance_score"]

# Find best fit
best_fit = max(results, key=results.get)
print(f"Best fit: {best_fit} ({results[best_fit]:.0f}%)")
```

---

## Scoring System

### Relevance Score Interpretation

| Score | Level | Recommendation |
|-------|-------|-----------------|
| 80-100% | 🟢 Excellent | Apply immediately |
| 60-79% | 🟡 Good | Apply - strong candidate |
| 40-59% | 🟠 Moderate | Develop missing skills |
| 20-39% | 🔴 Limited | Significant gaps |
| 0-19% | ⚫ Poor | Not recommended |

### Scoring Formula

```
Overall Score = (Skill% × 0.40) + (Experience% × 0.35) + (Tech% × 0.25)

Where:
  Skill% = (Matched Required Skills / Total Required Skills) × 100
  Experience% = min(Relevant Experiences × 25, 100)
  Tech% = (Matched Technologies / Total Technologies) × 100

Result: 0-100 scale
```

### What Gets Analyzed

**From Job Descriptions**:
- Required vs preferred skills
- Key technologies and tools
- Experience level requirements
- Years of experience needed
- Key responsibilities
- Industry keywords

**From Your Resume**:
- Technical skills with proficiency levels
- Work experience with achievements
- Educational background
- Certifications
- Portfolio links
- Years in each role
- Keywords in achievements

**Generated Analysis**:
- Relevance score (0-100%)
- Skill match percentage
- Missing skills (development opportunities)
- Top matching experiences
- Highlighted achievements
- Personalized professional summary
- Actionable recommendations

---

## Rules Engine

### Matching Algorithms

#### Skill Matching
```
1. Extract resume skills (set of {skill_name})
2. Extract job required skills (set of {skill_name})
3. Calculate intersection = matched skills
4. Score = (matched / required) × 100
```

#### Experience Scoring
```
For each resume experience:
  1. skill_overlap = (matching_skills / job_skills) × 100
  2. title_relevance = calculate_similarity(exp_title, job_title)
  3. score = (skill_overlap × 0.6) + (title_relevance × 0.4)
  4. Apply recency bonus:
     - Current position: score × 1.5
     - Past position: score × 1.0
```

#### Achievement Highlighting
```
For each achievement:
  1. Count keyword matches against job requirements
  2. Check for quantifiable metrics (numbers)
  3. Score = (keyword_matches × 0.6) + (has_metric × 0.4)
  4. Include if score > 0
```

### Customizing Weights

Edit `resume_builder/config.py`:

```python
# Adjust importance of each factor
SKILL_WEIGHT = 0.40          # Skills (increase for skill-focused roles)
EXPERIENCE_WEIGHT = 0.35     # Experience (increase for experienced roles)
TECHNOLOGY_WEIGHT = 0.25     # Technology (increase for tech-specific roles)

# Adjust matching thresholds
SKILL_MATCH_THRESHOLD = 0.60         # Minimum 60% skill match
EXPERIENCE_MATCH_THRESHOLD = 0.50    # Minimum 50% experience match
```

### Extending the Rules Engine

```python
from resume_builder.rules_engine import ResumeRulesEngine

class CustomEngine(ResumeRulesEngine):
    def _calculate_experience_relevance(self, exp, job):
        # Get base score
        base_score = super()._calculate_experience_relevance(exp, job)
        
        # Add custom bonus for specific companies
        if exp.company in ['Google', 'Microsoft', 'AWS']:
            base_score *= 1.2  # 20% bonus
        
        return base_score

# Use custom engine
engine = CustomEngine()
personalized = engine.personalize(resume, job)
```

---

## Architecture

### System Components

```
┌─────────────────────────────────────────┐
│         RESUME BUILDER SYSTEM           │
├─────────────────────────────────────────┤
│                                         │
│  INPUT: Resume + Job Description       │
│    ↓                                    │
│  ┌───────────────────────────────────┐ │
│  │ Job Parser (parser.py)            │ │
│  │ • Extract skills                  │ │
│  │ • Identify technologies           │ │
│  │ • Determine experience level      │ │
│  └───────────┬───────────────────────┘ │
│    ↓         ↓                          │
│  ┌─────────────────────────────────────┐│
│  │ Rules Engine (rules_engine.py)      ││
│  │ • Skill matching                    ││
│  │ • Experience scoring               ││
│  │ • Relevance calculation            ││
│  │ • Achievement highlighting         ││
│  └───────────┬───────────────────────┬─┘│
│    ↓         ↓                       ↓  │
│  ┌──────────────────────────────────────┐│
│  │ Formatters (formatters.py)           ││
│  │ • JSON      • Markdown               ││
│  │ • Text      • Report                 ││
│  └──────────────────────────────────────┘│
│    ↓                                     │
│  OUTPUT: Personalized Resume + Analysis  │
│                                         │
└─────────────────────────────────────────┘
```

### Data Models

```
Resume                    JobDescription
├─ name                   ├─ job_title
├─ email                  ├─ company
├─ phone                  ├─ required_skills
├─ location               ├─ preferred_skills
├─ skills[]               ├─ key_technologies
├─ experience[]           ├─ experience_level
├─ education[]            └─ years_of_experience_required
└─ certifications[]

PersonalizedResume
├─ original_resume
├─ target_job
├─ personalized_summary
├─ prioritized_experience[]
├─ matched_skills[]
├─ relevance_score
├─ missing_skills[]
└─ highlighted_achievements[]
```

---

## Examples

### Example 1: Basic Analysis

```python
from resume_builder import ResumeBuilder
from examples.example_usage import create_sample_resume, create_sample_job_description

resume = create_sample_resume()
builder = ResumeBuilder()

metrics = builder.get_analysis_metrics(
    resume=resume,
    job_title="Senior Data Engineer",
    company="CloudScale Technologies",
    job_description=create_sample_job_description()
)

print(f"Relevance Score: {metrics['analysis']['relevance_score']:.1f}%")
print(f"Matched Skills: {metrics['analysis']['matched_skills']}")
print(f"Recommendation: {metrics['analysis']['recommendation']}")
```

### Example 2: Generate Personalized Resume

```python
personalized = builder.build_personalized_resume(
    resume=resume,
    job_title="Senior Data Engineer",
    company="CloudScale Technologies",
    job_description=create_sample_job_description(),
    output_format='markdown'
)

# Print or save the personalized resume
print(personalized)
```

### Example 3: Compare Multiple Jobs

```python
jobs = [
    ("Senior Data Engineer", "Company A", "job_desc_a"),
    ("Data Engineer", "Company B", "job_desc_b"),
    ("Analytics Engineer", "Company C", "job_desc_c"),
]

scores = []
for title, company, desc in jobs:
    metrics = builder.get_analysis_metrics(resume, title, company, desc)
    scores.append({
        "company": company,
        "score": metrics['analysis']['relevance_score']
    })

# Sort by score
for result in sorted(scores, key=lambda x: x['score'], reverse=True):
    print(f"{result['company']}: {result['score']:.0f}%")
```

---

## Data Models

### Resume
```python
@dataclass
class Resume:
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
```

### Skill
```python
@dataclass
class Skill:
    name: str
    proficiency_level: str  # Beginner, Intermediate, Advanced, Expert
    years_of_experience: float = 0
    keywords: List[str] = field(default_factory=list)
    category: str = ""  # Technical, Soft, Domain
```

### Experience
```python
@dataclass
class Experience:
    job_title: str
    company: str
    start_date: str  # YYYY-MM format
    end_date: Optional[str] = None
    description: str = ""
    achievements: List[str] = field(default_factory=list)
    skills_used: List[str] = field(default_factory=list)
    is_current: bool = False
```

### JobDescription
```python
@dataclass
class JobDescription:
    job_title: str
    company: str
    description: str
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    experience_level: str = "Mid-level"
    years_of_experience_required: int = 0
    responsibilities: List[str] = field(default_factory=list)
    key_technologies: List[str] = field(default_factory=list)
```

---

## Configuration

### Available Settings (config.py)

```python
# Scoring Weights
SKILL_WEIGHT = 0.40              # 40% - Skills importance
EXPERIENCE_WEIGHT = 0.35         # 35% - Experience importance
TECHNOLOGY_WEIGHT = 0.25         # 25% - Technology importance

# Matching Thresholds
SKILL_MATCH_THRESHOLD = 0.60           # 60% minimum skill match
EXPERIENCE_MATCH_THRESHOLD = 0.50      # 50% minimum experience match
OVERALL_MATCH_THRESHOLD = 0.60         # 60% overall minimum

# Data Engineering Skills (50+)
DATA_ENGINEERING_SKILLS = {
    'python', 'sql', 'spark', 'hadoop', 'etl', 'java', 'scala',
    'airflow', 'kafka', 'flink', 'aws', 'gcp', 'azure',
    'snowflake', 'bigquery', 'redshift', 'postgresql', 'mongodb',
    'docker', 'kubernetes', 'git', 'jenkins', 'tableau', 'looker',
    'pandas', 'numpy', 'dbt', 'databricks', 'delta lake',
    'ci/cd', 'terraform', 'linux', 'bash', 'hive', ...
}
```

### Customization Example

```python
from resume_builder.rules_engine import ResumeRulesEngine

# Create customized engine
engine = ResumeRulesEngine()
engine.skill_weight = 0.50           # Increase skill importance
engine.experience_weight = 0.30
engine.technology_weight = 0.20
engine.matching_threshold = 0.70     # Require 70% match

# Use with personalization
personalized = engine.personalize(resume, job)
```

---

## Testing

### Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test class
python -m pytest tests/test_resume_builder.py::TestResumeRulesEngine -v

# Run with coverage
python -m pytest tests/ --cov=resume_builder

# Run specific test
python -m pytest tests/test_resume_builder.py::TestJobDescriptionParser::test_extract_required_skills -v
```

### Test Coverage

Tests cover:
- ✅ Job description parsing
- ✅ Skill extraction accuracy
- ✅ Experience relevance scoring
- ✅ Relevance score calculation
- ✅ Output formatting
- ✅ Data model validation

---

## Troubleshooting

### Installation Issues

**Problem**: `ImportError` when importing resume_builder
```
Solution:
1. Verify you're in the project root directory
2. Run: pip install -r requirements.txt
3. Check Python version: python --version (should be 3.8+)
```

**Problem**: Modules not found
```
Solution:
1. Ensure requirements.txt is installed: pip list
2. Try: pip install --upgrade pip
3. Reinstall: pip install -r requirements.txt --force-reinstall
```

### Parser Issues

**Problem**: Skills not recognized
```
Solution:
1. Check skill spelling and capitalization
2. Add skill to DATA_ENGINEERING_SKILLS in config.py
3. Use standard skill names (e.g., "Apache Spark" not "Spark framework")
```

**Problem**: Job requirements not extracted
```
Solution:
1. Use complete job description (not summary)
2. Ensure job description includes "Required Skills" or "Requirements" section
3. Check if parser recognizes skill variations
```

### Scoring Issues

**Problem**: Relevance score too low
```
Solution:
1. Verify all skills are entered in resume
2. Check if skill names match job requirements exactly
3. Add more achievements with metrics
4. Ensure skills_used array is accurate for experiences
```

**Problem**: Wrong experience prioritized
```
Solution:
1. Ensure achievements are filled in for all experiences
2. Verify skills_used matches skills in resume
3. Make job titles clear and relevant
4. Check is_current flag is set correctly
```

### Format Issues

**Problem**: Invalid JSON output
```
Solution:
1. Verify resume data is complete (no None values)
2. Check for special characters in text fields
3. Use json.loads() to validate output
```

---

## Project Structure

```
resume-builder/
├── resume_builder/                    # Main Package
│   ├── __init__.py                   # ResumeBuilder main class
│   ├── models.py                     # Data models
│   ├── parser.py                     # Job description parser
│   ├── rules_engine.py               # Personalization engine
│   ├── formatters.py                 # Output formatters
│   └── config.py                     # Configuration & constants
│
├── tests/                             # Unit Tests
│   ├── __init__.py
│   └── test_resume_builder.py        # Comprehensive test suite
│
├── examples/                          # Examples
│   └── example_usage.py              # Complete working example
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
└── [Other config files]
```

---

## Best Practices

### Resume Preparation

✅ **Include metrics** in achievements (numbers, percentages, impact)
✅ **Use standard skill names** (e.g., "Apache Spark" not "Spark framework")
✅ **Set proficiency levels** for each skill (affects matching)
✅ **Fill achievements** with quantifiable results
✅ **Tag skills used** for each job experience
✅ **Keep descriptions** concise but detailed (2-3 sentences)

### Job Description Input

✅ **Use complete job posting** (more context = better parsing)
✅ **Include all sections** (title, requirements, responsibilities)
✅ **Use standard format** (benefits from common patterns)
✅ **Copy exactly as posted** (preserves important details)

### Score Interpretation

✅ **80%+**: Apply immediately with confidence
✅ **60-79%**: Apply, highlight matched skills in cover letter
✅ **40-59%**: Consider developing missing skills first
✅ **<40%**: Focus on better-fit roles

### Workflow

1. **Create Resume** - Build Resume object with complete data
2. **Collect Jobs** - Gather target job descriptions
3. **Run Analysis** - Analyze each job against your resume
4. **Rank Results** - Sort by relevance score
5. **Generate Resumes** - Create personalized versions for top matches
6. **Apply** - Use personalized resumes for applications
7. **Monitor** - Track which roles get interviews
8. **Improve** - Update resume and skills based on feedback

---

## Performance

- **Time Complexity**: O(n×m) where n = resume skills, m = job skills
- **Space Complexity**: O(n+m)
- **Analysis Speed**: <1 second per job
- **Scalability**: Handles multiple simultaneous analyses

---

## Future Enhancements

- [ ] PDF output format
- [ ] Integration with job boards (LinkedIn, Indeed)
- [ ] AI-powered summary generation
- [ ] Salary range analysis
- [ ] ATS (Applicant Tracking System) compatibility check
- [ ] Multiple profile support
- [ ] Resume version history
- [ ] Browser extension for one-click analysis

---

## Contributing

Contributions welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

---

## License

MIT License - Feel free to use and modify

---

## Support

For issues, questions, or feature requests:

1. Check this README for common issues
2. Review the Troubleshooting section
3. Check test cases for usage examples
4. Run `python examples/example_usage.py` to see a working example

---

## Quick Reference

### Common Commands

```bash
# Install
pip install -r requirements.txt

# Run example
python examples/example_usage.py

# Run tests
python -m pytest tests/ -v

# Check Python version
python --version

# Check imports
python -c "from resume_builder import ResumeBuilder; print('OK')"
```

### Quick Scores Guide

| Score | Status | Action |
|-------|--------|--------|
| 80%+ | ✅ Go | Apply now |
| 60-79% | 🟡 Good | Apply + highlights |
| 40-59% | 🟠 Maybe | Develop skills |
| <40% | ❌ Skip | Find better fit |

### Output Formats

```python
# Markdown (default, human-readable)
output = builder.build_personalized_resume(..., output_format='markdown')

# JSON (programmatic use)
output = builder.build_personalized_resume(..., output_format='json')

# Plain Text (universal)
output = builder.build_personalized_resume(..., output_format='text')

# Detailed Report (analysis-focused)
output = builder.build_personalized_resume(..., output_format='report')
```

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Date**: January 15, 2026  
**Repository**: Resume Builder for Data Engineers
