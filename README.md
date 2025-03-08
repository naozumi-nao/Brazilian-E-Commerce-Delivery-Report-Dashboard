# 📦 Brazilian E-Commerce Delivery Report Dashboard
This project provides an interactive Streamlit-based dashboard for analyzing delivery performance and customer satisfaction in a Brazilian e-commerce dataset. The dashboard visualizes key insights, including delivery time distributions, customer review correlations, and statistical trends, enabling businesses to optimize logistics and improve user experience.

## 🚀 Features

    📊 Delivery Time Analysis: Explore the distribution of delivery times and cumulative distribution trends.
    ⭐ Customer Review Correlation: Identify the relationship between delivery time and review scores.
    🔥 Interactive Data Visualization: Boxplots, heatmaps, and bar charts for in-depth insights.
    ⚡ Fast & Easy Deployment: Built using Streamlit, allowing quick data exploration and visualization.

## 📌 Getting Started
### Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

### Run steamlit app
```
streamlit run dashboard.py
```
Once the app starts, open http://localhost:8501/ in your browser to interact with the dashboard.

## 📁 Dataset
The analysis is based on a cleaned version of the Brazilian e-commerce dataset from https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce, which includes delivery time, review scores, and customer feedback.

## 🤝 Contributions
Feel free to fork this repository, improve the dashboard, and submit a pull request! 🚀