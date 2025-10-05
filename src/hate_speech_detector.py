import torch
from transformers import BertTokenizer, BertForSequenceClassification
from pathlib import Path


class HateSpeechDetector:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = Path(__file__).parent.parent / "models" / "bert_hatespeech"
            model_path = str(model_path)

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path).to(self.device)
        self.model.eval()
        self.labels = ['normal', 'offensive', 'hate']

    def predict(self, text):
        encoding = self.tokenizer(
            text,
            max_length=128,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            probabilities = torch.softmax(outputs.logits, dim=1)
            prediction = torch.argmax(probabilities, dim=1).item()

        return {
            'label': self.labels[prediction],
            'confidence': probabilities[0][prediction].item(),
            'probabilities': {label: prob.item() for label, prob in zip(self.labels, probabilities[0])}
        }
