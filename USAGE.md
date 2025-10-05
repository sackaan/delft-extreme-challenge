# Usage of the code and model

# Install dependencies
```bash
pip install -r requirements.txt
```
# Download the model
You can download the model from this link:
https://drive.google.com/file/d/1N7E_WkrBBOVqoZuYOnHh11Vso_frkt3x/view?usp=sharing

Create a "models" folder in the root directory of the project and unzip the zip file into that folder.

The files of the model should be located in the folder 'models/bert_hatespeech'

# Running the app
You can run the app using the following command:
```bash
python ./src/app.py
```
and visiting the given URL in your browser. Usually at http://127.0.0.1:5000

# Using the app

You can upload audio files, text files or enter text directly into the text box. The app will process the input and display whether it contains extremist views or foul language.

# Classification

The app will display the result of the analysis marking sentences if they are hate speech, offensive or normal sentences.

If a sentence is marked as normal but the confidence level is below 80% it will still be flagged as the model is not very certain about the classification.