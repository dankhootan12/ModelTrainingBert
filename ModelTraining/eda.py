import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns

# Load the Dataset
df = pd.read_csv("labeled_malaysian_news.csv")  # Ensure this is the correct file name

# Step 1: Basic Dataset Information
print("Dataset Info:")
print(df.info())
print("\nDataset Description:")
print(df.describe())
print("\nFirst few rows:")
print(df.head())

# Check for Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# Drop rows with missing values for EDA
df = df.dropna()

# Check for Duplicates
print("\nChecking for duplicates:")
print(f"Number of duplicate rows: {df.duplicated().sum()}")

# Step 2: Label Distribution
print("\nLabel Distribution:")
label_counts = df["label"].value_counts()
print(label_counts)

# Visualize Label Distribution
plt.figure(figsize=(10, 6))
sns.countplot(y="label", data=df, order=label_counts.index, palette="viridis")
plt.title("Label Distribution")
plt.xlabel("Count")
plt.ylabel("Labels")
plt.show()

# Step 3: Text Data Exploration
# Word Count and Character Count
df["word_count"] = df["title"].apply(lambda x: len(str(x).split()))
df["char_count"] = df["title"].apply(lambda x: len(str(x)))

print("\nText Statistics:")
print(f"Average Word Count: {df['word_count'].mean()}")
print(f"Average Character Count: {df['char_count'].mean()}")

# Plot Word Count Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df["word_count"], kde=True, bins=20, color="blue")
plt.title("Word Count Distribution")
plt.xlabel("Word Count")
plt.ylabel("Frequency")
plt.show()

# Plot Character Count Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df["char_count"], kde=True, bins=20, color="green")
plt.title("Character Count Distribution")
plt.xlabel("Character Count")
plt.ylabel("Frequency")
plt.show()

# Step 4: Frequent Words
all_words = " ".join(df["title"].dropna()).split()
word_freq = Counter(all_words).most_common(20)

print("\nMost Common Words:")
print(word_freq)

# Visualize Most Common Words
common_words, word_counts = zip(*word_freq)
plt.figure(figsize=(12, 8))
sns.barplot(x=list(word_counts), y=list(common_words), palette="mako")
plt.title("Top 20 Most Frequent Words in Titles")
plt.xlabel("Frequency")
plt.ylabel("Words")
plt.show()

print("\nEDA completed.")
