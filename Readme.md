
# TITLE: **Hardened Linux Server Deployment**


### 🌐 Live Deployment: https://rubi-hng-internship.duckdns.org
### 🔗 Live Deployment: https://rubi-hng-internship.duckdns.org/api
### 👤 HNG Username: Rubi

### Role: DevOps Engineer (HNG Internship Training Project)
### Environment: Linux (Ubuntu Server) 
### Focus: Server Hardening | Web Server Configuration | SSL | Networking | DNS

## 📌 Project Overview
This project focuses on deploying and securing a production-ready Linux server using cloud AWS cloud infrastructure. The objective is to implement industry-standard security practices, including secure shell configuration, firewall enforcement, Nginx web server deployment to serve static HTML page, JSON API endpoint (/api) and HTTPS encryption using Let’s Encrypt.

## Project Architecture
```
Internet
   │
   ▼
DuckDNS Domain
   │
   ▼
Nginx
   ├── / → Static HTML Page
   └── /api → JSON API Response
   │
   ▼
UFW Firewall (Ports: 22, 80, 443)
   │
   ▼
Hardened Ubuntu Server (SSH Key Auth Only)
```
## 🛠️ Technologies Used

- [x] AWS EC2 Instance 
- [x] Nginx
- [x] UFW (Firewall)
- [x] OpenSSH
- [x] DNS Configuration (Duck DNS)
- [x] Certbot (Let’s Encrypt SSL)

## 🏗️ Infrastructure Setup (AWS)
✅ Created an EC2 Instance: 

- AMI: Ubuntu Server 
- Instance type: t2.micro (free tier)
- Key pair: create/download .pem
  

✅ Created Security Group Allowing Ingress Traffic:

- SSH (22) --> My IP only
- HTTP (80) --> anywhere
- HTTPS (443) --> anywhere

**NB**  `Deny everything else (default)`

## A. **Connect to the Server via SSH**

`Locate the downloaded ssh private key on your device`

    ssh -i key-pair -p 22 ubuntu@IP-address
![](../task-0/images/ssh-login-ubuntu.png)

## B. **User Management & Privileges**

### Create user named: hngdevops

    sudo useradd -m  hngdevops

    verify cat /etc/passwd
![](../task-0/images/useradd-hngdevops.png)
![](../task-0/images/hngdevops-verify.png)

### Granting Limited sudo Access to `hngdevops user`
```
sudo visudo

hngdevops ALL=(ALL) NOPASSWD:ALL
```
![](../task-0/images/visudo.png)

### SSH key for hngdevops user --> Allows hngdevops to ssh into the server

```
sudo mkdir /home/hngdevops/.ssh
sudo cp ~/.ssh/authorized_keys /home/hngdevops/.ssh/ 
sudo chown -R hngdevops:hngdevops /home/hngdevops/.ssh 
sudo chmod 700 /home/hngdevops/.ssh 
sudo chmod 600 /home/hngdevops/.ssh/authorized_keys 
```  
![](../task-0/images/ssh-keys.png)

- [x] copys the authorised_keys from ubuntu user to hngdevops user.
- [x] changing ownership and group of .ssh to hngdevops.
- [x] Grant owner rwx permissions
- [x] Grant owner rw permissions only.




### 🔐 SSH Security Hardening

    sudo nano /etc/ssh/sshd_config

![](../task-0/images/ssh-security.png)

- [x] Disabled root login: `PermitRootLogin no`
- [x] Disabled password authentication:`PasswordAuthentication no`
- [x] Enabled SSH key-based authentication only: `PubkeyAuthentication yes`

### ***Restart SSH:***

    sudo systemctl reload ssh
![](../task-0/images/ssh-reload.png)

## ⚠️ **DO NOT LOG OUT until you confirm new user is successfully loggedin:**

    ssh -i your-key.pem hngdevops@your-ip

![](../task-0/images/hng-devops-login.png)

## 🔥 C. Firewall Configuration on hngdevops User (UFW)

    sudo ufw status verbose
![](../task-0/images/ufw-inactive.png)

    sudo ufw enable
![](../task-0/images/ufw-enabled.png)

```
sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

sudo ufw status verbose
```
![](../task-0/images/incoming-traffic.png)

## 🌐 D. **Web Sever Configuration (Nginx) on hngdevops User**

sudo apt update
sudo apt install nginx -y
sudo systemctl status nginx

![](../task-0/images/nginx-status.png)

### ✅ **Static Page**
```
sudo nano /var/www/html/index.html

<!DOCTYPE html>
<html>
<head>
    <title>HNG14 Stage 0</title>
</head>
<body>
    <h1>Rubi</h1>
</body>
</html>
```
![](../task-0/images/index.html.png)
### ✅ **Configure Nginx Routes**

`sudo nano /etc/nginx/sites-available/hngdevops`

create a virtual host for your own
```
server {
    listen 80;
    server_name _;

    root /var/www/html;
    index index.html;

    # Route: GET /
    location / {
        try_files $uri $uri/ =404;
    }

    # Route: GET /api
    location /api {
        default_type application/json;
        return 200 '{
            "message": "HNGI14 Stage 1",
            "track": "DevOps",
            "username": "your-hng-username"
        }';
    }
} 
```
![](../task-0/images/server-config.png)
### Available Config
![](../task-0/images/site-available.png)

### `Enable config:`

    sudo ln -s /etc/nginx/sites-available/hngdevops /etc/nginx/sites-enabled/
![](../task-0/images/site-enable.png)

### Test Configuration

    sudo nginx -t

    sudo systemctl reload nginx

![](../task-0/images/test-config.png)

## 🌍 E. Domain Setup

Get Free domain from:

https://www.duckdns.org/

Point DNS:  rubi-hng-internship.duckdns.org updated to 3.92.57.126

A Record → your EC2 public IP
![](../task-0/images/dns.png)

## 🔒 E. SSL

    sudo apt install certbot python3-certbot-nginx -y
![](../task-0/images/install-certbot.png)

    sudo certbot --nginx -d rubi-hng-internship.duckdns.org
![](../task-0/images/ssl-certificate-issued.png)

## 🧪 F. Testing Deployment

Test endpoints:
curl http://rubi-hng-internship.duckdns.org

➡️ Should redirect to HTTPS (301)
![](../task-0/images/301.png)
![](../task-0/images/301-browser.png)

curl -I https://rubi-hng-internship.duckdns.org

➡️ Should return:

HTTP/1.1 200 OK

![](../task-0/images/200.png)

curl https://rubi-hng-internship.duckdns.org/api

➡️ MUST return EXACT JSON:

{"status":"success","message":"API working","username":"YOUR_HNG_USERNAME"}
![](../task-0/images/Screenshot%20from%202026-04-14%2013-09-36.png)
![](../task-0/images/Screenshot%20from%202026-04-14%2013-10-12.png)


## Issue Faced: misconfig, and errors



## 🧠 What I Learned

- [x] Deployed a live Linux Server Administration
- [x] SSH Hardening & Key-Based Authentication
- [x] Firewall Configuration (UFW)
- [x] Web Server Management (Nginx)
- [x] Reverse Proxy & Routing
- [x] REST API Deployment
- [x] SSL/TLS Certificate Management (Let’s Encrypt / Certbot)
- [x] Production-grade system security practices







