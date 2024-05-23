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


# START - Variables and Preparation
job: str = sys.argv[1]
loc: str = sys.argv[2]
filename = f"{job}_{loc}"
stop_words = set(stopwords.words("english"))
nltk = WordNetLemmatizer()

# Read File
df_original = pd.read_csv(f"original_{filename}.csv")


df_jobTitles: pd.DataFrame = df_original["title"].apply(tokenize_lemmatize)
df_jobLocations: pd.DataFrame = df_original["location"].apply(tokenize_lemmatize)

# Combine Location and Title
df_original['location_title'] = df_jobLocations  + ' - ' + df_jobTitles
# Splitting location and title
df_jobsLocations_count = df_original.groupby('location_title').size().reset_index(name='count')
df_jobsLocations_count[['location', 'title']] = df_jobsLocations_count['location_title'].str.split(' - ', expand=True)
# Sorting each city alphabetically and by count
df_sorted = df_jobsLocations_count.sort_values(by=['location', 'count'], ascending=[True, False])
df_sorted.drop(columns=['location_title'], inplace=True)


# Count Job Types by Location
# df_sorted = df_original.groupby('location_title').size().reset_index(name='count')
# df_sorted = df_jobsLocations_count.sort_values(by='count', ascending=False)
df_sorted.to_csv(f"jobsLocations_count_{filename}.csv", encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=True) 


