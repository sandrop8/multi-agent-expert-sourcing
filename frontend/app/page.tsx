"use client";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex-1 flex flex-col items-center justify-center p-4 md:p-6">
      <div className="w-full max-w-6xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-primary mb-4">
            Expert Sourcing Platform
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Connect projects with skilled freelancers through our AI-powered matching system.
            Choose your path below to get started.
          </p>
        </div>

        {/* Two main options side by side */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Project Submission Option */}
          <Card className="p-8 shadow-xl bg-background hover:shadow-2xl transition-shadow duration-300 h-full">
            <div className="text-center space-y-6 flex flex-col h-full">
              <div className="w-16 h-16 mx-auto bg-blue-100 rounded-full flex items-center justify-center">
                <svg
                  className="w-8 h-8 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>

              <div>
                <h2 className="text-2xl font-semibold text-primary mb-2">
                  Submit a Project
                </h2>
                <p className="text-muted-foreground mb-6">
                  Looking for skilled freelancers? Describe your project requirements
                  and let our AI help you find the perfect match for your needs.
                </p>
              </div>

              <div className="space-y-3 flex-grow">
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• AI-powered freelancer matching</li>
                  <li>• Detailed project requirement analysis</li>
                  <li>• Expert recommendations</li>
                </ul>
              </div>

              <div className="mt-auto">
                <Link href="/project" className="block">
                  <Button size="lg" className="w-full">
                    Submit Project
                  </Button>
                </Link>
              </div>
            </div>
          </Card>

          {/* Freelancer Option */}
          <Card className="p-8 shadow-xl bg-background hover:shadow-2xl transition-shadow duration-300 h-full">
            <div className="text-center space-y-6 flex flex-col h-full">
              <div className="w-16 h-16 mx-auto bg-blue-100 rounded-full flex items-center justify-center">
                <svg
                  className="w-8 h-8 text-blue-600"
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

              <div>
                <h2 className="text-2xl font-semibold text-primary mb-2">
                  I&apos;m a Freelancer
                </h2>
                <p className="text-muted-foreground mb-6">
                  Are you a skilled freelancer? Join our platform to discover
                  exciting projects that match your expertise and grow your career.
                </p>
              </div>

              <div className="space-y-3 flex-grow">
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• Get feedback for your CV</li>
                  <li>• Connect with clients</li>
                  <li>• Apply for projects</li>
                </ul>
              </div>

              <div className="mt-auto">
                <Link href="/freelancer" className="block">
                  <Button size="lg" className="w-full">
                    Join as Freelancer
                  </Button>
                </Link>
              </div>
            </div>
          </Card>
        </div>

        {/* Additional info section */}
        <div className="text-center mt-12">
          <p className="text-sm text-muted-foreground">
            Powered by advanced AI technology for intelligent project-freelancer matching
          </p>
        </div>
      </div>
    </main>
  );
} 