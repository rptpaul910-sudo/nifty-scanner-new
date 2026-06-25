# Nifty50 Scanner v2

Real-time Nifty50 market scanner using Yahoo Finance.

## Stack
- **Backend**: Flask + yfinance (Python)
- **Frontend**: React (Create React App)
- **Data**: Yahoo Finance — free, no API key needed

## Deploy on Railway

### Backend service
1. New service → Empty service → connect repo → set **Root Directory = `backend`**
2. No environment variables needed
3. Railway auto-detects Python and runs `gunicorn` via Procfile

### Frontend service
1. New service → Empty service → connect repo → set **Root Directory = `frontend`**
2. Add environment variable:
   ```
   REACT_APP_API_URL=https://YOUR-BACKEND-URL.up.railway.app
   ```
   (copy this from the backend service's generated domain — must start with https://)
3. Redeploy after setting the variable

## Local development
```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py

# Frontend (separate terminal)
cd frontend
npm install
REACT_APP_API_URL=http://localhost:5000 npm start
```
