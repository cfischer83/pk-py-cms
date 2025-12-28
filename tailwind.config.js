/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e6f7f8',
          100: '#cceff1',
          200: '#99dfe3',
          300: '#66cfd5',
          400: '#33bfc7',
          500: '#008c95',  /* Main primary color */
          600: '#007a82',
          700: '#00686e',
          800: '#00565b',
          900: '#004448',
          950: '#002324',
        },
        secondary: {
          50: '#f8f9fa',
          100: '#e9ecef',
          200: '#dee2e6',
          300: '#ced4da',
          400: '#adb5bd',
          500: '#6c757d',
          600: '#495057',
          700: '#343a40',
          800: '#212529',
          900: '#191c1f',
        },
        accent: {
          50: '#fef3e6',
          100: '#fde7cc',
          200: '#fbcf99',
          300: '#f9b766',
          400: '#f79f33',
          500: '#f58700',
          600: '#c46c00',
          700: '#935100',
          800: '#623600',
          900: '#311b00',
        }
      }
    }
  },
  plugins: [],
}
