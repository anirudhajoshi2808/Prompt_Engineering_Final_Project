import requests
import base64

# Your client credentials
client_id = "GQGTQiAI842hJ2QYQenpatlK64MCimmzbpfSI5eRTtZkCGV8"
client_secret = "1TnnU6K1ibyGz4BQplmbnHwMCsBBL6XahW7OoIJjuGgrV83qK3yjILRl9UrSEGQF"

# Encode credentials in Base64 (client_id:client_secret)
client_credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(client_credentials.encode()).decode()

# Set headers
headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Prepare the payload
payload = {
    "grant_type": "client_credentials"
}

# Send POST request to obtain the token
response = requests.post("https://api.coursera.com/oauth2/client_credentials/token", headers=headers, data=payload)

# Print the response
print("Status Code:", response.status_code)
print("Response Content:", response.text)

# Attempt to parse the JSON response
try:
    response_json = response.json()
    print(response_json)
except ValueError as e:
    print("Failed to parse JSON:", e)
