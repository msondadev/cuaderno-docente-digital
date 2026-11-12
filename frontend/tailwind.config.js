/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        docente: {
          primary: '#1E3A8A',    // Azul Marino
          success: '#10B981',    // Verde Presente
          danger: '#EF4444',     // Rojo Ausente
          warning: '#F59E0B',    // Amarillo Tardanza
        }
      }
    },
  },
  plugins: [],
}
