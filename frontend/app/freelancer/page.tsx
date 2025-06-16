"use client";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";

// DEBUG: Verify this code is loading
console.log('🚀 [FRONTEND] FreelancerPage component loaded at:', new Date().toISOString());

interface StatusUpdate {
    status: string;
    message: string;
    progress: number;
    details?: string;
    timestamp?: string;
}

export default function FreelancerPage() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState<string>("");
    const [currentStatus, setCurrentStatus] = useState<StatusUpdate | null>(null);
    const [sessionId, setSessionId] = useState<string>("");
    const [isPolling, setIsPolling] = useState<boolean>(false);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const statusPollingRef = useRef<NodeJS.Timeout | null>(null);

    // Cleanup polling on component unmount
    useEffect(() => {
        return () => {
            if (statusPollingRef.current) {
                clearInterval(statusPollingRef.current);
                statusPollingRef.current = null;
            }
        };
    }, []);

    // Debug: Watch state changes
    useEffect(() => {
        console.log('🔍 [STATE] sessionId changed to:', sessionId);
    }, [sessionId]);

    useEffect(() => {
        console.log('🔍 [STATE] isPolling changed to:', isPolling);
    }, [isPolling]);

    useEffect(() => {
        console.log('🔍 [STATE] isUploading changed to:', isUploading);
    }, [isUploading]);

    // Function to poll for status updates
    const pollStatus = async (sessionIdParam: string) => {
        const pollStartTime = new Date().toISOString();
        console.log('🔄 [FRONTEND] ========== POLL STATUS START ==========');
        console.log('🔄 [FRONTEND] Poll start time:', pollStartTime);
        console.log('🔄 [FRONTEND] Session ID parameter:', sessionIdParam);
        console.log('🔄 [FRONTEND] Session ID type:', typeof sessionIdParam);
        console.log('🔄 [FRONTEND] Session ID length:', sessionIdParam?.length);
        console.log('🔄 [FRONTEND] Current states - isPolling:', isPolling, 'isUploading:', isUploading);

        try {
            // Validate session ID
            if (!sessionIdParam || sessionIdParam.trim() === '') {
                console.error('❌ [FRONTEND] INVALID SESSION ID - ABORTING POLL');
                console.error('❌ [FRONTEND] Received:', JSON.stringify(sessionIdParam));
                return;
            }

            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const statusUrl = `${apiUrl}/cv-status/${sessionIdParam}`;

            console.log('🌐 [FRONTEND] API URL:', apiUrl);
            console.log('🌐 [FRONTEND] Full status URL:', statusUrl);
            console.log('🌐 [FRONTEND] About to make fetch request...');

            const fetchStartTime = new Date().toISOString();
            console.log('🌐 [FRONTEND] Fetch start time:', fetchStartTime);

            const response = await fetch(statusUrl, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors',
                cache: 'no-cache'
            });

            const fetchEndTime = new Date().toISOString();
            console.log('📡 [FRONTEND] Fetch completed at:', fetchEndTime);
            console.log('📡 [FRONTEND] Response status:', response.status);
            console.log('📡 [FRONTEND] Response statusText:', response.statusText);
            console.log('📡 [FRONTEND] Response ok:', response.ok);
            console.log('📡 [FRONTEND] Response headers:', Object.fromEntries(response.headers.entries()));

            if (response.ok) {
                console.log('✅ [FRONTEND] Response is OK - parsing...');
                const responseText = await response.text();
                console.log('📡 [FRONTEND] Raw response text length:', responseText.length);
                console.log('📡 [FRONTEND] Raw response text:', responseText);

                const statusData: StatusUpdate = JSON.parse(responseText);
                console.log('📊 [FRONTEND] Parsed status data:', JSON.stringify(statusData, null, 2));
                console.log('📊 [FRONTEND] Progress:', statusData.progress, '%');
                console.log('📊 [FRONTEND] Status:', statusData.status);
                console.log('📊 [FRONTEND] Message:', statusData.message);

                console.log('🔄 [FRONTEND] Updating React state...');
                setCurrentStatus(statusData);
                setUploadStatus(statusData.message);
                console.log('✅ [FRONTEND] React state updated');

                // Stop polling if completed or error
                if (statusData.status === 'completed' || statusData.status === 'error') {
                    console.log('🏁 [FRONTEND] FINAL STATUS REACHED:', statusData.status);
                    console.log('🏁 [FRONTEND] Stopping polling...');

                    if (statusPollingRef.current) {
                        console.log('🧹 [FRONTEND] Clearing interval:', statusPollingRef.current);
                        clearInterval(statusPollingRef.current);
                        statusPollingRef.current = null;
                        console.log('✅ [FRONTEND] Interval cleared');
                    } else {
                        console.log('⚠️ [FRONTEND] No interval to clear');
                    }

                    setIsUploading(false);
                    setIsPolling(false);
                    console.log('✅ [FRONTEND] States set to false');
                }
            } else {
                console.error('❌ [FRONTEND] Response not OK');
                const errorText = await response.text();
                console.error('❌ [FRONTEND] Status:', response.status, response.statusText);
                console.error('❌ [FRONTEND] Error body:', errorText);
            }
        } catch (error) {
            console.error('❌ [FRONTEND] POLL STATUS ERROR');
            console.error('❌ [FRONTEND] Error type:', error instanceof Error ? error.constructor.name : typeof error);
            console.error('❌ [FRONTEND] Error message:', error instanceof Error ? error.message : String(error));
            console.error('❌ [FRONTEND] Full error:', error);
            if (error instanceof Error && error.stack) {
                console.error('❌ [FRONTEND] Stack trace:', error.stack);
            }
        }

        const pollEndTime = new Date().toISOString();
        console.log('🔄 [FRONTEND] Poll end time:', pollEndTime);
        console.log('🔄 [FRONTEND] ========== POLL STATUS END ==========');
    };

    // Function to start status polling
    const startStatusPolling = (sessionIdParam: string) => {
        console.log('🔄 [FRONTEND] ===== STARTING STATUS POLLING =====');
        console.log('🔄 [FRONTEND] Session ID parameter:', sessionIdParam);
        console.log('🔄 [FRONTEND] Session ID type:', typeof sessionIdParam);
        console.log('🔄 [FRONTEND] Session ID length:', sessionIdParam?.length);
        console.log('🔄 [FRONTEND] Current component state - isPolling:', isPolling);
        console.log('🔄 [FRONTEND] Current component state - isUploading:', isUploading);
        console.log('🔄 [FRONTEND] Current component state - sessionId:', sessionId);

        // Validate session ID
        if (!sessionIdParam || sessionIdParam.trim() === '') {
            console.error('❌ [FRONTEND] Invalid session ID - cannot start polling');
            return;
        }

        console.log('🔄 [FRONTEND] Setting polling state to true...');
        setIsPolling(true);
        console.log('✅ [FRONTEND] setIsPolling(true) called');

        // Clear any existing polling
        if (statusPollingRef.current) {
            console.log('🧹 [FRONTEND] Clearing existing polling interval:', statusPollingRef.current);
            clearInterval(statusPollingRef.current);
            statusPollingRef.current = null;
        }

        // Create a counter to track interval fires
        let intervalCounter = 0;

        console.log('⏰ [FRONTEND] About to create setInterval...');
        console.log('⏰ [FRONTEND] Current time before setInterval:', new Date().toISOString());

        // Poll every 2 seconds
        statusPollingRef.current = setInterval(() => {
            intervalCounter++;
            console.log('⏰ [FRONTEND] 🔥🔥🔥 INTERVAL FIRED #' + intervalCounter + ' 🔥🔥🔥');
            console.log('⏰ [FRONTEND] Fire time:', new Date().toISOString());
            console.log('⏰ [FRONTEND] Polling for session:', sessionIdParam);
            console.log('⏰ [FRONTEND] Current isPolling state:', isPolling);
            console.log('⏰ [FRONTEND] Current isUploading state:', isUploading);

            // Call pollStatus with detailed logging
            console.log('⏰ [FRONTEND] About to call pollStatus...');
            pollStatus(sessionIdParam);
            console.log('⏰ [FRONTEND] pollStatus call completed');
        }, 2000);

        console.log('✅ [FRONTEND] setInterval created successfully');
        console.log('✅ [FRONTEND] Interval ID:', statusPollingRef.current);
        console.log('✅ [FRONTEND] Interval type:', typeof statusPollingRef.current);
        console.log('✅ [FRONTEND] Interval is truthy:', !!statusPollingRef.current);

        // Add a verification interval to check if our main interval is still active
        let verificationCounter = 0;
        const verificationInterval = setInterval(() => {
            verificationCounter++;
            console.log('🔍 [VERIFICATION] Check #' + verificationCounter + ' - Main interval still exists:', !!statusPollingRef.current);
            console.log('🔍 [VERIFICATION] Current isPolling state:', isPolling);
            console.log('🔍 [VERIFICATION] Current isUploading state:', isUploading);

            if (verificationCounter >= 10) {
                clearInterval(verificationInterval);
                console.log('🔍 [VERIFICATION] Verification checks completed');
            }
        }, 3000); // Check every 3 seconds

        // Test interval to verify setInterval is working at all
        let testCounter = 0;
        const testInterval = setInterval(() => {
            testCounter++;
            console.log('🧪 [TEST] Test interval fired #' + testCounter + ' at', new Date().toISOString());
            if (testCounter >= 5) {
                clearInterval(testInterval);
                console.log('🧪 [TEST] Test interval completed - setInterval is working');
            }
        }, 1000);

        // Initial poll with more detailed timing
        console.log('🚀 [FRONTEND] Scheduling initial poll in 500ms...');
        setTimeout(() => {
            console.log('🚀 [FRONTEND] ===== EXECUTING INITIAL POLL =====');
            console.log('🚀 [FRONTEND] Time:', new Date().toISOString());
            console.log('🚀 [FRONTEND] Session ID for initial poll:', sessionIdParam);
            pollStatus(sessionIdParam);
            console.log('🚀 [FRONTEND] Initial poll call completed');
        }, 500);

        console.log('🔄 [FRONTEND] ===== STATUS POLLING SETUP COMPLETE =====');
    };

    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            // Check file type
            const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
            if (!allowedTypes.includes(file.type)) {
                setUploadStatus("Please select a PDF or Word document");
                return;
            }
            // Check file size (10MB limit)
            if (file.size > 10 * 1024 * 1024) {
                setUploadStatus("File size must be less than 10MB");
                return;
            }
            setSelectedFile(file);
            setUploadStatus("");
            setCurrentStatus(null);
        }
    };

    const handleUpload = async () => {
        console.log('🚀 [FRONTEND] ===== HANDLE UPLOAD CALLED =====');
        console.log('🚀 [FRONTEND] Selected file:', selectedFile?.name);
        console.log('🚀 [FRONTEND] Current time:', new Date().toISOString());

        if (!selectedFile) {
            console.log('❌ [FRONTEND] No file selected - returning');
            return;
        }

        console.log('🚀 [FRONTEND] Setting upload states...');
        setIsUploading(true);
        setUploadStatus("Starting upload...");
        setCurrentStatus({
            status: "upload_started",
            message: "Starting upload...",
            progress: 5
        });
        console.log('✅ [FRONTEND] Upload states set');

        try {
            const formData = new FormData();
            formData.append('file', selectedFile);

            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const uploadUrl = `${apiUrl}/upload-cv`;

            console.log('=== UPLOAD DEBUG INFO ===');
            console.log('API URL:', apiUrl);
            console.log('Upload URL:', uploadUrl);
            console.log('File:', selectedFile.name, selectedFile.size, 'bytes');
            console.log('FormData entries:', Array.from(formData.entries()));

            console.log('Attempting fetch request...');

            const response = await fetch(uploadUrl, {
                method: 'POST',
                body: formData,
                // Add explicit headers (though FormData should handle this automatically)
                mode: 'cors',
            });

            console.log('Fetch completed!');
            console.log('Response status:', response.status, response.statusText);
            console.log('Response headers:', Object.fromEntries(response.headers.entries()));

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Response not OK:', errorText);
                throw new Error(`Upload failed: ${response.status} ${response.statusText}`);
            }

            // Parse the successful response
            const result = await response.json();
            console.log('Upload success result:', result);

            // If the backend returns a session_id, start status polling
            if (result.session_id) {
                console.log('🔄 [FRONTEND] ===== SESSION ID RECEIVED =====');
                console.log('🔄 [FRONTEND] Session ID value:', result.session_id);
                console.log('🔄 [FRONTEND] Session ID type:', typeof result.session_id);
                console.log('🔄 [FRONTEND] Session ID length:', result.session_id.length);
                console.log('🔄 [FRONTEND] Session ID is truthy:', !!result.session_id);
                console.log('🔄 [FRONTEND] Full response object:', JSON.stringify(result, null, 2));
                console.log('🔄 [FRONTEND] Current component states:');
                console.log('🔄 [FRONTEND] - isUploading:', isUploading);
                console.log('🔄 [FRONTEND] - isPolling:', isPolling);
                console.log('🔄 [FRONTEND] - sessionId state:', sessionId);

                // Set session ID immediately for debug display
                console.log('🆔 [FRONTEND] Setting session ID state...');
                setSessionId(result.session_id);
                console.log('✅ [FRONTEND] setSessionId called with:', result.session_id);

                // Start polling immediately - no delay needed
                console.log('🚀 [FRONTEND] Starting status polling immediately...');
                console.log('🚀 [FRONTEND] Calling startStatusPolling with:', result.session_id);

                try {
                    startStatusPolling(result.session_id);
                    console.log('✅ [FRONTEND] startStatusPolling call completed');
                } catch (error) {
                    console.error('❌ [FRONTEND] Error calling startStatusPolling:', error);
                }

            } else {
                console.warn('⚠️ [FRONTEND] ===== NO SESSION ID IN RESPONSE =====');
                console.warn('⚠️ [FRONTEND] Response keys:', Object.keys(result));
                console.warn('⚠️ [FRONTEND] Full response:', JSON.stringify(result, null, 2));
                console.warn('⚠️ [FRONTEND] Falling back to old behavior');

                // Fallback to old behavior if no session_id
                setUploadStatus(result.message || "CV uploaded successfully! Our AI will analyze it and provide feedback soon.");
                setIsUploading(false);
            }

            // Clear file selection after successful upload
            setSelectedFile(null);
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }

        } catch (error) {
            console.error('=== UPLOAD ERROR ===');
            console.error('Error type:', error instanceof Error ? error.constructor.name : typeof error);
            console.error('Error message:', error instanceof Error ? error.message : String(error));
            console.error('Full error:', error);

            // More specific error messages
            let errorMessage = "Upload failed. Please try again.";

            if (error instanceof TypeError && error.message.includes('Load failed')) {
                errorMessage = `Network error: Cannot connect to backend at ${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}. Please ensure:
1. Backend is running on port 8000
2. Frontend can reach the backend
3. No firewall blocking the connection`;
            } else if (error instanceof Error) {
                errorMessage = error.message;
            }

            setUploadStatus(errorMessage);
            setCurrentStatus({
                status: "error",
                message: errorMessage,
                progress: 0
            });
            setIsUploading(false);
        }
    };

    return (
        <main className="flex-1 flex flex-col items-center justify-center p-4 md:p-6 relative">
            {/* Golden background overlay to match homepage */}
            <div className="absolute inset-0 bg-gradient-to-br from-amber-100/40 via-orange-100/30 to-amber-200/40"></div>
            <div className="absolute inset-0 bg-gradient-to-t from-orange-200/20 via-transparent to-amber-100/15"></div>

            <div className="relative z-10 w-full flex justify-center">
                <Card className="w-full max-w-2xl p-8 shadow-xl bg-background">
                    <div className="text-center space-y-6">
                        {/* Header with back navigation */}
                        <div className="flex items-center justify-between mb-8">
                            <Link
                                href="/"
                                className="text-sm text-muted-foreground hover:text-primary transition-colors"
                            >
                                ← Back to Home
                            </Link>
                            <div className="flex-1"></div>
                        </div>

                        {/* Main content */}
                        <div className="space-y-6">
                            <div className="w-20 h-20 mx-auto bg-green-100 rounded-full flex items-center justify-center">
                                <svg
                                    className="w-10 h-10 text-green-600"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                    xmlns="http://www.w3.org/2000/svg"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                                    />
                                </svg>
                            </div>

                            <h1 className="text-3xl font-bold text-primary">
                                Hello, Freelancer! 👋
                            </h1>

                            <p className="text-lg text-muted-foreground">
                                Upload your CV to get started with AI-powered feedback.
                            </p>

                            {/* CV Upload Section */}
                            <div className="bg-muted/50 p-6 rounded-lg">
                                <div className="space-y-4">
                                    <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-6 text-center hover:border-muted-foreground/50 transition-colors">
                                        <svg
                                            className="w-12 h-12 mx-auto mb-4 text-muted-foreground"
                                            fill="none"
                                            stroke="currentColor"
                                            viewBox="0 0 24 24"
                                        >
                                            <path
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                strokeWidth={2}
                                                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                                            />
                                        </svg>

                                        <Input
                                            ref={fileInputRef}
                                            type="file"
                                            accept=".pdf,.doc,.docx"
                                            onChange={handleFileSelect}
                                            className="hidden"
                                            id="cv-upload"
                                        />

                                        <label
                                            htmlFor="cv-upload"
                                            className="cursor-pointer"
                                        >
                                            <div className="text-sm text-muted-foreground">
                                                <span className="text-primary hover:underline">Click to upload CV (PDF only, max 10MB)</span>
                                            </div>
                                        </label>
                                    </div>

                                    {selectedFile && (
                                        <div className="text-sm text-muted-foreground">
                                            Selected: {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                                        </div>
                                    )}

                                    {(uploadStatus || currentStatus) && (
                                        <div className="space-y-3">
                                            {/* Progress Bar */}
                                            {currentStatus && currentStatus.progress > 0 && (
                                                <div className="w-full bg-gray-200 rounded-full h-2">
                                                    <div
                                                        className="bg-green-600 h-2 rounded-full transition-all duration-500 ease-out"
                                                        style={{ width: `${currentStatus.progress}%` }}
                                                    ></div>
                                                </div>
                                            )}

                                            {/* Status Message */}
                                            <div className={`text-sm p-3 rounded ${currentStatus?.status === 'error' || uploadStatus.includes('failed') || uploadStatus.includes('error')
                                                ? 'bg-red-100 text-red-700'
                                                : 'bg-green-100 text-green-700'
                                                }`}>
                                                <div className="flex items-center space-x-2">
                                                    {/* Loading spinner for active processing */}
                                                    {isUploading && currentStatus?.status !== 'completed' && currentStatus?.status !== 'error' && (
                                                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-green-600 border-t-transparent"></div>
                                                    )}
                                                    <span>{currentStatus?.message || uploadStatus}</span>
                                                </div>
                                            </div>
                                        </div>
                                    )}

                                    <Button
                                        onClick={handleUpload}
                                        disabled={!selectedFile || isUploading}
                                        className="w-full"
                                    >
                                        {isUploading ? "Uploading..." : "Upload CV"}
                                    </Button>
                                </div>
                            </div>


                        </div>
                    </div>
                </Card>
            </div>
        </main>
    );
} 