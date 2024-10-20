from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow as tf
import pickle
import json
import random
from difflib import SequenceMatcher  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Load the model and tokenizer
model = load_model('F:/ChatBotUI/basic_model.h5')
with open('F:/ChatBotUI/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('F:/ChatBotUI/intents.json', 'r') as f: 
    intents = json.load(f)['intents']

class Message(BaseModel):
    message: str

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
        
        # Find the most relevant intent by checking the patterns
        best_match_intent = None
        highest_similarity = 0  # Track the highest similarity score
        
        for intent in intents:
            for pattern in intent['patterns']:
                # Calculate similarity between the input message and each pattern
                similarity = SequenceMatcher(None, message.message.lower(), pattern.lower()).ratio()
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_match_intent = intent

        # If an intent is found, choose a response, otherwise provide a fallback response
        if best_match_intent:
            response = random.choice(best_match_intent['responses'])
        else:
            response = "I'm sorry, I don't have a response for that."

        return {"response": response}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
