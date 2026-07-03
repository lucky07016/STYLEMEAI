# 👗 STYLEMEAI

STYLEMEAI is a simple and stylish web app that helps users get outfit suggestions based on their occasion, gender, preferred vibe, and budget. It is designed to make fashion choices feel easier, faster, and more personalized.

This project combines a clean front end with a Python Flask backend to generate helpful styling recommendations and save captured images for future use.

---

## ✨ What This Project Does

- Suggests outfits for casual, college, party, and formal occasions
- Allows users to choose gender, style, and budget preferences
- Gives practical fashion tips and color recommendations
- Saves uploaded or captured images locally for styling sessions

---

## 🛠️ Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- API: Flask REST endpoint
- Image handling: Base64 image processing and local file saving

---

## 🚀 How to Run

1. Install the required Python packages:

```bash
pip install -r src/requirements.txt
```

2. Start the Flask server:

```bash
python src/app.py
```

3. Open the app or test the API endpoint:

- The backend runs at http://127.0.0.1:5000
- The main suggestion route is http://127.0.0.1:5000/suggest

---

## 📁 Project Structure

- [src/app.py](src/app.py) - Flask backend and suggestion logic
- [src/index.html](src/index.html) - Frontend page
- [src/requirements.txt](src/requirements.txt) - Python dependencies

---

## 💡 Notes

This version uses rule-based suggestions for now, but it can later be upgraded with AI models or real fashion recommendation APIs.
