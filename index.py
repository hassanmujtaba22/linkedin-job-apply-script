import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace these with your LinkedIn credentials
linkedin_username = 'fullstackdeveloper2206@gmail.com'
linkedin_password = 'Hassan2206@'

# Keywords for job search
job_keywords = ['MEAN', 'MERN', 'JavaScript', 'frontend', 'backend']

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Initialize ChromeDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to the LinkedIn login page
    driver.get('https://www.linkedin.com/login')

    # Find the username and password fields and enter the credentials
    username_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')
    username_field.send_keys(linkedin_username)
    password_field.send_keys(linkedin_password)
    
    # Find and click the login button
    login_button = driver.find_element(By.XPATH, '//*[@type="submit"]')
    login_button.click()

    # Wait for the login to complete
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="global-nav-search"]'))
    )

    for keyword in job_keywords:
        # Navigate to the jobs page and search for the job keyword
        driver.get('https://www.linkedin.com/jobs/')
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="jobs-search-box-keyword-id-ember404"]'))
        )
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        # Filter jobs by "Past 24 hours" and "Easy Apply"
        time.sleep(3)  # Wait for search results to load
        posted_date_filter = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Date Posted"]'))
        )
        posted_date_filter.click()
        past_24_hours = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//label[@for="timePostedRange-r86400"]'))
        )
        past_24_hours.click()

        easy_apply_filter = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="All Filters"]'))
        )
        easy_apply_filter.click()
        time.sleep(1)  # Wait for filter options to load
        easy_apply = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//label[@for="f_LF-f_AL"]'))
        )
        easy_apply.click()
        apply_filters_button = driver.find_element(By.XPATH, '//button[text()="Show results"]')
        apply_filters_button.click()

        # Wait for filtered search results to load
        time.sleep(3)

        # Get the list of job postings
        job_postings = driver.find_elements(By.CLASS_NAME, 'job-card-container__link')

        # Iterate through the job postings and apply if possible
        for job in job_postings:
            job.click()
            time.sleep(2)  # Wait for job details to load

            try:
                easy_apply_button = driver.find_element(By.XPATH, '//button[text()="Easy Apply"]')
                easy_apply_button.click()
                time.sleep(2)  # Wait for the Easy Apply form to load

                # Click the submit application button (you might need to add additional form interactions here)
                submit_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//button[text()="Submit application"]'))
                )
                submit_button.click()
                time.sleep(2)  # Wait for the application to be submitted

            except Exception as e:
                logger.error(f"Could not apply for job: {e}")

finally:
    # Close the browser after the operations
    driver.quit()
