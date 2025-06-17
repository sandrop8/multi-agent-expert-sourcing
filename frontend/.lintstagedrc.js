module.exports = {
    // TypeScript and JavaScript files
    '*.{ts,tsx,js,jsx}': [
        'eslint --fix',
        'prettier --write',
        // Run tests related to staged files
        () => 'bun run test --passWithNoTests --findRelatedTests --bail',
    ],

    // JSON files
    '*.json': ['prettier --write'],

    // Markdown files
    '*.md': ['prettier --write'],

    // CSS files
    '*.{css,scss}': ['prettier --write'],

    // Run type checking on all TypeScript files when any TS file changes
    '*.{ts,tsx}': () => 'tsc --noEmit',
};
