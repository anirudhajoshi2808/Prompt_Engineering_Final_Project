import pandas as pd
import json
import re

# Load the CSV file
csv_file_path = '2024-08-13 6_09pm.csv'  # Update with your actual file path
df = pd.read_csv(csv_file_path)

# Assume default values for role, job description, and time commitment
default_role = 'Data Science'
default_job_description = (
    "Takeda Development Center Americas, Inc. is seeking a Cell Therapy Data Engineer in Cambridge, MA with the "
    "following requirements: Master’s degree in Information Technology, Information Systems, Data Analytics, "
    "Engineering, Computer Science, or related field plus 1 year of related experience. Prior experience must include: "
    "Utilize computing languages including R, C/C++, Python, and Java; Apply knowledge in distributed computing, "
    "databases (e.g., SQL), relational databases (e.g., PostgreSQL), and Amazon Web Services; Demonstrate experience in "
    "database programming and development of dashboards; Demonstrate experience in data integration, programming, and "
    "the objective evaluation & utilization of analytical tools & libraries"
)
default_time_commitment = 16  # hours per week

# Function to estimate duration in hours from text
def estimate_duration_in_hours(duration_text):
    # Try to extract a number (e.g., "3 months" -> 3)
    number_match = re.search(r'(\d+)', duration_text)
    if number_match:
        number = int(number_match.group(1))
        if 'month' in duration_text.lower():
            return number * 4 * 40  # Estimate 4 weeks/month * 40 hours/week
        elif 'week' in duration_text.lower():
            return number * 40  # Estimate 40 hours/week
        elif 'hour' in duration_text.lower():
            return number  # Already in hours
    return None  # If no estimation possible, return None

# Initialize a list to hold the formatted data
jsonl_data = []

# Iterate through each row in the dataframe and format it
for index, row in df.iterrows():
    # Estimate the duration in hours
    duration = estimate_duration_in_hours(row['DURATION'])

    # Skip rows where duration couldn't be estimated
    if duration is None:
        continue

    # Construct the prompt
    prompt = (
        f"The user is interested in a role as '{default_role}' and has provided the following job description: "
        f"'{default_job_description}'. They can commit {default_time_commitment} hours per week to learning. Based on "
        f"this information, please provide a detailed summary of the following course:\n\n"
        f"- **Course Title**: {row['TITLE']}\n"
        f"- **URL**: {row['URL']}\n"
        f"- **Description**: {row['DESCRIPTION']}\n"
        f"- **Duration**: {duration} hours\n"
        f"- **Rating**: {row['RATING']} stars\n"
        f"- **Viewers**: {row['VIEWERS']} people\n\n"
        "Please calculate how many weeks it would take for the user to complete this course based on their time "
        "commitment, and whether this fits the user's schedule. Please do not give hypothetical courses that do not "
        "have a URL. The structure of the output should be:\n"
        "1. Course Title:\n"
        "2. URL:\n"
        "3. Description:\n"
        "4. Duration:\n"
        "5. Rating:\n"
        "6. Viewers:\n"
        "7. Weekly Commitment Calculation:\n"
        "8. Total Time to complete the course:\n"
        "Keep the output under 250 words."
    )

    # Construct the completion
    completion = (
        f"Course Title: {row['TITLE']}\n"
        f"URL: {row['URL']}\n"
        f"Description: {row['DESCRIPTION']}\n"
        f"Duration: {duration} hours\n"
        f"Rating: {row['RATING']} stars\n"
        f"Viewers: {row['VIEWERS']} people\n"
        "Weekly Commitment Calculation:\n"
        f"o User's weekly commitment: {default_time_commitment} hours/week\n"
        "Total Time to complete the course:\n"
        f"o Total duration: {duration} hours\n"
        f"o Weekly commitment: {default_time_commitment} hours/week\n"
        f"o Total weeks required: {round(duration / default_time_commitment, 1)} weeks\n"
        f"The course will take approximately {round(duration / default_time_commitment, 1)} weeks to complete, given "
        f"the user’s time commitment of {default_time_commitment} hours per week. This fits the user's schedule well and "
        f"aligns with their career goals in {default_role}."
    )

    # Append the formatted data to the list in chat format
    jsonl_data.append({
        "messages": [
            {"role": "user", "content": prompt.strip()},
            {"role": "assistant", "content": completion.strip()}
        ]
    })

# Save the list as a .jsonl file
jsonl_file_path = 'chat_fine_tuning_data.jsonl'  # Update with your desired save location
with open(jsonl_file_path, 'w') as outfile:
    for entry in jsonl_data:
        json.dump(entry, outfile)
        outfile.write('\n')

print(f"Chat-format JSONL file created successfully at {jsonl_file_path}")
