import { useState, useCallback } from 'react';
import axios from 'axios';
import { API_URL } from '../constants';

export const useContentGeneration = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [result, setResult] = useState(null);

    const generateContent = useCallback(async (params) => {
        setLoading(true);
        setError(null);
        try {
            const { data } = await axios.post(`${API_URL}/generate`, params);
            if (data.status === 'success') {
                setResult(data.data);
            } else {
                throw new Error(data.message || 'Generation failed');
            }
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Something went wrong');
        } finally {
            setLoading(false);
        }
    }, []);

    return { loading, error, result, generateContent };
};

export const useHistory = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);

    const fetchHistory = useCallback(async (category = null) => {
        setLoading(true);
        try {
            const params = category ? { category } : {};
            const { data } = await axios.get(`${API_URL}/history`, { params });
            if (data.status === 'success') {
                setHistory(data.data);
            }
        } catch (err) {
            console.error('Failed to fetch history:', err);
        } finally {
            setLoading(false);
        }
    }, []);

    return { history, loading, fetchHistory };
};
