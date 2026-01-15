"""
Configuration for Resume Builder
Centralized settings and constants
"""

# Scoring Weights
SKILL_WEIGHT = 0.40          # 40% - Primary importance
EXPERIENCE_WEIGHT = 0.35     # 35% - Experience relevance
TECHNOLOGY_WEIGHT = 0.25     # 25% - Technology stack alignment

# Matching Thresholds
SKILL_MATCH_THRESHOLD = 0.60       # 60% skill match minimum
EXPERIENCE_MATCH_THRESHOLD = 0.50  # 50% experience match minimum
OVERALL_MATCH_THRESHOLD = 0.60     # 60% overall relevance minimum

# Data Engineering Domain Skills
DATA_ENGINEERING_SKILLS = {
    # Languages
    'python', 'scala', 'java', 'sql', 'r', 'bash', 'golang',
    
    # Big Data & Processing
    'spark', 'hadoop', 'mapreduce', 'flink', 'kafka', 'storm',
    
    # Workflow Orchestration
    'airflow', 'luigi', 'dagster', 'oozie', 'prefect', 'kestra',
    
    # Data Warehousing
    'snowflake', 'bigquery', 'redshift', 'delta lake', 'iceberg',
    'hive', 'presto', 'trino', 'athena',
    
    # Databases
    'postgresql', 'mysql', 'oracle', 'mongodb', 'cassandra', 'hbase',
    'elasticsearch', 'dynamodb',
    
    # Cloud Platforms
    'aws', 'gcp', 'azure', 's3', 'gcs', 'blob storage',
    
    # Container & Orchestration
    'docker', 'kubernetes', 'docker-compose', 'helm',
    
    # Version Control
    'git', 'github', 'gitlab', 'bitbucket',
    
    # CI/CD
    'jenkins', 'gitlab-ci', 'github-actions', 'circleci', 'travis-ci',
    
    # Data Transformation
    'dbt', 'talend', 'informatica', 'pentaho', 'apache nifi',
    
    # Monitoring & Logging
    'datadog', 'prometheus', 'grafana', 'elk', 'splunk', 'cloudwatch',
    
    # Infrastructure as Code
    'terraform', 'cloudformation', 'ansible', 'puppet',
    
    # API & Integration
    'rest', 'graphql', 'grpc', 'mqtt',
    
    # Testing & Quality
    'pytest', 'junit', 'datatest', 'great_expectations',
    
    # Serialization
    'json', 'parquet', 'avro', 'protobuf', 'delta',
}

# Experience Level Definitions
EXPERIENCE_LEVELS = {
    'entry-level': 0,
    'junior': 1,
    'mid-level': 2,
    'senior': 3,
    'lead': 4,
    'principal': 5,
}

# Output Formats
OUTPUT_FORMATS = {
    'json': 'JSON format (machine-readable)',
    'markdown': 'Markdown format (readable, shareable)',
    'text': 'Plain text format (universal)',
    'report': 'Detailed analysis report with recommendations',
}

# Proficiency Levels
PROFICIENCY_LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Expert']

# Score Interpretation
SCORE_INTERPRETATION = {
    (80, 100): 'Excellent - Perfect fit for this role',
    (60, 79): 'Good - Strong match with this position',
    (40, 59): 'Moderate - Partial match, some development needed',
    (20, 39): 'Limited - Significant skill gaps',
    (0, 19): 'Poor - Not well-suited for this role',
}

# Skills Categories
SKILL_CATEGORIES = [
    'Technical',
    'Domain',
    'Soft',
    'Leadership',
    'Tools',
    'Methodologies',
]

# Default Configuration
DEFAULT_CONFIG = {
    'skill_weight': SKILL_WEIGHT,
    'experience_weight': EXPERIENCE_WEIGHT,
    'technology_weight': TECHNOLOGY_WEIGHT,
    'skill_match_threshold': SKILL_MATCH_THRESHOLD,
    'experience_match_threshold': EXPERIENCE_MATCH_THRESHOLD,
    'overall_match_threshold': OVERALL_MATCH_THRESHOLD,
    'default_output_format': 'markdown',
    'max_highlighted_achievements': 5,
    'max_prioritized_experiences': 5,
    'max_missing_skills_to_show': 5,
}


def get_interpretation(score: float) -> str:
    """Get human-readable interpretation of relevance score"""
    for (min_score, max_score), interpretation in SCORE_INTERPRETATION.items():
        if min_score <= score <= max_score:
            return interpretation
    return "Unknown score"


def get_skill_category(skill_name: str) -> str:
    """Determine skill category (placeholder for future ML)"""
    skill_lower = skill_name.lower()
    
    if any(keyword in skill_lower for keyword in ['python', 'java', 'sql', 'spark', 'aws', 'gcp']):
        return 'Technical'
    elif any(keyword in skill_lower for keyword in ['leadership', 'communication', 'teamwork']):
        return 'Soft'
    elif any(keyword in skill_lower for keyword in ['data', 'etl', 'warehouse']):
        return 'Domain'
    else:
        return 'Tools'
