# Advertising Sales Prediction Using Machine Learning

## Project Overview
This project focuses on predicting product sales based on advertising expenditure across three different marketing platforms: TV, Radio, and Newspaper. Machine Learning regression algorithms are implemented to analyze the relationship between advertising investments and sales performance.

## Objectives
- Analyze the impact of advertising expenditure on sales.
- Understand relationships between advertising channels and sales.
- Build and compare multiple regression models.
- Identify the best-performing model for sales prediction.

## Dataset
The project uses the `Advertising.csv` dataset, which contains advertising expenditure and corresponding sales data.

**Features:**
- TV – Advertising expenditure on TV.
- Radio – Advertising expenditure on Radio.
- Newspaper – Advertising expenditure on Newspaper.
- Sales – Target variable representing product sales.

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

## Machine Learning Algorithms
The following regression algorithms were implemented:
1. Simple Linear Regression
2. Multiple Linear Regression
3. Polynomial Regression
4. Random Forest Regression

## Model Evaluation
Model performance was evaluated using:
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

**Best Model:** Polynomial Regression

**Achieved R² Score:** 0.9869

## Project Structure
```text
Advertising-Sales-Prediction/
│
├── Advertising_Sales_Prediction.ipynb
├── Advertising.csv
├── advertising_sales_model.pkl
└── README.md
```

## Key Findings
- Advertising expenditure has a measurable relationship with sales.
- Different advertising platforms contribute differently to sales performance.
- Polynomial Regression achieved the best performance among the evaluated models.

## Limitations
- The dataset contains limited advertising channels.
- Predictions are based on historical data.
- Other factors affecting sales, such as pricing, competition, and market demand, are not considered.

## Conclusion
This project demonstrates how Machine Learning regression techniques can be used to analyze advertising investments and predict sales. It also provides practical experience in data preprocessing, model development, evaluation, and comparison.

## Author
**Abijith Anil**

