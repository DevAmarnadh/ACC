import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Youtube, Instagram, Twitter, MessageCircle, FileText, CheckCircle2 } from 'lucide-react';
import './ResultsDisplay.css'; // We will create this file

const TABS = [
    { id: 'master', label: 'Master Story', icon: FileText },
    { id: 'youtube', label: 'YouTube Script', icon: Youtube },
    { id: 'instagram', label: 'Instagram Reel', icon: Instagram },
    { id: 'twitter', label: 'X Thread', icon: Twitter },
    { id: 'caption', label: 'Caption & CTA', icon: MessageCircle },
];

export default function ResultsDisplay({ data }) {
    const [activeTab, setActiveTab] = useState('master');

    // Handle single vs array results
    const content = Array.isArray(data) ? data[0] : data;

    return (
        <div className="results-container">
            <div className="results-header">
                <h3 className="section-title">
                    <CheckCircle2 color="#22c55e" size={20} />
                    Generated Content
                </h3>
                <span className="category-badge">
                    {content.category || 'Results'}
                </span>
            </div>

            <div className="results-card">
                {/* Tabs */}
                <div className="tabs-header">
                    {TABS.map((tab) => {
                        const Icon = tab.icon;
                        const isActive = activeTab === tab.id;

                        return (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`tab-item ${isActive ? 'active' : ''}`}
                            >
                                <Icon size={16} />
                                {tab.label}
                            </button>
                        );
                    })}
                </div>

                {/* Content Area */}
                <div className="tab-content">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={activeTab}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            transition={{ duration: 0.2 }}
                        >
                            {activeTab === 'master' && (
                                <div className="content-prose">
                                    <h4 className="content-label">Master Storyline</h4>
                                    <div className="text-body master-text">
                                        {content.master_storyline}
                                    </div>
                                </div>
                            )}

                            {activeTab === 'youtube' && (
                                <div className="platform-content youtube">
                                    <div className="platform-box">
                                        <h4 className="platform-title youtube-text">
                                            <Youtube size={18} />
                                            YouTube Shorts Script (Approx. 60s)
                                        </h4>
                                        <pre className="text-pre">
                                            {content.youtube_script}
                                        </pre>
                                    </div>
                                </div>
                            )}

                            {activeTab === 'instagram' && (
                                <div className="platform-content instagram">
                                    <div className="platform-box">
                                        <h4 className="platform-title instagram-text">
                                            <Instagram size={18} />
                                            Instagram Reel Script
                                        </h4>
                                        <pre className="text-pre">
                                            {content.instagram_script}
                                        </pre>
                                    </div>
                                </div>
                            )}

                            {activeTab === 'twitter' && (
                                <div className="twitter-thread">
                                    {content.twitter_thread?.map((tweet, idx) => (
                                        <div key={idx} className="tweet-card">
                                            <div className="tweet-line" />
                                            <div className="tweet-avatar" />
                                            <div className="tweet-body">
                                                {tweet}
                                            </div>
                                            <div className="tweet-actions">
                                                <span><MessageCircle size={12} /> Reply</span>
                                                <span>Retweet</span>
                                                <span>Like</span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}

                            {activeTab === 'caption' && (
                                <div className="caption-grid">
                                    <div className="caption-col">
                                        <h4 className="content-label">Social Caption</h4>
                                        <div className="caption-box">
                                            {content.caption}
                                        </div>
                                    </div>

                                    <div className="caption-col">
                                        <div className="meta-section">
                                            <h4 className="content-label">Hashtags</h4>
                                            <div className="tags-list">
                                                {content.hashtags?.map((tag, i) => (
                                                    <span key={i} className="tag">
                                                        {tag}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>

                                        <div className="meta-section">
                                            <h4 className="content-label">Call to Actions</h4>
                                            <ul className="cta-list">
                                                {content.cta?.map((cta, i) => (
                                                    <li key={i} className="cta-item">
                                                        <CheckCircle2 size={16} />
                                                        {cta}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </motion.div>
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
}
