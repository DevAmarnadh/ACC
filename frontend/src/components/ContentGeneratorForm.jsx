import { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Loader2, ArrowRight } from 'lucide-react';

export default function ContentGeneratorForm({ onGenerate, loading }) {
    const [topic, setTopic] = useState('');
    const [context, setContext] = useState('');
    const [generateAll, setGenerateAll] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!topic.trim()) return;
        onGenerate({ topic, context, generate_all: generateAll });
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card"
        >
            <div className="flex items-center" style={{ gap: '0.75rem', marginBottom: '1.5rem' }}>
                <div style={{ padding: '0.5rem', background: '#eff6ff', borderRadius: 'var(--radius-md)', color: '#2563eb' }}>
                    <Sparkles size={24} />
                </div>
                <div>
                    <h2 style={{ fontSize: '1.25rem', fontWeight: 700, margin: 0 }}>Generate New Content</h2>
                    <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', margin: 0 }}>Transform your ideas into viral multi-platform posts</p>
                </div>
            </div>

            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    <label className="label">Topic or Idea</label>
                    <input
                        type="text"
                        className="input"
                        value={topic}
                        onChange={(e) => setTopic(e.target.value)}
                        placeholder="e.g., The Future of AI Coding Agents"
                        required
                    />
                </div>

                <div className="input-group">
                    <label className="label">Additional Context (Optional)</label>
                    <textarea
                        className="input textarea"
                        value={context}
                        onChange={(e) => setContext(e.target.value)}
                        placeholder="Paste article text, notes, or specific points to include..."
                    />
                </div>

                <div className="flex items-center justify-between" style={{ marginTop: '1.5rem' }}>
                    <label className="flex items-center" style={{ gap: '0.5rem', cursor: 'pointer', userSelect: 'none' }}>
                        <input
                            type="checkbox"
                            checked={generateAll}
                            onChange={(e) => setGenerateAll(e.target.checked)}
                            style={{ width: '1rem', height: '1rem', accentColor: 'var(--accent-primary)' }}
                        />
                        <span style={{ fontSize: '0.875rem', fontWeight: 500, color: 'var(--text-primary)' }}>Generate for ALL Categories</span>
                    </label>

                    <button
                        type="submit"
                        disabled={loading || !topic.trim()}
                        className="btn btn-primary"
                        style={{ minWidth: '140px' }}
                    >
                        {loading ? (
                            <>
                                <Loader2 className="animate-spin" size={18} />
                                Generate...
                            </>
                        ) : (
                            <>
                                Generate Content
                                <ArrowRight size={18} />
                            </>
                        )}
                    </button>
                </div>
            </form>
        </motion.div>
    );
}
