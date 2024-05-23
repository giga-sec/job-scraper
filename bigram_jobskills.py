import re
import csv
import sys
import string
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
from nltk.stem import WordNetLemmatizer


def tokenize_lemmatize(text):
    # Tokenize the text
    tokens = word_tokenize(str(text).lower())

    # Remove punctuation and stop words then lemmatize
    # Lemmatization helps to reduce words to their base or dictionary form.
    tokens = [nltk.lemmatize(token) for token in tokens if token not in stop_words
                  and token not in string.punctuation]

    # Convert the list to a set to remove duplicates, then back to a list
    # tokens = list(set(tokens))

    # Join the tokens back into a string
    processed_text = " ".join(tokens)
    return processed_text  # <- str

# Function to count occurrences of each skill in the job description
def count_skill_occurrences(job_description, skills):
    skill_counts = {skill: 0 for skill in skills}
    for skill in skills:
        occurrences = len(re.findall(r'\b' + re.escape(skill) + r'\b', str(job_description), re.IGNORECASE))
        skill_counts[skill] = occurrences
    return skill_counts

# Function to tokenize text into bigrams
def generate_bigrams(text):
    tokens = word_tokenize(str(text).lower())
    filtered_tokens = [word for word in tokens if word.isalnum()]
    bigrams = list(ngrams(filtered_tokens, 2))
    return bigrams

# Function to count occurrences of bigrams in the text
def count_bigram_occurrences(text, bigram):
    return text.count(bigram)

# START - Variables and Preparation
job = sys.argv[1]
skills_list = sys.argv[2]
filename = f"{job}"
stop_words = set(stopwords.words("english"))
nltk = WordNetLemmatizer()

# Read File
original_df: pd.DataFrame = pd.read_csv(f"csv\\original_{filename}.csv")

# Read the skills list
# with open(f"skills\{job}_skills.txt", "r") as file:
    # skills_list = file.read()
skills_list = [skill.strip() for skill in skills_list.split(",")]
# END - Variables and Preparation


# START - Bigram Job Skills Scanning
# Tokenize and Lemmatize First
original_df["text"] = original_df["description"].apply(tokenize_lemmatize)


# Initialize skill occurrences dictionary
# skill_occurrences: dict[str, int] = {skill: 0 for skill in skills_list}
skill_occurrences: list[tuple[str, int]] = [(skill, 0) for skill in skills_list]
# ^-- Example: dict["Content Writer": 20]

# Initialize bigram occurrences dictionary
bigram_occurrences = {}

# Iterate over each job description
for index, row in original_df.iterrows():
    job_description = row['text']
    
    # Count occurrences of each skill
    skill_counts = count_skill_occurrences(job_description, skills_list)
    for skill, count in skill_counts.items():
        for i, (s, c) in enumerate(skill_occurrences):
            if s == skill:
                skill_occurrences[i] = (skill, c + count)
                break
        else:
            skill_occurrences.append((skill, count))
    
    # Count occurrences of each bigram
    bigrams = generate_bigrams(job_description)
    for bigram in bigrams:
        if bigram in bigram_occurrences:
            bigram_occurrences[bigram] += 1
        else:
            bigram_occurrences[bigram] = 1




# Saving data
# Extract keys and values as separate lists
# Create a DataFrame with transposed data
# df = pd.DataFrame.from_dict(skill_occurrences, orient='index')
df_jobTitles_count = pd.DataFrame(skill_occurrences, columns=['jobSkills', 'count'], index=None)
# df_jobTitles_count = df_jobTitles_count.iloc[:, 0:]
df_jobTitles_count = df_jobTitles_count.sort_values(by='count', ascending=False)
# df_job_titles_count = df_job_titles_count.sort_values(by=1, ascending=False)

# Convert the list of tuples to a DataFrame
df_jobTitles_count.to_csv(f"csv\\jobSkills_{filename}.csv", encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_xlsx


