# from pinecone import Pinecone, Index, ServerlessSpec
# import os
# from sentence_transformers import SentenceTransformer
# from dotenv import load_dotenv

# load_dotenv()
# # Read the chunks from the output.txt file
# with open('output.txt', 'r') as file:
#     formatted_rows = file.readlines()

# # Strip any leading/trailing whitespace characters (like newlines)
# formatted_rows = [row.strip() for row in formatted_rows]

# # Initialize Pinecone
# PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
# PINECONE_INDEX_NAME = 'interview-prep'

# pc = Pinecone(api_key=PINECONE_API_KEY)

# # List all indexes
# index_list = pc.list_indexes()

# # if PINECONE_INDEX_NAME not in index_list:
# #     # Create index if it doesn't exist
# #     pc.create_index(
# #         name=PINECONE_INDEX_NAME,
# #         dimension=384,  # Adjust based on your vector model
# #         metric='cosine',
# #         spec=ServerlessSpec(
# #             cloud='aws',
# #             region='us-east-1'
# #         )
# #     )

# # Access the existing index
# index = pc.Index(PINECONE_INDEX_NAME)

# # Initialize a model for text to vector conversion
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Convert rows to vectors and store in Pinecone
# for i, row in enumerate(formatted_rows):
#     vector = model.encode(row).tolist()
#     index.upsert(vectors=[(str(i), vector)])  # Use the row index or any unique ID as the identifier

# # Close the Pinecone connection
# index.close()



import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load environment variables
load_dotenv()

# Pinecone API key and initialization
pinecone_api_key = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=pinecone_api_key)

# Index name
index_name = "interview-prep"

# Check if the index exists, and create if not
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=384,  # Adjust dimension based on your embeddings model
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

# Access the existing index
index = pc.Index(index_name)

# Function to split text and store in Pinecone
def create_pinecone_index_and_store(structured_text_file_path, index_name):
    # Read the text from the file
    with open(structured_text_file_path, 'r') as file:
        text = file.read()
   
    # Manually split the text into chunks using '##' as the delimiter
    text_chunks = [chunk for chunk in text.split("####") if chunk.strip()]
   
    # Initialize the HuggingFace embeddings model
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Create a Pinecone Vector Store and add the text chunks
    docsearch = PineconeVectorStore.from_texts(text_chunks, embeddings, index_name=index_name)
    
    # Wait briefly to ensure everything is processed
    time.sleep(10)
    
    return docsearch

# Example usage
structured_text_file_path = 'output.txt'  # Path to your structured text file
docsearch = create_pinecone_index_and_store(structured_text_file_path, index_name)


