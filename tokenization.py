import pandas
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import csv
from nltk.stem import WordNetLemmatizer


# Load the CSV file
filename = "original_copywriter_philippines"
df = pandas.read_csv(f"{filename}.csv")

stop_words = set(stopwords.words("english"))
nltk = WordNetLemmatizer()

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(str(text).lower())

    # Remove punctuation and stop words then lemmatize
    # Lemmatization helps to reduce words to their base or dictionary form.
    tokens = [nltk.lemmatize(token) for token in tokens if token not in stop_words
                  and token not in string.punctuation]

    # Join the tokens back into a string
    processed_text = " ".join(tokens)
    return processed_text  # <- str


df["text"] = df["description"].apply(preprocess_text)
df["text"].to_csv(f"Token{filename}.csv", encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_xlsx

print(df)


