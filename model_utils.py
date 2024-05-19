from transformers import BertTokenizer, BertModel
import torch

def load_model_and_tokenizer():
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    return tokenizer, model

def get_meal_embeddings(meals, tokenizer, model):
    embedding_dim = model.config.hidden_size
    meal_embeddings = torch.zeros(len(meals), embedding_dim)

    for i, meal in enumerate(meals):
        inputs = tokenizer(meal, return_tensors="pt", max_length=512, truncation=True)
        outputs = model(**inputs, return_dict=True)
        last_hidden_states = outputs.last_hidden_state
        pooled_output = last_hidden_states.mean(dim=1)
        meal_embeddings[i] = pooled_output

    return meal_embeddings