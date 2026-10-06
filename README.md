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

## 🔄 ETL Pipeline

```text
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



## ETL Implementation

### 1. Extract

The extraction stage collects job-related information from job portals and stores the results in CSV files.

Collected attributes include:

- Job title
- Company name
- Job location
- Experience requirements
- Salary information
- Job description
- Required technical skills
- Employment type
- Industry and department
- Company ratings
- Job posting date
- Job URL

The extraction process uses Python-based web scraping techniques.

### 2. Transform

The transformation stage converts raw job data into a consistent and structured format using Pandas.

**Data Cleaning**

- Handle missing and null values.
- Remove duplicate records.
- Remove unnecessary whitespace and formatting.
- Standardize inconsistent text values.

**Location Standardization**

- Clean location strings.
- Identify cities and states.
- Map city names to corresponding Indian states.
- Organize location information for relational storage.

**Salary and Experience Processing**

- Extract relevant salary information.
- Separate minimum and maximum salary values where possible.
- Process experience ranges.
- Handle unavailable or undisclosed information.

**Skills Processing**

- Clean skill-related text.
- Separate multiple skills.
- Standardize skill values.
- Prepare skill mappings for relational tables.

**Date Processing**

- Convert relative posting dates into standardized date values.
- Handle values such as "Today", "1 day ago", and "1 week ago".

### 3. Load

The loading stage transfers processed data into MySQL using Python and SQLAlchemy.

The database is organized into related tables to reduce redundancy and improve data consistency.

Key considerations include:

- Primary and foreign keys
- Relational database design
- Duplicate record handling
- Data type consistency
- Transaction management
- Error handling

## Database Design

The project uses the following main entities:

| Table | Description |
|---|---|
| `companies` | Stores unique company information |
| `locations` | Stores city, state, and country details |
| `jobs` | Stores job listings and related attributes |
| `skills` | Stores unique technical skills |
| `job_skills` | Maps jobs to their required skills |
| `company_rating_history` | Stores historical company rating information |

The `job_skills` table represents a many-to-many relationship between jobs and skills.

The company rating history table supports tracking rating information across collection periods.

*Note: Refer to the SQL schema in the repository for the exact table definitions and constraints.*



The folder structure above summarizes the main components. Refer to the repository for the latest files and script names.

## Data Quality and Validation

Data quality is an important part of the ETL process.

The pipeline focuses on:

1. Identifying duplicate job records.
2. Handling missing values.
3. Maintaining consistent column formats.
4. Standardizing locations and technical skills.
5. Preparing unique company and location records.
6. Maintaining relationships between database tables.
7. Handling database loading errors.

These steps help make the dataset more reliable for downstream analysis.

## Planned Data Analysis

The structured database can support questions such as:

- Which technical skills appear most frequently in IT job listings?
- Which cities have the highest number of job opportunities?
- Which companies advertise the most positions?
- What experience levels are commonly requested?
- How do salary ranges differ across job roles?
- Which job titles are most frequently advertised?
- How do hiring trends change over time?

## Future Improvements

- [x] Build job data extraction workflow.
- [x] Implement data cleaning and transformation.
- [x] Design relational database tables.
- [x] Develop MySQL data-loading workflow.
- [ ] Add automated ETL scheduling.
- [ ] Expand SQL-based exploratory analysis.
- [ ] Develop an interactive Power BI dashboard.
- [ ] Add pipeline monitoring and execution logs.
- [ ] Improve incremental loading and historical tracking.
- [ ] Deploy the pipeline using cloud services.

## Key Learning Outcomes

Through this project, I gained practical experience in:

- Developing ETL workflows using Python.
- Processing real-world datasets with Pandas.
- Handling inconsistent and duplicate information.
- Designing relational database structures.
- Connecting Python applications to MySQL.
- Working with SQLAlchemy for database operations.
- Preparing structured datasets for business intelligence.
- Managing a data project using Git and GitHub.

## Author

**Dhiraj More**

Computer Engineering Graduate | Python | SQL | Data Analytics | ETL

**GitHub:** [dhirajmore7](https://github.com/dhirajmore7)

**Project Repository:** [IT Job Market Analysis](https://github.com/dhirajmore7/IT_job_market_analysis)

---

*This project is developed for practical learning and portfolio demonstration. Job-market data reflects collected listings and should not be interpreted as a complete representation of the employment market.*

