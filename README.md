# EthioExplore – Ethiopian Travel Platform

EthioExplore is a web-based Ethiopian travel platform that helps users discover destinations, explore travel information, make bookings, manage payments through a demo simulation, and share destination reviews.

It consists of a Django REST Framework backend and a React + Vite frontend.

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

- Django 5 + Django REST Framework
- PostgreSQL
- React 19 + Vite
- Tailwind CSS 4
- JavaScript
- Oxlint

## Backend Setup

### Requirements

- Python 3.12+
- PostgreSQL

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements-dev.txt
```

Use `requirements.txt` instead if you do not need development tools such as the Django Debug Toolbar.

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

At minimum set `DJANGO_SECRET_KEY`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD`.

### 4. Run migrations and start the server

```bash
python manage.py migrate
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000` and the API documentation at `http://127.0.0.1:8000/api/docs/`.

### 5. Run the tests

```bash
python manage.py test
```

## Frontend Setup

### Requirements

- Node.js
- npm
- A running EthioExplore backend

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

### 4. Configure the API URL

```bash
cp .env.example .env
```

Set `VITE_API_BASE_URL` if the backend runs somewhere other than `http://127.0.0.1:8000`.

### 5. Start the development server

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

The frontend communicates with the Django REST Framework backend running at:

`http://127.0.0.1:8000`

Make sure the backend server and PostgreSQL database are running before using features that require API access.

## Production Build

Create an optimized production build:

```bash
npm run build
```

The generated files are placed in the `dist/` directory.

## Docker

Run PostgreSQL, the Django backend, and the frontend with Docker Compose:

```bash
docker compose up --build
```

- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:8000`
- API documentation: `http://localhost:8000/api/docs/`

The Compose stack uses development settings and keeps database and media files in named volumes.

## Continuous Integration

GitHub Actions runs the backend test suite against PostgreSQL and the frontend lint/build on pushes to `main` and on pull requests. See `.github/workflows/ci.yml`.

## Troubleshooting

If the frontend cannot load destinations, check that the backend is reachable:

```bash
curl http://127.0.0.1:8000/api/destinations/
```

If that fails, restart the dev server:

```bash
pkill -f "manage.py runserver"
python manage.py runserver
```

If `runserver` hangs and never starts listening, run it without the autoreloader:

```bash
python manage.py runserver --noreload
```

## Project Status

EthioExplore is a portfolio project demonstrating frontend development, REST API integration, authentication, and travel-platform functionality.
