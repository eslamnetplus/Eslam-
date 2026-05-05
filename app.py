from flask import Flask, request
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        text = ""

        # محاولة استخراج نص عادي
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t

        # إذا النص قليل → استخدم OCR
        if len(text.strip()) < 50:
            images = convert_from_bytes(file.read())
            for img in images:
                text += pytesseract.image_to_string(img)

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
