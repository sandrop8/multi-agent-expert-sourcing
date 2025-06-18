import React from 'react';

interface HeroSectionProps {
    title: string;
    subtitle: string;
}

const HeroSection: React.FC<HeroSectionProps> = ({ title, subtitle }) => {
    return (
        <div className="header-section text-center mb-6 lg:mb-8 xl:mb-12">
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-5xl xl:text-6xl font-bold text-black mb-3 lg:mb-4 xl:mb-6 drop-shadow-sm">
                {title}
            </h1>
            <p className="text-base md:text-lg xl:text-xl text-black max-w-3xl mx-auto leading-relaxed font-medium">
                {subtitle}
            </p>
        </div>
    );
};

export default HeroSection;
