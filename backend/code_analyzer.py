"""
Code Analyzer - Main logic for analyzing code changes
"""

import logging
from typing import Dict, Any, List
import asyncio

from backend.models import AnalysisResult, CodeIssue, Severity, IssueType
from backend.llm_provider import get_llm_provider
from backend.prompts import get_review_prompt
from backend.config import settings
from backend.feedback import learning_system

logger = logging.getLogger(__name__)


class CodeAnalyzer:
    """Analyzes code changes using LLM"""
    
    def __init__(self):
        self.llm_provider = get_llm_provider()
        logger.info("✅ Code Analyzer initialized")
    
    def _format_changes_for_analysis(self, changes: List[Dict]) -> str:
        """Format GitLab changes into readable text for LLM"""
        formatted = []
        
        for change in changes:
            file_path = change.get('new_path', change.get('old_path', 'unknown'))
            diff = change.get('diff', '')
            
            formatted.append(f"\n{'='*60}")
            formatted.append(f"FILE: {file_path}")
            formatted.append(f"{'='*60}")
            formatted.append(diff)
        
        return "\n".join(formatted)
    
    def _truncate_if_needed(self, code_text: str, max_length: int = None) -> str:
        """Truncate code if it exceeds max length"""
        max_length = max_length or settings.MAX_CODE_LENGTH
        
        if len(code_text) > max_length:
            logger.warning(f"⚠️ Code length {len(code_text)} exceeds limit {max_length}. Truncating...")
            return code_text[:max_length] + "\n\n... (код обрезан из-за размера)"
        
        return code_text
    
    def _parse_llm_response(self, llm_result: Dict[str, Any]) -> AnalysisResult:
        """Parse LLM response into structured AnalysisResult"""
        
        # Parse issues
        issues = []
        critical_count = 0
        medium_count = 0
        low_count = 0
        
        for issue_data in llm_result.get('issues', []):
            try:
                severity = Severity(issue_data.get('severity', 'info'))
                issue_type = IssueType(issue_data.get('issue_type', 'best_practice'))
                
                issue = CodeIssue(
                    line=issue_data.get('line'),
                    file_path=issue_data.get('file_path', 'unknown'),
                    severity=severity,
                    issue_type=issue_type,
                    description=issue_data.get('description', ''),
                    suggestion=issue_data.get('suggestion', ''),
                    code_snippet=issue_data.get('code_snippet')
                )
                
                issues.append(issue)
                
                # Count by severity
                if severity == Severity.CRITICAL:
                    critical_count += 1
                elif severity == Severity.MEDIUM:
                    medium_count += 1
                elif severity == Severity.LOW:
                    low_count += 1
                    
            except Exception as e:
                logger.warning(f"⚠️ Failed to parse issue: {str(e)}")
                continue
        
        # Create analysis result
        result = AnalysisResult(
            summary=llm_result.get('summary', 'Анализ завершён'),
            score=float(llm_result.get('score', 7.0)),
            issues=issues,
            recommendation=llm_result.get('recommendation', 'needs_review'),
            critical_count=critical_count,
            medium_count=medium_count,
            low_count=low_count,
            estimated_time_saved=llm_result.get('estimated_time_saved', 90)
        )
        
        return result
    
    async def analyze_changes(self, changes: List[Dict], mr_data: Dict, custom_rules: str = None) -> Dict[str, Any]:
        """
        Main method to analyze code changes
        
        Args:
            changes: List of file changes from GitLab
            mr_data: Merge Request metadata
            custom_rules: Optional custom rules from settings
            
        Returns:
            Analysis result dictionary
        """
        logger.info(f"🔍 Analyzing {len(changes)} file(s)")
        
        try:
            # Format changes for LLM
            code_text = self._format_changes_for_analysis(changes)
            code_text = self._truncate_if_needed(code_text)
            
            # Get review prompt with custom rules if provided
            import os
            rules = custom_rules or os.getenv("CUSTOM_RULES", "")
            prompt = get_review_prompt(code_text, custom_rules=rules if rules else None)
            
            # Add learned patterns from feedback
            learned_context = learning_system.get_feedback_for_prompt()
            if learned_context:
                prompt += learned_context
                logger.info("📚 Added learned patterns to prompt")
            
            # Call LLM with timeout
            llm_result = await asyncio.wait_for(
                self.llm_provider.analyze_code(prompt),
                timeout=settings.ANALYSIS_TIMEOUT
            )
            
            # Parse result
            analysis = self._parse_llm_response(llm_result)
            
            logger.info(f"✅ Analysis complete: {len(analysis.issues)} issues found")
            logger.info(f"   Critical: {analysis.critical_count}, Medium: {analysis.medium_count}, Low: {analysis.low_count}")
            
            return analysis.model_dump()
            
        except asyncio.TimeoutError:
            logger.error(f"⏱️ Analysis timeout after {settings.ANALYSIS_TIMEOUT}s")
            raise Exception("Analysis timeout")
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {str(e)}")
            raise
