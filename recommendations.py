import faiss
import torch
import random
from model_utils import load_model_and_tokenizer, get_meal_embeddings
from db import meals, prices

tokenizer, model = load_model_and_tokenizer()
meal_embeddings = get_meal_embeddings(meals, tokenizer, model)

embedding_dim = model.config.hidden_size
index = faiss.IndexFlatL2(embedding_dim)
index.add(meal_embeddings.detach().numpy())


def recommend_meal(preference, budget):
    inputs = tokenizer(preference, return_tensors="pt", max_length=512, truncation=True)
    outputs = model(**inputs, return_dict=True)
    last_hidden_states = outputs.last_hidden_state
    pooled_output = last_hidden_states.mean(dim=1)

    preference_embedding = torch.zeros(1, embedding_dim)
    preference_embedding[0] = pooled_output
    _, similar_meals = index.search(preference_embedding.detach().numpy(), 1)

    preference_words = set(preference.lower().split())
    meal_words = set(word.lower() for meal in meals for word in meal.split())
    if not bool(preference_words & meal_words):
        return "Sorry, couldn't find meals based on your search."

    meals_within_budget = [meals[i] for i in similar_meals[0] if prices[i] <= budget]
    if not meals_within_budget:
        return "Sorry, couldn't find meals within your budget."

    recommended_meal = random.choice(meals_within_budget)
    recommended_price = prices[meals.index(recommended_meal)]

    return f"{recommended_meal}, Price: {recommended_price}"
