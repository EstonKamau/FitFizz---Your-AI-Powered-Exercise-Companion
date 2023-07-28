import os
import openai
import panel as pn

# Set up OpenAI API key
openai.api_key = "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"

# Function to get GPT-3 response
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

# Function to process food input and get GPT-3 response for calories
def on_food_enter_click(event):
    context = [{'role': 'user', 'content': f""" 
                In less than 10 words approximate the total amount of calories in the food. \
                If it is not a food politely ask the consumer to give an appropriate input. \
                the food is delimited with triple backticks. \
                Food Intake: '''{input_food.value}'''
                """}]
    response = get_completion_from_messages(context)
    output_calories.object = f" {response}"

# Function to collect user inputs and get GPT-3 response for exercise recommendation
def on_exercise_enter_click(event):
    user_inputs = {
        "Height": input_height.value,
        "Age": input_age.value,
        "Current Weight": input_weight.value,
        "Weight to Lose per Week": input_weight_loss.value,
        "Food Intake": input_food.value,
        "Gym Equipment": input_gym_equipment.value,
        "Exercise Days per Week": input_exercise_days.value,
        "Minutes per Day": input_minutes_per_day.value,
        "Other Information": input_other_info.value
    }

    context2 = []
    for key, value in user_inputs.items():
        context2.append({'role': 'user', 'content': f"{key}: {value}"})
    context3 = [{'role': 'user', 'content': f"""
                 In context2 that is delimited with triple backticks is a list of user characteristics in form of key and value.
                 You are supposed to take that information and prepare a well presented and detailed exercise session for that day.
                 Take the weight the user aims to loose for that week and divide it by the number of days he plans to exercise for that week to get the amount of weight he should loose for that day. 
                 Use that information together with the other user's information to generate a well designed workout. 
                 Make sure the exercises have the highest probability to help the user achieve his desired goal for that day. 
                 If any of the important information like age, weight, weight to loose is missing, unclear or wildly ambiguous politely ask the user to clarify. 
                 When generating the workouts, dont give any other information other than the workouts and briefly describe them
                 Present the workout in short sentences and in bullets in this format:

                 1. Warm-up:
                    - Spend...
                 2. ...
                 ...
                 N
                 
                 '''{context2}'''
                 """}]
    response = get_completion_from_messages(context3)
    output_exercise.object = f"{response}"

# Create input widgets
input_height = pn.widgets.TextInput(name="Height (in meters)", placeholder="e.g., 1.75")
input_age = pn.widgets.IntInput(name="Age", value=25)
input_weight = pn.widgets.FloatInput(name="Current Weight (in kg)", value=70.0)
input_weight_loss = pn.widgets.FloatInput(name="Weight to Lose per Week (in kg)", value=0.5)
input_food = pn.widgets.TextAreaInput(name="What did you eat today?", placeholder="Enter food details...")
input_gym_equipment = pn.widgets.TextInput(name="Briefly list gym equipment (if available)", placeholder="e.g., Treadmill, Dumbbells")
input_exercise_days = pn.widgets.IntInput(name="Exercise Days per Week", value=5)
input_minutes_per_day = pn.widgets.IntInput(name="Minutes per Day", value=30)
input_other_info = pn.widgets.TextAreaInput(name="Any other information?", placeholder="Enter any other relevant information...")

# Create output widget for exercise recommendation
output_calories = pn.pane.Str(sizing_mode="stretch_width", height=50, styles={"white-space": "pre-wrap"})
output_exercise = pn.pane.Str(sizing_mode="stretch_width", height=300, styles={"white-space": "pre-wrap"})

# Create "Enter" buttons
btn_food_enter = pn.widgets.Button(name="Calculate Calories", button_type="primary")
btn_exercise_enter = pn.widgets.Button(name="Enter", button_type="primary")

# Assign click events to buttons
btn_food_enter.on_click(on_food_enter_click)
btn_exercise_enter.on_click(on_exercise_enter_click)

# Create layout for the app
layout = pn.Column(
    "# FitFizz",
    "***Fizz Your Way to Fitness***",
    pn.layout.Divider(),
    pn.Column(
        pn.pane.Markdown("## User Information"),
        pn.Row(input_height, input_age),
        pn.Row(input_weight, input_weight_loss),
        pn.layout.Divider(),
        pn.pane.Markdown("## Food Intake"),
        pn.Row(input_food, btn_food_enter),
        pn.pane.Markdown("#### Approximate Calories"),
        output_calories,
        pn.layout.Divider(),
        pn.pane.Markdown("## Workout Plan"),
        input_gym_equipment,
        pn.Row(input_exercise_days, input_minutes_per_day),
        pn.layout.Divider(),
        pn.pane.Markdown("## Other Information"),
        input_other_info,
        btn_exercise_enter
    ),
    
    pn.layout.Divider(),     
    pn.pane.Markdown("## Exercise Recommendation"),
    output_exercise
)


# Add custom CSS style for the enter buttons
css_style = """
.enter-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    font-size: 16px;
    cursor: pointer;
}

.enter-button:hover {
    background-color: #45a049;
}
"""

pn.config.raw_css.append(css_style)

# Run the app
if __name__ == "__main__":
    layout.show()













