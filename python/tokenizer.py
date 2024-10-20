import json
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle

# Load your dataset
with open('F:/ChatBotUI/intents.json', 'r') as file:
    data = json.load(file)

# Extract all patterns (user inputs)
patterns = []
for intent in data['intents']:
    patterns.extend(intent['patterns'])

# Initialize the Tokenizer
tokenizer = Tokenizer(oov_token="<OOV>")  # OOV token for handling out-of-vocabulary words
tokenizer.fit_on_texts(patterns)

# Save the tokenizer as a .pkl file
with open('F:/ChatBotUI/tokenizer.pkl', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("Tokenizer created and saved!")
