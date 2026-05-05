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

        # اقرأ الملف كـ bytes مرة واحدة
        file_bytes = file.read()

        # استخراج النص العادي
        with pdfplumber.open(file_bytes) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t

        # إذا النص قليل → استخدم OCR
        if len(text.strip()) < 50:
            images = convert_from_bytes(file_bytes)
            for img in images:
                text += pytesseract.image_to_string(img)

        # استخراج الأرقام
        numbers = re.findall(r'\d+', text)

        return "<br>".join(numbers)

    return '''
    <h2>رفع ملف PDF</h2>
    <form method="post" enctype="multipart/form-data">
    <input type="file" name="file" required>
    <button type="submit">استخراج</button>
    </form>
    '''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
