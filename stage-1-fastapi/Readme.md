# 🚀 TITLE: Build & Deploy a Personal API
## 📌 Overview



## 📌 Project Overview
This project focuses on deploying simple FastAPI service built and deployed on AWS Linux server.

It shows how a basic API can be run behind Nginx, served through a reverse proxy, and kept running as a background service. The goal is to demonstrate how an application is actually deployed and managed in a real environment, not just how it is written.


## ⚙️ Tech Stack

- **Backend:** FastAPI (Python)
- **Server:** AWS Linux (Ubuntu) 
- **Web Server:** Nginx (Reverse Proxy)
- **Process Manager:** systemd
- **ASGI Server:** Uvicorn


## 📍 API Endpoints

### 1. GET `/`

`Returns API status`

```json
{
  "message": "API is running"
}
```
### 2. GET /health

`Health check endpoint`

{
  "message": "healthy"
}
3. GET /me

Returns developer information
```JSON

{
  "Name": "Oluwatobiloba Reuben Adeje",
  "Email": "oluwatobilobaadeje59@gmail.com",
  "GitHub": "https://github.com/Tobilee10/hng-internship-journey"
}
```

## 🖥️ Running Locally

### 1. Clone the repository

    git clone https://github.com/Tobilee10/hng-internship-journey/stage-1-fastapi

```
cd stage-1-fastapi
```

### 2. Create virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Run the application

    uvicorn app.main:app --reload
    
### 5. Access locally
http://127.0.0.1:8000



## 🌐 Deployment Architecture

```
Client Request
      ↓
   Nginx (Port 80)
      ↓
FastAPI App (127.0.0.1:8000)
```
- [x] FastAPI runs on a private port (8000)
- [x] Nginx handles public traffic (port 80)
- [x] Reverse proxy ensures security and scalability

## 🔁 Nginx Configuration

```
server {
    listen 80;
    server_name rubi-hng-internship.duckdns.org;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```
![]()

## ⚡ Process Management (systemd)

The application runs as a background service using systemd:
```json
[Unit]
Description=FastAPI App
After=network.target

[Service]
User=hngdevops
WorkingDirectory=/home/hngdevops/fastapi-stage1
ExecStart=/home/hngdevops/fastapi-stage1/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 
Restart=always

[Install]
WantedBy=multi-user.target
```
![]()


✅ Requirements Compliance

-  Returns JSON responses (Content-Type: application/json)
- All endpoints return HTTP 200
- Response time under 500ms
- Runs on private port behind Nginx
- Persistent service using systemd
- Public GitHub repository

## 🧪 Testing

- [x] curl http://rubi-hng-internship.duckdns.org/
![]()
- [x] curl http://rubi-hng-internship.duckdns.org/health
![]()
- [x] curl http://rubi-hng-internship.duckdns.org/me
![]()