# 🗞️ Newsletter Curator

A Django-powered application that automatically curates, compiles, and sends weekly/daily newsletters to subscribers. Built with PostgreSQL, Celery-ready architecture, and Pandas-powered article transformation.

> ⚙️ Live automation-ready | ✉️ Email delivery system | 📊 Analytics Dashboard | 📰 Public Archive

---

## 📌 Features

- 🔄 **Automatic Newsletter Delivery** (Daily/Weekly)
- 📬 **Subscription Management** (with frequency preference)
- 🧹 **Article Scraping + Cleaning** (via Pandas)
- 📊 **Admin Analytics Dashboard**
- 💌 **Email Sending via SMTP (Gmail)**
- 🗃️ **Public Newsletter Archive**
- 🧠 Celery-ready for background automation (future integration)

---

## 🛠️ Tech Stack

| Layer            | Tech                                |
|------------------|-------------------------------------|
| Backend          | Django, Python                      |
| Database         | PostgreSQL (via Railway)            |
| Email System     | Django Email (SMTP - Gmail)         |
| Scheduling       | django-cron (Celery-ready)          |
| Data Processing  | Pandas                              |
| Templates        | Django Templates (Bootstrap-ready)  |
| Deployment       | Local/Cloud/Render/Railway-ready    |

---

## 🚀 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/newsletter-curator.git
cd newsletter-curator
````

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate    # On Windows
# source venv/bin/activate  # On Unix/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env` or environment variables

Set these in your shell or `.env` file:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=True
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## 🧪 Usage Overview

### ➕ Subscribe

* Visit `/` (homepage)
* Enter email and select **Daily** or **Weekly**
* Confirm subscription

### 📰 Send Newsletters Manually

```bash
python manage.py send_newsletter
```

### 🧠 Schedule via django-cron

```bash
python manage.py runcrons
```

Schedules:

* Daily: `DailyNewsletterCronJob`
* Weekly: `WeeklyNewsletterCronJob`

📝 Add to CRON scheduler or replace with Celery in production.

### 📊 Admin Analytics Dashboard

* Visit `/dashboard/analytics/` (requires admin login)
* View:

  * Total Subscribers
  * Frequency Breakdown
  * (Optionally) Top Categories

---

## 📂 Folder Structure

```
newsletter_curator/
├── backend/                 # Django project config
├── newsletter/              # Core app: models, views, etc.
│   ├── templates/newsletter/
│   │   ├── index.html
│   │   ├── newsletter_detail.html
│   │   └── admin_dashboard.html
│   └── cron.py              # Scheduled newsletter logic
├── manage.py
└── requirements.txt
```

---

## 🔮 Improvements to be done

* ✅ Celery Integration with Redis
* ✅ Advanced Click/Open Tracking
* ✅ HTML Email Templates (Branded)
* ✅ User Preferences by Category
* ✅ Web Scraper / API News Puller

---

## 👤 Author

**Aryav Bhandary**
📊 Data Enthusiast | 🧠 Building automation with purpose

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).

---


