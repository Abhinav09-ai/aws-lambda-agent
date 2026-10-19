/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        'aws-orange': '#FF9900',
        'aws-blue': '#232F3E',
        'aws-dark': '#0D1117',
        'aws-surface': '#161B22',
        'aws-border': '#30363D',
        'aws-text': '#C9D1D9',
        'aws-muted': '#8B949E',
        'success': '#3FB950',
        'warning': '#D29922',
        'danger': '#F85149',
      },
    },
  },
  plugins: [],
}
