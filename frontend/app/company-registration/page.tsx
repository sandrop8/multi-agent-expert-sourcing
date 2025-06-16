"use client";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import Link from "next/link";
import { useState } from "react";

export default function CompanyRegistrationPage() {
    const [websiteUrl, setWebsiteUrl] = useState("");
    const [linkedinUrl, setLinkedinUrl] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [message, setMessage] = useState<{ type: 'error' | 'success', text: string } | null>(null);

    async function handleSubmit() {
        if (!websiteUrl.trim()) {
            setMessage({ type: 'error', text: 'Company website URL is required.' });
            return;
        }
        setIsLoading(true);
        setMessage(null);

        // For now, this is a placeholder.
        console.log("Submitting:", { websiteUrl, linkedinUrl });

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));

        console.log('Submission placeholder successful.');
        setMessage({ type: 'success', text: 'Registration submitted for analysis. We will get back to you shortly.' });

        // Reset form after a delay
        setTimeout(() => {
            setWebsiteUrl("");
            setLinkedinUrl("");
            setMessage(null);
        }, 5000);

        setIsLoading(false);
    }

    return (
        <main className="flex-1 flex flex-col items-center justify-center p-4 md:p-6 relative">
            {/* Background overlay to match other pages */}
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
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth="2"
                                        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0v-4a2 2 0 012-2h6a2 2 0 012 2v4m-6 0h-2">
                                    </path>
                                </svg>
                            </div>

                            <h1 className="text-3xl font-bold text-primary">
                                Company Registration
                            </h1>

                            <p className="text-lg text-muted-foreground">
                                Provide your company's website for an AI-powered analysis of your services.
                            </p>

                            {/* Form Section */}
                            <div className="bg-muted/50 p-6 rounded-lg text-left space-y-6">
                                <div className="space-y-2">
                                    <label htmlFor="website-url" className="text-sm font-medium text-foreground">Company Website URL <span className="text-red-500">*</span></label>
                                    <Input
                                        id="website-url"
                                        placeholder="https://example.com"
                                        value={websiteUrl}
                                        onChange={(e) => setWebsiteUrl(e.target.value)}
                                        disabled={isLoading}
                                        required
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label htmlFor="linkedin-url" className="text-sm font-medium text-foreground">LinkedIn Profile URL (Optional)</label>
                                    <Input
                                        id="linkedin-url"
                                        placeholder="https://linkedin.com/company/example"
                                        value={linkedinUrl}
                                        onChange={(e) => setLinkedinUrl(e.target.value)}
                                        disabled={isLoading}
                                    />
                                </div>
                            </div>

                            {message && (
                                <div className={`p-3 rounded-md text-sm ${message.type === 'error' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                                    {message.text}
                                </div>
                            )}

                            <Button onClick={handleSubmit} disabled={isLoading} className="w-full">
                                {isLoading ? "Analyzing..." : "Register"}
                            </Button>
                        </div>
                    </div>
                </Card>
            </div>
        </main>
    );
} 