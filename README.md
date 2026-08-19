
# ⚡ Tech Career & Skill Intelligence

### Data-Driven Tech Market Analytics, AI Resilience Index & Career Recommendation Engine

**[🌐 Launch Live Web Application](https://tech-career-intelligence-7hna5me6mzpnwifmub2cbn.streamlit.app/)**

---

## 📌 Overview

**Tech Career & Skill Intelligence** is an end-to-end analytical platform designed to provide data-driven career navigation for software engineers and data professionals.

By mining and analyzing **32,000+ developer profiles from Stack Overflow**, real-world **LinkedIn job postings**, and multi-year **Google Trends** time-series data, the system evaluates career readiness, predicts skill market longevity, benchmarks compensation, and delivers personalized skill acquisition roadmaps.

---

## ✨ Key Capabilities

| Module | Core Functionality |
| --- | --- |
| **✦ Stack Recommender** | Data-mining recommendation vector using **Association Rules** (Lift, Confidence, Support) to suggest high-synergy adjacent skills. |
| **↗ Future Outlook** | Multi-horizon time-series forecasting (3-year linear trajectories & 4-month velocity pulse) combined with **Skill Half-Life** modeling. |
| **◈ Market Valuation** | Normalized tech stack compensation benchmarks and dynamic synergy premium calculator. |
| **⇄ 1v1 Tech Arena** | 6-axis head-to-head architectural radar benchmarking (Compensation, AI Shield, Demand, Learning Curve, Remote %, Maturity). |
| **⎔ Track Roadmaps & Vault** | Milestone-driven phase breakdown for 6 core engineering disciplines with curated official documentation and study hour estimates. |
| **📄 Resume & ATS Gap Hunter** | Automated PDF/Text ATS parser comparing candidate profiles against live target job descriptions to identify missing keywords. |
| **🔀 Career Pivot Simulator** | Discipline-to-discipline transition modeling estimating timeline, transferable stack overlap, and salary delta. |
| **⟐ Live Jobs Radar** | Multi-threaded real-time job crawler aggregating live openings across remote and global job boards ranked by stack compatibility. |

---

## 🛠️ Technology Stack

* **Core Language:** Python 3.10+
* **Dashboard & UI:** Streamlit, Custom Responsive CSS (Bento Grid & Glassmorphism)
* **Data Mining & Analytics:** Pandas, NumPy, Scikit-Learn, MLxtend
* **Data Visualization:** Plotly Graph Objects & Plotly Express
* **Web Scraping & Parsing:** Selenium, BeautifulSoup4, PyPDF

---

## 📁 Repository Architecture

```text
tech-career-intelligence/
├── app.py                      # Main Streamlit dashboard application
├── job_scraper.py              # Multi-platform live job crawler
├── requirements.txt            # Project dependencies & libraries
├── images.jpg                  # Application assets & branding
├── data/                       # Curated datasets & serialized mining outputs
│   ├── clean_google_trends.csv
│   ├── clean_linkedin_jobs.csv
│   ├── clean_stackoverflow_skills.csv
│   └── skill_association_rules.csv
└── README.md                   # System documentation

```

---

## 🚀 Quick Start (Local Setup)

1. **Clone the repository:**

```bash
git clone https://github.com/meh5ii/tech-career-intelligence.git
cd tech-career-intelligence

```

2. **Create and activate a virtual environment:**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

```

3. **Install dependencies:**

```bash
pip install -r requirements.txt

```

4. **Launch the dashboard:**

```bash
streamlit run app.py

```

---

## 👤 Author

* **Mehdi Bagheri**
* Undergraduate Thesis Project in Computer Science
* **GitHub:** [@meh5ii](https://www.google.com/search?q=https://github.com/meh5ii)
* **Live Demo:** [Tech Career Intelligence](https://tech-career-intelligence-7hna5me6mzpnwifmub2cbn.streamlit.app/)

1. روی آیکون مداد (Edit) در بالای فایل README کلیک کنید.
2. کل متن قبلی را با `Ctrl + A` انتخاب و حذف (`Delete`) کنید.
3. متن بالا را پیست کرده و روی دکمه سبز **Commit changes** بزنید.
