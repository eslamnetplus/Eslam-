from flask import Flask, request
import pdfplumber
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        text = ""

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text()

        numbers = re.findall(r'\d+', text)

        return "<br>".join(numbers)

    return '''
    <h2>رفع PDF</h2>
    <form method="post" enctype="multipart/form-data">
    <input type="file" name="file">
    <button type="submit">استخراج</button>
    </form>
    '''

app.run()
