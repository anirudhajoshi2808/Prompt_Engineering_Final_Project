import pandas as pd

# Load the Online Courses dataset
online_courses_df = pd.read_csv('data/Online_Courses.csv')

# Define the required columns
required_columns = [
    'Title', 'URL', 'Short Intro', 'Category', 'Sub-Category', 'Course Type',
    'Language', 'Subtitle Languages', 'Skills', 'Instructors', 'Rating',
    'Number of viewers', 'Duration', 'Site'
]

# Ensure all required columns are present in the DataFrame
for col in required_columns:
    if col not in online_courses_df.columns:
        online_courses_df[col] = None  # Add missing columns with None values

# Filter out rows where 'URL' is missing or empty
online_courses_df = online_courses_df.dropna(subset=['URL']).reset_index(drop=True)

# Remove duplicate rows
online_courses_df = online_courses_df.drop_duplicates()

# Save the cleaned dataset to a new CSV file
output_file_path = 'data/cleaned_online_courses.csv'
online_courses_df.to_csv(output_file_path, index=False)

print("Cleaned CSV file has been created successfully.")
