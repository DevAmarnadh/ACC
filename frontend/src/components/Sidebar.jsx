import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { History, LayoutGrid, Clock, ChevronRight } from 'lucide-react';
import { useHistory } from '../hooks/useApi';
import { CATEGORIES } from '../constants';
import './Sidebar.css';

export default function Sidebar({ onSelectFromHistory }) {
    const { history, fetchHistory, loading } = useHistory();
    const [filter, setFilter] = useState('all');

    useEffect(() => {
        fetchHistory(filter === 'all' ? null : filter);
    }, [filter, fetchHistory]);

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <div className="brand">
                    <div className="brand-logo">AI</div>
                    <span className="brand-name">Content Engine</span>
                </div>
            </div>

            <div className="sidebar-content">
                <div className="sidebar-section">
                    <h3 className="sidebar-title">
                        <LayoutGrid size={16} /> Filters
                    </h3>
                    <select
                        className="filter-select"
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                    >
                        <option value="all">All Categories</option>
                        {Object.entries(CATEGORIES).map(([key, label]) => (
                            <option key={key} value={key}>{label}</option>
                        ))}
                    </select>
                </div>

                <div className="sidebar-section flex-grow">
                    <h3 className="sidebar-title">
                        <History size={16} /> History
                        <span className="badge">{history.length}</span>
                    </h3>

                    <div className="history-list">
                        {loading ? (
                            <div className="loading-state">Loading...</div>
                        ) : history.length === 0 ? (
                            <div className="empty-state">No history yet</div>
                        ) : (
                            history.map((item) => (
                                <motion.button
                                    key={item.id}
                                    whileHover={{ x: 4 }}
                                    className="history-item"
                                    onClick={() => onSelectFromHistory(item)}
                                >
                                    <div className="history-item-content">
                                        <span className="history-category">
                                            {CATEGORIES[item.category] || item.category}
                                        </span>
                                        <h4 className="history-topic">
                                            {item.topic}
                                        </h4>
                                        <span className="history-date">
                                            <Clock size={12} />
                                            {new Date(item.created_at).toLocaleDateString()}
                                        </span>
                                    </div>
                                    <ChevronRight size={16} className="history-arrow" />
                                </motion.button>
                            ))
                        )}
                    </div>
                </div>

                <div className="sidebar-footer">
                    <div className="status-indicator online">
                        <span className="dot"></span>
                        System Online
                    </div>
                </div>
            </div>
        </div>
    );
}
