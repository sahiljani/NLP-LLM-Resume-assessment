from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import os
import subprocess
from PyPDF2 import PdfReader

from resume_parser.resume_parser import parse_resume

resume_parser_bp = Blueprint('resume_parser', __name__)

UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def create_latex_file(latex_code, filename="document.tex"):
    with open(filename, "w") as f:
        f.write(latex_code)

def compile_latex_to_pdf(latex_filename):
    try:
        subprocess.run(["pdflatex", latex_filename], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during LaTeX compilation: {e}")
    pdf_filename = latex_filename.replace(".tex", ".pdf")
    return pdf_filename

@resume_parser_bp.route('/', methods=['GET'])
def upload_form():
    return render_template('upload_resume.html')



@resume_parser_bp.route('/', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        flash('No file part')
        return redirect(url_for('resume_parser.upload_form'))

    file = request.files['resume']

    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('resume_parser.upload_form'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        try:
            text = extract_text_from_pdf(file_path)
            parsed_data = parse_resume(text)
            return render_template('result.html', data=parsed_data)
        except Exception as e:
            flash(f'An error occurred while processing the file: {e}')
            return redirect(url_for('resume_parser.upload_form'))
    else:
        flash('Invalid file type. Only PDF files are allowed.')
        return redirect(url_for('resume_parser.upload_form'))


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
    app.secret_key = 'supersecretkey'
    app.register_blueprint(resume_parser_bp, url_prefix='/resume_parser')
    app.run(debug=True)