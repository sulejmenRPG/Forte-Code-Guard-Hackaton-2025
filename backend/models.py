"""
Data models for the application
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import os
from datetime import datetime


class Severity(str, Enum):
    """Issue severity levels"""
    CRITICAL = "critical"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IssueType(str, Enum):
    """Types of code issues"""
    SECURITY = "security"
    PERFORMANCE = "performance"
    BUG = "bug"
    CODE_STYLE = "code_style"
    BEST_PRACTICE = "best_practice"
    ARCHITECTURE = "architecture"


class CodeIssue(BaseModel):
    """Represents a single code issue found during analysis"""
    line: Optional[int] = None
    file_path: str
    severity: Severity
    issue_type: IssueType
    description: str
    suggestion: str
    code_snippet: Optional[str] = None


class AnalysisResult(BaseModel):
    """Result of code analysis"""
    summary: str
    score: float = Field(ge=0, le=10)
    issues: List[CodeIssue]
    recommendation: str  # "merge", "needs_fixes", "reject"
    critical_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    estimated_time_saved: int = 0  # minutes


class WebhookPayload(BaseModel):
    """GitLab webhook payload structure"""
    object_kind: str
    object_attributes: Dict[str, Any]
    project: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    version: str


class ReviewSummary(BaseModel):
    """Summary for posting to GitLab MR"""
    title: str
    score: float
    recommendation: str
    critical_issues: int
    medium_issues: int
    low_issues: int
    summary_text: str
    detailed_issues: List[str]


class CodeReviewRecord(BaseModel):
    """Database record for code review"""
    id: Optional[int] = None
    merge_request_id: int
    project_id: int
    project_name: str
    author: str
    team: Optional[str] = None
    created_at: datetime
    analysis_time: int  # seconds
    score: float
    critical_issues: int
    medium_issues: int
    low_issues: int
    status: str
    senior_time_saved: int  # minutes


class AISettings(BaseModel):
    """AI Configuration Settings"""
    custom_rules: Optional[str] = None
    min_score: float = Field(default=7.0, ge=0, le=10)
    max_length: int = Field(default=50000, gt=0)
