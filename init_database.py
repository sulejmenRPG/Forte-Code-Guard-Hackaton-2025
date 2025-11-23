"""
Database initialization script
Creates tables and populates with sample data for demo
"""

import os
from backend.database import init_db, save_review
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_data():
    """Create sample reviews for demo"""
    
    # Sample MR data
    sample_mrs = [
        {
            "id": 5,
            "iid": 5,
            "title": "Edit config.py",
            "author": {"username": "sulejmenRPG"},
            "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
            "source_branch": "ai-test-password",
            "target_branch": "main",
        },
        {
            "id": 4,
            "iid": 4,
            "title": "Fix security vulnerabilities",
            "author": {"username": "sulejmenRPG"},
            "created_at": (datetime.now() - timedelta(hours=4)).isoformat(),
            "source_branch": "fix-security",
            "target_branch": "main",
        },
        {
            "id": 3,
            "iid": 3,
            "title": "Add payment feature",
            "author": {"username": "sulejmenRPG"},
            "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
            "source_branch": "feature-payment",
            "target_branch": "main",
        }
    ]
    
    # Sample analysis results
    sample_results = [
        {
            "score": 2.0,
            "summary": "Критические уязвимости безопасности обнаружены",
            "issues": [
                {
                    "file_path": "config.py",
                    "line": 8,
                    "severity": "critical",
                    "issue_type": "security",
                    "description": "SQL injection уязвимость"
                },
                {
                    "file_path": "config.py",
                    "line": 2,
                    "severity": "critical",
                    "issue_type": "security",
                    "description": "Hardcoded password"
                },
                {
                    "file_path": "config.py",
                    "line": 3,
                    "severity": "critical",
                    "issue_type": "security",
                    "description": "Hardcoded API key"
                }
            ],
            "time_saved_minutes": 60
        },
        {
            "score": 3.5,
            "summary": "Обнаружены проблемы безопасности",
            "issues": [
                {
                    "file_path": "app.py",
                    "line": 15,
                    "severity": "critical",
                    "issue_type": "security",
                    "description": "Используйте параметризованные запросы"
                },
                {
                    "file_path": "utils.py",
                    "line": 42,
                    "severity": "medium",
                    "issue_type": "performance",
                    "description": "Неэффективный алгоритм сортировки"
                }
            ],
            "time_saved_minutes": 45
        },
        {
            "score": 7.5,
            "summary": "Код хорошего качества с минорными замечаниями",
            "issues": [
                {
                    "file_path": "models.py",
                    "line": 23,
                    "severity": "low",
                    "issue_type": "code_style",
                    "description": "Несоответствие PEP 8"
                }
            ],
            "time_saved_minutes": 30
        }
    ]
    
    # Save to database
    for mr_data, result in zip(sample_mrs, sample_results):
        try:
            save_review(mr_data, result)
            logger.info(f"✅ Saved review for MR #{mr_data['iid']}")
        except Exception as e:
            logger.error(f"❌ Failed to save MR #{mr_data['iid']}: {e}")

def main():
    """Main initialization function"""
    logger.info("🚀 Initializing database...")
    
    # Check if DATABASE_URL is set
    if not os.getenv("DATABASE_URL"):
        logger.warning("⚠️ DATABASE_URL not set! Using SQLite fallback.")
        logger.info("Set DATABASE_URL to use PostgreSQL:")
        logger.info("export DATABASE_URL=postgresql://user:pass@host:5432/db")
    
    # Initialize database
    try:
        init_db()
        logger.info("✅ Database initialized!")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        return
    
    # Create sample data
    logger.info("📝 Creating sample data...")
    create_sample_data()
    
    logger.info("✅ Database setup complete!")
    logger.info("")
    logger.info("🎯 Next steps:")
    logger.info("1. Start the backend: uvicorn backend.main:app --reload")
    logger.info("2. Create a GitLab MR to add real data")
    logger.info("3. Check the dashboard for real-time statistics!")

if __name__ == "__main__":
    main()
