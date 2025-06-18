import axios, { AxiosError, AxiosResponse } from 'axios';

const apiClient = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

apiClient.interceptors.request.use(async (config) => {
    // In a real app, you might get the token from a state manager or secure cookie
    // const token = localStorage.getItem('authToken');
    // if (token && config.headers) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
});

apiClient.interceptors.response.use(
    (response: AxiosResponse) => response,
    (error: AxiosError) => {
        // Here you can handle global errors, like logging or showing a toast
        if (error.response && error.response.status === 401) {
            // For example, redirect to login page
            // window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default apiClient;
