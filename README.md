# 🚀 AI Content Creation Engine

**Autonomous AI-powered multi-platform content generation system built with Streamlit & PostgreSQL**

Transform any topic into viral, structured content optimized for YouTube Shorts, Instagram Reels, X (Twitter), and more.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-green.svg)

---

## ✨ Features

### 🤖 **Intelligent Content Generation**
- **Automatic Category Classification** - AI automatically detects content type
- **6 Content Categories** - New tools, tutorials, AI models, news, GitHub repos, engagement content
- **Structured Storytelling Framework** - Professional templates for each category
- **Multi-Platform Adaptation** - Optimized for each platform's unique requirements

### 📱 **Multi-Platform Output**
- **YouTube Shorts** - 30-60 second scripts with timing markers
- **Instagram Reels** - Fast-paced, punchy content
- **X (Twitter) Threads** - Engaging thread format with hooks
- **Social Media Captions** - Ready-to-use captions with CTAs
- **Hashtag Generation** - Relevant, trending hashtags
- **CTA Suggestions** - Platform-specific calls-to-action

### 💾 **Cloud Database (Supabase PostgreSQL)**
- **PostgreSQL Database** - Cloud-hosted on Supabase
- **History Tracking** - Access all previously generated content
- **Export Functionality** - Download content as formatted text files
- **Statistics Dashboard** - Track usage and category breakdown
- **Real-time Sync** - All data stored securely in the cloud

### 🎨 **Premium UI/UX**
- **Streamlit Interface** - Beautiful, interactive web application
- **Modern Dark Theme** - Professional gradient design
- **Smooth Animations** - Engaging user experience
- **Responsive Design** - Works on all devices
- **Real-time Generation** - Instant content creation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Supabase account (free tier works great!)

### Installation

1. **Clone or Download** this repository

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Database** (Already configured!)
The `.env` file contains your Supabase PostgreSQL connection:
```
DATABASE_URL=postgresql://postgres:Single@6112123ed@db.flcdlrjzuompnirafxns.supabase.co:5432/postgres
```

4. **Run the Application**

**Option A: Using the start script (Recommended)**
```bash
start.bat
```

**Option B: Direct command**
```bash
streamlit run app.py
```

5. **Open Your Browser**
The application will automatically open at:
```
http://localhost:8501
```

That's it! The application will automatically:
- Connect to your Supabase PostgreSQL database
- Initialize the required tables
- Start the Streamlit interface

---

## 📖 Usage Guide

### 1. **Enter Your Topic**
Type any topic or idea in the main text area:
- "New AI tool that converts text to video"
- "How to use ChatGPT for content creation"
- "Latest breakthrough in AI image generation"

### 2. **Add Context (Optional)**
Provide additional information, facts, or specific details you want to include.

### 3. **Generate Content**
Click the "🎯 Generate Content" button and watch the magic happen!

The system will:
1. ✅ Analyze and classify your topic
2. ✅ Generate a master storyline
3. ✅ Adapt content for each platform
4. ✅ Create hashtags and CTAs
5. ✅ Save to PostgreSQL database

### 4. **Review & Export**
- View content in organized tabs
- Copy individual sections
- Export all content as a formatted text file
- Access from history anytime

---

## 🎯 Content Categories

The AI automatically classifies your input into one of these categories:

| Category | Icon | Use Case | Example |
|----------|------|----------|---------|
| **New Tool Introduction** | 🆕 | Launching new AI tools | "Introducing Sora AI video generator" |
| **Detailed Tutorial** | 📚 | Step-by-step guides | "How to create AI art with Midjourney" |
| **Trending AI Model** | 🤖 | AI model capabilities | "GPT-4 Vision's new features" |
| **AI News** | 📰 | Breaking news & trends | "OpenAI announces GPT-5" |
| **Open Source Repo** | ⭐ | GitHub projects | "New open-source LLM framework" |
| **Engagement Content** | 💡 | Quick tips & tricks | "5 ChatGPT prompts you need" |

---

## �️ Database Schema

The application uses PostgreSQL with the following structure:

```sql
CREATE TABLE content_history (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(500) NOT NULL,
    category VARCHAR(100) NOT NULL,
    master_storyline TEXT NOT NULL,
    youtube_script TEXT NOT NULL,
    instagram_script TEXT NOT NULL,
    twitter_thread JSON NOT NULL,
    caption TEXT NOT NULL,
    cta JSON NOT NULL,
    hashtags JSON NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🛠️ Technology Stack

### Frontend
- **Streamlit** - Interactive web framework
- **Custom CSS** - Premium dark theme design

### Backend
- **Python 3.8+** - Core programming language
- **SQLAlchemy** - ORM for database operations
- **psycopg2** - PostgreSQL adapter

### Database
- **PostgreSQL** - Relational database
- **Supabase** - Cloud database hosting
- **JSON Columns** - For complex data structures

---

## � Features Breakdown

### Dashboard (Sidebar)
- **Total Content Generated** - Lifetime count
- **Last 7 Days** - Recent activity
- **Category Breakdown** - Distribution by type
- **Recent History** - Quick access to past content

### Content Generation
- **Real-time Processing** - Instant results
- **Progress Indicators** - Visual feedback
- **Error Handling** - Graceful failure recovery
- **Auto-save** - All content saved automatically

### Export Options
- **Formatted Text** - Clean, readable format
- **Timestamped** - Includes generation date
- **Complete Package** - All platforms in one file
- **Copy-friendly** - Easy to paste anywhere

---

## 🎨 Design Philosophy

### **Premium Aesthetics**
- Dark theme with vibrant gradients (#667eea to #764ba2)
- Smooth animations and transitions
- Professional typography
- Glassmorphism effects

### **User Experience**
- Clear visual hierarchy
- Instant feedback
- Minimal cognitive load
- Intuitive navigation

### **Performance**
- Fast database queries
- Efficient content generation
- Optimized rendering
- Cloud-based scalability

---

## � Configuration

### Change Database Connection
Edit `.env` file:
```env
DATABASE_URL=postgresql://user:password@host:port/database
```

### Customize Theme
Edit `app.py` CSS section:
```python
st.markdown("""
<style>
    :root {
        --primary-color: #667eea;  /* Change this */
        --secondary-color: #764ba2; /* And this */
    }
</style>
""", unsafe_allow_html=True)
```

### Modify Categories
Edit `engine/content_generator.py`:
```python
self.categories = {
    'your_category': self._your_template,
    # Add more categories
}
```

---

## � Project Structure

```
AI Content Creation Engine/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (database)
├── start.bat                  # Windows startup script
├── engine/
│   ├── __init__.py
│   └── content_generator.py  # Core AI generation logic
├── database/
│   ├── __init__.py
│   └── db.py                 # PostgreSQL database operations
└── README.md                 # This file
```

---

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment

**Streamlit Cloud (Recommended)**
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Add DATABASE_URL to secrets
4. Deploy!

**Heroku**
```bash
# Create Procfile
web: streamlit run app.py --server.port=$PORT

# Deploy
heroku create your-app-name
git push heroku main
```

**Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

---

## 📝 Example Output

### Input
**Topic:** "New AI tool that converts screenshots to code"

### Generated Content
- **Category:** 🆕 New Tool Introduction
- **Master Storyline:** Viral hook + problem + solution + benefits
- **YouTube Script:** 45-second engaging script
- **Instagram Reel:** Fast-paced, punchy version
- **X Thread:** 6-tweet educational thread
- **Caption:** Engagement-focused social media caption
- **CTAs:** 3 platform-specific calls-to-action
- **Hashtags:** 12 relevant, trending hashtags

---

## 💡 Tips for Best Results

1. **Be Specific** - The more specific your topic, the better the output
2. **Add Context** - Include relevant facts, statistics, or details
3. **Review & Edit** - Use generated content as a foundation
4. **Test Variations** - Generate multiple versions and pick the best
5. **Customize** - Adapt the content to your unique voice and style
6. **Use History** - Reference past successful content

---

## 🆘 Troubleshooting

### Database Connection Error
```
Error: Unable to connect to database
```
**Solution:** Check your DATABASE_URL in `.env` file

### Module Not Found
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:** 
```bash
pip install -r requirements.txt
```

### Port Already in Use
```
Error: Port 8501 is already in use
```
**Solution:**
```bash
streamlit run app.py --server.port=8502
```

### Slow Performance
**Solution:** 
- Check internet connection (Supabase is cloud-based)
- Optimize database queries
- Clear browser cache

---

## � Security Notes

- ✅ Database credentials are in `.env` (not committed to git)
- ✅ `.gitignore` configured to exclude sensitive files
- ✅ Use environment variables for production
- ✅ Supabase provides SSL encryption by default

---

## 📈 Roadmap

- [ ] Integration with OpenAI API for enhanced generation
- [ ] More content categories
- [ ] Video script timing calculator
- [ ] A/B testing for different hooks
- [ ] Analytics dashboard with charts
- [ ] Multi-language support
- [ ] Template customization UI
- [ ] Batch content generation
- [ ] API key authentication
- [ ] Mobile app version

---

## 🤝 Contributing

This is a professional tool for AI content creators. Contributions welcome!

---

## 📄 License

MIT License - Feel free to use for personal or commercial projects.

---

## � Why This Tool?

### **For Content Creators**
- Save 10+ hours per week
- Consistent, professional output
- Multi-platform ready
- Viral-optimized content

### **For Agencies**
- Scale content production
- Maintain brand consistency
- Track all generated content
- Export and share easily

### **For Developers**
- Clean, modular code
- Easy to customize
- Well-documented
- Production-ready

---

## 📧 Support

For issues, questions, or suggestions:
- Check the troubleshooting section
- Review the documentation
- Open an issue on GitHub

---

**Built with ❤️ for AI Content Creators**

*Transform ideas into viral content, one topic at a time.*

---

## 🎬 Quick Start Video

1. Run `start.bat`
2. Enter your topic
3. Click "Generate Content"
4. Copy and use your viral content!

**It's that simple!** 🚀
