# 🤖 AI-Powered Personalized Tutor System 📚

Welcome to the **AI-Powered Personalized Tutor System** — an innovative platform developed during our industrial training under Intel Corporation. This system leverages Artificial Intelligence (AI) to transform traditional education by offering highly **personalized, data-driven, and adaptive learning** experiences.

🎥 **[Watch Demo Video](https://drive.google.com/file/d/1fmBu_Rc0zRrdN-mTF0xDnbvApZ8glTd-/view?usp=sharing)**

---

## 🎯 Objective
To create an engaging, effective, and tailored educational environment using AI, with features like real-time feedback, personalized content, and student-specific performance insights.

---

## 🔍 Problem Definition

* ❌ Lack of personalization in traditional classrooms
* ❌ Uniform content delivery regardless of student needs
* ❌ Student disengagement and lack of motivation
* ❌ Heavy administrative workload for educators

---

## ✨ Proposed Solution

Using machine learning and NLP, our platform addresses these gaps through:

* 📈 **Performance Prediction**
* 📚 **Tailored Content Recommendations**
* 📄 **AI-Powered PDF Querying**
* 📊 **Content Retention/Skipping Suggestions**

---

## 🛠️ Technologies Utilized

### 🧱 Data Manipulation & Analysis:

* `NumPy`, `Pandas`

### 📊 Data Visualization:

* `Matplotlib`, `Seaborn`

### 🤖 Machine Learning:

* `Scikit-learn`, `XGBoost`, `Pickle`, `Pipeline`, `ColumnTransformer`

### 🗣 Natural Language Processing:

* NLP for intelligent query handling
* RAG (Retrieval-Augmented Generation) using `FAISS` / `Chroma` for PDF querying

### 🌐 Web Development:

* `Streamlit` (Frontend)
* `HTML`, `CSS`

---

## 🏠 System Architecture

```plaintext
User Interface (Streamlit)
       ↓
Recommendation Engine (Content-Based + Collaborative)
       ↓
ML Models (RandomForest, XGBoost, Softmax)
       ↓
Data Layer (Historical Student Data)
```

---

## 💻 Features

### 🔐 User Authentication

* Secure Login and Registration
* Personalized Dashboard for each student

### 📈 Student Performance Predictions

* **Promotion Prediction** using `RandomForestClassifier`
* **Assessment Score Forecasting** via `RandomForestRegressor`

### 🌟 Adaptive Content

* **Level-Based Recommendations** using `Softmax Regression`
* **Content Retention & Skipping** with `XGBoostClassifier`

### 📄 PDF Query Engine

* AI-enabled querying from uploaded PDFs using `Langchain` + RAG

---

## 📊 Model Performance Metrics

| Feature                      | Model                  | Accuracy / Score       |
| ---------------------------- | ---------------------- | ---------------------- |
| Student Promotion Prediction | RandomForestClassifier | 99.99%                 |
| Assessment Score Prediction  | RandomForestRegressor  | R² = 1.0, MSE = 0.0008 |
| Content Recommendation       | Softmax Regression     | 100%                   |
| Content Retention/Skipping   | XGBoostClassifier      | 100%                   |

---

## ⚠️ Challenges Faced

* ⚠️ Incomplete/low-quality datasets
* ⚠️ High computational needs (especially for NLP)
* ⚠️ Integration issues with external platforms
* ⚠️ Maintaining answer precision during document querying

---

## 📈 Future Enhancements

* ♻️ **Data Augmentation** for broader training
* 🌍 **Scalability** improvements for larger user base
* 🧠 **Advanced NLP Models** (e.g., LLaMA, GPT-style)
* 💌 **Feedback Mechanisms** for continuous iteration
* 🎓 **Gamification** and performance visualizations

---

## 📂 Repository Structure

```
AI-Powered-Personalized-Tutor-System-main/
💽 data/                     # Cleaned and processed datasets
📁 models/                   # Pickled ML models
📂 notebooks/                # EDA and training notebooks
📄 pdf_query/                # RAG implementation scripts
📁 app/                      # Streamlit frontend and routing
📄 utils/                    # Helper functions
README.md                 # This file
code_unnati_ppt[1].pptx   # Presentation
```

---

## 🤝 Contributing

We welcome contributions to improve this system!

1. 🍴 Fork the repo
2. 🌿 Create a new branch
3. 🛠 Make your changes
4. ✅ Test thoroughly
5. 📩 Submit a pull request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE), giving you freedom to use, modify, and distribute it.

---

## 👨‍💼 Authors

* **Divyanshu Dubey**
* **Gopal**
* **Atharv Gehlot**

---

## 📊 GitHub Stats

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=Divyanshu1Dubey&show_icons=true&theme=radical" width="50%" />
  <br/>
  <img src="https://streak-stats.demolab.com?user=Divyanshu1Dubey&theme=radical" width="50%" />
  <br/>
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=Divyanshu1Dubey&theme=react-dark" width="90%" />
</p>

---

## 🐍 Contribution Snake

![snake gif](https://github.com/Divyanshu1Dubey/Divyanshu1Dubey/blob/output/github-contribution-grid-snake.svg)

---

## 🛡️ Badge Board

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge\&logo=python\&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge\&logo=scikit-learn\&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-A41E11?style=for-the-badge\&logo=data\:image/png;base64,...)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

> 🎉 *Empowering personalized learning, one student at a time!*
