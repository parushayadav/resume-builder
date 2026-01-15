"""
Resume Rules Engine - Core logic for personalizing resumes
Implements matching, scoring, and customization rules
"""
from typing import List, Dict, Tuple, Set
from .models import Resume, JobDescription, PersonalizedResume, Skill, Experience


class ResumeRulesEngine:
    """Rules engine for customizing resumes based on job descriptions"""
    
    def __init__(self):
        self.matching_threshold = 0.6  # 60% match threshold
        self.skill_weight = 0.4
        self.experience_weight = 0.35
        self.technology_weight = 0.25
    
    def personalize(self, 
                   resume: Resume, 
                   job: JobDescription) -> PersonalizedResume:
        """
        Main method to personalize a resume for a specific job
        
        Args:
            resume: Original resume
            job: Target job description
            
        Returns:
            PersonalizedResume with customized content
        """
        # Calculate matches
        skill_matches = self._match_skills(resume, job)
        technology_matches = self._match_technologies(resume, job)
        experience_matches = self._match_experience(resume, job)
        
        # Calculate relevance score
        relevance_score = self._calculate_relevance_score(
            skill_matches, technology_matches, experience_matches, job
        )
        
        # Identify missing skills
        missing_skills = self._identify_missing_skills(resume, job)
        
        # Generate personalized summary
        personalized_summary = self._generate_summary(resume, job, skill_matches)
        
        # Prioritize experience
        prioritized_experience = self._prioritize_experience(resume, job, skill_matches)
        
        # Highlight relevant achievements
        highlighted_achievements = self._highlight_achievements(
            prioritized_experience, job
        )
        
        # Get matched skills
        matched_skills = [s for s in resume.skills if s.name.lower() in skill_matches]
        
        return PersonalizedResume(
            original_resume=resume,
            target_job=job,
            personalized_summary=personalized_summary,
            prioritized_experience=prioritized_experience,
            matched_skills=matched_skills,
            relevance_score=relevance_score,
            missing_skills=missing_skills,
            highlighted_achievements=highlighted_achievements
        )
    
    def _match_skills(self, resume: Resume, job: JobDescription) -> Set[str]:
        """Match resume skills with job requirements"""
        resume_skills = {s.name.lower() for s in resume.skills}
        required_skills = {s.lower() for s in job.required_skills}
        preferred_skills = {s.lower() for s in job.preferred_skills}
        
        # Match with required (higher priority)
        matched_required = resume_skills.intersection(required_skills)
        
        # Match with preferred
        matched_preferred = resume_skills.intersection(preferred_skills)
        
        # Combine matches
        matches = matched_required.union(matched_preferred)
        
        return matches
    
    def _match_technologies(self, resume: Resume, job: JobDescription) -> Set[str]:
        """Match technologies in resume with job requirements"""
        resume_skills_lower = {s.name.lower() for s in resume.skills}
        resume_tech = resume_skills_lower.union(resume_skills_lower)  # Combine skill names
        
        job_tech = {t.lower() for t in job.key_technologies}
        
        return resume_tech.intersection(job_tech)
    
    def _match_experience(self, resume: Resume, job: JobDescription) -> List[Experience]:
        """Find most relevant experience entries"""
        relevant_experiences = []
        
        for exp in resume.experience:
            relevance = self._calculate_experience_relevance(exp, job)
            if relevance > self.matching_threshold:
                relevant_experiences.append((exp, relevance))
        
        # Sort by relevance
        relevant_experiences.sort(key=lambda x: x[1], reverse=True)
        
        return [exp for exp, _ in relevant_experiences]
    
    def _calculate_experience_relevance(self, exp: Experience, job: JobDescription) -> float:
        """Calculate how relevant an experience entry is to the job"""
        job_skills_lower = {s.lower() for s in job.required_skills + job.key_technologies}
        exp_skills_lower = {s.lower() for s in exp.skills_used}
        
        if not job_skills_lower:
            return 0.5
        
        # Calculate skill overlap
        skill_overlap = len(exp_skills_lower.intersection(job_skills_lower)) / len(job_skills_lower)
        
        # Check if job title is related
        title_relevance = self._calculate_title_relevance(exp.job_title, job.job_title)
        
        # Combine scores
        combined_score = (skill_overlap * 0.6) + (title_relevance * 0.4)
        
        return combined_score
    
    def _calculate_title_relevance(self, exp_title: str, job_title: str) -> float:
        """Calculate relevance between two job titles"""
        exp_words = set(exp_title.lower().split())
        job_words = set(job_title.lower().split())
        
        # Remove common words
        common_words = {'engineer', 'developer', 'senior', 'junior', 'lead'}
        exp_words -= common_words
        job_words -= common_words
        
        if not job_words:
            return 0.5
        
        overlap = len(exp_words.intersection(job_words)) / len(job_words)
        return overlap
    
    def _calculate_relevance_score(self,
                                   skill_matches: Set[str],
                                   tech_matches: Set[str],
                                   exp_matches: List[Experience],
                                   job: JobDescription) -> float:
        """
        Calculate overall relevance score (0-100)
        Based on skill matches, technology overlap, and experience relevance
        """
        required_skills_count = len(job.required_skills)
        all_skills_count = required_skills_count + len(job.preferred_skills)
        
        # Skill score (40% weight)
        if required_skills_count > 0:
            skill_score = (len(skill_matches) / required_skills_count) * 100
        else:
            skill_score = 50
        
        # Technology score (25% weight)
        if len(job.key_technologies) > 0:
            tech_score = (len(tech_matches) / len(job.key_technologies)) * 100
        else:
            tech_score = 50
        
        # Experience score (35% weight)
        if len(exp_matches) > 0:
            exp_score = min(len(exp_matches) * 25, 100)  # Max 100
        else:
            exp_score = 0
        
        # Weighted average
        total_score = (
            (skill_score * self.skill_weight) +
            (tech_score * self.technology_weight) +
            (exp_score * self.experience_weight)
        )
        
        return min(total_score, 100)  # Cap at 100
    
    def _identify_missing_skills(self, resume: Resume, job: JobDescription) -> List[str]:
        """Identify skills from job that are missing in resume"""
        resume_skills = {s.name.lower() for s in resume.skills}
        required_skills = {s.lower() for s in job.required_skills}
        
        missing = required_skills - resume_skills
        
        return sorted(list(missing))
    
    def _generate_summary(self, 
                         resume: Resume, 
                         job: JobDescription,
                         matched_skills: Set[str]) -> str:
        """
        Generate a personalized professional summary
        Tailored to the job requirements
        """
        summary_parts = []
        
        # Start with role/level
        summary_parts.append(f"{job.experience_level.title()} {job.job_title} ")
        
        # Add key matched skills
        if matched_skills:
            top_skills = list(matched_skills)[:3]
            summary_parts.append(f"with expertise in {', '.join(top_skills)}")
        
        # Add value proposition
        summary_parts.append(f"specializing in data engineering solutions")
        
        # Add relevant experience
        if resume.experience:
            years_total = len(resume.experience)
            summary_parts.append(
                f"with {years_total}+ years of experience delivering data pipelines and infrastructure"
            )
        
        # Add key technologies
        if job.key_technologies:
            top_tech = job.key_technologies[:2]
            summary_parts.append(f"skilled in {', '.join(top_tech)}")
        
        summary = ". ".join(summary_parts) + "."
        
        return summary
    
    def _prioritize_experience(self,
                              resume: Resume,
                              job: JobDescription,
                              matched_skills: Set[str]) -> List[Experience]:
        """
        Reorder experience entries by relevance to job
        Most relevant first
        """
        scored_experiences = []
        
        for exp in resume.experience:
            # Score based on skill match
            exp_skills = {s.lower() for s in exp.skills_used}
            skill_overlap = len(exp_skills.intersection(matched_skills))
            
            # Boost score for current positions
            recency_boost = 1.5 if exp.is_current else 1.0
            
            score = skill_overlap * recency_boost
            scored_experiences.append((exp, score))
        
        # Sort by score descending
        scored_experiences.sort(key=lambda x: x[1], reverse=True)
        
        return [exp for exp, _ in scored_experiences]
    
    def _highlight_achievements(self,
                               experiences: List[Experience],
                               job: JobDescription) -> List[str]:
        """
        Extract and highlight achievements most relevant to job
        Focus on quantifiable results and job-related keywords
        """
        highlighted = []
        job_keywords = set(job.required_skills + job.key_technologies)
        
        for exp in experiences[:2]:  # Look at top 2 experiences
            for achievement in exp.achievements:
                # Score achievement based on keyword matches
                achievement_lower = achievement.lower()
                keyword_matches = sum(
                    1 for keyword in job_keywords 
                    if keyword.lower() in achievement_lower
                )
                
                # Prioritize achievements with numbers/metrics
                has_metric = any(char.isdigit() for char in achievement)
                
                if keyword_matches > 0 or has_metric:
                    highlighted.append(achievement)
        
        return highlighted[:5]  # Return top 5
    
    def get_recommendation_report(self, personalized: PersonalizedResume) -> Dict:
        """
        Generate a detailed recommendation report
        """
        return {
            "relevance_score": personalized.relevance_score,
            "matched_skills": [s.name for s in personalized.matched_skills],
            "missing_skills": personalized.missing_skills,
            "skill_match_percentage": f"{(len(personalized.matched_skills) / max(1, len(personalized.original_resume.skills)) * 100):.1f}%",
            "recommended_improvements": [
                f"Learn: {', '.join(personalized.missing_skills[:3])}" if personalized.missing_skills else "All required skills present",
                f"Highlight: {', '.join([a[:50] + '...' if len(a) > 50 else a for a in personalized.highlighted_achievements[:2]])}" if personalized.highlighted_achievements else "No specific achievements to highlight"
            ],
            "top_matching_experience": [e.job_title for e in personalized.prioritized_experience[:3]],
            "personalized_summary": personalized.personalized_summary,
            "recommendation": self._generate_recommendation(personalized)
        }
    
    def _generate_recommendation(self, personalized: PersonalizedResume) -> str:
        """Generate overall recommendation"""
        score = personalized.relevance_score
        
        if score >= 80:
            return "Excellent match! Your resume aligns well with this position. Ready to apply."
        elif score >= 60:
            return f"Good match ({score:.0f}%). Consider highlighting matched skills and addressing missing skills."
        elif score >= 40:
            return f"Moderate match ({score:.0f}%). Focus on relevant experience and consider upskilling in required areas."
        else:
            return f"Limited match ({score:.0f}%). Consider developing key skills before applying."
