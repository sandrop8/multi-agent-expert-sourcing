"use client";
import CallToActionCard from "@/components/common/CallToActionCard";
import HeroSection from "@/components/common/HeroSection";
import FeatureGallery from "@/components/features/landing/FeatureGallery";

const cardData = [
  {
    icon: (
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
    ),
    title: "Submit a Project",
    description: "Looking for skilled freelancers? Describe your project requirements and let our AI help you find the perfect match for your needs.",
    features: ["AI-powered freelancer matching", "Detailed project requirement analysis", "Expert recommendations"],
    buttonText: "Submit Project",
    href: "/project",
  },
  {
    icon: (
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
    ),
    title: "I'm a Freelancer",
    description: "Are you a skilled freelancer? Join our platform to discover exciting projects that match your expertise and grow your career.",
    features: ["Get feedback for your CV", "Connect with clients", "Apply for projects"],
    buttonText: "Join as Freelancer",
    href: "/freelancer",
  },
  {
    icon: (
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
          strokeWidth="2"
          d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0v-4a2 2 0 012-2h6a2 2 0 012 2v4m-6 0h-2"
        ></path>
      </svg>
    ),
    title: "Register as a Service Provider",
    description: "Offer your company's services to a wide range of projects. Register your agency to get matched with clients.",
    features: ["Showcase your portfolio", "Connect with project owners", "Bid on high-value projects"],
    buttonText: "Register as Provider",
    href: "/company-registration",
    className: "md:col-span-2 lg:col-span-1",
  },
];


export default function HomePage() {
  return (
    <main className="main-container flex-1 flex flex-col items-center justify-start p-3 md:p-4 xl:p-6 relative overflow-hidden min-h-screen">
      {/* Background overlays */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-100/80 via-orange-100/60 to-amber-200/80"></div>
      <div className="absolute inset-0 bg-gradient-to-t from-orange-200/30 via-transparent to-amber-100/20"></div>
      <div className="absolute inset-0 opacity-40">
        <div className="absolute inset-0 bg-gradient-to-r from-amber-900/5 via-transparent to-amber-900/5 transform rotate-45"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-orange-800/3 via-transparent to-orange-800/3 transform -rotate-45"></div>
      </div>

      <div className="w-full max-w-6xl relative z-10 pt-4 lg:pt-8 xl:pt-12">
        <HeroSection
          title="Expert Sourcing Platform"
          subtitle="Connect projects with skilled freelancers through our AI-powered matching system. Choose your path below to get started."
        />

        {/* Mobile Decorative Element */}
        <div className="lg:hidden mb-8">
          <div className="flex justify-center items-center space-x-4">
            <div className="w-3 h-3 bg-gradient-to-r from-amber-400 to-orange-400 rounded-full animate-pulse"></div>
            <div className="w-16 h-0.5 bg-gradient-to-r from-amber-400 via-orange-400 to-amber-400 rounded-full"></div>
            <div className="w-3 h-3 bg-gradient-to-r from-orange-400 to-amber-400 rounded-full animate-pulse delay-500"></div>
          </div>
        </div>

        <FeatureGallery />

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
          {cardData.map((data, index) => (
            <CallToActionCard key={index} {...data} />
          ))}
        </div>

        {/* Enhanced footer section */}
        <div className="text-center mt-8 lg:mt-10 xl:mt-12">
          <div className="flex justify-center mb-3 lg:mb-4">
            <div className="w-16 h-0.5 bg-gradient-to-r from-transparent via-amber-400 to-transparent rounded-full opacity-60"></div>
          </div>
          <p className="text-sm lg:text-base text-black font-medium">
            Note: This is just a demo page showcasing agentic workflows with OpenAI Agents SDK
          </p>
        </div>
      </div>
    </main>
  );
}
