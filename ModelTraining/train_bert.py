import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils.class_weight import compute_class_weight

# Check GPU availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the labeled dataset
df = pd.read_csv("labeled_malaysian_news.csv")

# Filter out missing or duplicate entries
df.dropna(subset=["title", "label"], inplace=True)
df.drop_duplicates(inplace=True)

# Encode labels
df["label_encoded"] = pd.factorize(df["label"])[0]

# Analyze class distribution
print("Category Distribution:")
print(df["label"].value_counts())

# Compute class weights
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=df["label_encoded"].unique(),
    y=df["label_encoded"]
)
class_weights_tensor = torch.tensor(class_weights, dtype=torch.float).to(device)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    df["title"], df["label_encoded"], test_size=0.2, random_state=42
)

# Define a custom dataset class
class NewsDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts.iloc[idx]
        label = self.labels.iloc[idx]

        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "label": torch.tensor(label, dtype=torch.long),
        }

# Initialize tokenizer and datasets
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
train_dataset = NewsDataset(X_train, y_train, tokenizer, max_length=128)
test_dataset = NewsDataset(X_test, y_test, tokenizer, max_length=128)

# Create DataLoaders
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

# Initialize the model
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=len(df["label_encoded"].unique())
)
model.to(device)

# Optimizer and loss function
optimizer = AdamW(model.parameters(), lr=2e-5, eps=1e-8)
loss_fn = torch.nn.CrossEntropyLoss(weight=class_weights_tensor)

# Training loop with accuracy calculation
def train_model(model, train_loader, loss_fn, optimizer, epochs=3):
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        correct_predictions = 0
        total_samples = 0

        for batch in train_loader:
            optimizer.zero_grad()
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            loss = loss_fn(logits, labels)

            # Update gradients and optimizer
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

            # Calculate training accuracy for the current batch
            preds = torch.argmax(logits, axis=1)
            correct_predictions += (preds == labels).sum().item()
            total_samples += labels.size(0)

        # Calculate epoch-level accuracy
        epoch_accuracy = correct_predictions / total_samples

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(train_loader):.4f}, Accuracy: {epoch_accuracy:.4f}")

# Evaluation function
def evaluate_model(model, test_loader):
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            outputs = model(input_ids, attention_mask=attention_mask)
            preds = torch.argmax(outputs.logits, axis=1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    accuracy = accuracy_score(all_labels, all_preds)
    print("\nAccuracy:", accuracy)
    print("\nClassification Report:")
    print(classification_report(all_labels, all_preds))

# Train and evaluate
train_model(model, train_loader, loss_fn, optimizer, epochs=3)
evaluate_model(model, test_loader)

# Save the trained model
model.save_pretrained("bert_malaysian_news_model")
tokenizer.save_pretrained("bert_malaysian_news_model")
print("Model saved successfully!")
