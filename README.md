---

# Chatbot Application

## Overview

This project is a simple chatbot application that leverages a FastAPI backend and a React frontend. The chatbot uses a machine learning model to provide responses based on user input, and it features a user-friendly interface for interaction.

## Features

- **User Interface**: A responsive React-based UI that allows users to send messages and receive responses from the chatbot.
- **FastAPI Backend**: A RESTful API built with FastAPI to handle user requests and respond with appropriate messages based on a trained machine learning model.
- **Message Prediction**: Utilizes a TensorFlow model to predict user intents and generate appropriate responses.
- **Error Handling**: Includes error handling for network issues and timeout scenarios.
- **Fuzzy Matching**: Implements fuzzy matching to improve intent recognition and response accuracy.

## Technologies Used

- **Frontend**: 
  - React
  - Axios for API calls
  - CSS for styling

- **Backend**:
  - FastAPI for the API framework
  - TensorFlow and Keras for the machine learning model
  - Pickle for model serialization
  - JSON for handling intent data

## Installation

### Prerequisites

1. Python 3.x
2. Node.js and npm
3. TensorFlow
4. FastAPI
5. React

### Backend Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required Python packages:
   ```bash
   pip install fastapi uvicorn tensorflow numpy pickle5
   ```

3. Ensure your model (`basic_model.h5`), tokenizer (`tokenizer.pkl`), and intents JSON (`intents.json`) are available in the specified paths in your FastAPI code.

4. Run the FastAPI server:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```

2. Install the required Node packages:
   ```bash
   npm install
   ```

3. Start the React application:
   ```bash
   npm start
   ```

## Usage

1. Open your web browser and navigate to `http://localhost:3000` to access the chatbot interface.
2. Type your message in the input area and hit enter to send it.
3. The chatbot will respond based on the input and its trained model.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT WPU License.

---
