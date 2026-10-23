# 🔗 LaborConnect
### 🛠️ Connecting Skilled Workers with Opportunities

**LaborConnect** is a web-based labor hiring and service booking platform built using Python and Django. It connects customers with local workers, making it easier to discover services, explore worker profiles, and manage bookings through a centralized platform.

🎯 **Our Mission:** To simplify the process of finding reliable local workers through an accessible, convenient, and location-aware digital platform.

---

## ✨ Key Features

- 🔐 **Authentication & Authorization** — Secure registration, login, and role-based access.
- 👥 **Dual User Interfaces** — Separate dashboards for customers and laborers.
- 🧑‍🔧 **Laborer Profiles** — Manage worker details, skills, pricing, and profile pictures.
- 🛠️ **Service Management** — Add, view, edit, and delete services.
- 📅 **Booking Management** — Create and manage labor booking requests.
- 📍 **Location & Maps** — Support for map integration and worker location discovery.
- 💬 **Communication** — Chat functionality for customers and laborers.
- 🤖 **AI Chatbot** — Chatbot assistance for user queries.
- 🔔 **Notifications** — Booking-related notifications.
- ⭐ **Reviews & Ratings** — Support customer feedback.
- 🌐 **Multilingual Support** — Kannada and English language support.

---

## 🧰 Technology Stack

| Category | Technologies |
|---|---|
| 🖥️ Backend | Python, Django |
| 🎨 Frontend | HTML5, CSS3, JavaScript |
| 🗄️ Database | MySQL / configured database |
| 🗺️ Maps | JavaScript mapping and location features |
| 🤖 AI | Chatbot integration |
| 🛠️ IDE | Visual Studio Code |
| 🔄 Version Control | Git, GitHub |

---

## 📂 Project Structure

```text
LaborConnect/
├── 📁 accounts/
├── 📁 bookings/
├── 📁 chat/
├── 📁 chatbot/
├── 📁 config/
├── 📁 customer/
├── 📁 labor/
├── 📁 notifications/
├── 📁 reviews/
├── 📁 services/
├── 📁 static/
├── 📁 media/
├── 📁 templates/
├── 📄 manage.py
├── 📄 .gitignore
└── 📄 README.md
```

---

## 🚀 Installation & Setup

### 📋 Prerequisites

- 🐍 Python
- 🗄️ MySQL, if required by your configuration
- 🔧 Git

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/gagannaik-n/LabourConnect.git
cd LabourConnect
```

### 2️⃣ Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3️⃣ Install Dependencies

If `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

If it is missing, generate it from your working environment and review the packages before committing:

```bash
pip freeze > requirements.txt
```

### 4️⃣ Configure Environment Variables

Configure the required settings, such as:

- 🔑 Django secret key
- 🗄️ Database credentials
- 🗺️ Maps API key, if applicable
- 🤖 AI API key, if applicable

⚠️ **Security:** Never commit `.env` files, passwords, or API keys to GitHub.

### 5️⃣ Apply Database Migrations

```bash
python manage.py migrate
```

### 6️⃣ Create an Administrator Account

```bash
python manage.py createsuperuser
```

### 7️⃣ Run the Application

```bash
python manage.py runserver
```

🌐 Open your browser at:

**http://127.0.0.1:8000/**

---

## ☁️ Deployment Checklist

Before deploying to a production hosting platform:

- ✅ Set `DEBUG=False`.
- 🔒 Configure environment variables securely.
- 🌍 Configure `ALLOWED_HOSTS`.
- 🗄️ Set up the production database.
- 📦 Configure static file collection and serving.
- 🖼️ Configure persistent media storage.
- 🔐 Enable HTTPS.
- 🧪 Run Django deployment checks.

```bash
python manage.py check --deploy
```

---

## 🔮 Future Enhancements

- 📱 Improved mobile-responsive experience.
- 📍 Advanced distance-based worker search.
- 💬 Real-time messaging and booking updates.
- 🌐 Expanded Kannada and English localization.
- 🔔 Enhanced notification system.
- ⚡ Improved performance and scalability.

---

## 👨‍💻 Author

**Gagan Gopal Naik**  
🎓 Computer Science Engineering

---

## 📜 License

No open-source license has been specified. Unless a license is added, all rights remain reserved by the project owner.

---

<p align="center">
  🛠️ <b>LaborConnect</b> — Connecting People, Skills & Opportunities 🤝
</p>
