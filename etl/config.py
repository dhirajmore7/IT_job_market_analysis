import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine

from pathlib import Path


db_host = os.getenv("db_host")
db_port = int(os.getenv("db_port"))
db_name = os.getenv("db_name")
db_password = os.getenv("db_password")

engine = create_engine(f"mysql+pymysql://root:{db_password}@{db_host}:{db_port}/{db_name}")



# job roles

job_role = "data-analyst"

# FILE paths
naukri_link_data = Path("data/extracted_data/naukri_data/naukri_link_data.csv")

history_data = Path("data/extracted_data/naukri_data/naukri_scrap_history.csv")

clean_data_path = Path("data/processed_data/naukri/naukri_clean_data.csv")




skills = [
    # Programming
    "Python",
    "R",
    "SQL",

    # Python Libraries
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Plotly",
    "SciPy",
    "Scikit-learn",

    # Databases
    "MySQL",
    "PostgreSQL",
    "Oracle",
    "SQL Server",
    "Microsoft SQL Server",
    "SQLite",
    "MongoDB",

    # BI / Visualization
    "Power BI",
    "Tableau",
    "Looker",
    "Looker Studio",
    "Qlik Sense",
    "QlikView",
    "Excel",
    "Advanced Excel",

    # Excel Skills
    "VLOOKUP",
    "XLOOKUP",
    "INDEX MATCH",
    "Pivot Table",
    "Power Query",
    "Power Pivot",
    "DAX",

    # Data Analysis
    "Data Analysis",
    "Data Analytics",
    "Data Cleaning",
    "Data Wrangling",
    "Data Visualization",
    "Data Mining",
    "Exploratory Data Analysis",
    "EDA",
    "Statistical Analysis",
    "Predictive Analytics",

    # Statistics
    "Statistics",
    "Descriptive Statistics",
    "Inferential Statistics",
    "Hypothesis Testing",
    "Regression Analysis",
    "Correlation Analysis",
    "A/B Testing",

    # ETL / Data Engineering
    "ETL",
    "ELT",
    "Data Pipeline",
    "Data Pipelines",
    "Data Integration",
    "Data Transformation",
    "Data Modeling",
    "Data Warehouse",
    "Data Warehousing",
    "Data Lake",

    # ETL Tools
    "SSIS",
    "Informatica",
    "Talend",
    "Alteryx",
    "Apache Airflow",
    "dbt",

    # Cloud
    "AWS",
    "Amazon Web Services",
    "Azure",
    "Microsoft Azure",
    "Google Cloud",
    "GCP",
    "BigQuery",
    "Amazon Redshift",
    "Snowflake",

    # Python / Data Processing
    "Jupyter",
    "Jupyter Notebook",
    "JupyterLab",
    "OpenPyXL",

    # Big Data
    "Spark",
    "PySpark",
    "Hadoop",
    "Hive",

    # Business Analysis
    "Business Intelligence",
    "Business Analysis",
    "KPI",
    "KPIs",
    "Dashboard",
    "Dashboards",
    "Reporting",
    "MIS",
    "MIS Reporting",

    # Version Control
    "Git",
    "GitHub",
    "GitLab",

    # APIs / Data Collection
    "REST API",
    "REST APIs",
    "API",
    "APIs",
    "JSON",
    "Web Scraping",
    "BeautifulSoup",
    "Selenium",
    "Playwright",

    # Other useful analytics skills
    "Data Quality",
    "Data Validation",
    "Data Governance",
    "Data Profiling",
    "Time Series Analysis",
    "Forecasting",
    "Machine Learning",
    "Artificial Intelligence",
    "Natural Language Processing",
    "NLP"
]



