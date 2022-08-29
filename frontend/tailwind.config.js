module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    screens: {
      'sm': '640px',
      // => @media (min-width: 640px) { ... }

      'md': '768px',
      // => @media (min-width: 768px) { ... }

      'lg': '1024px',
      // => @media (min-width: 1024px) { ... }

      'xl': '1280px',
      // => @media (min-width: 1280px) { ... }

      '2xl': '1537px',
      // => @media (min-width: 1536px) { ... }
    },
    extend: {
      boxShadow: {
        'xl':	'0 2px 35px 0px rgb(0 0 0 / 0.1)',
        'input': '0 0px 0px 2px rgb(56 189 248 / 0.4)',
        'input-active': '0 0 0 5px rgb(56 189 248 / .4)',
        'btn-primary-focus': '0 0 0 4px rgb(14 165 233 / .4)',
        'btn-warning-focus': '0 0 0 4px rgb(251 191 36 / .4)',
        'btn-danger-focus': '0 0 0 4px rgb(248 113 113 / .4)',
        'btn-focus': '0 0 0 4px rgb(255 255 255 / .4)',
        'btn-white-focus': '0 0 0 4px rgb(0 0 0 / .2)',
        'btn-success-focus': '0 0 0 4px rgb(0 255 0 / .4)',
      },
      
      width: {
        '64%': '64%',
      },

      colors: {
        'custom-blue': '#1EBAEB'
      }
    },
    
  },
  plugins: [],
}
