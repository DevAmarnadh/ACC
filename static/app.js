/**
 * AI Content Creation Engine - Frontend Application
 * Connects to FastAPI backend
 */

const API_BASE_URL = 'http://localhost:8000/api';

// State management
let currentContent = null;
let contentHistory = [];

// DOM Elements
const topicInput = document.getElementById('topicInput');
const contextInput = document.getElementById('contextInput');
const generateBtn = document.getElementById('generateBtn');
const loadingState = document.getElementById('loadingState');
const loadingText = document.getElementById('loadingText');
const progressBar = document.getElementById('progressBar');
const resultsSection = document.getElementById('resultsSection');
const historyBtn = document.getElementById('historyBtn');
const exportBtn = document.getElementById('exportBtn');
const toast = document.getElementById('toast');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadHistory();
});

// Event Listeners
function setupEventListeners() {
    generateBtn.addEventListener('click', handleGenerate);
    exportBtn.addEventListener('click', handleExport);
    historyBtn.addEventListener('click', showHistory);

    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => switchTab(e.target.dataset.tab));
    });

    // Copy buttons
    document.querySelectorAll('.btn-copy').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const target = e.currentTarget.dataset.target;
            copyToClipboard(target);
        });
    });

    // Enter key to generate
    topicInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleGenerate();
        }
    });
}

// Generate Content
async function handleGenerate() {
    const topic = topicInput.value.trim();

    if (!topic) {
        showToast('Please enter a topic', 'error');
        topicInput.focus();
        return;
    }

    if (topic.length < 5) {
        showToast('Topic should be at least 5 characters', 'error');
        return;
    }

    // Show loading state
    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                topic: topic,
                context: contextInput.value.trim() || null
            })
        });

        if (!response.ok) {
            throw new Error('Failed to generate content');
        }

        const data = await response.json();
        currentContent = data;

        // Display results
        displayResults(data);

        // Reload history
        loadHistory();

        // Scroll to results
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);

    } catch (error) {
        console.error('Error:', error);
        showToast('Failed to generate content. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

// Display Results
function displayResults(data) {
    // Show results section
    resultsSection.style.display = 'block';

    // Category badge
    const categoryText = document.getElementById('categoryText');
    categoryText.textContent = formatCategoryName(data.category);

    // Master storyline
    document.getElementById('masterStoryline').textContent = data.master_storyline;

    // YouTube script
    document.getElementById('youtubeScript').textContent = data.youtube_script;

    // Instagram script
    document.getElementById('instagramScript').textContent = data.instagram_script;

    // Twitter thread
    const twitterThread = document.getElementById('twitterThread');
    twitterThread.innerHTML = '';
    data.twitter_thread.forEach((tweet, index) => {
        const tweetDiv = document.createElement('div');
        tweetDiv.className = 'tweet';
        tweetDiv.innerHTML = `
            <span class="tweet-number">Tweet ${index + 1}</span>
            <p>${tweet}</p>
        `;
        twitterThread.appendChild(tweetDiv);
    });

    // Caption
    document.getElementById('captionText').textContent = data.caption;

    // CTA
    const ctaContainer = document.getElementById('ctaSuggestions');
    ctaContainer.innerHTML = '<ul style="margin: 0; padding-left: 1.5rem;">';
    data.cta.forEach(cta => {
        ctaContainer.innerHTML += `<li style="margin-bottom: 0.5rem;">${cta}</li>`;
    });
    ctaContainer.innerHTML += '</ul>';

    // Hashtags
    const hashtagContainer = document.getElementById('hashtagList');
    hashtagContainer.innerHTML = '';
    data.hashtags.forEach(tag => {
        const hashtagSpan = document.createElement('span');
        hashtagSpan.className = 'hashtag';
        hashtagSpan.textContent = tag;
        hashtagContainer.appendChild(hashtagSpan);
    });

    // Animate in
    resultsSection.classList.add('fade-in');
}

// Loading State
function showLoading() {
    generateBtn.disabled = true;
    loadingState.style.display = 'block';
    resultsSection.style.display = 'none';

    // Simulate progress
    let progress = 0;
    const steps = [
        'Analyzing topic and classifying content...',
        'Generating master storyline...',
        'Adapting for YouTube Shorts...',
        'Creating Instagram Reel script...',
        'Building X thread...',
        'Finalizing content...'
    ];

    const interval = setInterval(() => {
        progress += 16.67;
        progressBar.style.width = `${Math.min(progress, 95)}%`;

        const stepIndex = Math.floor(progress / 16.67);
        if (stepIndex < steps.length) {
            loadingText.textContent = steps[stepIndex];
        }

        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 800);

    // Store interval ID to clear it later
    loadingState.dataset.intervalId = interval;
}

function hideLoading() {
    // Clear interval
    const intervalId = loadingState.dataset.intervalId;
    if (intervalId) {
        clearInterval(parseInt(intervalId));
    }

    progressBar.style.width = '100%';
    setTimeout(() => {
        loadingState.style.display = 'none';
        progressBar.style.width = '0%';
        generateBtn.disabled = false;
    }, 300);
}

// Tab Switching
function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-content`).classList.add('active');
}

// Copy to Clipboard
function copyToClipboard(targetId) {
    const element = document.getElementById(targetId);
    let textToCopy = '';

    if (targetId === 'twitterThread') {
        // Special handling for Twitter thread
        const tweets = element.querySelectorAll('.tweet p');
        textToCopy = Array.from(tweets).map(p => p.textContent).join('\n\n---\n\n');
    } else if (targetId === 'hashtagList') {
        // Special handling for hashtags
        const hashtags = element.querySelectorAll('.hashtag');
        textToCopy = Array.from(hashtags).map(h => h.textContent).join(' ');
    } else {
        textToCopy = element.textContent;
    }

    navigator.clipboard.writeText(textToCopy).then(() => {
        showToast('Copied to clipboard!');
    }).catch(() => {
        showToast('Failed to copy', 'error');
    });
}

// Export All Content
function handleExport() {
    if (!currentContent) {
        showToast('No content to export', 'error');
        return;
    }

    const exportData = {
        topic: topicInput.value,
        generated_at: new Date().toISOString(),
        category: currentContent.category,
        content: {
            master_storyline: currentContent.master_storyline,
            youtube_shorts: currentContent.youtube_script,
            instagram_reel: currentContent.instagram_script,
            twitter_thread: currentContent.twitter_thread,
            caption: currentContent.caption,
            cta_suggestions: currentContent.cta,
            hashtags: currentContent.hashtags
        }
    };

    // Create formatted text file
    let exportText = `AI CONTENT CREATION ENGINE - EXPORT\n`;
    exportText += `${'='.repeat(60)}\n\n`;
    exportText += `Topic: ${exportData.topic}\n`;
    exportText += `Category: ${formatCategoryName(exportData.category)}\n`;
    exportText += `Generated: ${new Date(exportData.generated_at).toLocaleString()}\n\n`;
    exportText += `${'='.repeat(60)}\n\n`;

    exportText += `MASTER STORYLINE\n${'-'.repeat(60)}\n${exportData.content.master_storyline}\n\n`;
    exportText += `${'='.repeat(60)}\n\n`;

    exportText += `YOUTUBE SHORTS SCRIPT\n${'-'.repeat(60)}\n${exportData.content.youtube_shorts}\n\n`;
    exportText += `${'='.repeat(60)}\n\n`;

    exportText += `INSTAGRAM REEL SCRIPT\n${'-'.repeat(60)}\n${exportData.content.instagram_reel}\n\n`;
    exportText += `${'='.repeat(60)}\n\n`;

    exportText += `X (TWITTER) THREAD\n${'-'.repeat(60)}\n`;
    exportData.content.twitter_thread.forEach((tweet, i) => {
        exportText += `Tweet ${i + 1}:\n${tweet}\n\n`;
    });
    exportText += `${'='.repeat(60)}\n\n`;

    exportText += `SOCIAL MEDIA CAPTION\n${'-'.repeat(60)}\n${exportData.content.caption}\n\n`;
    exportText += `${'='.repeat(60)}\n\n`;

    exportText += `CALL-TO-ACTION SUGGESTIONS\n${'-'.repeat(60)}\n`;
    exportData.content.cta_suggestions.forEach((cta, i) => {
        exportText += `${i + 1}. ${cta}\n`;
    });
    exportText += `\n${'='.repeat(60)}\n\n`;

    exportText += `HASHTAGS\n${'-'.repeat(60)}\n${exportData.content.hashtags.join(' ')}\n\n`;
    exportText += `${'='.repeat(60)}\n`;

    // Download as text file
    const blob = new Blob([exportText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ai-content-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showToast('Content exported successfully!');
}

// Load History
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/history?limit=10`);
        if (response.ok) {
            contentHistory = await response.json();
        }
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

// Show History Modal (simplified version)
function showHistory() {
    if (contentHistory.length === 0) {
        showToast('No history available yet');
        return;
    }

    let historyHTML = 'Recent Content:\n\n';
    contentHistory.forEach((item, index) => {
        const date = new Date(item.created_at).toLocaleDateString();
        historyHTML += `${index + 1}. ${item.topic} (${formatCategoryName(item.category)}) - ${date}\n`;
    });

    alert(historyHTML);
}

// Toast Notification
function showToast(message, type = 'success') {
    const toastMessage = document.getElementById('toastMessage');
    toastMessage.textContent = message;

    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Utility Functions
function formatCategoryName(category) {
    const names = {
        'new_tool_intro': 'New Tool Introduction',
        'tool_detailed_tutorial': 'Detailed Tutorial',
        'trending_ai_model': 'Trending AI Model',
        'ai_trending_news': 'AI News',
        'github_open_source_repo': 'Open Source Repository',
        'instagram_engagement_content': 'Engagement Content'
    };
    return names[category] || category;
}

// Service Worker Registration (for PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment to enable service worker
        // navigator.serviceWorker.register('/sw.js');
    });
}
