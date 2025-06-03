"use client";
import Link from "next/link";

export default function TestStylesPage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">
                    🎨 Tailwind CSS v4 Test Page
                </h1>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                    {/* Color Test */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h2 className="text-xl font-semibold text-gray-800 mb-4">Colors</h2>
                        <div className="space-y-2">
                            <div className="bg-blue-500 text-white p-2 rounded">Blue</div>
                            <div className="bg-green-500 text-white p-2 rounded">Green</div>
                            <div className="bg-red-500 text-white p-2 rounded">Red</div>
                            <div className="bg-yellow-500 text-black p-2 rounded">Yellow</div>
                        </div>
                    </div>

                    {/* Spacing Test */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h2 className="text-xl font-semibold text-gray-800 mb-4">Spacing</h2>
                        <div className="space-y-4">
                            <div className="bg-gray-200 p-2 rounded">Padding: p-2</div>
                            <div className="bg-gray-200 p-4 rounded">Padding: p-4</div>
                            <div className="bg-gray-200 p-6 rounded">Padding: p-6</div>
                        </div>
                    </div>

                    {/* Typography Test */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h2 className="text-xl font-semibold text-gray-800 mb-4">Typography</h2>
                        <div className="space-y-2">
                            <p className="text-xs">Extra Small</p>
                            <p className="text-sm">Small</p>
                            <p className="text-base">Base</p>
                            <p className="text-lg">Large</p>
                            <p className="text-xl">Extra Large</p>
                        </div>
                    </div>
                </div>

                {/* Interactive Elements */}
                <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-4">Interactive Elements</h2>
                    <div className="flex flex-wrap gap-4">
                        <button className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded transition-colors">
                            Primary Button
                        </button>
                        <button className="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded transition-colors">
                            Secondary Button
                        </button>
                        <button className="bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-4 rounded transition-colors">
                            Success Button
                        </button>
                        <button className="bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded transition-colors">
                            Danger Button
                        </button>
                    </div>
                </div>

                {/* Responsive Test */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-4">Responsive Design</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                        <div className="bg-indigo-100 p-4 rounded text-center">
                            <div className="text-indigo-800 font-medium">Mobile</div>
                            <div className="text-indigo-600 text-sm">Always visible</div>
                        </div>
                        <div className="bg-purple-100 p-4 rounded text-center hidden sm:block">
                            <div className="text-purple-800 font-medium">Tablet+</div>
                            <div className="text-purple-600 text-sm">sm:block</div>
                        </div>
                        <div className="bg-pink-100 p-4 rounded text-center hidden md:block">
                            <div className="text-pink-800 font-medium">Desktop+</div>
                            <div className="text-pink-600 text-sm">md:block</div>
                        </div>
                        <div className="bg-orange-100 p-4 rounded text-center hidden lg:block">
                            <div className="text-orange-800 font-medium">Large+</div>
                            <div className="text-orange-600 text-sm">lg:block</div>
                        </div>
                    </div>
                </div>

                <div className="mt-8 text-center">
                    <p className="text-gray-600">
                        If you can see proper colors, spacing, and responsive design,
                        <span className="font-semibold text-green-600"> Tailwind CSS is working correctly! ✅</span>
                    </p>
                    <Link
                        href="/"
                        className="inline-block mt-4 bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
                    >
                        ← Back to Chat
                    </Link>
                </div>
            </div>
        </div>
    );
} 