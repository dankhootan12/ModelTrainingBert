import pandas as pd
import random
from nltk.corpus import wordnet
from sklearn.utils import resample

# Load dataset
df = pd.read_csv("labeled_malaysian_news.csv")

# Ensure required columns are present
df.dropna(subset=["title", "label"], inplace=True)
df.drop_duplicates(inplace=True)

# Function to replace a word with its synonym
def synonym_replacement(sentence, n=1):
    words = sentence.split()
    new_words = words.copy()
    for _ in range(n):
        word_to_replace = random.choice(words)
        synonyms = wordnet.synsets(word_to_replace)
        if synonyms:
            synonym = random.choice(synonyms).lemmas()[0].name()
            new_words = [synonym if word == word_to_replace else word for word in new_words]
    return " ".join(new_words)

# Function to randomly delete words
def random_deletion(sentence, p=0.2):
    words = sentence.split()
    if len(words) == 1:  # Don't delete single-word sentences
        return sentence
    new_words = [word for word in words if random.uniform(0, 1) > p]
    return " ".join(new_words) if new_words else random.choice(words)

# Augment a single class
def augment_class(df_class, target_count):
    augmented_data = []
    while len(df_class) + len(augmented_data) < target_count:
        row = df_class.sample(n=1).iloc[0]
        title = row["title"]
        label = row["label"]

        # Apply random augmentation
        if random.random() < 0.5:
            augmented_title = synonym_replacement(title)
        else:
            augmented_title = random_deletion(title)

        augmented_data.append({"title": augmented_title, "label": label})

    return pd.DataFrame(augmented_data)

# Balance dataset using augmentation
def balance_with_augmentation(df):
    max_size = df["label"].value_counts().max()
    balanced_df = pd.DataFrame()

    for label in df["label"].unique():
        class_df = df[df["label"] == label]
        if len(class_df) < max_size:
            augmented_df = augment_class(class_df, max_size)
            balanced_df = pd.concat([balanced_df, class_df, augmented_df])
        else:
            balanced_df = pd.concat([balanced_df, class_df])

    return balanced_df

# Apply augmentation and balance dataset
print("Balancing dataset with augmentation...")
balanced_df = balance_with_augmentation(df)

# Shuffle the dataset
balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save augmented dataset
balanced_df.to_csv("augmented_malaysian_news.csv", index=False)
print(f"Balanced dataset saved to 'augmented_malaysian_news.csv' with {len(balanced_df)} rows.")
