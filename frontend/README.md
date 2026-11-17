
# EthioExplore – Frontend

EthioExplore is a web-based Ethiopian travel platform that helps users 
discover destinations, explore travel information, make bookings, manage 
payments through a demo simulation, and share destination reviews.

The frontend is built with React and Vite and communicates with a Django 
REST Framework backend.

## Features

- Browse and explore Ethiopian travel destinations.
- Search, filter, and sort destinations.
- View detailed destination information.
- Register, log in, and manage user profiles.
- Book trips and manage bookings.
- Save and manage favorite destinations.
- Submit, edit, and manage destination reviews.
- Simulate booking payments for demonstration purposes.

## Technologies

- React 19
- Vite
- Tailwind CSS 4
- JavaScript
- Oxlint
- Django REST Framework API

## Requirements

- Node.js
- npm
- A running EthioExplore backend

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Navigate to the frontend

```bash
cd ethiopian-travel-platform/frontend
```

### 3. Install dependencies

```bash
npm install
```

### 4. Start the development server

```bash
npm run dev
```

Open the local URL displayed in your terminal.

## Available Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start the development server |
| `npm run build` | Create a production build |
| `npm run preview` | Preview the production build |
| `npm run lint` | Check code quality |

## Backend Integration

The frontend communicates with the Django REST Framework backend running 
at:

`http://127.0.0.1:8000`

Make sure the backend server and PostgreSQL database are running before 
using features that require API access.

## Production Build

Create an optimized production build:

```bash
npm run build
```

The generated files are placed in the `dist/` directory.

## Project Status

EthioExplore is a portfolio project demonstrating frontend development, 
REST API integration, authentication, and travel-platform functionality.

