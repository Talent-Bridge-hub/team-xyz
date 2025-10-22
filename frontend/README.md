# UtopiaHire Frontend

React + TypeScript + Vite frontend for the UtopiaHire platform.

## Setup

### Install Dependencies
```bash
npm install
```

### Start Development Server
```bash
npm run dev
```

The frontend will be available at http://localhost:5173

## Features

✅ Authentication (Login/Register)
✅ Protected Routes
✅ Dashboard Layout
✅ Responsive Design
✅ TailwindCSS Styling
✅ Axios API Client with Interceptors

## Modules

- 🏠 **Dashboard** - Overview and quick actions
- 📄 **Resume** - Upload and analyze resumes (Coming Soon)
- 💼 **Jobs** - Search and match jobs (Coming Soon)
- 💬 **Interview** - Practice interviews (Coming Soon)
- 🔍 **Footprint** - Analyze digital presence (Coming Soon)

## API Configuration

Backend API URL is configured in `.env`:
```
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## Build for Production

```bash
npm run build
```

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Router** - Routing
- **Axios** - HTTP client
- **TailwindCSS** - Styling
