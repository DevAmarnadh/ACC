"""
AI-Powered Content Generator using OpenRouter
Generates content using selected AI models with Google search
"""
from typing import Dict, Optional
from .openrouter_ai import OpenRouterAI
from .search import search_and_format


class AIContentGenerator:
    """AI-powered content generation using OpenRouter"""
    
    def __init__(self):
        try:
            self.ai = OpenRouterAI()
            self.ai_available = True
        except:
            self.ai = None
            self.ai_available = False
    
    def generate(self, topic: str, context: Optional[str] = None, model: str = "openai/gpt-3.5-turbo") -> Dict:
        """
        Generate multi-platform content using AI with Google search
        
        Args:
            topic: The main topic
            context: Additional context
            model: AI model to use
            
        Returns:
            Dictionary with all generated content
        """
        if not self.ai_available:
            raise Exception("AI service not available. Check OPENROUTER_API_KEY in .env")
        
        # Always search for the topic to get REAL facts
        print(f"Searching for: {topic}")
        search_context = search_and_format(topic)
        
        # Combine Search Results + User Script
        full_context = ""
        
        if search_context:
            full_context += f"REAL-TIME SEARCH FACTS:\n{search_context}\n\n"
            
        if context:
            full_context += f"USER UPLOADED SOURCE:\n{context}"
        
        # Build the prompt with search results
        prompt = self._build_prompt(topic, full_context)
        
        # Generate content using AI
        print(f"Generating with model: {model}")
        response = self.ai.generate(prompt, model=model, max_tokens=3500)
        
        if not response:
            raise Exception("Failed to generate content from AI")
        
        # Debug: Print first 500 chars of response
        print(f"AI Response (first 500 chars): {response[:500]}")
        
        # Parse the AI response
        return self._parse_response(response, topic)
    
    def _build_prompt(self, topic: str, context: Optional[str]) -> str:
        """Build the prompt for AI generation following framework.md"""
        prompt = f"""Generate viral multi-platform content for: {topic}

{f'CONTEXT/SOURCE MATERIAL: {context}' if context else ''}

INSTRUCTIONS:
1. Analyze the Topic and Context (if provided).
2. If a script/content is provided in Context, EXTRACT its key messages but REWRITE them to fit the framework below.
3. DO NOT just summarize. You must TRANSFORM the content into the requested format.
4. Ensures the content is viral, engaging, and follows the "Hook -> Value -> CTA" principle.

OUTPUT FORMAT (YOU MUST GENERATE ALL SECTIONS):

CATEGORY: [one of: new_tool_intro, tool_detailed_tutorial, trending_ai_model, ai_trending_news, github_open_source_repo, instagram_engagement_content]

MASTER_STORYLINE:
[Write 200-300 words. If source script provided, map its points to the framework nodes. If no script, generate creative content.]
[Follow the framework flow for the category EXACTLY.]

YOUTUBE_SCRIPT:
[0:00] Hook - Grab attention (Use the Hook from framework)
[0:05] Main point 1
[0:15] Main point 2  
[0:25] Main point 3
[0:35] Main point 4
[0:50] CTA - Call to action

INSTAGRAM_SCRIPT:
⚡ HOOK: [Attention grabber]
→ [Point 1]
→ [Point 2]
→ [Point 3]
→ [Point 4]
💬 Save this for later!
Follow @youraccount for daily tips

TWITTER_THREAD:
Tweet 1: [Hook + "A thread 🧵"]
---
Tweet 2: [First key point]
---
Tweet 3: [Second key point]
---
Tweet 4: [Third key point]
---
Tweet 5: [Fourth key point]
---
Tweet 6: [CTA - Follow for more]

CAPTION:
[Hook line]

Here's what you need to know:
✓ [Key point 1]
✓ [Key point 2]
✓ [Key point 3]

💬 What do you think? Comment below!
🔖 Save this for later
📤 Share with someone who needs this

CTA:
[CTA option 1]
---
[CTA option 2]
---
[CTA option 3]

HASHTAGS:
#AI #Tech #Innovation #TechNews #Viral #Trending #MustKnow #Technology #Future #Digital #ContentCreator #SocialMedia

IMPORTANT: Generate ALL sections above. Make content specific to the topic "{topic}". Be detailed and engaging!"""
        
        return prompt
    
    def _parse_response(self, response: str, topic: str) -> Dict:
        """Parse AI response into structured format"""
        result = {
            'topic': topic,
            'category': 'new_tool_intro',
            'master_storyline': '',
            'youtube_script': '',
            'instagram_script': '',
            'twitter_thread': [],
            'caption': '',
            'cta': [],
            'hashtags': []
        }
        
        try:
            # Extract sections
            sections = response.split('\n\n')
            current_section = None
            current_content = []
            
            for section in sections:
                section = section.strip()
                
                if section.startswith('CATEGORY:'):
                    result['category'] = section.replace('CATEGORY:', '').strip()
                
                elif section.startswith('MASTER_STORYLINE:'):
                    current_section = 'master_storyline'
                    current_content = [section.replace('MASTER_STORYLINE:', '').strip()]
                
                elif section.startswith('YOUTUBE_SCRIPT:'):
                    if current_section and current_content:
                        result[current_section] = '\n\n'.join(current_content).strip()
                    current_section = 'youtube_script'
                    current_content = [section.replace('YOUTUBE_SCRIPT:', '').strip()]
                
                elif section.startswith('INSTAGRAM_SCRIPT:'):
                    if current_section and current_content:
                        result[current_section] = '\n\n'.join(current_content).strip()
                    current_section = 'instagram_script'
                    current_content = [section.replace('INSTAGRAM_SCRIPT:', '').strip()]
                
                elif section.startswith('TWITTER_THREAD:'):
                    if current_section and current_content:
                        result[current_section] = '\n\n'.join(current_content).strip()
                    current_section = 'twitter_thread'
                    current_content = []
                
                elif section.startswith('CAPTION:'):
                    if current_section == 'twitter_thread' and current_content:
                        result['twitter_thread'] = [t.strip() for t in '\n\n'.join(current_content).split('---') if t.strip()]
                    current_section = 'caption'
                    current_content = [section.replace('CAPTION:', '').strip()]
                
                elif section.startswith('CTA:'):
                    if current_section and current_content:
                        result[current_section] = '\n\n'.join(current_content).strip()
                    current_section = 'cta'
                    current_content = []
                
                elif section.startswith('HASHTAGS:'):
                    if current_section == 'cta' and current_content:
                        result['cta'] = [c.strip() for c in '\n\n'.join(current_content).split('---') if c.strip()]
                    hashtags_text = section.replace('HASHTAGS:', '').strip()
                    result['hashtags'] = [h.strip() for h in hashtags_text.split() if h.strip().startswith('#')]
                    current_section = None
                
                elif current_section:
                    current_content.append(section)
            
            # Handle last section
            if current_section and current_content:
                if current_section == 'twitter_thread':
                    result['twitter_thread'] = [t.strip() for t in '\n\n'.join(current_content).split('---') if t.strip()]
                elif current_section == 'cta':
                    result['cta'] = [c.strip() for c in '\n\n'.join(current_content).split('---') if c.strip()]
                else:
                    result[current_section] = '\n\n'.join(current_content).strip()
            
            # Ensure we have at least some content
            if not result['master_storyline']:
                result['master_storyline'] = response[:500]
            
            if not result['twitter_thread']:
                result['twitter_thread'] = [response[:280]]
            
            if not result['cta']:
                result['cta'] = ["Follow for more!", "Share this post!", "Comment your thoughts!"]
            
            if not result['hashtags']:
                result['hashtags'] = ['#AI', '#Tech', '#Innovation']
            
        except Exception as e:
            print(f"Parse error: {e}")
            # Return basic structure with raw response
            result['master_storyline'] = response
            result['youtube_script'] = response[:500]
            result['instagram_script'] = response[:300]
            result['twitter_thread'] = [response[:280]]
            result['caption'] = response[:200]
            result['cta'] = ["Follow for more!", "Share this!", "Comment below!"]
            result['hashtags'] = ['#AI', '#Tech', '#Innovation']
        
        return result
