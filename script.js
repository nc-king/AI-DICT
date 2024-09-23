document.getElementById('wordInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        getDefinition();
    }
});

function getDefinition() {
    const word = document.getElementById('wordInput').value;
    fetch(`/define?word=${word}`)
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '';
            if (data.definitions) {
                data.definitions.forEach((definition, index) => {
                    const p = document.createElement('p');
                    p.textContent = `${index + 1}. ${definition}`;
                    resultDiv.appendChild(p);

                    // Generate image for each definition
                    generateImage(definition, resultDiv);
                });
            } else {
                resultDiv.textContent = 'Definition not found.';
            }
            if (data.suggestions && data.suggestions.length > 0) {
                const suggestionDiv = document.createElement('div');
                suggestionDiv.innerHTML = '<strong>Did you mean:</strong>';
                const ul = document.createElement('ul');
                data.suggestions.forEach(suggestion => {
                    const li = document.createElement('li');
                    li.textContent = suggestion;
                    ul.appendChild(li);
                });
                suggestionDiv.appendChild(ul);
                resultDiv.appendChild(suggestionDiv);
            }
        });
}

function generateImage(definition, resultDiv) {
    fetch('/generate_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ definition: definition })
    })
    .then(response => response.json())
    .then(data => {
        if (data.image_url) {
            const img = document.createElement('img');
            img.src = data.image_url;
            resultDiv.appendChild(img);
        }
    });
}
