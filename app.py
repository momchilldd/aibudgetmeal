import gradio as gr
from recommendations import recommend_meal
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def recommend_meal_wrapper(preference, budget):
    if not preference:
        return "Please enter a meal preference."
    if budget < 1 or budget > 50:
        return "Please enter a budget between 1 and 50."
    
    return recommend_meal(preference, budget)

# Create an enhanced Gradio interface with a description and examples
iface = gr.Interface(
    fn=recommend_meal_wrapper,
    inputs=[
        gr.Textbox(label="Meal Preference", placeholder="Enter your preference"),
        gr.Slider(minimum=1, maximum=50, label="Budget")
    ],
    outputs=gr.Textbox(label="Recommended Meal"),
    live=True,
    title="AI Budget Meal Assistant",
    description="Get meal recommendations based on your preferences and budget. Enter a type of meal you like and your budget, and I'll suggest something delicious!",

)

iface.launch(share=True)