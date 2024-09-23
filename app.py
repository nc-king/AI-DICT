from flask import Flask, request, jsonify, send_from_directory
import nltk
from nltk.corpus import wordnet
import difflib
import requests
import openai  # OpenAI library for generating images

# Download WordNet data
nltk.download('wordnet')

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = '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'  # Replace with your OpenAI API key

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def styles():
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')

@app.route('/define', methods=['GET'])
def define():
    word = request.args.get('word')
    if not word:
        return jsonify({'error': 'No word provided'}), 400
    
    synsets = wordnet.synsets(word)
    if synsets:
        definitions = [synset.definition() for synset in synsets]
        suggestions = []
    else:
        definitions = ["Definition not found."]
        # Find close matches
        all_words = set(wordnet.words())
        suggestions = difflib.get_close_matches(word, all_words, n=5)

    return jsonify({'definitions': definitions, 'suggestions': suggestions})

@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.get_json()
    definition = data.get('definition')
    if not definition:
        return jsonify({'error': 'No definition provided'}), 400
    
    # Call the OpenAI image generation API
    image_url = generate_image_from_definition(definition)
    
    return jsonify({'image_url': image_url})

def generate_image_from_definition(definition):
    try:
        # Use the OpenAI API to generate an image based on the definition
        response = openai.Image.create(
            prompt=definition,  # Use the definition as the prompt
            n=1,
            size='256x256'  # Adjust size as needed
        )
        # Extract the URL of the generated image
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
