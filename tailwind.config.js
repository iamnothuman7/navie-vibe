/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./core/templates/**/*.html",
    "./hoteis/templates/**/*.html"
  ],
  theme: {
    extend: {
      colors: {
        'action-blue': '#2563eb',
        'action-blue-dark': '#1d4ed8'
      },
      fontFamily: {
        'sans': ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
