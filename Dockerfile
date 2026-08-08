FROM node:22-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci || npm install
COPY frontend ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
COPY --from=frontend-build /app/frontend/dist ./frontend/dist
ENV PORT=8080
EXPOSE 8080
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT"]
