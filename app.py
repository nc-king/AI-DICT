from flask import Flask, request, jsonify, send_from_directory
import nltk
from nltk.corpus import wordnet
import difflib
import requests

# Download WordNet data
nltk.download('wordnet')

app = Flask(__name__)

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
    
    # Call the image generation API (replace with actual API call)
    image_url = generate_image_from_definition(definition)
    
    return jsonify({'image_url': image_url})

def generate_image_from_definition(definition):
    # Placeholder function for image generation
    # Replace with actual API call to an image generation service
    return "https://via.placeholder.com/150"

if __name__ == '__main__':
    app.run(debug=True)
