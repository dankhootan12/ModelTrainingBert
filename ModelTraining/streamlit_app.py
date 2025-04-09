import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load the model and tokenizer
@st.cache_resource
def load_model():
    tokenizer = BertTokenizer.from_pretrained("./bert_malaysian_news_model_augmented")
    model = BertForSequenceClassification.from_pretrained("./bert_malaysian_news_model_augmented")
    return tokenizer, model

tokenizer, model = load_model()

# Set device to CPU (Streamlit sharing doesn't support GPU)
device = torch.device("cpu")
model.to(device)

# Mapping of label indices to category names
label_dict = {
    0: "Business and Economy",
    1: "Science & Technology",
    2: "Environment",
    3: "Education",
    4: "World & Politics",
    5: "People and Living",
    6: "Travel & Culture",
    7: "Sports",
    8: "Crime",
    9: "Entertainment & Style",
    10: "Health and Family"
}

def predict(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=128, truncation=True, padding="max_length")
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_index = predictions.argmax().item()
        return label_dict[predicted_index]  # Return the category name

# Streamlit user interface
st.title('News Category Prediction')
news_text = st.text_area("Enter a news headline:")
if st.button("Classify"):
    if news_text.strip():  # Ensure input is not empty
        label_name = predict(news_text)
        st.write(f"The predicted category is: {label_name}")
    else:
        st.write("Please enter a valid news headline.")
