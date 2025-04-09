import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample

# Load the  Dataset
df = pd.read_csv("labeled_malaysian_news.csv")  # Ensure this file exists
print("First few rows of the dataset:")
print(df.head())

# Select Relevant Columns
df = df[["title", "label"]]
print("\nSelected columns:")
print(df.head())

# Rename 'Column1' to 'title'
df.rename(columns={"Column1": "title"}, inplace=True)

# Check for Missing Values and Duplicates
print("\nChecking for missing values:")
print(df.isnull().sum())  # Check for any missing values

# Drop rows with missing values
df = df.dropna()
print(f"Dataset shape after removing missing values: {df.shape}")

print("\nChecking for duplicates:")
print(f"Number of duplicate rows: {df.duplicated().sum()}")

# Drop duplicates if any
df = df.drop_duplicates()
print(f"Dataset shape after removing duplicates: {df.shape}")

# Address Class Imbalance (Oversampling)
print("\nBalancing the dataset...")
def balance_dataset(df):
    classes = df["label"].unique()
    max_size = df["label"].value_counts().max()
    balanced_df = pd.DataFrame()

    for label in classes:
        class_samples = df[df["label"] == label]
        if len(class_samples) < max_size:
            # Oversample the minority class
            oversampled = resample(
                class_samples,
                replace=True,
                n_samples=max_size,
                random_state=42
            )
            balanced_df = pd.concat([balanced_df, oversampled])
        else:
            balanced_df = pd.concat([balanced_df, class_samples])

    return balanced_df

df = balance_dataset(df)
print("Balanced dataset:")
print(df["label"].value_counts())

# Encode the Labels
print("\nEncoding labels...")
encoder = LabelEncoder()

# Encode the labels in the "label" column
df["label_encoded"] = encoder.fit_transform(df["label"])
print("Label encoding mapping:")
print(df[["label", "label_encoded"]].drop_duplicates())

# Split the Dataset into Training and Testing Sets
print("\nSplitting dataset into training and testing sets...")
X = df["title"]  # News titles as features
y = df["label_encoded"]  # Encoded labels as target

# Stratified Split to maintain label distribution in train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

# Save Processed Data
# Save the train and test splits to CSV files
X_train.to_csv("X_train.csv", index=False, header=False)
X_test.to_csv("X_test.csv", index=False, header=False)
y_train.to_csv("y_train.csv", index=False, header=False)
y_test.to_csv("y_test.csv", index=False, header=False)
print("\nProcessed data saved to CSV files.")


print("\nPreprocessing completed successfully.")
