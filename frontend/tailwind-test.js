const fs = require('fs');

console.log('🔍 Testing Tailwind CSS v4 setup...\n');

// Test PostCSS config
try {
    const postcssConfig = require('./postcss.config.js');
    console.log('✅ PostCSS configuration loaded');
    if (postcssConfig.plugins['@tailwindcss/postcss']) {
        console.log('✅ @tailwindcss/postcss plugin configured');
    } else {
        console.log('❌ @tailwindcss/postcss plugin not found');
    }
} catch (e) {
    console.log('❌ PostCSS config error:', e.message);
}

// Test globals.css
try {
    const globalsCss = fs.readFileSync('./app/globals.css', 'utf8');
    if (globalsCss.includes('@import "tailwindcss"')) {
        console.log('✅ Tailwind CSS v4 import found');
    } else {
        console.log('❌ Tailwind import not found');
    }

    if (globalsCss.includes('@theme')) {
        console.log('✅ Custom theme configuration found');
    }
} catch (e) {
    console.log('❌ globals.css error:', e.message);
}

// Test dependencies
try {
    const pkg = require('./package.json');
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };

    console.log('\n📦 Dependencies:');
    console.log('  - tailwindcss:', deps.tailwindcss || '❌ Not found');
    console.log('  - @tailwindcss/postcss:', deps['@tailwindcss/postcss'] || '❌ Not found');
    console.log('  - postcss:', deps.postcss || '❌ Not found');
    console.log('  - autoprefixer:', deps.autoprefixer || '❌ Not found');
} catch (e) {
    console.log('❌ package.json error:', e.message);
}

console.log('\n🎉 Tailwind CSS v4 test completed!'); 