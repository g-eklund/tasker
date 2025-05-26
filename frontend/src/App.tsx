import React from 'react';
import { ChakraProvider, createSystem, defaultConfig, defineConfig } from '@chakra-ui/react';
import HouseHuntGame from './components/HouseHuntGame';

// Kid-friendly theme with bright, fun colors
const customConfig = defineConfig({
  theme: {
    tokens: {
      colors: {
        primary: {
          50: { value: '#f0e6ff' },
          100: { value: '#d4b3ff' },
          200: { value: '#b880ff' },
          300: { value: '#9c4dff' },
          400: { value: '#801aff' },
          500: { value: '#6600e6' },
          600: { value: '#5000b4' },
          700: { value: '#3a0082' },
          800: { value: '#240050' },
          900: { value: '#0e001f' },
        },
        secondary: {
          50: { value: '#e6f0ff' },
          100: { value: '#b3d4ff' },
          200: { value: '#80b8ff' },
          300: { value: '#4d9cff' },
          400: { value: '#1a80ff' },
          500: { value: '#0066e6' },
          600: { value: '#0050b4' },
          700: { value: '#003a82' },
          800: { value: '#002450' },
          900: { value: '#000e1f' },
        },
        accent: {
          50: { value: '#fff5e6' },
          100: { value: '#ffe0b3' },
          200: { value: '#ffcb80' },
          300: { value: '#ffb64d' },
          400: { value: '#ffa11a' },
          500: { value: '#e68c00' },
          600: { value: '#b46d00' },
          700: { value: '#824e00' },
          800: { value: '#502f00' },
          900: { value: '#1f1000' },
        },
        background: { value: '#f0f8ff' },
      },
      fonts: {
        heading: { value: '"Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' },
        body: { value: '"Inter", "SF Pro Text", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' },
      },
    },
  },
});

// Create the system by merging with default config
const system = createSystem(defaultConfig, customConfig);

function App() {
  return (
    <ChakraProvider value={system}>
      <HouseHuntGame />
    </ChakraProvider>
  );
}

export default App;
