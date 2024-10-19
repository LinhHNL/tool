import pandas as pd
import json

# Read JSON data from file
with open('questions.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Flatten the JSON data
data = []
for quiz in json_data:
    for question in quiz["questions"]:
        question_text = question["question"].replace("\n", " ")  # Clean up the question text
        options = question["options"]
        
        # Prepare row data
        row = {
            "Question Text": question_text,
            "Question Type": "Multiple Choice",  # Default type; you can change it as needed
            "Option 1": options[0]["option"] if len(options) > 0 else "",
            "Option 2": options[1]["option"] if len(options) > 1 else "",
            "Option 3": options[2]["option"] if len(options) > 2 else "",
            "Option 4": options[3]["option"] if len(options) > 3 else "",
            "Option 5": "",  # Leave blank as per your format
            "Correct Answer": str(next(i + 1 for i, opt in enumerate(options) if opt["is_correct"])) if any(opt["is_correct"] for opt in options) else "",
            "Time in seconds": 20  # Default time; adjust if needed
        }
        data.append(row)

# Create a DataFrame
df = pd.DataFrame(data)

# Save to Excel
df.to_excel("quiz_data_formatted.xlsx", index=False)
