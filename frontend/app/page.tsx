"use client";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import Image from "next/image";
import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex-1 flex flex-col items-center justify-center p-4 md:p-6 relative overflow-hidden">
      {/* Sophisticated wooden texture background overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-100/80 via-orange-100/60 to-amber-200/80"></div>
      <div className="absolute inset-0 bg-gradient-to-t from-orange-200/30 via-transparent to-amber-100/20"></div>

      {/* Subtle wooden grain effect using CSS patterns */}
      <div className="absolute inset-0 opacity-40">
        <div className="absolute inset-0 bg-gradient-to-r from-amber-900/5 via-transparent to-amber-900/5 transform rotate-45"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-orange-800/3 via-transparent to-orange-800/3 transform -rotate-45"></div>
      </div>

      <div className="w-full max-w-6xl relative z-10">
        {/* Enhanced Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-black mb-6 drop-shadow-sm">
            Expert Sourcing Platform
          </h1>
          <p className="text-lg md:text-xl text-black max-w-3xl mx-auto leading-relaxed font-medium">
            Connect projects with skilled freelancers through our AI-powered matching system.
            Choose your path below to get started.
          </p>
        </div>

        {/* Mobile Decorative Element - Shows on mobile/tablet instead of office images */}
        <div className="lg:hidden mb-12">
          <div className="flex justify-center items-center space-x-4">
            <div className="w-3 h-3 bg-gradient-to-r from-amber-400 to-orange-400 rounded-full animate-pulse"></div>
            <div className="w-16 h-0.5 bg-gradient-to-r from-amber-400 via-orange-400 to-amber-400 rounded-full"></div>
            <div className="w-3 h-3 bg-gradient-to-r from-orange-400 to-amber-400 rounded-full animate-pulse delay-500"></div>
          </div>
        </div>

        {/* Office Images Gallery - Desktop Only */}
        <div className="hidden lg:block mb-16">
          <div className="grid grid-cols-4 gap-6 max-w-4xl mx-auto">
            <div className="group relative overflow-hidden rounded-2xl shadow-2xl hover:shadow-3xl transition-all duration-500 transform hover:scale-105 w-52 h-52">
              <div className="absolute inset-0 bg-gradient-to-t from-amber-900/40 via-transparent to-transparent z-10"></div>
              <Image
                src="/office1.png"
                alt="Modern office workspace 1"
                width={208}
                height={208}
                className="w-full h-full object-cover object-center transition-transform duration-700 group-hover:scale-110"
                priority
              />
              <div className="absolute inset-0 bg-amber-200/10 group-hover:bg-transparent transition-colors duration-300"></div>
            </div>

            <div className="group relative overflow-hidden rounded-2xl shadow-2xl hover:shadow-3xl transition-all duration-500 transform hover:scale-105 mt-8 w-52 h-52">
              <div className="absolute inset-0 bg-gradient-to-t from-orange-900/40 via-transparent to-transparent z-10"></div>
              <Image
                src="/office2.png"
                alt="Modern office workspace 2"
                width={208}
                height={208}
                className="w-full h-full object-cover object-center transition-transform duration-700 group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-orange-200/10 group-hover:bg-transparent transition-colors duration-300"></div>
            </div>

            <div className="group relative overflow-hidden rounded-2xl shadow-2xl hover:shadow-3xl transition-all duration-500 transform hover:scale-105 w-52 h-52">
              <div className="absolute inset-0 bg-gradient-to-t from-amber-900/40 via-transparent to-transparent z-10"></div>
              <Image
                src="/office3.png"
                alt="Modern office workspace 3"
                width={208}
                height={208}
                className="w-full h-full object-cover object-center transition-transform duration-700 group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-amber-200/10 group-hover:bg-transparent transition-colors duration-300"></div>
            </div>

            <div className="group relative overflow-hidden rounded-2xl shadow-2xl hover:shadow-3xl transition-all duration-500 transform hover:scale-105 mt-8 w-52 h-52">
              <div className="absolute inset-0 bg-gradient-to-t from-orange-900/40 via-transparent to-transparent z-10"></div>
              <Image
                src="/office4.png"
                alt="Modern office workspace 4"
                width={208}
                height={208}
                className="w-full h-full object-cover object-center transition-transform duration-700 group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-orange-200/10 group-hover:bg-transparent transition-colors duration-300"></div>
            </div>
          </div>

          {/* Decorative element below images */}
          <div className="flex justify-center mt-8">
            <div className="w-40 h-1 bg-gradient-to-r from-transparent via-amber-400 to-transparent rounded-full opacity-60"></div>
          </div>
        </div>

        {/* Enhanced Two main options side by side */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Project Submission Option */}
          <Card className="p-8 shadow-2xl bg-white/95 backdrop-blur-sm border-0 hover:shadow-3xl hover:bg-white transition-all duration-500 h-full transform hover:-translate-y-2">
            <div className="text-center space-y-6 flex flex-col h-full">
              <div className="w-20 h-20 mx-auto bg-gradient-to-br from-green-100 to-green-200 rounded-2xl flex items-center justify-center shadow-lg">
                <svg
                  className="w-10 h-10 text-green-800"
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
                <h2 className="text-2xl font-semibold text-black mb-2">
                  Submit a Project
                </h2>
                <p className="text-black mb-6">
                  Looking for skilled freelancers? Describe your project requirements
                  and let our AI help you find the perfect match for your needs.
                </p>
              </div>

              <div className="space-y-3 flex-grow">
                <ul className="text-sm text-black space-y-2">
                  <li className="flex items-center justify-center space-x-2">
                    <span className="w-1.5 h-1.5 bg-amber-400 rounded-full"></span>
                    <span>AI-powered freelancer matching</span>
                  </li>
                  <li className="flex items-center justify-center space-x-2">
                    <span className="w-1.5 h-1.5 bg-amber-400 rounded-full"></span>
                    <span>Detailed project requirement analysis</span>
                  </li>
                  <li className="flex items-center justify-center space-x-2">
                    <span className="w-1.5 h-1.5 bg-amber-400 rounded-full"></span>
                    <span>Expert recommendations</span>
                  </li>
                </ul>
              </div>

              <div className="mt-auto">
                <Link href="/project" className="block">
                  <Button size="lg" className="w-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105">
                    Submit Project
                  </Button>
                </Link>
              </div>
            </div>
          </Card>

          {/* Freelancer Option */}
          <Card className="p-8 shadow-2xl bg-white/95 backdrop-blur-sm border-0 hover:shadow-3xl hover:bg-white transition-all duration-500 h-full transform hover:-translate-y-2">
            <div className="text-center space-y-6 flex flex-col h-full">
              <div className="w-20 h-20 mx-auto bg-gradient-to-br from-green-100 to-green-200 rounded-2xl flex items-center justify-center shadow-lg">
                <svg
                  className="w-10 h-10 text-green-800"
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
                <h2 className="text-2xl font-semibold text-black mb-2">
                  I&apos;m a Freelancer
                </h2>
                <p className="text-black mb-6">
                  Are you a skilled freelancer? Join our platform to discover
                  exciting projects that match your expertise and grow your career.
                </p>
              </div>

              <div className="space-y-3 flex-grow">
                <ul className="text-sm text-black space-y-2">
                  <li className="flex items-center justify-center space-x-2">
                    <span className="w-1.5 h-1.5 bg-amber-400 rounded-full"></span>
                    <span>Get feedback for your CV</span>
                  </li>
                  <li className="flex items-center justify-center space-x-2">
                    <span className="w-1.5 h-1.5 bg-amber-400 rounded-full"></span>
                    <span>Connect with clients</span>
                  </li>
                  <li className="flex items-center justify-center space-x-2">
                    <span className="w-1.5 h-1.5 bg-amber-400 rounded-full"></span>
                    <span>Apply for projects</span>
                  </li>
                </ul>
              </div>

              <div className="mt-auto">
                <Link href="/freelancer" className="block">
                  <Button size="lg" className="w-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105">
                    Join as Freelancer
                  </Button>
                </Link>
              </div>
            </div>
          </Card>
        </div>

        {/* Enhanced footer section */}
        <div className="text-center mt-12">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-0.5 bg-gradient-to-r from-transparent via-amber-400 to-transparent rounded-full opacity-60"></div>
          </div>
          <p className="text-black font-medium">
            Powered by advanced AI technology for intelligent project-freelancer matching
          </p>
        </div>
      </div>
    </main>
  );
} 