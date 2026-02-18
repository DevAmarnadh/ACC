"""
Google Search Integration
Searches Google for topic information before generating content
"""
import requests
from typing import List, Dict, Optional


def search_google(query: str, num_results: int = 5) -> Optional[str]:
    """
    Search Google for information about the topic
    
    Args:
        query: Search query
        num_results: Number of results to fetch
        
    Returns:
        Formatted search results as context string
    """
    try:
        # Use DuckDuckGo Instant Answer API (no API key needed)
        url = "https://api.duckduckgo.com/"
        params = {
            'q': query,
            'format': 'json',
            'no_html': 1,
            'skip_disambig': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            context_parts = []
            
            # Abstract
            if data.get('Abstract'):
                context_parts.append(f"Overview: {data['Abstract']}")
            
            # Related topics
            if data.get('RelatedTopics'):
                topics = []
                for topic in data['RelatedTopics'][:3]:
                    if isinstance(topic, dict) and topic.get('Text'):
                        topics.append(topic['Text'])
                if topics:
                    context_parts.append(f"Related Info: {' | '.join(topics)}")
            
            if context_parts:
                return "\n\n".join(context_parts)
            else:
                return f"Search query: {query} (Use general knowledge)"
        
        return None
        
    except Exception as e:
        print(f"Search error: {e}")
        return None


def search_and_format(topic: str) -> str:
    """
    Search for topic and format results for AI prompt
    
    Args:
        topic: The topic to search for
        
    Returns:
        Formatted context string
    """
    results = search_google(topic)
    
    if results:
        return f"""
SEARCHED INFORMATION:
{results}

Use this information to make the content more accurate and relevant.
"""
    else:
        return ""
