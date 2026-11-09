import parser from '@typescript-eslint/parser';
import stylex from '@stylexjs/eslint-plugin';

export default [{
  files: ['src/**/*.{ts,tsx}'],
  languageOptions: { parser, parserOptions: { ecmaFeatures: { jsx: true } } },
  plugins: { '@stylexjs': stylex },
  rules: { '@stylexjs/valid-styles': 'error', '@stylexjs/no-unused': 'error' },
}];
