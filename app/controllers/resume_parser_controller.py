from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, send_file, send_from_directory, abort, current_app, render_template_string, send_from_directory
from werkzeug.utils import safe_join
from werkzeug.utils import secure_filename
import os
import json
import subprocess
from PyPDF2 import PdfReader
from resume_parser.gemini import generate_structured_json
from job_parser.job_parser import jd_parser  
from resume_parser.resume_parser import parse_resume
from resume_parser.LaTeXGen import generate_latex_from_json, latex_to_pdf
import uuid
from resume_parser.kw import suggest_verbs
from resume_parser.repetitive_verbs import repetitive_verbs
from resume_parser.filler import detect_filler_words

resume_parser_bp = Blueprint('resume_parser', __name__)

UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def shorten_text(text, max_length=10):
    return (text[:max_length] + '...') if len(text) > max_length else text





# Path to the directory containing PDF files
PDF_DIRECTORY = 'app/newoutput'

# Ensure the PDF directory exists
if not os.path.exists(PDF_DIRECTORY):
    os.makedirs(PDF_DIRECTORY)

@resume_parser_bp.route('/pdfs')
def list_pdfs():
    """List all PDF files in the directory."""
    files = os.listdir(PDF_DIRECTORY)
    pdf_files = [f for f in files if f.endswith('.pdf')]
    return render_template_string('''
        <h1>List of PDF Files</h1>
        <ul>
            {% for pdf in pdf_files %}
                <li><a href="{{ url_for('resume_parser.download_pdf', filename=pdf) }}">{{ pdf }}</a></li>
            {% endfor %}
        </ul>
        ''', pdf_files=pdf_files)

@resume_parser_bp.route('/download/<path:filename>', methods=['GET'])
def download(filename):

    # "app/newoutput", "7b15c701-8c0a-4636-a50d-c8f89432ad25.pdf" make the path and print
    path = os.path.join("newoutput", filename)
    try:
        return send_file(path, as_attachment=True)
    except FileNotFoundError:
        return render_template_string('<h1>File not found</h1>'), 404   
    
  







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

def check_bullet_points(text):
    lines = text.split('•')
    bullet_points = [line for line in lines if line.strip().startswith('-') or line.strip().startswith('*') or line.strip()]
    too_long_bullets = [bp for bp in bullet_points if len(bp.split()) > 20]  # Assuming an average of 20 words per bullet point
    return (bullet_points), (too_long_bullets)

@resume_parser_bp.route('/api/recheck', methods=['POST'])
def recheck():
    data = request.json.get('data', {})
    job_skills = request.json.get('jobSkills', [])
    suggestions = []

    # Check the length of responsibilities in work experience
    if 'Work Experience' in data:
        for experience in data['Work Experience']:
            responsibilities = experience.get('responsibilities', experience.get('responsibilities_and_achievements', []))
            for idx, responsibility in enumerate(responsibilities):
                if len(responsibility) < 50:
                    suggestions.append({
                        'type': 'responsibility_length',
                        'message': f'Responsibility {idx + 1} in job "{experience["job_title"]}" is too short.'
                    })

    # Check for missing skills
    for skill in job_skills:
        if skill not in data.get('Skills', ''):
            suggestions.append({
                'type': 'missing_skill',
                'message': f'Skill "{skill}" is required for the job but is not listed in the skills section.'
            })

    # Check for weak verbs
    verb_suggestions = suggest_verbs(json.dumps(data))
    for verb in verb_suggestions['matched_verbs']:
        suggestions.append({
            'type': 'weak_verb',
            'verb': verb,
            'suggestion': ", ".join(verb_suggestions['suggestions'][verb])
        })
    
    repetitiveverbs = repetitive_verbs(json.dumps(data))

    filler_words = detect_filler_words(json.dumps(data))
    print(filler_words)
    
    # Check bullet points length
    bullet_points_length_issues = []
    for section in ['Work Experience', 'Projects']:
        if section in data:
            for item in data[section]:
                for key, value in item.items():
                    if isinstance(value, str):
                        total_bullets, too_long_bullets = check_bullet_points(value)
                        if too_long_bullets:
                            bullet_points_length_issues.append({
                                'section': section,
                                'item': item.get('job_title', item.get('projectTitle', '')),
                                'total_bullets': total_bullets,
                                'too_long_bullets': too_long_bullets
                            })
                    elif isinstance(value, list):
                        for v in value:
                            if isinstance(v, str):
                                total_bullets, too_long_bullets = check_bullet_points(v)
                                if too_long_bullets:
                                    bullet_points_length_issues.append({
                                        'section': section,
                                        'item': item.get('job_title', item.get('job_title', '')),
                                        'total_bullets': total_bullets,
                                        'too_long_bullets': too_long_bullets
                                    })
    
    for issue in bullet_points_length_issues:
        suggestions.append({
            'type': 'bullet_point_length',
            'message': f'In {issue["section"]} "{(issue["item"])}", {len(issue["total_bullets"])} bullet points are too long.'
        })

    return jsonify(suggestions=suggestions, repetitiveVerbs=repetitiveverbs, filler_words=filler_words)


@resume_parser_bp.route('/api/rewrite', methods=['POST'])
def rewrite():
    data = request.json.get('data', "")
    prompt = f"""
    Rewrite the following RESPONSIBILITY in an ATS-friendly manner, ensuring the description is between 20 to 30 words and includes specific metrics:
    
    '{data}' Return the result as a JSON object with the key 'response'.
    """
    

    response = generate_structured_json(prompt)  
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
