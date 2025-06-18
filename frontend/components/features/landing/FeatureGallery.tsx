import Image from 'next/image';

const galleryItems = [
    { src: '/office1.png', alt: 'Modern office workspace 1', marginTop: false },
    { src: '/office2.png', alt: 'Modern office workspace 2', marginTop: true },
    { src: '/office3.png', alt: 'Modern office workspace 3', marginTop: false },
    { src: '/office4.png', alt: 'Modern office workspace 4', marginTop: true },
];

const FeatureGallery = () => {
    return (
        <div className="office-gallery hidden lg:block mb-8 xl:mb-12 2xl:mb-16">
            <div className="grid grid-cols-4 gap-4 xl:gap-6 max-w-3xl xl:max-w-4xl mx-auto">
                {galleryItems.map((item, index) => (
                    <div
                        key={index}
                        className={`group relative overflow-hidden rounded-2xl shadow-2xl hover:shadow-3xl transition-all duration-500 transform hover:scale-105 w-40 h-40 xl:w-52 xl:h-52 ${item.marginTop ? 'mt-6 xl:mt-8' : ''
                            }`}
                    >
                        <div className="absolute inset-0 bg-gradient-to-t from-amber-900/40 via-transparent to-transparent z-10"></div>
                        <Image
                            src={item.src}
                            alt={item.alt}
                            width={208}
                            height={208}
                            className="w-full h-full object-cover object-center transition-transform duration-700 group-hover:scale-110"
                            priority={index === 0}
                        />
                        <div className="absolute inset-0 bg-amber-200/10 group-hover:bg-transparent transition-colors duration-300"></div>
                    </div>
                ))}
            </div>
            <div className="flex justify-center mt-6 xl:mt-8">
                <div className="w-40 h-1 bg-gradient-to-r from-transparent via-amber-400 to-transparent rounded-full opacity-60"></div>
            </div>
        </div>
    );
};

export default FeatureGallery;
