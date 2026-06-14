# FocusSense AI

AI-Based Focus Score Engine using Behavioral Data

# Project Overview

FocusSense AI is a real-time behavioral analytics system that monitors user activity (keyboard, mouse, idle patterns) and uses machine learning to estimate a **Focus Score** and **Distraction Probability**.

The system transforms raw interaction logs into meaningful features and applies classification models to understand productivity patterns.

#*Key Features*

* Real-time keyboard activity tracking
* Mouse movement monitoring
* Idle time detection
* Feature engineering from raw logs
* Machine learning models (Logistic Regression, Random Forest)
* Focus score computation
* Interactive dashboard (Streamlit)

#How It Works

1. **Data Collection**

   * Tracks keyboard and mouse activity
   * Logs timestamped events

2. **Feature Engineering**

   * Activity frequency (actions per minute)
   * Idle duration
   * Mouse vs keyboard ratio

3. **Modeling**

   * Predicts distraction probability
   * Converts prediction into focus score

4. **Visualization**

   * Displays focus score trends via dashboard


# 🛠️ Tech Stack

* **Python**
* **Pandas**
* **Scikit-learn**
* **Streamlit**
* **Pynput**


## 📁 Project Structure

```
focussense-ai/
│
├── .venv/
├── data/
│   ├── activity_log.csv
│   └── features.csv
│
├── notebooks/
│   └── model.ipynb
│
├── src/
│   ├── collector.py
│   ├── features.py
│
├── app/
│   └── dashboard.py
│
├── requirements.txt
├── README.md
└── .gitignore
```
#Installation & Setup

1. Clone Repository

bash
```
git clone https://github.com/your-username/focussense-ai.git
cd focussense-ai
``` 

### 2. Create Virtual Environment

bash
```
python -m venv .venv
.venv\Scripts\activate   # Windows
```
3. Install Dependencies

bash
```
pip install -r requirements.txt
```


Usage
Step 1: Run Activity Tracker

bash
```
python src/collector.py
```
* Tracks keyboard & mouse activity
* Saves data every 10 seconds


Step 2: Generate Features

Run the notebook:

bash
```
notebooks/feature_engineering.ipynb
```
* Converts raw logs → ML dataset

Step 3: Train Model

bash
```
python src/model.py
```
* Trains Logistic Regression & Random Forest
* Evaluates using:
  * Precision
  * Recall
  * F1-score
  * ROC-AUC

Step 4: Run Dashboard

bash
```
streamlit run app/dashboard.py
```


Focus Score Logic

Focus is inferred from behavioral patterns:

| Signal                 | Interpretation |
| ---------------------- | -------------- |
| High keyboard activity | Deep work      |
| High mouse usage       | Browsing       |
| High idle time         | Distraction    |

Formula:


Focus Score = (1 - Distraction Probability) × 100


# Example Features

| minute | actions | idle_count | mouse_ratio |
| ------ | ------- | ---------- | ----------- |
| 10:30  | 120     | 2          | 0.65        |



Model Evaluation

* Logistic Regression
* Random Forest Classifier

Metrics:

* Precision
* Recall
* F1-score
* ROC-AUC


Privacy Considerations

* No keystroke content is stored
* Only behavioral metadata is collected
* Runs locally (no cloud tracking)


# Future Improvements

* App usage classification (productive vs distracting)
* Deep learning (LSTM for time-series behavior)
* Personalized focus models
* Real-time alerts for distraction


Author

AFIFA AMEER

