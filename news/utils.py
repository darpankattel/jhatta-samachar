from news.models import News
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load your transformer model
model = load_model('models/transformer.latest.keras')

# Tokenization and padding (example, modify as per your model's requirements)
tokenizer = Tokenizer()  # Initialize the tokenizer
# Load your tokenizer's word index if you have one
# tokenizer.word_index = {...}  # Uncomment and define if needed


def preprocess_text(content: str) -> np.array:
    """
    Preprocess the news content for the transformer model.

    :param content: The news content to be summarized.
    :return: Preprocessed input for the model.
    """
    # Convert to lower case
    content = content.lower()

    # Tokenization
    sequences = tokenizer.texts_to_sequences([content])

    # Padding sequences to ensure uniform input size
    padded_sequences = pad_sequences(
        sequences, maxlen=500)  # Adjust maxlen as needed

    return padded_sequences


def generate_summary(predictions: np.array) -> str:
    """
    Generate a human-readable summary from the model's predictions.

    :param predictions: The output from the model.
    :return: A summarized string.
    """
    # Post-processing logic to convert model predictions to text
    # This is a placeholder; you need to implement this according to your model's output
    summary = " ".join([str(pred) for pred in predictions])

    return summary


def get_news_summary(news: News) -> str:
    """
    Generate summaries for news articles.

    :param news: An instance of a news article.
    :return: A summary of the news article.
    """
    return "hehe"
    # Step 1: Preprocess the news content
    preprocessed_content = preprocess_text(news.content)

    # Step 2: Generate predictions using the transformer model
    predictions = model.predict(preprocessed_content)

    # Step 3: Convert model predictions to a readable summary
    summary = generate_summary(predictions)

    return summary
