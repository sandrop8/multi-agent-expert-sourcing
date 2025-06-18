import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import Link from 'next/link';
import React from 'react';

interface CallToActionCardProps {
    icon: React.ReactNode;
    title: string;
    description: string;
    features: string[];
    buttonText: string;
    href: string;
    className?: string;
}

const CallToActionCard: React.FC<CallToActionCardProps> = ({
    icon,
    title,
    description,
    features,
    buttonText,
    href,
    className = '',
}) => {
    return (
        <Card
            className={`p-6 lg:p-8 shadow-2xl bg-white/95 backdrop-blur-sm border-0 hover:shadow-3xl hover:bg-white transition-all duration-500 h-full transform hover:-translate-y-2 ${className}`}
        >
            <div className="text-center space-y-4 lg:space-y-6 flex flex-col h-full">
                <div className="w-20 h-20 mx-auto bg-gradient-to-br from-green-100 to-green-200 rounded-2xl flex items-center justify-center shadow-lg">
                    {icon}
                </div>

                <div>
                    <h2 className="text-2xl font-semibold text-black mb-2">{title}</h2>
                    <p className="text-black mb-6">{description}</p>
                </div>

                <div className="space-y-3 flex-grow">
                    <ul className="text-sm text-black space-y-2">
                        {features.map((feature, index) => (
                            <li key={index} className="flex items-center justify-center space-x-2">
                                <span className="w-1.5 h-1.5 bg-amber-400 rounded-full"></span>
                                <span>{feature}</span>
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="mt-auto">
                    <Link href={href} className="block">
                        <Button size="lg" className="w-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105">
                            {buttonText}
                        </Button>
                    </Link>
                </div>
            </div>
        </Card>
    );
};

export default CallToActionCard;
