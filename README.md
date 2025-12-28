![Django](https://img.shields.io/badge/Django-Backend-green)
![Render](https://img.shields.io/badge/Deployed-Render-blue)
![Status](https://img.shields.io/badge/Status-Live-success)

# 🌾 Farmplace – Farmer to Consumer Marketplace

Farmplace is a full-stack web application that connects farmers directly with consumers, enabling transparent product listing, order management, and role-based dashboards. The platform removes middlemen and ensures fair pricing.

🔗 **Live Demo:**  
https://farmplace-lcm5.onrender.com

---

## 🚀 Features

### 👨‍🌾 Farmer Module
- Farmer registration & login
- Product listing and management
- View consumer orders
- Order status updates
- Farmer dashboard with order insights

### 🛒 Consumer Module
- Consumer registration & login
- Browse farmers and products
- Place orders directly from farmers
- View order history and order status

### 📦 Order Management
- Farmer–consumer order flow
- Order tracking system

### 🔐 Authentication
- Custom user model
- Role-based login
- Protected routes

---

## 🛠️ Tech Stack

**Frontend**
- HTML
- CSS
- Bootstrap
- JavaScript

**Backend**
- Python
- Django

**Database**
- SQLite

**Deployment**
- Render
- Gunicorn
- WhiteNoise

---

## 🧱 Project Structure

farmplace/
├── accounts/
├── farmers/
├── consumers/
├── orders/
├── templates/
├── static/
├── media/
├── Farmplace/
├── manage.py
└── requirements.txt

---

## ⚙️ Run Locally

```bash
git clone https://github.com/kaushik-ryn/farmplace.git
cd farmplace
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

👨‍💻 Author

Kaushik Roy
Full Stack Django Developer

GitHub: https://github.com/kaushik-ryn
