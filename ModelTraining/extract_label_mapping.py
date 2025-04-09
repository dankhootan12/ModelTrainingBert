import pandas as pd
from sklearn.preprocessing import LabelEncoder

def main():
    # Load the dataset
    df = pd.read_csv("labeled_malaysian_news.csv")

    # Ensure there are no missing values in 'label' column
    df.dropna(subset=['label'], inplace=True)

    # Initialize the label encoder
    encoder = LabelEncoder()

    # Fit the encoder to the labels
    df['label_encoded'] = encoder.fit_transform(df['label'])

    # Create a mapping from encoded labels back to original labels
    label_mapping = dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))

    # Print the mapping
    print("Label to integer mapping:", label_mapping)

    # Optionally, save this mapping to a file
    with open('label_mapping.txt', 'w') as f:
        for label, encoded in label_mapping.items():
            f.write(f"{encoded}: {label}\n")
    print("Mapping saved to 'label_mapping.txt'.")

if __name__ == "__main__":
    main()
