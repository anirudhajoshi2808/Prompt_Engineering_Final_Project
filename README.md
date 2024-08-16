# Custom Learning Paths for Your Next Job Interview

## Applications
[![Demo Video](https://img.shields.io/badge/Video-CC6699?style=for-the-badge)](https://www.youtube.com/watch?v=fD6B2vpPlX8)
[![Application Link](https://img.shields.io/badge/Application-green?style=for-the-badge)](https://promptengineeringfinalproject-hbrr4esveegtan4vbbhyfd.streamlit.app/)

## Project Overview

This project aims to provide personalized course recommendations to help users prepare for job interviews by creating custom learning paths. The application extracts data from multiple online learning platforms such as Coursera, Udemy, edX, MIT OpenCourseWare, and Udacity using their respective APIs. After cleaning the data, it is stored in Snowflake and then further processed using LangChain to chunk the data. These chunks are stored in Pinecone's vector database, which allows for efficient cosine similarity searches. The system also fine-tunes a GPT-4 model to generate tailored course recommendations based on user inputs.

## Problem Statement

Job seekers often struggle to find the most relevant and effective learning resources to prepare for specific job roles. This project addresses this challenge by providing custom-tailored course recommendations that align with the user's career goals, job description, and time commitment.

## Key Features

- **Data Collection & Storage**: Extracted data from Coursera, Udemy, edX, MIT OCW, and Udacity APIs. The data was cleaned and stored in Snowflake.
- **Data Chunking**: Converted the data into manageable chunks using LangChain, solving the issue of identifying records corresponding to individual courses.
- **Vector Storage**: Stored the chunked data in Pinecone using LangChain's `PineconeVectorStore` along with the associated metadata.
- **Resume Analysis**: Users upload their resume, which is converted to text using PyPDF2, along with the job title, job description, and their weekly time commitment.
- **Course Recommendations**: OpenAI API provides a tailored list of the top 5 courses after performing a cosine similarity search.
- **Model Fine-Tuning**: Fine-tuned a GPT-4 model using 100 prompts and 100 responses for better accuracy in generating recommendations.

## Technology Stack

[![OpenAI](https://img.shields.io/badge/OpenAI-6BA539?style=for-the-badge&logo=OpenAI&logoColor=black)](https://openai.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-A100FF?style=for-the-badge)](https://www.pinecone.io/)
[![Snowflake](https://img.shields.io/badge/Snowflake-29A8E0?style=for-the-badge&logo=snowflake&logoColor=white)](https://www.snowflake.com/)
[![LangChain](https://img.shields.io/badge/LangChain-FF6B6B?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![PyPDF2](https://img.shields.io/badge/PyPDF2-6A9F98?style=for-the-badge&logo=python&logoColor=white)](https://pypdf2.readthedocs.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

## Project Structure

```
FinalProject
├── backend
│   ├── chunks_text.py
│   ├── clean_data.py
│   ├── coursera.py
│   ├── data
│   │   ├── Coursera.csv
│   │   ├── Online_Courses.csv
│   │   ├── Udemy.csv
│   │   ├── cleaned_online_courses.csv
│   │   ├── combined_online_learning_resources.csv
│   │   ├── edx.csv
│   │   └── skillshare.csv
│   ├── output.txt
│   ├── pinecone_transfer.py
│   └── snowflake_transfer.py
├── finetuning
│   ├── 2024-08-13 6_09pm.csv
│   ├── chat_fine_tuning_data.jsonl
│   ├── fine_tuning_data.jsonl
│   └── test.py
├── frontend
│   └── app.py
└── requirements.txt
```


## How to Use the Application

1. **Upload Inputs**: Upload your resume (in PDF format), job title, job description, and your weekly time commitment.
2. **Receive Recommendations**: The application processes your input and provides you with the top 5 recommended courses tailored to your job preparation needs.
3. **Interactive Interface**: Use the Streamlit interface for a seamless experience in navigating through the recommendations and related features.

## References

- [ChatGPT](https://chat.openai.com/)
- [OpenAI API](https://openai.com/)
- [Pinecone](https://www.pinecone.io/learn/vector-database/)
- [Snowflake](https://www.snowflake.com/)
- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)

## Contributors

| Name            | Contribution % | Contributions                                                                                            |LinkedIn                                       |Email                     |
|-----------------|----------------|----------------------------------------------------------------------------------------------------------|-----------------------------------------------|--------------------------|
| Anirudha Joshi  | 100%            | Data extraction, storage, processing, vector database setup, OpenAI fine-tuning, application deployment. |https://www.linkedin.com/in/anirudhajoshi424/ | joshi.anir@northeastern.edu |



