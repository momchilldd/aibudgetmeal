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

custom_css = """
    .container {
        max-width: 800px;
        margin: auto;
        padding: 2em;
        background-color: #f9f9f9;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    h1 {
        text-align: center;
        color: #333;
    }
    p {
        text-align: center;
        color: #666;
    }
    .input-textbox, .output-textbox {
        font-size: 1.2em;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .slider {
        margin: 20px 0;
    }
    .btn-primary {
        background-color: #28a745;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 1em;
    }
"""


iface.launch(share=True)
