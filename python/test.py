import requests

# URL of your FastAPI server
url = "http://localhost:8000/predict"  # Update this if your backend runs on a different port

# Sample message to test the model
data = {
    "message": "quick sort"
}

try:
    # Send POST request to the backend
    response = requests.post(url, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        result = response.json()
        print(f"AI Response: {result.get('response')}")
    else:
        print(f"Failed to communicate with backend. Status code: {response.status_code}")
        print(f"Error: {response.text}")

except Exception as e:
    print(f"An error occurred: {e}")
