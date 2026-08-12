# 🛒 LOCAL-it — Grocery Management App

A lightweight **Online-to-Offline (O2O) Grocery Management Platform** designed for neighborhood grocery stores.

LOCAL-it connects customers with local grocery merchants through an online product catalog and **scheduled store counter pickup**, while providing merchants with an administrative dashboard for inventory, orders, billing, alerts, and business analytics.

---

## 📌 Overview

Traditional neighborhood grocery stores often depend on manual inventory records, physical queues, and third-party delivery platforms.

LOCAL-it provides an independent digital solution that allows merchants to:

* Manage products and inventory digitally
* Receive customer reservations online
* Prepare orders before customer arrival
* Manage pickup schedules
* Track low-stock products
* Generate printable invoices
* Monitor sales and estimated profits
* Analyze category-wise sales
* Manage customers and orders from a centralized dashboard

Instead of relying on expensive delivery logistics, LOCAL-it follows a **scheduled counter-pickup model**, helping local merchants reduce operational complexity and third-party commission dependency.

---

## ✨ Features

### 👤 Customer Portal

* Customer registration and login
* Browse grocery products
* Browse products by category
* View product details
* Add products to cart
* Update product quantities
* Real-time stock validation
* Checkout and order reservation
* Select pickup date
* Select pickup time slot
* View order information
* Printable invoice/receipt

### 🏪 Merchant Dashboard

* Secure business/admin login
* Product management
* Inventory management
* Inline stock updates
* Inline price updates
* Order management
* Customer statistics
* Sales statistics
* Low-stock alerts
* Order status management
* Business analytics
* Category-wise sales visualization

### 📊 Analytics

The dashboard provides visual business insights including:

* Total sales
* Estimated net profit
* Transaction count
* Category-wise sales distribution
* Order status distribution
* Historical transaction information

Charts are rendered using **Chart.js** on the client side.

### 🔐 Security

* Role-based access
* Secure authentication
* Password hashing using Werkzeug
* Flask-Login session management
* Protected administrative routes
* Database-backed transactional operations

### 🗄️ Data Integrity

LOCAL-it includes backend-level validation for common grocery-store data problems.

For example, barcode-free products can use database `NULL` values instead of duplicate empty strings, allowing products without factory barcodes to coexist with uniquely identified products.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      Customer        │
                    │      Web Portal      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Flask Backend    │
                    │   Routing & Logic    │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       Authentication      SQLAlchemy       Order / Cart
       Flask-Login           ORM             Processing
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Relational Database │
                    │ SQLite / PostgreSQL  │
                    └──────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Merchant Dashboard │
                    │ Inventory / Orders   │
                    │ Analytics / Alerts   │
                    └──────────┬───────────┘
                               │
                               ▼
                         ┌────────────┐
                         │ Chart.js   │
                         │ Analytics  │
                         └────────────┘
```

---

## 🛠️ Technology Stack

| Technology              | Purpose                     |
| ----------------------- | --------------------------- |
| **Python**              | Backend programming         |
| **Flask**               | Web application framework   |
| **SQLAlchemy**          | Object-Relational Mapping   |
| **SQLite / PostgreSQL** | Relational database         |
| **HTML5**               | Page structure              |
| **CSS3**                | Styling                     |
| **Bootstrap 5**         | Responsive UI               |
| **JavaScript**          | Client-side functionality   |
| **AJAX**                | Asynchronous updates        |
| **Chart.js**            | Business analytics          |
| **Flask-Login**         | Authentication and sessions |
| **Werkzeug**            | Password hashing/security   |
| **Jinja2**              | Server-side templates       |

---

## 📂 Project Structure

```text
local-IT/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── cart.html
│   ├── checkout.html
│   ├── product_detail.html
│   ├── login_customer.html
│   ├── register_customer.html
│   ├── login_business.html
│   └── business_dashboard.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── ...
```

> The exact structure may vary depending on the current implementation.

---

## 🔄 Order Workflow

```text
Customer
   │
   ▼
Browse Products
   │
   ▼
Add to Cart
   │
   ▼
Stock Validation
   │
   ▼
Select Pickup Date & Time
   │
   ▼
Checkout
   │
   ▼
Order Created
   │
   ▼
Merchant Dashboard
   │
   ▼
Pending → Accepted/Packing → Ready
   │
   ▼
Customer Counter Pickup
   │
   ▼
Completed
```

---

## 📦 Inventory Management

The merchant can manage:

* Product name
* Brand
* Barcode
* Wholesale price
* Selling price
* Stock quantity
* Minimum stock level
* Product category

The system monitors inventory after successful transactions and can generate low-stock alerts when the available quantity falls below the configured minimum threshold.

---

## 📈 Business Analytics

The merchant dashboard provides visual representations of business performance.

Example metrics include:

```text
Total Sales
Estimated Profit
Total Transactions
Category Sales
Order Distribution
Low Stock Products
```

Chart.js is used to visualize business data directly in the browser.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/nowhereSOURAV1708/local-IT.git
```

```bash
cd local-IT
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

If the application uses a cloud database, configure the required database connection through an environment variable rather than committing credentials to GitHub.

Example:

```env
DATABASE_URL=your_database_connection_string
SECRET_KEY=your_secret_key
```

**Never commit `.env` files or database credentials to GitHub.**

---

## ▶️ Running the Application

After installing the dependencies:

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

## 🧪 Performance

The project report describes the following observed performance measurements during testing:

| Operation                      | Reported Average |
| ------------------------------ | ---------------: |
| Customer order transaction     |      **14.2 ms** |
| Inline inventory update        |       **8.5 ms** |
| Notification transmission      |      **12.5 ms** |
| Analytics server response      |      **11.4 ms** |
| Local runtime memory footprint |     **< 256 MB** |

These figures are based on the project's reported test environment and should be treated as project-specific measurements rather than universal benchmarks.

---

## 🎯 Project Objectives

The main objectives of LOCAL-it are:

1. Build a lightweight multi-role grocery management platform.
2. Digitize inventory and customer ordering.
3. Reduce physical checkout congestion.
4. Provide scheduled counter pickup instead of delivery logistics.
5. Maintain transactional data integrity.
6. Provide real-time low-stock notifications.
7. Provide merchants with business analytics.
8. Create a low-overhead alternative for neighborhood grocery stores.

---

## 🚀 Future Improvements

Potential future development includes:

* 📱 Progressive Web App (PWA)
* 📶 Offline/local-network support
* 📦 Barcode scanner integration
* 📷 Camera-based barcode scanning
* 🤖 Automated demand forecasting
* 💳 UPI payment reconciliation
* 🏪 Multi-store/multi-tenant support
* ☁️ Database scaling and read replicas
* 🔄 Automated deployment
* 📊 Advanced business intelligence
* 🤖 AI-based product recommendations

---

## 👨‍💻 Developers

### Sourav Sandilya

B.Tech — Computer Science and Design

### Navin Kumar

B.Tech — Computer Science and Design

### Ankit Kumar

B.Tech — Computer Science and Design

**Institution:**
Dr. B. C. Roy Engineering College, Durgapur

**Academic Year:** 2025–2026

---

## 📚 Project Documentation

The complete academic project report contains detailed information about:

* System architecture
* Database schema
* Methodology
* Experimental setup
* Results and discussion
* Database initialization
* Deployment workflow
* Future development

---

## 📄 License

This project was developed as an academic major project.

If you intend to use, modify, or redistribute the project commercially, please contact the authors first.

---

## ⭐ LOCAL-it

**Local grocery. Digital management. Smarter pickup.**
