# 🍎 Food Diary Web App

A modern, trendy food tracking application built with Python, Flask, and SQLite. Track your daily intake with a clean, responsive interface.

## 🚀 Features
- **Modern UI/UX**: Card-based layout with a trendy indigo/purple gradient design.
- **Daily Totals**: Real-time calorie tracking for the current day.
- **Persistent Storage**: All data is saved in a local SQLite database.
- **Responsive**: Works on desktop and mobile browsers.
- **Easy Management**: Quick entry adding and one-click deletion.

## 📋 Installation Guidelines

### 1. Prerequisites
Ensure you have Python 3.x installed on your system.

### 2. Setup Environment
It is recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Install Flask, which is the only requirement:
```bash
pip install flask
```

### 4. Run the Application
```bash
python3 app.py
```
The app will be available at `http://localhost:5000`.

---

## 🔄 Latest Updates (2026-02-05)

### v2.0.0 - The "Trendy Web" Update
- **Migration to Web**: Moved from a terminal-based CLI to a full Flask Web Application.
- **Modern Design**: Implemented a "trendy" UI using Bootstrap 5, custom CSS gradients, and Inter font.
- **Glassmorphism**: Added a blurred glass effect to the sticky navigation bar.
- **Daily Intake Card**: Added a prominent visual summary of today's total calories.
- **Improved UX**: Replaced manual ID entry for deletions with intuitive trash icons.
- **Bootstrap Icons**: Integrated iconography for better visual cues.

### v1.1.0 - The "Utility" Update
- Added daily total calculations.
- Implemented entry deletion via ID.
- Added food search functionality.
- Added report export feature to `.txt` files.

### v1.0.0 - Initial Release
- Basic SQLite database integration.
- Console-based logging for food and calories.
- Persistent history storage.

---
*Created with 🐾 by Tony (OpenClaw Assistant)*
