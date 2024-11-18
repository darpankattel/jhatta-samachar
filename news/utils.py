from news.models import News
from datasets import load_dataset
from transformers import T5ForConditionalGeneration, T5Tokenizer
from django.conf import settings
import os

model = T5ForConditionalGeneration.from_pretrained(os.path.join(
    settings.BASE_DIR, 'models/kaggle/working/pre_trained/model/pretrained_t5-small'))
tokenizer = T5Tokenizer.from_pretrained(os.path.join(
    settings.BASE_DIR, 'models/kaggle/working/pre_trained/model/pretrained_t5-small-tokenizer'))


def summarize(article: str) -> str:
    inputs = tokenizer(
        f"summarize: {article}", return_tensors='pt', max_length=1024, truncation=True)
    summary_ids = model.generate(inputs['input_ids'], max_length=150,
                                 min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


def get_news_summary(news: News) -> str:
    """
    Generate summaries for news articles.

    :param news: An instance of a news article.
    :return: A summary of the news article.
    """
    summary = summarize(f"{news.content}")
    return summary
