import sys
import os

import time
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Database connection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database")))
from db_connection import connect_to_db



# Job roles to scrape
JOB_TITLES = [
    "Data Analyst", "Business Intelligence Analyst", 
    "Data Scientist", "Data Engineer", "Machine Learning Engineer"
]

def scrape_linkedin_jobs():
    """Scrapes job postings from LinkedIn and extracts locations dynamically."""
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.linkedin.com/jobs/search/?keywords={}"

    all_jobs = []  # Store job data
    unique_locations = set()  # Store dynamically discovered locations

    for job_title in JOB_TITLES:
        url = base_url.format(job_title.replace(" ", "%20"))
        driver.get(url)
        time.sleep(3)  # Allow time for page to load

        jobs = driver.find_elements(By.CLASS_NAME, "job-card-container")

        for job in jobs:
            try:
                title = job.find_element(By.CLASS_NAME, "job-card-list__title").text
                company = job.find_element(By.CLASS_NAME, "job-card-container__company-name").text
                location = job.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
                description = job.find_element(By.CLASS_NAME, "job-card-list__snippet").text
                date_posted = job.find_element(By.CLASS_NAME, "job-card-container__listed-time").text
                
                unique_locations.add(location)  # Capture unique locations dynamically

                job_data = {
                    "job_title": title,
                    "company": company,
                    "location": location,
                    "date_posted": date_posted,
                    "job_description": description,
                    "source": "LinkedIn"
                }
                all_jobs.append(job_data)

            except Exception as e:
                print("Error extracting job:", e)

    driver.quit()
    
    # Save jobs to PostgreSQL
    save_to_db(all_jobs)

    print(f"✅ Scraped {len(all_jobs)} jobs from LinkedIn")
    print(f"📍 Unique Locations Extracted: {unique_locations}")

def save_to_db(jobs):
    """Saves the scraped jobs to the PostgreSQL database."""
    conn = connect_to_db()
    if conn is None:
        print("❌ Database connection failed.")
        return

    try:
        cursor = conn.cursor()

        for job in jobs:
            cursor.execute("""
                INSERT INTO jobs (job_title, company, location, date_posted, job_description, source) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                job["job_title"], job["company"], job["location"], 
                job["date_posted"], job["job_description"], job["source"]
            ))

        conn.commit()
        print("✅ Jobs saved to the database.")

    except Exception as e:
        print("❌ Error saving jobs:", e)
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    scrape_linkedin_jobs()
