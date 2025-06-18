import apiClient from '@/lib/api';
import { AxiosError, AxiosRequestConfig } from 'axios';
import { useCallback, useEffect, useState } from 'react';

interface UseApiResult<T> {
    data: T | null;
    loading: boolean;
    error: AxiosError | null;
    refetch: () => void;
}

export function useApi<T>(url: string, options?: AxiosRequestConfig): UseApiResult<T> {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<AxiosError | null>(null);

    const fetchData = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await apiClient.get<T>(url, options);
            setData(response.data);
        } catch (err) {
            setError(err as AxiosError);
        } finally {
            setLoading(false);
        }
    }, [url, options]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    return { data, loading, error, refetch: fetchData };
}
