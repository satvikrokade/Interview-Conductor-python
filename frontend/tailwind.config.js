/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        aurora1: "#6366f1",
        aurora2: "#8b5cf6",
        aurora3: "#06b6d4",
        auroraBg: "#0f0f17",
      },
      backgroundImage: {
        aurora: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%)",
      }
    }
  },
  plugins: [],
};
