# --- שלב 1: בניית ה-Frontend (React) ---
FROM node:22-alpine AS build-stage
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# --- שלב 2: סביבת ה-Python ---
FROM python:3.11-slim
WORKDIR /app

# התקנת תלויות פייתון
COPY backend/requirements.txt .
RUN pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

# העתקת קוד ה-Backend
COPY backend/ .

# העתקת הקבצים הבנויים של הריאקט לתוך תיקייה שה-FastAPI יוכל להגיש (אופציונלי)
COPY --from=build-stage /app/frontend/dist ./static

# הערה: אנחנו נשתמש בקובץ הזה עבור שני השירותים (producer ו-consumer)