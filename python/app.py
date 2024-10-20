from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow as tf
import pickle
import json
import random

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Load the model and tokenizer
model = load_model('F:/ChatBotUI/basic_model.h5')
with open('F:/ChatBotUI/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load responses from the JSON file
with open('F:/ChatBotUI/intents.json', 'r') as f: 
    intents = json.load(f)['intents']

# Define request body schema
class Message(BaseModel):
    message: str

# Preprocessing function with reshaping logic
def preprocess_message(message):
    sequences = tokenizer.texts_to_sequences([message])
    padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=50)  # Adjust maxlen

    # Reshape to match expected input shape (1, 1, 43)
    if padded_sequences.shape[1] < 43:
        reshaped_sequences = np.pad(padded_sequences, ((0, 0), (0, 43 - padded_sequences.shape[1])), 'constant')
    else:
        reshaped_sequences = padded_sequences[:, :43]
    
    reshaped_sequences = np.expand_dims(reshaped_sequences, axis=1)  # Shape (1, 1, 43)
    
    return reshaped_sequences

# Prediction endpoint
@app.post("/predict")
async def predict(message: Message):
    try:
        # Preprocess the input message
        preprocessed_message = preprocess_message(message.message)

        # Make prediction
        prediction = model.predict(preprocessed_message)
        response_idx = np.argmax(prediction, axis=-1)[0]

        # Get the tag associated with the predicted index
        predicted_tag = intents[response_idx]['tag']
        
        # Find the corresponding responses for the predicted tag
        responses = None
        for intent in intents:
            if intent['tag'] == predicted_tag:
                responses = intent['responses']
                break
        
        # Randomly select a response from the list of possible responses
        if responses:
            response = random.choice(responses)
        else:
            response = "I'm sorry, I don't have a response for that."

        return {"response": response}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
