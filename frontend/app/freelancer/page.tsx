"use client";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import Link from "next/link";
import { useRef, useState } from "react";

export default function FreelancerPage() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState<string>("");
    const fileInputRef = useRef<HTMLInputElement>(null);

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
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setIsUploading(true);
        setUploadStatus("Uploading...");

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

            setUploadStatus("CV uploaded successfully! Our AI will analyze it and provide feedback soon.");
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
        } finally {
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
                                Welcome to the freelancer portal. Upload your CV to get started with AI-powered feedback.
                            </p>

                            {/* CV Upload Section */}
                            <div className="bg-muted/50 p-6 rounded-lg">
                                <h2 className="text-xl font-semibold text-primary mb-4">
                                    Upload Your CV
                                </h2>

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
                                                <span className="text-primary hover:underline">Click to upload</span>
                                            </div>
                                            <div className="text-xs text-muted-foreground mt-1">
                                                PDF, DOC, DOCX (Max 10MB)
                                            </div>
                                        </label>
                                    </div>

                                    {selectedFile && (
                                        <div className="text-sm text-muted-foreground">
                                            Selected: {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                                        </div>
                                    )}

                                    {uploadStatus && (
                                        <div className={`text-sm p-3 rounded ${uploadStatus.includes('successfully') ? 'bg-green-100 text-green-700' : uploadStatus.includes('failed') || uploadStatus.includes('error') ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'}`}>
                                            {uploadStatus}
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

                            <div className="pt-4">
                                <p className="text-sm text-muted-foreground mb-4">
                                    Our AI will analyze your CV and provide personalized feedback to help you improve your profile.
                                </p>
                            </div>
                        </div>
                    </div>
                </Card>
            </div>
        </main>
    );
} 