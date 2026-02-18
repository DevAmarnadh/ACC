import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv

from engine.content_generator import ContentGenerator
from engine.ai_content_generator import AIContentGenerator
from engine.openrouter_ai import OpenRouterAI
from engine.multi_category_generator import MultiCategoryGenerator

# Try to import database, but don't fail if it doesn't work
try:
    from database.supabase_db import SupabaseDB
    DB_AVAILABLE = True
except:
    DB_AVAILABLE = False

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Content Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, minimal CSS
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
    }
    h1 {
        color: #1a1a1a;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    h2 {
        color: #2c2c2c;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    .stTextArea textarea {
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
    }
    .stTextArea textarea:focus {
        border-color: #4285f4 !important;
    }
    .stButton > button {
        background-color: #4285f4 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
    }
    .stButton > button:hover {
        background-color: #3367d6 !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'content_generator' not in st.session_state:
    st.session_state.content_generator = ContentGenerator()

if 'ai_generator' not in st.session_state:
    try:
        st.session_state.ai_generator = AIContentGenerator()
        st.session_state.ai_available = st.session_state.ai_generator.ai_available
    except:
        st.session_state.ai_generator = None
        st.session_state.ai_available = False

if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "GPT-3.5 Turbo"

if 'use_ai' not in st.session_state:
    st.session_state.use_ai = True  # Default to AI generation

if 'generate_all_categories' not in st.session_state:
    st.session_state.generate_all_categories = False

if 'multi_generator' not in st.session_state:
    try:
        st.session_state.multi_generator = MultiCategoryGenerator()
    except:
        st.session_state.multi_generator = None

if 'all_category_results' not in st.session_state:
    st.session_state.all_category_results = []

if 'database' not in st.session_state:
    if DB_AVAILABLE:
        try:
            st.session_state.database = SupabaseDB()
            st.session_state.db_connected = st.session_state.database.test_connection()
        except:
            st.session_state.database = None
            st.session_state.db_connected = False
    else:
        st.session_state.database = None
        st.session_state.db_connected = False

if 'current_content' not in st.session_state:
    st.session_state.current_content = None

if 'local_history' not in st.session_state:
    st.session_state.local_history = []

# Helper functions
def format_category_name(category):
    names = {
        'new_tool_intro': 'New Tool',
        'tool_detailed_tutorial': 'Tutorial',
        'trending_ai_model': 'AI Model',
        'ai_trending_news': 'AI News',
        'github_open_source_repo': 'GitHub',
        'instagram_engagement_content': 'Engagement'
    }
    return names.get(category, category)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Database status - simple indicator
    if st.session_state.db_connected:
        st.caption("✅ Database Connected")
    else:
        st.caption("💡 Working Offline (Session Mode)")
    
    st.markdown("---")
    
    # Category Filters (based on framework)
    st.markdown("### 🔍 Filter Content")
    
    category_options = [
        "All Categories",
        "🆕 New Tool Introduction",
        "📚 Detailed Tutorial",
        "🤖 Trending AI Model",
        "📰 AI Trending News",
        "⭐ GitHub Repository",
        "💡 Engagement Content"
    ]
    
    selected_category = st.selectbox(
        "Category",
        category_options,
        key="category_filter"
    )
    
    # Map display names to internal category names
    category_map = {
        "🆕 New Tool Introduction": "new_tool_intro",
        "📚 Detailed Tutorial": "tool_detailed_tutorial",
        "🤖 Trending AI Model": "trending_ai_model",
        "📰 AI Trending News": "ai_trending_news",
        "⭐ GitHub Repository": "github_open_source_repo",
        "💡 Engagement Content": "instagram_engagement_content"
    }
    
    # Show framework flow for selected category
    if selected_category != "All Categories":
        with st.expander("📖 Story Flow", expanded=False):
            if selected_category == "🆕 New Tool Introduction":
                st.markdown("""
                **Flow:**
                1. Scroll Hook
                2. User Problem
                3. Tool Introduction
                4. Unique Differentiator
                5. Real Use Case
                6. Why It Matters Now
                7. Call To Action
                """)
            elif selected_category == "📚 Detailed Tutorial":
                st.markdown("""
                **Flow:**
                1. Hook
                2. Problem Statement
                3. Tool Overview
                4. Step 1, 2, 3...
                5. Pro Tips
                6. Common Mistakes
                7. Final Result
                8. CTA
                """)
            elif selected_category == "🤖 Trending AI Model":
                st.markdown("""
                **Flow:**
                1. Breaking Hook
                2. Model Introduction
                3. Key Innovation
                4. Performance Insight
                5. Real World Applications
                6. Target Users
                7. Future Impact
                8. CTA
                """)
            elif selected_category == "📰 AI Trending News":
                st.markdown("""
                **Flow:**
                1. Viral Hook
                2. What Happened
                3. Why It's Trending
                4. Simplified Explanation
                5. Industry Impact
                6. Expert Insight
                7. CTA
                """)
            elif selected_category == "⭐ GitHub Repository":
                st.markdown("""
                **Flow:**
                1. Hook
                2. Repository Overview
                3. Core Features
                4. Why Developers Like It
                5. Use Case Example
                6. Trend Signals
                7. CTA
                """)
            elif selected_category == "💡 Engagement Content":
                st.markdown("""
                **Flow:**
                1. Relatable Hook
                2. Quick Insight
                3. Simple Example
                4. Audience Question
                5. Micro Takeaway
                6. CTA
                """)
    
    st.markdown("---")
    
    # History
    st.markdown("### 📜 History")
    
    if st.session_state.db_connected:
        try:
            # Get filter value
            filter_category = None
            if selected_category != "All Categories":
                filter_category = category_map.get(selected_category)
            
            history = st.session_state.database.get_history(
                limit=10,
                category_filter=filter_category
            )
            if history:
                for item in history:
                    with st.expander(f"{item['topic'][:25]}...", expanded=False):
                        st.caption(f"**{format_category_name(item['category'])}**")
                        st.caption(f"{item['created_at'][:10]}")
                        if st.button("Load", key=f"load_{item['id']}"):
                            content = st.session_state.database.get_content_by_id(item['id'])
                            if content:
                                st.session_state.current_content = content
                                st.rerun()
            else:
                st.info("No history yet")
        except:
            st.info("Database unavailable")
    else:
        # Show local session history with filter
        if st.session_state.local_history:
            filtered_history = st.session_state.local_history
            if selected_category != "All Categories":
                filter_cat = category_map.get(selected_category)
                filtered_history = [h for h in st.session_state.local_history if h.get('category') == filter_cat]
            
            if filtered_history:
                for i, item in enumerate(reversed(filtered_history[-10:])):
                    with st.expander(f"{item['topic'][:25]}...", expanded=False):
                        st.caption(f"**{format_category_name(item['category'])}**")
                        if st.button("Load", key=f"local_load_{i}"):
                            st.session_state.current_content = item
                            st.rerun()
            else:
                st.info("No matching content")
        else:
            st.info("No history this session")

# ==================== MAIN CONTENT ====================
# Main Content Area
st.markdown("## 🚀 AI Content Engine")
st.caption("Transform topics into viral multi-platform content")

# Input Mode Selection
input_mode = st.radio(
    "Input Mode",
    ["💡 Enter Topic", "📄 Upload Script"],
    horizontal=True,
    help="Choose to enter a topic or upload your own script to rephrase"
)

col1, col2 = st.columns([2, 1])

with col1:
    if input_mode == "💡 Enter Topic":
        topic = st.text_area(
            "Enter your topic",
            placeholder="e.g., ChatGPT 5 new features",
            height=100,
            key="topic_input"
        )
        uploaded_script = None
    else:
        # File upload
        uploaded_file = st.file_uploader(
            "Upload your script (.txt, .md)",
            type=['txt', 'md'],
            help="Upload your existing script to rephrase using framework flows"
        )
        
        if uploaded_file:
            uploaded_script = uploaded_file.read().decode('utf-8')
            st.text_area("Your Script", value=uploaded_script, height=200, disabled=True)
            topic = st.text_input("Topic/Title", placeholder="e.g., ChatGPT Tutorial")
        else:
            uploaded_script = None
            topic = None
            st.info("👆 Upload a script file to rephrase it using framework flows")
    
    # Generation settings
    st.session_state.use_ai = st.session_state.ai_available
    
    # Only show "Generate All" if AI is available
    if st.session_state.ai_available:
        generate_all = st.checkbox(
            "🎯 Generate All 6 Categories",
            value=False,
            help="Generate content for ALL 6 framework categories at once!"
        )
        st.session_state.generate_all_categories = generate_all
    else:
        st.session_state.generate_all_categories = False
    
    # Status
    if not st.session_state.ai_available:
        st.caption("⚠️ AI not configured - using templates")
    elif st.session_state.generate_all_categories:
        st.caption("✅ AI mode - Will generate ALL 6 categories!")
    elif st.session_state.use_ai:
        st.caption("✅ AI mode - Single category")
    else:
        st.caption("📝 Template mode")
    
    # Model selection (only if AI mode is enabled)
    if st.session_state.ai_available and st.session_state.use_ai:
        model_names = OpenRouterAI.get_model_names()
        selected_model_name = st.selectbox(
            "🤖 AI Model",
            model_names,
            index=model_names.index(st.session_state.selected_model) if st.session_state.selected_model in model_names else 0,
            help="Select the AI model to generate content"
        )
        st.session_state.selected_model = selected_model_name
    elif not st.session_state.ai_available:
        st.info("💡 Using template-based generation (AI not configured)")

with col2:
    st.markdown("")  # Spacing
    st.markdown("")  # Spacing
    if st.button("🎯 Generate", type="primary", use_container_width=True):
        if not topic or len(topic.strip()) < 3:
            st.error("Please enter a topic/title")
        else:
            # Prepare context from uploaded script
            context = None
            if uploaded_script:
                context = f"ORIGINAL SCRIPT TO REPHRASE:\n\n{uploaded_script}\n\nRephrase this script following the framework flows while keeping the core message."
            
            with st.spinner(f"🔍 {'Rephrasing script' if uploaded_script else 'Searching Google'} & generating with {st.session_state.selected_model if st.session_state.ai_available and st.session_state.use_ai else 'templates'}..."):
                try:
                    # Check if generating all categories
                    if st.session_state.generate_all_categories and st.session_state.multi_generator:
                        # Generate ALL 6 categories
                        model_id = OpenRouterAI.MODELS[st.session_state.selected_model]
                        
                        progress_placeholder = st.empty()
                        
                        # Don't search if rephrasing a script? User wants accurate search!
                        # So we search to supplement the script
                        progress_placeholder.info("🔍 Searching Google & Analyzing script...")
                        
                        all_results = st.session_state.multi_generator.generate_all(
                            topic=topic.strip(),
                            model=model_id,
                            context=context
                        )
                        
                        progress_placeholder.empty()
                        st.success(f"✅ Generated ALL 6 categories with {st.session_state.selected_model}!")
                        
                        # Store all results
                        st.session_state.all_category_results = all_results
                        
                        # Set first one as current for display if available
                        if all_results:
                            st.session_state.current_content = all_results[0]
                            st.session_state.current_content['topic'] = topic.strip()
                            st.session_state.current_content['created_at'] = datetime.now().isoformat()
                        
                        # Show success message
                        st.info("📊 View all 6 categories below!")
                        
                    # Generate single category
                    elif st.session_state.ai_available and st.session_state.use_ai:
                        try:
                            # Get model ID
                            model_id = OpenRouterAI.MODELS[st.session_state.selected_model]
                            
                            # Show search status
                            search_placeholder = st.empty()
                            search_placeholder.info("🔍 Searching Google & Analyzing...")
                            
                            result = st.session_state.ai_generator.generate(
                                topic=topic.strip(),
                                context=context,
                                model=model_id
                            )
                            
                            search_placeholder.empty()
                            st.success(f"✅ Generated with {st.session_state.selected_model}!")
                            
                            result['topic'] = topic.strip()
                            result['created_at'] = datetime.now().isoformat()
                            st.session_state.current_content = result
                            st.session_state.all_category_results = []  # Clear multi results
                            
                            # Save Logic for Single Category
                            if st.session_state.db_connected:
                                try:
                                    content_id = st.session_state.database.save_content(
                                        topic=topic.strip(),
                                        category=result['category'],
                                        content_data=result
                                    )
                                    result['id'] = content_id
                                except:
                                    result['id'] = None
                                    st.warning("⚠️ Not saved (database error)")
                                    # Save to local history
                                    st.session_state.local_history.append(result.copy())
                            else:
                                result['id'] = None
                                # Save to local history
                                st.session_state.local_history.append(result.copy())
                                
                        except Exception as ai_error:
                            st.error(f"AI Generation Error: {str(ai_error)}")
                            # Fallback logic here if needed, or just stop
                    
                    else:
                        # Use template-based generation (Fallback)
                        result = st.session_state.content_generator.generate(
                            topic=topic.strip(),
                            context=None
                        )
                        st.success("✅ Generated with templates!")
                        
                        result['topic'] = topic.strip()
                        result['created_at'] = datetime.now().isoformat()
                        st.session_state.current_content = result
                        st.session_state.all_category_results = []
                        
                        # Save Logic for Template Mode
                        result['id'] = None
                        st.session_state.local_history.append(result.copy())

                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

st.markdown("---")

# Display ALL 6 Categories if generated
if st.session_state.all_category_results:
    st.markdown("## 🎯 ALL 6 FRAMEWORK CATEGORIES")
    st.caption(f"Topic: **{st.session_state.all_category_results[0].get('topic', '')}**")
    st.markdown("---")
    
    for idx, content in enumerate(st.session_state.all_category_results, 1):
        category_name = format_category_name(content['category'])
        
        with st.expander(f"**{idx}. {category_name}**", expanded=(idx == 1)):
            # Master Storyline
            st.markdown("**📖 Master Storyline**")
            st.text_area("", value=content['master_storyline'], height=200, key=f"multi_master_{idx}", label_visibility="collapsed")
            
            # Tabs for platforms
            tab1, tab2, tab3, tab4 = st.tabs(["📺 YouTube", "📸 Instagram", "🐦 X", "💬 Caption"])
            
            with tab1:
                st.text_area("YouTube Script", value=content.get('youtube_script', 'Not generated'), height=200, key=f"multi_yt_{idx}")
            
            with tab2:
                st.text_area("Instagram Script", value=content.get('instagram_script', 'Not generated'), height=200, key=f"multi_ig_{idx}")
            
            with tab3:
                for i, tweet in enumerate(content.get('twitter_thread', []), 1):
                    st.info(f"**Tweet {i}**\n\n{tweet}")
            
            with tab4:
                st.text_area("Caption", value=content.get('caption', 'Not generated'), height=150, key=f"multi_cap_{idx}")
            
            # CTAs and Hashtags
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📢 CTAs**")
                for cta in content.get('cta', []):
                    st.markdown(f"• {cta}")
            with col2:
                st.markdown("**#️⃣ Hashtags**")
                st.code(' '.join(content.get('hashtags', [])), language=None)
    
    st.markdown("---")
    st.info("💡 **Tip:** Each category follows its specific framework flow. Choose the one that fits your content best!")

# Display Single Result
elif st.session_state.current_content:
    content = st.session_state.current_content
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 📝 {content.get('topic', 'Generated Content')}")
        st.caption(f"**Category:** {format_category_name(content['category'])}")
    with col2:
        # Export
        export_text = f"""AI CONTENT ENGINE

Topic: {content.get('topic', '')}
Category: {format_category_name(content['category'])}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

{'='*60}

MASTER STORYLINE
{'-'*60}
{content['master_storyline']}

{'='*60}

YOUTUBE SHORTS
{'-'*60}
{content['youtube_script']}

{'='*60}

INSTAGRAM REEL
{'-'*60}
{content['instagram_script']}

{'='*60}

X (TWITTER) THREAD
{'-'*60}
"""
        for i, tweet in enumerate(content['twitter_thread'], 1):
            export_text += f"Tweet {i}:\n{tweet}\n\n"
        
        export_text += f"""{'='*60}

CAPTION
{'-'*60}
{content['caption']}

{'='*60}

CALL-TO-ACTION
{'-'*60}
"""
        for i, cta in enumerate(content['cta'], 1):
            export_text += f"{i}. {cta}\n"
        
        export_text += f"""
{'='*60}

HASHTAGS
{'-'*60}
{' '.join(content['hashtags'])}
"""
        
        st.download_button(
            "📥 Export",
            data=export_text,
            file_name=f"content-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 Master",
        "📺 YouTube",
        "📸 Instagram",
        "🐦 X",
        "💬 Caption"
    ])
    
    with tab1:
        st.text_area("Master Storyline", value=content['master_storyline'], height=300, key="master_display")
    
    with tab2:
        st.text_area("YouTube Shorts (30-60s)", value=content['youtube_script'], height=300, key="youtube_display")
    
    with tab3:
        st.text_area("Instagram Reel", value=content['instagram_script'], height=300, key="instagram_display")
    
    with tab4:
        for i, tweet in enumerate(content['twitter_thread'], 1):
            st.info(f"**Tweet {i}**\n\n{tweet}")
    
    with tab5:
        st.text_area("Social Caption", value=content['caption'], height=200, key="caption_display")
    
    st.markdown("---")
    
    # CTA and Hashtags
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📢 CTAs**")
        for i, cta in enumerate(content['cta'], 1):
            st.markdown(f"{i}. {cta}")
    
    with col2:
        st.markdown("**#️⃣ Hashtags**")
        st.code(' '.join(content['hashtags']), language=None)

# Footer
st.markdown("---")
st.caption("🚀 AI Content Engine | Works online or offline")
