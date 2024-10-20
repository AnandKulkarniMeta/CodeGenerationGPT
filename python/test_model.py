import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle
import json

# Load your tokenizer
with open('F:/ChatBotUI/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load your model
model = load_model('F:/ChatBotUI/basic_model.h5')

# Load intents from a JSON file
def load_intents(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data['intents']

# Specify the path to your JSON file containing intents
intents_file_path = 'F:/ChatBotUI/intents.json'
intents = load_intents(intents_file_path)

# Function to get responses based on the predicted tag
def get_responses(tag):
    for intent in intents:
        if intent['tag'] == tag:
            return intent['responses']
    return ["I'm sorry, I don't have a response for that."]

# Sample input message for testing
test_message = "Write a function for selection sort"

# Function to preprocess input message
def preprocess_message(message):
    sequences = tokenizer.texts_to_sequences([message])
    padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=50)  # Adjust maxlen as needed

    # Reshape to match expected input shape (1, 1, 43)
    if padded_sequences.shape[1] < 43:
        reshaped_sequences = np.pad(padded_sequences, ((0, 0), (0, 43 - padded_sequences.shape[1])), 'constant')
    else:
        reshaped_sequences = padded_sequences[:, :43]
    
    reshaped_sequences = np.expand_dims(reshaped_sequences, axis=1)  # Shape (1, 1, 43)
    
    return reshaped_sequences

# Preprocess the test message
preprocessed_message = preprocess_message(test_message)

# Make a prediction
try:
    prediction = model.predict(preprocessed_message)
    
    # Print the raw prediction output for debugging
    print(f"Raw Prediction Output: {prediction}")

    # Get the predicted index
    response_idx = np.argmax(prediction, axis=-1)[0]
    
    # Map index to the corresponding tag if your model outputs the tag directly
    # For example, you might have a list of tags corresponding to the outputs
    # Here we assume the order of tags in intents corresponds to the model's output
    predicted_tag = intents[response_idx]['tag']
    
    # Get possible responses for the predicted tag
    responses = get_responses(predicted_tag)

    # Randomly select a response from the list of possible responses
    import random
    selected_response = random.choice(responses)

    print(f"Predicted Response Index: {response_idx}")
    print(f"AI Response: {selected_response}")
except Exception as e:
    print(f"An error occurred during prediction: {e}")
