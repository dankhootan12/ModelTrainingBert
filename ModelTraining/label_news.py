import pandas as pd

# Load the dataset
input_file = "latest_malaysian_news.csv"  # Replace with your file name
output_file = "labeled_malaysian_news.csv"

df = pd.read_csv(input_file)

# Fill missing titles with a placeholder and ensure all titles are strings
df["title"] = df["title"].fillna("Unknown Title")  # Replace NaN with placeholder
df["title"] = df["title"].astype(str)  # Ensure all titles are strings

# Define categories and keywords
categories = {
    "Politics": [
        "election", "government", "minister", "policy", "parliament",
        "senate", "president", "cabinet", "campaign", "bill", "legislation"
    ],
    "Sports": [
        "football", "soccer", "Olympics", "match", "team", "tournament",
        "league", "cricket", "badminton", "athletics", "game", "championship"
    ],
    "Technology": [
        "tech", "AI", "gadget", "software", "innovation", "robot",
        "blockchain", "cybersecurity", "internet", "mobile", "startup",
        "data", "cloud", "digital", "machine learning", "coding", "algorithm"
    ],
    "Health": [
        "covid", "vaccine", "hospital", "health", "disease", "pandemic",
        "virus", "medicine", "surgery", "therapy", "treatment", "mental health",
        "diet", "fitness", "doctor", "nurse"
    ],
    "Business": [
        "economy", "market", "business", "stock", "finance", "investment",
        "revenue", "startup", "trade", "profit", "loss", "industry", "tax",
        "inflation", "bank", "loan", "real estate"
    ],
    "Entertainment": [
        "movie", "film", "celebrity", "music", "concert", "festival",
        "actor", "actress", "award", "song", "album", "show", "performance",
        "series", "drama", "comedy"
    ],
    "Education": [
        "school", "university", "exam", "student", "teacher", "education",
        "curriculum", "college", "scholarship", "learning", "study", "degree",
        "class", "course", "tuition"
    ],
    "Environment": [
        "climate", "pollution", "wildlife", "forest", "nature", "renewable",
        "recycling", "conservation", "biodiversity", "green", "energy",
        "global warming", "sustainability", "carbon", "fossil fuels"
    ],
    "Crime": [
        "crime", "murder", "arrest", "police", "court", "theft", "fraud",
        "prison", "trial", "robbery", "assault", "drug", "gang", "shooting"
    ],
    "World": [
        "war", "international", "diplomacy", "foreign", "global", "country",
        "conflict", "UN", "NATO", "peace", "summit", "relations", "treaty"
    ],
    "Science": [
        "research", "space", "experiment", "discovery", "biology", "physics",
        "chemistry", "genetics", "astronomy", "nasa", "scientist", "technology",
        "innovation", "breakthrough"
    ],
    "Lifestyle": [
        "fashion", "travel", "food", "recipe", "luxury", "hobby", "home",
        "design", "décor", "style", "trend", "lifestyle", "culture", "art"
    ]
}

# Step 4: Function to assign labels based on keywords
def assign_label(title):
    for category, keywords in categories.items():
        if any(keyword.lower() in title.lower() for keyword in keywords):
            return category
    return "Unknown"  # Assign "Unknown" if no category matches

# Step 5: Apply the labeling function
df["label"] = df["title"].apply(assign_label)

# Step 6: Save the labeled dataset
df.to_csv(output_file, index=False)
print(f"Data saved to {output_file} with {len(df)} articles.")

# Step 7: Analyze labeled data (optional)
label_counts = df["label"].value_counts()
print("\nLabel distribution:")
print(label_counts)
