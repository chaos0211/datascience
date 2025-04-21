function analyzeText(){
    const inputText = document.getElementById('inputText').value;

    fetch('/api/analysis/analyze', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text: inputText})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('result').innerText = data.sentiment;
    });
}