"""
AI Content Generator Engine
Implements the structured storytelling framework for multi-platform content
"""
from typing import Dict, List, Optional
import re


class ContentGenerator:
    """Main content generation engine"""
    
    def __init__(self):
        self.categories = {
            'new_tool_intro': self._new_tool_intro_template,
            'tool_detailed_tutorial': self._tool_tutorial_template,
            'trending_ai_model': self._trending_model_template,
            'ai_trending_news': self._trending_news_template,
            'github_open_source_repo': self._github_repo_template,
            'instagram_engagement_content': self._engagement_template
        }
    
    def generate(self, topic: str, context: Optional[str] = None) -> Dict:
        """
        Generate multi-platform content from a topic
        
        Args:
            topic: The main topic or idea
            context: Additional context or information
            
        Returns:
            Dictionary containing all generated content
        """
        # Step 1: Classify content category
        category = self._classify_content(topic, context)
        
        # Step 2: Generate master storyline
        master_storyline = self._generate_master_storyline(topic, context, category)
        
        # Step 3: Adapt for multiple platforms
        youtube_script = self._adapt_for_youtube(master_storyline, category)
        instagram_script = self._adapt_for_instagram(master_storyline, category)
        twitter_thread = self._adapt_for_twitter(master_storyline, category)
        caption = self._generate_caption(master_storyline, category)
        cta = self._generate_cta(category)
        hashtags = self._generate_hashtags(topic, category)
        
        return {
            'category': category,
            'master_storyline': master_storyline,
            'youtube_script': youtube_script,
            'instagram_script': instagram_script,
            'twitter_thread': twitter_thread,
            'caption': caption,
            'cta': cta,
            'hashtags': hashtags
        }
    
    def _classify_content(self, topic: str, context: Optional[str] = None) -> str:
        """Automatically classify content into appropriate category"""
        topic_lower = topic.lower()
        context_lower = (context or "").lower()
        combined = f"{topic_lower} {context_lower}"
        
        # Classification rules
        if any(word in combined for word in ['new', 'just released', 'launched', 'introducing', 'announcement']):
            if any(word in combined for word in ['tool', 'app', 'platform', 'software']):
                return 'new_tool_intro'
        
        if any(word in combined for word in ['how to', 'tutorial', 'guide', 'step by step', 'learn']):
            return 'tool_detailed_tutorial'
        
        if any(word in combined for word in ['model', 'gpt', 'llm', 'ai model', 'neural network']):
            return 'trending_ai_model'
        
        if any(word in combined for word in ['news', 'breaking', 'trending', 'latest', 'update']):
            return 'ai_trending_news'
        
        if any(word in combined for word in ['github', 'open source', 'repository', 'repo', 'code']):
            return 'github_open_source_repo'
        
        if any(word in combined for word in ['tip', 'trick', 'quick', 'simple', 'easy']):
            return 'instagram_engagement_content'
        
        # Default to new tool intro if unclear
        return 'new_tool_intro'
    
    def _generate_master_storyline(self, topic: str, context: Optional[str], category: str) -> str:
        """Generate the master storyline using the appropriate template"""
        template_func = self.categories.get(category, self._new_tool_intro_template)
        return template_func(topic, context)
    
    # ==================== CATEGORY TEMPLATES ====================
    
    def _new_tool_intro_template(self, topic: str, context: Optional[str]) -> str:
        """Template for new tool introduction"""
        return f"""🔥 VIRAL HOOK:
Stop scrolling! This new AI tool is about to change everything.

💡 THE PROBLEM:
Content creators are spending hours on tasks that should take minutes. The old tools are slow, expensive, and complicated.

🚀 THE SOLUTION:
{topic} just dropped, and it's a game-changer.

✨ KEY DIFFERENTIATOR:
Unlike other tools, this one actually understands context and delivers professional results in seconds, not hours.

🎯 REAL-WORLD EXAMPLE:
Imagine creating a full week's worth of social media content in under 5 minutes. That's exactly what this does.

💎 QUICK BENEFITS:
• Save 10+ hours per week
• Professional quality output
• No learning curve
• Affordable pricing

📢 CALL TO ACTION:
Try it yourself and see the difference. Link in bio!

{f'📝 CONTEXT: {context}' if context else ''}"""
    
    def _tool_tutorial_template(self, topic: str, context: Optional[str]) -> str:
        """Template for detailed tutorial"""
        return f"""🎯 STRONG HOOK:
Want to master {topic}? Here's the exact step-by-step process.

❌ THE PROBLEM:
Most tutorials are either too vague or too complicated. You need a clear, actionable guide.

📋 STEP-BY-STEP WORKFLOW:

STEP 1: Set Up Your Environment
Get everything ready before you start. This saves time later.

STEP 2: Configure Your Settings
These are the exact settings that work best. Don't skip this.

STEP 3: Execute the Process
Follow this sequence exactly. Order matters here.

STEP 4: Optimize Your Results
Fine-tune these parameters for maximum impact.

⚡ KEY TIPS:
• Always start with default settings
• Test one change at a time
• Save your successful configurations

🚫 MISTAKES TO AVOID:
• Don't rush the setup phase
• Never skip the testing step
• Avoid changing multiple settings at once

✅ FINAL OUTCOME:
You'll have a repeatable system that delivers consistent, professional results every time.

{f'📝 ADDITIONAL INFO: {context}' if context else ''}"""
    
    def _trending_model_template(self, topic: str, context: Optional[str]) -> str:
        """Template for trending AI model"""
        return f"""🚨 BREAKING:
{topic} is breaking the internet right now. Here's why.

🤖 MODEL OVERVIEW:
This isn't just another AI model. It's a fundamental shift in what's possible.

💡 UNIQUE INNOVATION:
The breakthrough? It can understand context at a level we've never seen before. This changes everything.

📊 PERFORMANCE INSIGHTS:
Early tests show it outperforms previous models by 40% on complex tasks. The results speak for themselves.

🌍 REAL-WORLD APPLICATIONS:
• Content creators: Generate ideas 10x faster
• Developers: Debug code in seconds
• Businesses: Automate customer support
• Students: Learn complex topics easily

👥 WHO SHOULD USE THIS:
Anyone working with AI, content, or data. Seriously, this is for everyone.

🔮 FUTURE IMPACT:
This is just the beginning. Expect this technology to reshape entire industries in the next 12 months.

{f'📝 TECHNICAL DETAILS: {context}' if context else ''}"""
    
    def _trending_news_template(self, topic: str, context: Optional[str]) -> str:
        """Template for AI trending news"""
        return f"""⚡ BREAKING NEWS:
{topic} - and the AI community is going wild.

📰 WHAT HAPPENED:
In the last 24 hours, a major development has shifted the entire AI landscape.

🔥 WHY IT'S TRENDING:
This isn't just hype. Real experts are calling this a pivotal moment for the industry.

🧠 SIMPLIFIED EXPLANATION:
Think of it this way: What used to take specialized teams months can now be done by anyone in minutes.

🏢 INDUSTRY IMPACT:
• Tech companies are scrambling to adapt
• Investors are paying close attention
• Developers are already building on it
• Users are seeing immediate benefits

💬 EXPERT INSIGHT:
Industry leaders are saying this could be as significant as the launch of ChatGPT. That's not an exaggeration.

🎯 WHAT THIS MEANS FOR YOU:
If you work in tech, content, or business, you need to understand this. It's going to affect your workflow.

{f'📝 BACKGROUND: {context}' if context else ''}"""
    
    def _github_repo_template(self, topic: str, context: Optional[str]) -> str:
        """Template for GitHub open source repository"""
        return f"""⭐ GITHUB ALERT:
{topic} just hit trending, and developers are losing their minds.

📦 REPO OVERVIEW:
This open-source project solves a problem that's been plaguing developers for years.

🔑 CORE FEATURES:
• Lightning-fast performance
• Zero configuration needed
• Works with any tech stack
• Active community support
• Comprehensive documentation

💻 WHY DEVELOPERS CARE:
It cuts development time in half while improving code quality. That's the dream combo.

🎯 EXAMPLE USE CASE:
Instead of writing 500 lines of boilerplate code, you import this library and you're done in 5 lines.

📈 GROWTH SIGNALS:
• 10K+ stars in the first week
• 500+ contributors already
• Major companies adopting it
• Active daily commits

🚀 GET STARTED:
Clone the repo, follow the quick start guide, and you'll be up and running in under 5 minutes.

{f'📝 TECHNICAL SPECS: {context}' if context else ''}"""
    
    def _engagement_template(self, topic: str, context: Optional[str]) -> str:
        """Template for Instagram engagement content"""
        return f"""💡 QUICK TIP:
{topic} - this simple trick will save you hours.

🎯 THE INSIGHT:
Most people overcomplicate this. The solution is actually super simple.

✨ HERE'S THE EXAMPLE:
Instead of doing it the hard way, just do this one thing differently. Watch what happens.

❓ QUESTION FOR YOU:
Have you tried this approach? Drop a comment and let me know your experience!

🔥 WHY IT WORKS:
It's all about working smarter, not harder. This is the shortcut the pros use.

{f'📝 BONUS TIP: {context}' if context else ''}"""
    
    # ==================== PLATFORM ADAPTATIONS ====================
    
    def _adapt_for_youtube(self, storyline: str, category: str) -> str:
        """Adapt master storyline for YouTube Shorts (30-60 seconds)"""
        # Extract key points and make them more explanatory
        lines = storyline.split('\n')
        script_lines = []
        
        script_lines.append("[OPENING - 0:00]")
        script_lines.append("Hey! " + self._extract_hook(storyline))
        script_lines.append("")
        script_lines.append("[MAIN CONTENT - 0:05]")
        
        # Extract main points
        main_points = [line for line in lines if line.strip() and not line.startswith('📝')]
        for i, point in enumerate(main_points[2:7], 1):  # Get 5 key points
            clean_point = re.sub(r'[🔥💡🚀✨🎯💎📢❌📋⚡🚫✅🚨🤖📊🌍👥🔮⚡📰🧠🏢💬⭐📦🔑💻📈💡🎯✨❓🔥]', '', point).strip()
            if clean_point and len(clean_point) > 10:
                script_lines.append(f"{clean_point}")
        
        script_lines.append("")
        script_lines.append("[CLOSING - 0:50]")
        script_lines.append("That's it! Follow for more AI tips.")
        script_lines.append("Comment below if you have questions!")
        
        return '\n'.join(script_lines)
    
    def _adapt_for_instagram(self, storyline: str, category: str) -> str:
        """Adapt master storyline for Instagram Reels (faster pacing)"""
        lines = storyline.split('\n')
        script_lines = []
        
        script_lines.append("⚡ HOOK:")
        script_lines.append(self._extract_hook(storyline))
        script_lines.append("")
        
        # Get punchy points
        main_points = [line for line in lines if line.strip() and not line.startswith('📝')]
        for point in main_points[2:6]:  # Get 4 key points
            clean_point = re.sub(r'[🔥💡🚀✨🎯💎📢❌📋⚡🚫✅🚨🤖📊🌍👥🔮⚡📰🧠🏢💬⭐📦🔑💻📈💡🎯✨❓🔥]', '', point).strip()
            if clean_point and len(clean_point) > 10:
                # Make it punchier
                if ':' in clean_point:
                    clean_point = clean_point.split(':')[0]
                script_lines.append(f"→ {clean_point[:80]}")
        
        script_lines.append("")
        script_lines.append("💬 Save this!")
        script_lines.append("Follow @youraccount for daily AI tips")
        
        return '\n'.join(script_lines)
    
    def _adapt_for_twitter(self, storyline: str, category: str) -> List[str]:
        """Adapt master storyline for X/Twitter thread"""
        lines = storyline.split('\n')
        tweets = []
        
        # Tweet 1: Hook
        hook = self._extract_hook(storyline)
        tweets.append(f"{hook}\n\nA thread 🧵")
        
        # Extract main sections
        sections = []
        current_section = []
        for line in lines:
            if line.strip() and not line.startswith('📝'):
                clean_line = re.sub(r'[🔥💡🚀✨🎯💎📢❌📋⚡🚫✅🚨🤖📊🌍👥🔮⚡📰🧠🏢💬⭐📦🔑💻📈💡🎯✨❓🔥]', '', line).strip()
                if clean_line:
                    if len(clean_line) > 15:  # Meaningful content
                        current_section.append(clean_line)
                        if len(current_section) >= 2:
                            sections.append(current_section[:2])
                            current_section = []
        
        # Create tweets from sections
        for i, section in enumerate(sections[:5], 2):  # Max 6 tweets total
            tweet_content = '\n'.join(section[:2])
            if len(tweet_content) > 280:
                tweet_content = tweet_content[:277] + "..."
            tweets.append(f"{i}/ {tweet_content}")
        
        # Final CTA tweet
        tweets.append(f"{len(tweets) + 1}/ Found this helpful?\n\n• Follow me for daily AI insights\n• RT the first tweet to share\n• Reply with your thoughts!")
        
        return tweets
    
    def _generate_caption(self, storyline: str, category: str) -> str:
        """Generate social media caption"""
        hook = self._extract_hook(storyline)
        
        caption_parts = [
            hook,
            "",
            "Here's what you need to know:",
            ""
        ]
        
        # Extract 3 key points
        lines = storyline.split('\n')
        points = []
        for line in lines:
            clean_line = re.sub(r'[🔥💡🚀✨🎯💎📢❌📋⚡🚫✅🚨🤖📊🌍👥🔮⚡📰🧠🏢💬⭐📦🔑💻📈💡🎯✨❓🔥]', '', line).strip()
            if clean_line and len(clean_line) > 20 and ':' in clean_line:
                points.append(f"✓ {clean_line.split(':')[0]}")
                if len(points) >= 3:
                    break
        
        caption_parts.extend(points)
        caption_parts.extend([
            "",
            "💬 What do you think? Comment below!",
            "🔖 Save this for later",
            "📤 Share with someone who needs this"
        ])
        
        return '\n'.join(caption_parts)
    
    def _generate_cta(self, category: str) -> List[str]:
        """Generate call-to-action suggestions"""
        cta_options = {
            'new_tool_intro': [
                "Try it yourself - link in bio!",
                "Click the link to get started for free",
                "Join 10,000+ creators already using this"
            ],
            'tool_detailed_tutorial': [
                "Follow for more step-by-step guides",
                "Save this tutorial for when you need it",
                "Comment 'GUIDE' for the full PDF version"
            ],
            'trending_ai_model': [
                "Follow for daily AI model updates",
                "Share this with your AI community",
                "Comment your thoughts below!"
            ],
            'ai_trending_news': [
                "Follow for breaking AI news",
                "Turn on notifications to stay updated",
                "Share your take in the comments"
            ],
            'github_open_source_repo': [
                "Star the repo if you find it useful",
                "Follow for more open-source discoveries",
                "Comment if you've tried this!"
            ],
            'instagram_engagement_content': [
                "Save this tip for later!",
                "Try it and tag me in your results",
                "Follow for daily quick tips"
            ]
        }
        
        return cta_options.get(category, cta_options['new_tool_intro'])
    
    def _generate_hashtags(self, topic: str, category: str) -> List[str]:
        """Generate relevant hashtags"""
        # Base hashtags
        base_tags = ['#AI', '#ArtificialIntelligence', '#Tech', '#Innovation']
        
        # Category-specific hashtags
        category_tags = {
            'new_tool_intro': ['#AITools', '#ProductLaunch', '#TechNews', '#NewTech'],
            'tool_detailed_tutorial': ['#Tutorial', '#HowTo', '#LearnAI', '#TechTutorial'],
            'trending_ai_model': ['#AIModel', '#MachineLearning', '#DeepLearning', '#AIResearch'],
            'ai_trending_news': ['#AINews', '#TechNews', '#TrendingNow', '#BreakingNews'],
            'github_open_source_repo': ['#OpenSource', '#GitHub', '#Coding', '#Developer'],
            'instagram_engagement_content': ['#TechTips', '#QuickTip', '#LifeHack', '#Productivity']
        }
        
        # Topic-based hashtags
        topic_words = topic.lower().split()
        topic_tags = [f"#{word.capitalize()}" for word in topic_words if len(word) > 4][:3]
        
        # Combine all hashtags
        all_tags = base_tags + category_tags.get(category, []) + topic_tags
        
        # Return unique hashtags
        return list(dict.fromkeys(all_tags))[:12]  # Max 12 hashtags
    
    def _extract_hook(self, storyline: str) -> str:
        """Extract the hook from storyline"""
        lines = storyline.split('\n')
        for line in lines:
            clean_line = re.sub(r'[🔥💡🚀✨🎯💎📢❌📋⚡🚫✅🚨🤖📊🌍👥🔮⚡📰🧠🏢💬⭐📦🔑💻📈💡🎯✨❓🔥]', '', line).strip()
            if clean_line and len(clean_line) > 20 and not clean_line.endswith(':'):
                return clean_line
        return "This is going to change everything."
