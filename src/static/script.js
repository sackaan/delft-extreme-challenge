function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

document.getElementById("defaultOpen").click();

async function analyzeAudio() {
    const fileInput = document.getElementById('audioFile');
    const resultDiv = document.getElementById('audioResult');

    if (!fileInput.files[0]) {
        alert('Please select an audio file');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    resultDiv.innerHTML = '<p>Processing...</p>';

    const response = await fetch('/analyze/audio', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    if (data.error) {
        resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        return;
    }

    let html = `<h3>Transcription:</h3><p>${data.transcription}</p>`;
    const overallClass = data.overall.confidence < 0.80 ? 'hate' : data.overall.label;
    html += `<h3>Overall: <span class="${overallClass}">${data.overall.label.toUpperCase()}</span> (${(data.overall.confidence * 100).toFixed(2)}%)</h3>`;
    html += '<h3>Segments:</h3>';

    data.segments.forEach(seg => {
        const segClass = seg.confidence < 0.80 ? 'hate' : seg.label;
        html += `<div style="margin: 10px 0; padding: 10px; background: white;">`;
        html += `<p><strong>[${seg.start}s - ${seg.end}s]</strong></p>`;
        html += `<p>${seg.text}</p>`;
        html += `<p>Classification: <span class="${segClass}">${seg.label.toUpperCase()}</span> (${(seg.confidence * 100).toFixed(2)}%)</p>`;
        html += `</div>`;
    });

    resultDiv.innerHTML = html;
}

async function analyzeText() {
    const textInput = document.getElementById('textInput').value;
    const fileInput = document.getElementById('textFile');
    const resultDiv = document.getElementById('textResult');

    const formData = new FormData();

    if (fileInput.files[0]) {
        formData.append('file', fileInput.files[0]);
    } else if (textInput) {
        const response = await fetch('/analyze/text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: textInput })
        });

        displayTextResult(await response.json(), resultDiv);
        return;
    } else {
        alert('Please enter text or select a file');
        return;
    }

    resultDiv.innerHTML = '<p>Processing...</p>';

    const response = await fetch('/analyze/text', {
        method: 'POST',
        body: formData
    });

    displayTextResult(await response.json(), resultDiv);
}

function displayTextResult(data, resultDiv) {
    if (data.error) {
        resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        return;
    }

    const overallClass = data.overall.confidence < 0.80 ? 'hate' : data.overall.label;
    let html = `<h3>Overall: <span class="${overallClass}">${data.overall.label.toUpperCase()}</span> (${(data.overall.confidence * 100).toFixed(2)}%)</h3>`;
    html += '<h3>Sentences:</h3>';

    data.sentences.forEach(sent => {
        const sentClass = sent.confidence < 0.80 ? 'hate' : sent.label;
        html += `<div style="margin: 10px 0; padding: 10px; background: white;">`;
        html += `<p><strong>Sentence ${sent.index}:</strong> ${sent.text}</p>`;
        html += `<p>Classification: <span class="${sentClass}">${sent.label.toUpperCase()}</span> (${(sent.confidence * 100).toFixed(2)}%)</p>`;
        html += `</div>`;
    });

    resultDiv.innerHTML = html;
}
