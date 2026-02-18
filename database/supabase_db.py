"""
Supabase Database Module
Clean implementation with filters
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class ContentHistory(Base):
    """Content history model"""
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


class SupabaseDB:
    """Supabase PostgreSQL Database Manager"""
    
    def __init__(self):
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL not found")
        
        try:
            self.engine = create_engine(
                database_url,
                echo=False,
                poolclass=NullPool,
                connect_args={
                    'connect_timeout': 10,
                    'sslmode': 'require'
                }
            )
            self.SessionLocal = sessionmaker(bind=self.engine)
            self.connected = True
            
            # Initialize tables
            Base.metadata.create_all(self.engine)
        except Exception as e:
            print(f"Database error: {e}")
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
        except:
            return False
    
    def save_content(self, topic: str, category: str, content_data: Dict) -> int:
        """Save generated content"""
        if not self.connected:
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
    
    def get_history(
        self, 
        limit: int = 20,
        category_filter: Optional[str] = None,
        date_filter: str = "All Time"
    ) -> List[Dict]:
        """Get content history with filters"""
        if not self.connected:
            return []
        
        session = self.SessionLocal()
        try:
            query = session.query(ContentHistory)
            
            # Apply category filter (expects internal category name)
            if category_filter:
                query = query.filter(ContentHistory.category == category_filter)
            
            # Apply date filter
            if date_filter != "All Time":
                now = datetime.now()
                if date_filter == "Today":
                    start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
                elif date_filter == "This Week":
                    start_date = now - timedelta(days=7)
                elif date_filter == "This Month":
                    start_date = now - timedelta(days=30)
                else:
                    start_date = None
                
                if start_date:
                    query = query.filter(ContentHistory.created_at >= start_date)
            
            # Order and limit
            contents = query.order_by(ContentHistory.created_at.desc()).limit(limit).all()
            
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
        """Get specific content by ID"""
        if not self.connected:
            return None
        
        session = self.SessionLocal()
        try:
            content = session.query(ContentHistory)\
                .filter(ContentHistory.id == content_id)\
                .first()
            
            if content:
                return content.to_dict()
            return None
        except:
            return None
        finally:
            session.close()
    
    def get_stats(self) -> Dict:
        """Get usage statistics"""
        if not self.connected:
            return {'total': 0, 'week': 0}
        
        session = self.SessionLocal()
        try:
            total = session.query(ContentHistory).count()
            
            week_ago = datetime.now() - timedelta(days=7)
            week_count = session.query(ContentHistory)\
                .filter(ContentHistory.created_at >= week_ago)\
                .count()
            
            return {
                'total': total,
                'week': week_count
            }
        except:
            return {'total': 0, 'week': 0}
        finally:
            session.close()
