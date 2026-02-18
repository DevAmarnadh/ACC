import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ContentGeneratorForm from './components/ContentGeneratorForm';
import ResultsDisplay from './components/ResultsDisplay';
import { useContentGeneration } from './hooks/useApi';
import { motion } from 'framer-motion';

function App() {
  const { loading, error, result, generateContent } = useContentGeneration();
  const [currentContent, setCurrentContent] = useState(null);

  // Sync result to current content when generated
  useEffect(() => {
    if (result) {
      setCurrentContent(result);
    }
  }, [result]);

  const handleHistorySelect = (item) => {
    setCurrentContent(item);
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg-secondary)' }}>
      <Sidebar onSelectFromHistory={handleHistorySelect} />

      <main style={{ flex: 1, marginLeft: '280px', padding: '2rem' }}>
        <div className="container">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            style={{ marginBottom: '2.5rem', textAlign: 'center' }}
          >
            <h1 style={{ marginBottom: '0.75rem' }}>
              Create Stunning Content
            </h1>
            <p style={{ fontSize: '1.125rem' }}>
              Transform your ideas into viral multi-platform posts in seconds.
            </p>
          </motion.div>

          <ContentGeneratorForm onGenerate={generateContent} loading={loading} />

          {error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              style={{
                marginTop: '1.5rem',
                padding: '1rem',
                background: '#fef2f2',
                border: '1px solid #fee2e2',
                color: '#b91c1c',
                borderRadius: 'var(--radius-md)',
                textAlign: 'center'
              }}
            >
              {error}
            </motion.div>
          )}

          {currentContent && (
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <ResultsDisplay data={currentContent} />
            </motion.div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
