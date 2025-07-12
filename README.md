# 🎓 AIU Course Advisor

AIU Course Advisor is an intelligent course recommendation system built using Python, Streamlit, and Experta. It helps students choose the most appropriate courses based on their CGPA, academic history, and university policies.

---

## 📂 Project Structure

```
AIU-Course-Advisor/
│
├── app/
│   └── app.py                  # Streamlit app interface
│
├── data/
│   ├── Cyber Security Track Courses Updated.csv
│   ├── Elective courses.csv
│   └── policies.csv            # Course & policy data files
│
├── docs/                       # Project documentation (optional)
│
├── src/
│   ├── editor.py               # Handles course loading/merging
│   ├── engine.py               # Inference engine using Experta
│   ├── explanation.py          # Explanation logger for rules
│   └── main.py                 # (optional) CLI test runner
│
├── requirements.txt            # Python dependencies
└── README.md                   # You're reading it!
```

---

## 🚀 Features

* 📘 Rule-based reasoning using Experta (PyKnow)
* 📊 Dynamically limits credit hours based on CGPA
* ✅ Checks prerequisites and failed courses
* 🧠 Explains each recommendation decision
* 🖼️ GUI built with Streamlit

---

## 🧪 Example Usage

Run the app:

```bash
streamlit run app/app.py
```

Then:

1. Enter CGPA
2. Select current semester
3. Choose passed and failed courses from dropdowns
4. Click **Run Advisor**
5. View recommended courses and explanations

---

## ⚙️ Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/AIU-Course-Advisor.git
cd AIU-Course-Advisor
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the Streamlit app:**

```bash
streamlit run app/app.py
```

---

## 📁 Data Files

Ensure these files are inside the `data/` folder:

* `Cyber Security Track Courses Updated.csv`
* `Elective courses.csv`
* `policies.csv`

---

## 📌 Requirements

* Python 3.7+
* `streamlit`
* `experta`
* `pandas`

You can install them with:

```bash
pip install -r requirements.txt
```

---

## 👨‍💻 Authors


* Developed by Gawad 🚀

---

## 🧠 License

This project is for educational and academic use. Contact the author for licensing.

---
