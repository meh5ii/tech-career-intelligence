<div align="center">

# ⚡ Tech Career & Skill Intelligence
### End-to-End Technology Market Analytics, AI Resilience & Career Recommendation Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tech-career-intelligence-7hna5me6mzpnwifmub2cbn.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Viz-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![Status](https://img.shields.io/badge/Status-Active%20Production-10B981?style=for-the-badge)](https://github.com/meh5ii/tech-career-intelligence)

<br/>

**[🌐 مشاهده داشبورد زنده (Live Demo)](https://tech-career-intelligence-7hna5me6mzpnwifmub2cbn.streamlit.app/)**

</div>

---

## 📌 درباره پروژه (About The Project)

سامانه **Tech Career & Skill Intelligence** یک پلتفرم جامع، داده‌محور و تعاملی است که با تحلیل کلان داده‌های دنیای تکنولوژی (شامل بیش از **۳۲,۰۰۰ پروفایل توسعه‌دهنده از Stack Overflow**، **فرصت‌های شغلی LinkedIn** و داده‌های زمانی **Google Trends**)، به مهندسان نرم‌افزار و دانشمندان داده کمک می‌کند تا وضعیت بازار کار، ارزش اقتصادی تخصص‌ها، میزان پایداری در برابر هوش مصنوعی و مسیر توسعه فردی خود را بسنجند.

---

## ✨ ویژگی‌های کلیدی (Core Features)

این داشبورد دارای **۸ ماژول و تب اختصاصی** با طراحی مدرن Bento-Grid است:

| تب / ماژول | عملکرد و قابلیت‌ها |
| :--- | :--- |
| **✦ Stack Recommender** | پیشنهاد مهارت‌های مکمل بر اساس قوانین انجمنی (*Association Rules*) با سنجش دقیق ضریب نفوذ (*Lift*) و ضریب اطمینان (*Confidence*). |
| **↗ Future Outlook** | پیش‌بینی روند تقاضای تکنولوژی‌ها تا ۳ سال آینده با مدل‌سازی رگرسیون زمانی و ارزیابی طول عمر مفید مهارت‌ها (*Half-life*). |
| **◈ Market Valuation** | تحلیل اقتصادی ارزش بازار، توزیع درآمد دلاری مهارت‌ها و ماشین‌حساب محاسبه سودافزوده ترکیب تکنولوژی‌ها (*Stack Synergy*). |
| **⇄ 1v1 Tech Arena** | مقایسه رودرروی فریم‌ورک‌ها و زبان‌ها در ۶ بُعد معماری (درآمد، مصونیت هوش مصنوعی، تقاضای کار، سهولت یادگیری، ریموت و بلوغ). |
| **⎔ Track Roadmaps & Vault** | مسیر یادگیری گام‌به‌گام برای ۶ تخصص اصلی به همراه تخمین ساعت مطالعه مورد نیاز و کتابخانه لینک‌های مرجع (*Official Vault*). |
| **📄 Resume ATS & Gap Hunter** | پارسر رزومه (PDF/متن) و بررسی انطباق با نیازمندی‌های شغلی (*ATS Compliance*) به همراه شناسایی شکاف‌های فنی. |
| **🔀 Career Pivot Simulator** | شبیه‌ساز تغییر مسیر شغلی میان حوزه‌ها با برآورد زمان انتقال، میزان انتقال‌پذیری دانش و تغییرات حقوق دریافتی. |
| **⟐ Live Jobs Radar** | رادار و اسکرپر هوشمند آگهی‌های شغلی و فریلنسری (LinkedIn, RemoteOK, Jobinja, Jobvision, Karlancer, Quera). |

---

## 🛠️ تکنولوژی‌ها و ابزارها (Tech Stack)

* **Language:** Python 3.10+
* **Frontend / Framework:** Streamlit, Custom HTML5 & Glassmorphic CSS Engine
* **Data Processing & Analytics:** Pandas, NumPy, Scikit-Learn, MLxtend
* **Data Visualization:** Plotly Graph Objects & Express
* **Web Scraping & Extraction:** Selenium, BeautifulSoup4, PyPDF

---

## 📁 ساختار پروژه (Project Structure)

```text
tech-career-intelligence/
├── app.py                      # فایل اصلی داشبورد و رابط کاربری Streamlit
├── job_scraper.py              # ماژول خزشگر وب و اسکرپینگ فرصت‌های شغلی زنده
├── requirements.txt            # پکیج‌ها و وابستگی‌های پروژه
├── images.jpg                  # بنر و فایل‌های تصویری
├── data/                       # پایگاه داده پاک‌سازی‌شده و خروجی‌های تحلیلی
│   ├── clean_google_trends.csv
│   ├── clean_linkedin_jobs.csv
│   ├── clean_stackoverflow_skills.csv
│   └── skill_association_rules.csv
└── README.md                   # مستندات پروژه
