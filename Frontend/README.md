npx create-react-app login-app --template typescript
cd login-app
-npm install react-router-dom
-npm install axios redux react-redux @reduxjs/toolkit
-npm install tailwindcss @tailwindcss/vite
-npm install -D @vitejs/plugin-react
-npm install -D @types/node

#Create folder
mkdir .\src\app
mkdir .\src\components
mkdir .\src\features
mkdir .\src\hooks
mkdir .\src\pages

# Routing & HTTP client

npm install react-router-dom axios

# State management

npm install redux react-redux @reduxjs/toolkit

# Styling

npm install tailwindcss @tailwindcss/vite

# React plugin for Vite

npm install -D @vitejs/plugin-react

# Node.js type definitions

npm install -D @types/node

# Create Folder Structure

mkdir src/app
mkdir src/components
mkdir src/features
mkdir src/hooks
mkdir src/pages

# Project Structure

src/
├── app/ # Redux store configuration
├── components/ # Reusable UI components
├── features/ # Redux slices and feature logic
├── hooks/ # Custom React hooks
├── pages/ # Page-level components
└── index.tsx # Application entry point
