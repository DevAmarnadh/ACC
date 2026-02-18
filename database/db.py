"""
Database module for PostgreSQL (Supabase) connection
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from datetime import datetime
import json
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

Base = declarative_base()

class ContentHistory(Base):
    """Content history model for PostgreSQL"""
    __tablename__ = 'content_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(500), nullable=False)
    category = Column(String(100), nullable=False)
    master_storyline = Column(Text, nullable=False)
    youtube_script = Column(Text, nullable=False)
    instagram_script = Column(Text, nullable=False)
    twitter_thread = Column(JSON, nullable=False)
    caption = Column(Text, nullable=False)
    cta = Column(JSON, nullable=False)
    hashtags = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'topic': self.topic,
            'category': self.category,
            'master_storyline': self.master_storyline,
            'youtube_script': self.youtube_script,
            'instagram_script': self.instagram_script,
            'twitter_thread': self.twitter_thread,
            'caption': self.caption,
            'cta': self.cta,
            'hashtags': self.hashtags,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Database:
    """Database manager for PostgreSQL"""
    
    def __init__(self):
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL not found in environment variables")
        
        # Create engine with connection pooling and SSL
        try:
            self.engine = create_engine(
                database_url,
                echo=False,
                poolclass=NullPool,  # Disable pooling for serverless
                connect_args={
                    'connect_timeout': 10,
                    'sslmode': 'require'
                }
            )
            self.SessionLocal = sessionmaker(bind=self.engine)
            self.connected = True
        except Exception as e:
            print(f"Database connection error: {e}")
            self.connected = False
            self.engine = None
            self.SessionLocal = None
    
    def test_connection(self) -> bool:
        """Test database connection"""
        if not self.connected or not self.engine:
            return False
        
        try:
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def init_db(self):
        """Initialize database tables"""
        if not self.connected or not self.engine:
            return False
        
        try:
            Base.metadata.create_all(self.engine)
            return True
        except Exception as e:
            print(f"Error initializing database: {e}")
            return False
    
    def save_content(self, topic: str, category: str, content_data: Dict) -> int:
        """
        Save generated content to database
        
        Args:
            topic: The original topic
            category: Content category
            content_data: Generated content dictionary
            
        Returns:
            ID of the saved content
        """
        if not self.connected or not self.SessionLocal:
            raise Exception("Database not connected")
        
        session = self.SessionLocal()
        try:
            content = ContentHistory(
                topic=topic,
                category=category,
                master_storyline=content_data['master_storyline'],
                youtube_script=content_data['youtube_script'],
                instagram_script=content_data['instagram_script'],
                twitter_thread=content_data['twitter_thread'],
                caption=content_data['caption'],
                cta=content_data['cta'],
                hashtags=content_data['hashtags']
            )
            session.add(content)
            session.commit()
            session.refresh(content)
            return content.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_history(self, limit: int = 20) -> List[Dict]:
        """
        Get content generation history
        
        Args:
            limit: Maximum number of items to return
            
        Returns:
            List of history items
        """
        if not self.connected or not self.SessionLocal:
            return []
        
        session = self.SessionLocal()
        try:
            contents = session.query(ContentHistory)\
                .order_by(ContentHistory.created_at.desc())\
                .limit(limit)\
                .all()
            
            return [
                {
                    'id': c.id,
                    'topic': c.topic,
                    'category': c.category,
                    'created_at': c.created_at.isoformat() if c.created_at else None
                }
                for c in contents
            ]
        except Exception as e:
            print(f"Error fetching history: {e}")
            return []
        finally:
            session.close()
    
    def get_content_by_id(self, content_id: int) -> Optional[Dict]:
        """
        Get specific content by ID
        
        Args:
            content_id: ID of the content
            
        Returns:
            Content dictionary or None
        """
        if not self.connected or not self.SessionLocal:
            return None
        
        session = self.SessionLocal()
        try:
            content = session.query(ContentHistory)\
                .filter(ContentHistory.id == content_id)\
                .first()
            
            if content:
                return content.to_dict()
            return None
        except Exception as e:
            print(f"Error fetching content: {e}")
            return None
        finally:
            session.close()
    
    def delete_content(self, content_id: int) -> bool:
        """
        Delete content by ID
        
        Args:
            content_id: ID of the content to delete
            
        Returns:
            True if deleted, False if not found
        """
        if not self.connected or not self.SessionLocal:
            return False
        
        session = self.SessionLocal()
        try:
            content = session.query(ContentHistory)\
                .filter(ContentHistory.id == content_id)\
                .first()
            
            if content:
                session.delete(content)
                session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error deleting content: {e}")
            return False
        finally:
            session.close()
    
    def get_stats(self) -> Dict:
        """
        Get usage statistics
        
        Returns:
            Statistics dictionary
        """
        if not self.connected or not self.SessionLocal:
            return {
                'total_content_generated': 0,
                'category_breakdown': {},
                'last_7_days': 0
            }
        
        session = self.SessionLocal()
        try:
            total_content = session.query(ContentHistory).count()
            
            # Category breakdown
            category_stats = {}
            categories = session.query(ContentHistory.category).distinct().all()
            for (category,) in categories:
                count = session.query(ContentHistory)\
                    .filter(ContentHistory.category == category)\
                    .count()
                category_stats[category] = count
            
            # Recent activity (last 7 days)
            from datetime import timedelta
            week_ago = datetime.now() - timedelta(days=7)
            recent_count = session.query(ContentHistory)\
                .filter(ContentHistory.created_at >= week_ago)\
                .count()
            
            return {
                'total_content_generated': total_content,
                'category_breakdown': category_stats,
                'last_7_days': recent_count
            }
        except Exception as e:
            print(f"Error fetching stats: {e}")
            return {
                'total_content_generated': 0,
                'category_breakdown': {},
                'last_7_days': 0
            }
        finally:
            session.close()
