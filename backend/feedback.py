"""
AI Feedback and Learning System
Collects feedback from senior developers to improve AI recommendations
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Feedback(BaseModel):
    """Feedback model"""
    comment_id: str
    mr_id: int
    project_id: int
    feedback_type: str  # 'positive' or 'negative'
    reason: str
    senior_name: str
    ai_comment: str
    timestamp: str = None
    
    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        super().__init__(**data)


class LearningSystem:
    """System for collecting and applying feedback"""
    
    def __init__(self, feedback_file: str = "data/feedback.json"):
        self.feedback_file = Path(feedback_file)
        self.feedback_file.parent.mkdir(exist_ok=True)
        
        # Create file if doesn't exist
        if not self.feedback_file.exists():
            self._save_feedback([])
    
    def add_feedback(self, feedback: Feedback) -> None:
        """Add new feedback"""
        try:
            feedbacks = self._load_feedback()
            feedbacks.append(feedback.dict())
            self._save_feedback(feedbacks)
            
            logger.info(f"✅ Feedback added: {feedback.feedback_type} for comment {feedback.comment_id}")
            
            # Update learning patterns
            self._update_learning_patterns(feedback)
            
        except Exception as e:
            logger.error(f"❌ Failed to add feedback: {str(e)}")
    
    def get_feedback_stats(self) -> Dict:
        """Get feedback statistics"""
        feedbacks = self._load_feedback()
        
        positive = sum(1 for f in feedbacks if f['feedback_type'] == 'positive')
        negative = sum(1 for f in feedbacks if f['feedback_type'] == 'negative')
        
        return {
            'total': len(feedbacks),
            'positive': positive,
            'negative': negative,
            'positive_rate': positive / len(feedbacks) * 100 if feedbacks else 0
        }
    
    def get_learning_patterns(self) -> List[Dict]:
        """Get learned patterns from negative feedback"""
        patterns_file = Path("data/learning_patterns.json")
        
        if patterns_file.exists():
            with open(patterns_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return []
    
    def get_feedback_for_prompt(self) -> str:
        """Get feedback context for AI prompt"""
        patterns = self.get_learning_patterns()
        
        if not patterns:
            return ""
        
        prompt_addition = "\n\n## LEARNED PATTERNS (from senior feedback):\n"
        
        for pattern in patterns[-10:]:  # Last 10 patterns
            prompt_addition += f"- {pattern['rule']}\n"
        
        return prompt_addition
    
    def _load_feedback(self) -> List[Dict]:
        """Load feedback from file"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading feedback: {str(e)}")
            return []
    
    def _save_feedback(self, feedbacks: List[Dict]) -> None:
        """Save feedback to file"""
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(feedbacks, f, indent=2, ensure_ascii=False)
    
    def _update_learning_patterns(self, feedback: Feedback) -> None:
        """Update learning patterns based on feedback"""
        if feedback.feedback_type != 'negative':
            return
        
        patterns_file = Path("data/learning_patterns.json")
        
        # Load existing patterns
        if patterns_file.exists():
            with open(patterns_file, 'r', encoding='utf-8') as f:
                patterns = json.load(f)
        else:
            patterns = []
        
        # Add new pattern
        pattern = {
            'rule': feedback.reason,
            'context': feedback.ai_comment,
            'added_by': feedback.senior_name,
            'date': feedback.timestamp,
            'mr_id': feedback.mr_id
        }
        
        patterns.append(pattern)
        
        # Save patterns
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(patterns, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📚 New learning pattern added: {feedback.reason}")


# Global instance
learning_system = LearningSystem()
