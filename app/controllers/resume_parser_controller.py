from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, send_file, send_from_directory, abort, current_app
from werkzeug.utils import safe_join
from werkzeug.utils import secure_filename
import os
import subprocess
from PyPDF2 import PdfReader
from resume_parser.gemini import generate_structured_json
from job_parser.job_parser import jd_parser  
from resume_parser.resume_parser import parse_resume
from resume_parser.LaTeXGen import generate_latex_from_json, latex_to_pdf
import uuid

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
OUTPUT_FOLDER = 'output'
@resume_parser_bp.route('/files/<path:filename>')
def download_file(filename):
    try:
        # Ensure the file path is safe and within the output folder
        file_path = safe_join(OUTPUT_FOLDER, filename)
        current_app.logger.debug(f"File path resolved to: {file_path}")
        
        # Check if the file exists and log this
        if os.path.isfile(file_path):
            current_app.logger.debug(f"File exists: {file_path}")
            return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)
        else:
            current_app.logger.error(f"File not found: {file_path}")
            abort(404)  # File not found
    except Exception as e:
        current_app.logger.exception("An error occurred while processing the file download request.")
        abort(500)  # Internal server error



@resume_parser_bp.route('/', methods=['GET'])
def upload_form():
    return render_template('upload_resume.html')



@resume_parser_bp.route('/', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        flash('No file part')
        return redirect(url_for('resume_parser.upload_form'))

    file = request.files['resume']
    job = request.form['job']
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
            return render_template('result.html', data=parsed_data, job=job)
        except Exception as e:
            flash(f'An error occurred while processing the file: {e}')
            # return redirect(url_for('resume_parser.upload_form'))
    else:
        flash('Invalid file type. Only PDF files are allowed.')
        return redirect(url_for('resume_parser.upload_form'))


@resume_parser_bp.route('/api/JD', methods=['POST'])
def upload_jd_form():
    JD = request.json.get('JD')
    data = jd_parser(JD)
    return jsonify(data)
    
        
    
@resume_parser_bp.route('/api/recheck', methods=['POST'])
def recheck():
    data = request.json.get('data', {})
    job_skills = request.json.get('jobSkills', [])
    suggestions = []

    # Check the length of responsibilities in work experience
    if 'Work Experience' in data:
        for experience in data['Work Experience']:
            if 'responsibilities' in experience:
                for idx, responsibility in enumerate(experience['responsibilities']):
                    if len(responsibility) < 50:
                        suggestions.append({
                            'type': 'responsibility_length',
                            'message': f'Responsibility {idx + 1} in job "{experience["jobTitle"]}" is too short.'
                        })

    # Example check for matching job skills (extend as needed)
    for skill in job_skills:
        if skill not in data.get('Skills', ''):
            suggestions.append({
                'type': 'missing_skill',
                'message': f'Skill "{skill}" is required for the job but is not listed in the skills section.'
            })

    return jsonify(suggestions=suggestions)

@resume_parser_bp.route('/api/rewrite', methods=['POST'])
def rewrite():
    data = request.json.get('data', "")
    prompt = f"""
    Rewrite the following RESPONSIBILITY in an ATS-friendly manner, ensuring the description is between 20 to 30 words and includes specific metrics:
    
    '{data}' Return the result as a JSON object with the key 'response'.
    """
    
    # Simulating the response from some external function like an AI model
    response = generate_structured_json(prompt)  # You need to implement this function
    return jsonify(response)


@resume_parser_bp.route('API/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    latex_code = generate_latex_from_json(data)
    # unique file name
    output_pdf = f"{uuid.uuid4()}.pdf"
    pdf_path = latex_to_pdf(latex_code, output_pdf)
    
    if pdf_path:
        response = {
            "message": "PDF generated successfully",
            "pdf_path": output_pdf
        }
    else:
        response = {
            "message": "An error occurred during PDF generation"
        }
    
    return jsonify(response)


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
    app.secret_key = 'supersecretkey'
    app.register_blueprint(resume_parser_bp, url_prefix='/resume_parser')
    app.run(debug=True)
