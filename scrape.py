import csv
import sys
import os
import pandas
from jobspy import scrape_jobs

# Variables Here
job: str = sys.argv[1]
filename = f"original_{job}"

# Check if File exists
if os.path.exists(f"csv\\{filename}.csv"):
    print(f"File '{filename}' already exists. Exiting scrape.py...")
    sys.exit()

# Scrape Jobs
six_months = 183;
jobs: pandas.DataFrame = scrape_jobs(
    site_name=["indeed"],
    search_term=job,
    location="Cebu City",
    distance=50, # miles
    # is_remote= 
    results_wanted=500,
    # hours_old = six_months, # (only linkedin is hour specific, others round up to days old)
    country_indeed='philippines',  # only needed for indeed / glassdoor
    linkedin_fetch_description=True
)
print(f"Found {len(jobs)} jobs")
print(jobs.head())

columns_to_remove = [
    "company_description",
    "logo_photo_url",
    "banner_photo_url",
    "ceo_name",
    "ceo_photo_url",
    "company_num_employees",
    "company_industry",
    "company_addresses",
    "company_url_direct",
    "emails",
    "currency",
    "interval",
    "min_amount",
    "max_amount",
    "job_type",
    "company_revenue",
    "site",
    "job_url_direct",
    "company_url",
]

jobs_filtered = jobs.drop(columns_to_remove, axis=1, errors='ignore')

# Pandas Dataframe to CSV
jobs_filtered.to_csv(f"csv\\{filename}.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)