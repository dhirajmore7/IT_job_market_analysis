# IT Job Market Analysis

Making a ETL pipeline to scrap data from linkedin,naukri.com using python PlayWright and collect data about IT jobs. clean that data using python pandas to analyze and create power bi dashboard.


An end-to-end **ETL (Extract, Transform, Load) pipeline** for collecting, cleaning, transforming, and storing IT job-market data.

The project extracts job listings from online job portals, processes the raw data using Python and Pandas, and loads the structured data into a relational MySQL database for further analysis and visualization.

---

## 📌 Project Overview

The IT job market contains a large amount of information such as job titles, companies, locations, salaries, experience requirements, skills, ratings, and job descriptions.

This information is often inconsistent and difficult to analyze directly.

This project solves this problem by building an ETL pipeline that:

1. Extracts job data from job portals.
2. Stores the extracted data as raw datasets.
3. Cleans and transforms the data using Python and Pandas.
4. Creates structured datasets for database loading.
5. Loads the processed data into MySQL.
6. Prepares the data for SQL analysis and Power BI visualization.

---
## Tools & Technologies

| Category | Technology |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Database | MySQL |
| ETL | Python, SQLAlchemy |
| Visualization | Power BI |
| Version Control | Git, GitHub |
## 🔄 ETL Pipeline

``
             Job Portals
                  │
                  ▼
          ┌───────────────┐
          │   Extraction  │
          │ Python/Scraper│
          └───────┬───────┘
                  │
                  ▼
            Raw CSV Data
                  │
                  ▼
          ┌───────────────┐
          │ Transformation│
          │ Python/Pandas │
          └───────┬───────┘
                  │
                  ▼
         Processed / Clean Data
                  │
                  ▼
          ┌───────────────┐
          │     Loading   │
          │ SQLAlchemy +  │
          │     MySQL     │
          └───────┬───────┘
                  │
                  ▼
           MySQL Database
                  │
                  ▼
           SQL Analysis
                  │
                  ▼
          Power BI Dashboard



