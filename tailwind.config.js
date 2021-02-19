const colors = require('tailwindcss/colors')

module.exports = {
  purge: {
    enabled: process.env.NODE_ENV === "production",
    content: [
      "app/**/*.html"
    ]
  },
  theme: {
    extend: {
      colors: {
        'blue-gray': colors.blueGray,
      },
    },
  },
  variants: {},
  plugins: [],
}
