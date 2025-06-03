"use client";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import Link from "next/link";

export default function FreelancerPage() {
    return (
        <main className="flex-1 flex flex-col items-center justify-center p-4 md:p-6">
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
                            Welcome to the freelancer portal. This section is currently under development.
                        </p>

                        <div className="bg-muted/50 p-6 rounded-lg">
                            <h2 className="text-xl font-semibold text-primary mb-3">
                                Coming Soon
                            </h2>
                            <ul className="text-left text-muted-foreground space-y-2">
                                <li>• Browse available projects</li>
                                <li>• Create your professional profile</li>
                                <li>• Showcase your portfolio</li>
                                <li>• Apply to projects that match your skills</li>
                                <li>• Communicate with clients</li>
                                <li>• Track your earnings and projects</li>
                            </ul>
                        </div>

                        <div className="pt-4">
                            <p className="text-sm text-muted-foreground mb-4">
                                Stay tuned for updates! In the meantime, you can explore our project submission portal.
                            </p>

                            <div className="flex gap-3 justify-center">
                                <Link href="/project">
                                    <Button variant="outline">
                                        View Project Portal
                                    </Button>
                                </Link>
                                <Link href="/">
                                    <Button>
                                        Back to Home
                                    </Button>
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </Card>
        </main>
    );
} 