/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        indigoPrimary: '#4F46E5',
        indigoDark: '#3730A3',
        violetAI: '#7C3AED',
        violetSecondary: '#8B5CF6',
        softIndigo: '#EEF2FF',
        softViolet: '#F5F3FF',
        appBg: '#F8F9FC',
        appSurface: '#FFFFFF',
        appText: '#111827',
        appTextSub: '#6B7280',
        appBorder: '#E5E7EB',
        brand: {
          50: '#eef2ff',
          100: '#e0e7ff',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
        ai: {
          50: '#f5f3ff',
          100: '#ede9fe',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
        },
        slate: {
          850: '#111827',
          900: '#0f172a',
          950: '#0b0b14',
        },
        score: {
          excellent: '#059669',
          good: '#10B981',
          warning: '#D97706',
          error: '#DC2626'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
