
USE it_jobs_data;

-- 1. Companies
CREATE TABLE IF NOT EXISTS companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company VARCHAR(255) NOT NULL,
    UNIQUE KEY unique_company (company)
) ENGINE=InnoDB;


-- 2. Locations
CREATE TABLE IF NOT EXISTS locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,

    CONSTRAINT unique_location UNIQUE (city, state, country)
) ENGINE=InnoDB;


-- 3. Skills
CREATE TABLE IF NOT EXISTS skills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(255) NOT NULL,

    CONSTRAINT unique_skill UNIQUE (skill_name)
) ENGINE=InnoDB;


-- 4. Jobs
CREATE TABLE jobs (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(255) NOT NULL,
    company_id INT NOT NULL,
    location_id INT NOT NULL,

    
    min_experience INT,
    max_experience INT,
    min_salary INT,
    max_salary INT,
    job_description TEXT,

    job_url VARCHAR(2048) NOT NULL,
    job_url_hash CHAR(64) NOT NULL,
    posted_date DATETIME  NOT NULL ,

    UNIQUE KEY unique_job_url_hash (job_url_hash),

    FOREIGN KEY (company_id) REFERENCES companies(company_id),

    FOREIGN KEY (location_id)  REFERENCES locations(location_id)

) ENGINE=InnoDB;


-- 5. Job Skills (Bridge Table)
CREATE TABLE IF NOT EXISTS job_skills (
    job_id INT NOT NULL,
    skill_id INT NOT NULL,

    PRIMARY KEY (job_id, skill_id),

    CONSTRAINT fk_jobskills_job FOREIGN KEY (job_id) REFERENCES jobs(job_id)  ON DELETE CASCADE,

    CONSTRAINT fk_jobskills_skill  FOREIGN KEY (skill_id)  REFERENCES skills(skill_id) ON DELETE CASCADE
) ENGINE=InnoDB;


-- 6. Company Rating History
CREATE TABLE IF NOT EXISTS company_rating_history (
    rr_id INT AUTO_INCREMENT PRIMARY KEY,

    company_id INT NOT NULL,
    rating DECIMAL(3,1),
    reviews INT,
    source VARCHAR(100),

    collected_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_rating_company FOREIGN KEY (company_id)  REFERENCES companies(company_id)  ON DELETE CASCADE
) ENGINE=InnoDB;