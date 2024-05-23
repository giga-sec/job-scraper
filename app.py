import subprocess


job = "Call Center"
loc = "Philippines"


# Execute scrape.py
subprocess.run(["python", "scrape.py", job, loc])

# Execute tokenization.py
# subprocess.run(["python", "tokenization.py"])

# Execute bigram_tokenization.py
subprocess.run(["python", "bigram_jobskills.py", job, loc])

subprocess.run(["python", "jobTitle_counter.py", job, loc])

subprocess.run(["python", "jobTitle_counter.py", job, loc])




