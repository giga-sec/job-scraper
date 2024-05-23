import csv
import sys
import string
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


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


def count_job_titles(job_titles: pd.DataFrame, allJobs_totalCount: int):
    # Create a frequency distribution of job titles
    freq_dist = FreqDist(job_titles)

    most_common_jobs: list[tuple[str, int]] = freq_dist.most_common(allJobs_totalCount)
    return most_common_jobs



# START - Variables and Preparation
job: str = sys.argv[1]
loc: str = sys.argv[2]
filename = f"{job}_{loc}"
stop_words = set(stopwords.words("english"))
nltk = WordNetLemmatizer()

# Read File
df_original = pd.read_csv(f"original_{filename}.csv")


df_jobTitles: pd.DataFrame = df_original["title"].apply(tokenize_lemmatize)

# START Counting Job Titles
allJobs_totalCount = len(df_jobTitles)
each_jobTitles_count: list[tuple[str, int]] = count_job_titles(df_jobTitles, allJobs_totalCount) 
# ^-- Tuple inside of a list. Example [('Content Writer', 2), ('Copy Editor - Ogilvy Philippines', 1)
print(each_jobTitles_count)
# END Counting Job Titles


# Convert the list of tuples to a DataFrame
df_jobTitles_count = pd.DataFrame(each_jobTitles_count, columns=['job_titles', 'count'])
df_jobTitles_count = df_jobTitles_count.sort_values(by='count', ascending=False)
df_jobTitles_count.to_csv(f"jobTitle_count_{filename}.csv", encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=True) 
