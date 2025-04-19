
# ⏱️ TimeBolt

TimeBolt is a simple time tracking web application built with Django. It helps users track their daily tasks, view task durations, generate reports, and monitor productivity over time.

## 🚀 Features

- ⌛ Start & stop task tracking
- 📊 Dashboard with task summaries
- 📅 Filter tasks by date
- 📈 View worked hours and task counts
- 🔐 User authentication (sign up / login)
- 🧠 Daily summary (basic)
- 🖥️ Responsive and user-friendly UI

## 🛠️ Tech Stack

- Python 3
- Django
- Django Rest Framework (DRF)
- HTML/CSS
- Bootstrap (for UI styling)
- JavaScript (for interactivity)
- SQLite (default Django DB)

## 📦 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/saqiba123/TimeBolt
   cd timebolt
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the app**
   - Open your browser and go to: `http://127.0.0.1:8000/`

## ✍️ Optional Enhancements

- Add charts to the dashboard using Chart.js or Plotly
- Integrate with third-party calendar/task tools
- Add dark mode toggle

## 🙋‍♂️ Author

Built with 💙 by Saqiba
## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
