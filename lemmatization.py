
import pandas as pd
import csv

nltk = WordNetLemmatizer()
filename = "tokenJapanese_philippines"
df = pd.read_csv(f"{filename}.csv")


def preprocess_text(text):
    # Tokenize the text
    word_list = word_tokenize(str(text))

    lemmatized_tokens = [nltk.lemmatize(str(word)) for word in word_list] # Lemmatize each word

    # Join the tokens back into a string
    processed_text = " ".join(lemmatized_tokens)
    return processed_text  # <- str


df["text"] = df["text"].apply(preprocess_text) # Complicated kayni minatay, tan-aw official website documentaiton
df["text"].to_csv(f"lem_{filename}.csv", encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_xlsx


