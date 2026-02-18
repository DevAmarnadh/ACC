"""
Multi-Category Content Generator
Generates content for ALL 6 framework categories at once
"""
from typing import Dict, List
from .openrouter_ai import OpenRouterAI
from .search import search_and_format


class MultiCategoryGenerator:
    """Generate content for all 6 categories simultaneously"""
    
    CATEGORIES = {
        'new_tool_intro': 'New Tool Introduction',
        'tool_detailed_tutorial': 'Detailed Tutorial',
        'trending_ai_model': 'Trending AI Model',
        'ai_trending_news': 'AI Trending News',
        'github_open_source_repo': 'GitHub Repository',
        'instagram_engagement_content': 'Engagement Content'
    }
    
    def __init__(self):
        try:
            self.ai = OpenRouterAI()
            self.ai_available = True
        except:
            self.ai = None
            self.ai_available = False
    
    def generate_all(self, topic: str, context: str = None, model: str = "openai/gpt-3.5-turbo") -> List[Dict]:
        """
        Generate content for ALL 6 categories
        
        Args:
            topic: The main topic
            context: Additional context (like uploaded script)
            model: AI model to use
            
        Returns:
            List of 6 dictionaries, one for each category
        """
        if not self.ai_available:
            raise Exception("AI service not available")
        
        # Search for topic to get REAL facts
        print(f"Searching for: {topic}")
        search_context = search_and_format(topic)
        
        # Combine Search Results + User Context (Script)
        full_context = ""
        
        if search_context:
            full_context += f"REAL-TIME SEARCH FACTS:\n{search_context}\n\n"
            
        if context:
            full_context += f"USER UPLOADED SOURCE:\n{context}"
            
        # If no context at all, just use the search results
        if not full_context:
            full_context = search_context or "No specific context provided."
        
        results = []
        
        # Generate for each category
        for category_id, category_name in self.CATEGORIES.items():
            print(f"Generating {category_name}...")
            
            prompt = self._build_prompt(topic, category_id, full_context)
            response = self.ai.generate(prompt, model=model, max_tokens=2000)
            
            if response:
                result = self._parse_response(response, topic, category_id)
                results.append(result)
        
        return results
    
    def _build_prompt(self, topic: str, category: str, context: str) -> str:
        """Build prompt for specific category"""
        
        flows = {
            'new_tool_intro': """
1. SCROLL HOOK - Stop scrolling! Attention grabber
2. USER PROBLEM - What problem does this solve?
3. TOOL INTRODUCTION - Introduce the tool
4. UNIQUE DIFFERENTIATOR - What makes it special?
5. REAL USE CASE - Show it in action
6. WHY IT MATTERS NOW - Urgency
7. CALL TO ACTION""",
            
            'tool_detailed_tutorial': """
1. HOOK - Compelling opening
2. PROBLEM STATEMENT - Challenge to solve
3. TOOL OVERVIEW - Brief introduction
4. STEP 1, 2, 3 - Action steps
5. PRO TIPS - Expert advice
6. COMMON MISTAKES - What to avoid
7. FINAL RESULT - What they'll achieve
8. CTA""",
            
            'trending_ai_model': """
1. BREAKING HOOK - News-style opening
2. MODEL INTRODUCTION - Name and overview
3. KEY INNOVATION - What's new?
4. PERFORMANCE INSIGHT - How well it works
5. REAL WORLD APPLICATIONS - Practical uses
6. TARGET USERS - Who should use this
7. FUTURE IMPACT - Long-term meaning
8. CTA""",
            
            'ai_trending_news': """
1. VIRAL HOOK - Trending news angle
2. WHAT HAPPENED - The news/event
3. WHY IT IS TRENDING - Why people care
4. SIMPLIFIED EXPLANATION - Break it down
5. INDUSTRY IMPACT - Broader implications
6. EXPERT INSIGHT - Analysis
7. CTA""",
            
            'github_open_source_repo': """
1. HOOK - Developer-focused opening
2. REPOSITORY OVERVIEW - What is it?
3. CORE FEATURES - Key capabilities
4. WHY DEVELOPERS LIKE IT - Benefits
5. USE CASE EXAMPLE - Practical example
6. TREND SIGNALS - Stars, adoption
7. CTA""",
            
            'instagram_engagement_content': """
1. RELATABLE HOOK - Connect with audience
2. QUICK INSIGHT - The main tip
3. SIMPLE EXAMPLE - Show how it works
4. AUDIENCE QUESTION - Engage them
5. MICRO TAKEAWAY - Key learning
6. CTA"""
        }
        
        prompt = f"""Generate viral content for: {topic}

{f'CONTEXT/SOURCE MATERIAL: {context}' if context else ''}

INSTRUCTIONS:
1. Analyze the Topic and Context.
2. If source script is provided, EXTRACT key points and REWRITE them into the {category} framework.
3. STRICTLY follow the node-based structure below.
4. Do not just summarize. Transform the content to be viral and platform-specific.

CATEGORY: {category}

STORY FLOW (Follow EXACTLY):
{flows[category]}

Generate content following this EXACT flow:

MASTER_STORYLINE:
[Write 150-200 words. Map source content to the flow above. Be creative but accurate.]

YOUTUBE_SCRIPT:
[0:00] Hook
[0:10] Point 1
[0:20] Point 2
[0:30] Point 3
[0:50] CTA

INSTAGRAM_SCRIPT:
⚡ [Hook]
→ [Point 1]
→ [Point 2]
→ [Point 3]
💬 Save this!

TWITTER_THREAD:
Tweet 1: [Hook + "A thread 🧵"]
---
Tweet 2: [Point 1]
---
Tweet 3: [Point 2]
---
Tweet 4: [Point 3]
---
Tweet 5: [CTA]

CAPTION:
[Hook]
✓ [Point 1]
✓ [Point 2]
✓ [Point 3]
💬 Comment below!

Make it specific to "{topic}" following the {category} flow."""
        
        return prompt
    
    def _parse_response(self, response: str, topic: str, category: str) -> Dict:
        """Parse AI response"""
        result = {
            'topic': topic,
            'category': category,
            'master_storyline': '',
            'youtube_script': '',
            'instagram_script': '',
            'twitter_thread': [],
            'caption': '',
            'cta': ['Follow for more!', 'Share this!', 'Comment below!'],
            'hashtags': ['#AI', '#Tech', '#Innovation', '#Viral', '#Trending']
        }
        
        # Simple parsing
        lines = response.split('\n')
        current_section = None
        content = []
        
        for line in lines:
            if 'MASTER_STORYLINE:' in line:
                current_section = 'master_storyline'
                content = []
            elif 'YOUTUBE_SCRIPT:' in line:
                if current_section and content:
                    result[current_section] = '\n'.join(content).strip()
                current_section = 'youtube_script'
                content = []
            elif 'INSTAGRAM_SCRIPT:' in line:
                if current_section and content:
                    result[current_section] = '\n'.join(content).strip()
                current_section = 'instagram_script'
                content = []
            elif 'TWITTER_THREAD:' in line:
                if current_section and content:
                    result[current_section] = '\n'.join(content).strip()
                current_section = 'twitter_thread'
                content = []
            elif 'CAPTION:' in line:
                if current_section == 'twitter_thread' and content:
                    result['twitter_thread'] = [t.strip() for t in '\n'.join(content).split('---') if t.strip()]
                current_section = 'caption'
                content = []
            elif current_section:
                content.append(line)
        
        # Handle last section
        if current_section and content:
            if current_section == 'twitter_thread':
                result['twitter_thread'] = [t.strip() for t in '\n'.join(content).split('---') if t.strip()]
            else:
                result[current_section] = '\n'.join(content).strip()
        
        # Ensure we have something
        if not result['master_storyline']:
            result['master_storyline'] = response[:300]
        if not result['twitter_thread']:
            result['twitter_thread'] = [response[:280]]
        
        return result
