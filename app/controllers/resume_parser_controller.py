from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, send_file, render_template_string
from werkzeug.utils import secure_filename
import os
import subprocess
from PyPDF2 import PdfReader
from job_parser.job_parser import jd_parser  # Correct import
from resume_parser.resume_parser import parse_resume
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-interactive environments
import matplotlib.pyplot as plt



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
            return redirect(url_for('resume_parser.upload_form'))
    else:
        flash('Invalid file type. Only PDF files are allowed.')
        return redirect(url_for('resume_parser.upload_form'))


@resume_parser_bp.route('/api/JD', methods=['POST'])
def upload_jd_form():
    JD = request.json.get('JD')
    print(JD)
    data = jd_parser(JD)
    return jsonify(data)
    
    
from flask import Blueprint, request, send_file
import matplotlib.pyplot as plt
from io import BytesIO

resume_parser_bp = Blueprint('resume_parser_bp', __name__)

@resume_parser_bp.route('/latex', methods=['GET'])
def latexPreview():
    latex_code = request.args.get('latex', r"""
\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}


%----------FONT OPTIONS----------
% sans-serif
% \usepackage[sfdefault]{FiraSans}
% \usepackage[sfdefault]{roboto}
% \usepackage[sfdefault]{noto-sans}
% \usepackage[default]{sourcesanspro}

% serif
% \usepackage{CormorantGaramond}
% \usepackage{charter}


\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%



\begin{document}

%----------HEADING----------
% \begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
%   \textbf{\href{http://sourabhbajaj.com/}{\Large Sourabh Bajaj}} & Email : \href{mailto:sourabh@sourabhbajaj.com}{sourabh@sourabhbajaj.com}\\
%   \href{http://sourabhbajaj.com/}{http://www.sourabhbajaj.com} & Mobile : +1-123-456-7890 \\
% \end{tabular*}

\begin{center}
    \textbf{\Huge \scshape Sahil Jani} \\ \vspace{1pt}
    \small 249-877-2908 $|$ \href{mailto:iam@janisahil.com} 
        \small Toronto, Ontario $|$ 
    {\underline{iam@janisahil.com}} $|$ 

    \vspace{2pt}
  \href{https://www.linkedin.com/in/jani-sahil/}{\underline{linkedin.com/in/jani-sahil/}}  $|$
    \href{https://github.com/sahiljani}{\underline{github.com/sahiljani}} $|$ 
     \href{https://leetcode.com/u/sahiljani/}{\underline{https://leetcode.com/u/sahiljani/}}
\end{center}

%-----------EXPERIENCE-----------
\section{Experience}
  \resumeSubHeadingListStart

    \resumeSubheading
  {Web Developer (Contract)}{Jul 2023 – Dec 2023}
  {Leasey.AI}{Vancouver, Canada}

  \resumeItemListStart
    \resumeItem{Led migration from SaaS to open-source CMS, cutting costs by 75\% and adding advanced functionalities.}
        \resumeItem{Engineered custom PHP solutions for dynamic functionality, enhancing interactivity with JavaScript and CSS, and achieved a 25\% reduction in bounce rate.}
         \resumeItem{Implemented PhpRedis for caching in the PHP environment, boosting application speed by 40\%.}
  \resumeItemListEnd

      
% -----------Multiple Positions Heading-----------
%    \resumeSubSubheading
%     {Software Engineer I}{Oct 2014 - Sep 2016}
%     \resumeItemListStart
%        \resumeItem{Apache Beam}
%          {Apache Beam is a unified model for defining both batch and streaming data-parallel processing pipelines}
%     \resumeItemListEnd
%    \resumeSubHeadingListEnd
%-------------------------------------------

    \resumeSubheading
  {Software Developer}{Jun 2021 – May 2023}
  {ManticLabs Web Solutions Pvt. Ltd.}{Gujarat, India}
  \resumeItemListStart
    \resumeItem{Enhanced system performance by 40\% and supported over 100,000 users through designing, developing, and maintaining software applications.}
        \resumeItem{Showcased proficiency in Java, PHP, and JavaScript, implementing over 15 scalable solutions, and mastered SQL and NoSQL database management.}
    \resumeItem{Implemented agile methodologies which reduced project turnaround times by 25\%, fostering a more responsive development environment and enhancing overall team productivity.}
  
  \resumeItemListEnd


 \resumeSubheading
      {Web Developer - Internship}{Nov 2020 – May 2021}
      {Cyberstrek Technologies}{Gujarat, India}
      \resumeItemListStart
     \resumeItem{Developed CRM features using Node.js and MySQL, meeting industry standards for clean, efficient solutions. Seamlessly integrated backend functionalities, improving data processing efficiency by 20\%.}
\resumeItem{Designed responsive interfaces using HTML, CSS, and JavaScript to enhance user experience.}
    \resumeItemListEnd

  \resumeSubHeadingListEnd


%-----------PROJECTS-----------
\section{Projects}
    \resumeSubHeadingListStart
      \resumeProjectHeading
    {\textbf{Investor Management System  
    \href{https://github.com/sahiljani/e-valuate}{\underline{(Github)}} 
     }  \emph{}}{Mar 2024 -- Apr 2024}
    \resumeItemListStart
        \resumeItem{Developed and integrated over 15 advanced filters using MySQL and Eloquent ORM to match projects with ideal investors based on specific requirements, enhancing project-investor matching efficiency.}
        \resumeItem{Integrated an Amazon SES email sending feature to send up to 2,000 bulk emails at once, utilizing Laravel Queue for efficient processing, with open rate tracking and reporting.}
    \resumeItemListEnd

\resumeProjectHeading
    {\textbf{Cross-Platform Carpooling App with React Native}  \emph{}}{Oct 2023 - Dec 2023}
    \resumeItemListStart
        \resumeItem{Built a cross-platform carpooling app with a Node.js backend and React Native front-end for iOS and Android, leveraging Git version control to improve project efficiency by 30\% in a group project.}    
        \resumeItemListEnd    

\resumeProjectHeading
     {\textbf{Website Design \& Content Management System} \href{https://wssurgical.com/}{\underline{(wssurgical.com)}}   \emph{}}{May 2023 - Jul 2023}
    \resumeItemListStart
        \resumeItem{Transformed Figma designs into a responsive web app with Tailwind CSS and Alpine.js, boosting user engagement by 30\%, and built a CMS with Laravel, increasing lead generation by 20\% through a new submission system.}
    \resumeItemListEnd



    \resumeSubHeadingListEnd



%
%-----------PROGRAMMING SKILLS-----------
\section{Technical Skills}





 \begin{itemize}[leftmargin=0.15in, label={}]
     \small{\item{
     \textbf{Languages/Scripting}{: PHP, Rust, Java, Python} \\
     \vspace{2pt}
     \textbf{Web Technologies}{: HTML, CSS, JavaScript, Typescript, React.js, Next.js, Node.js, NestJS, Spring Boot, Laravel} \\
     \vspace{2pt}
     \textbf{Databases}{: MySQL, Postgres, MongoDB, DynamoDB} \\
     \vspace{2pt}
     \textbf{Cloud Technologies}{: AWS (EC2, Lambda, S3, RDS, DynamoDB, VPC, Bedrock), Azure, GCP, Docker, Kubernetes} \\
     \vspace{2pt}
     \textbf{Development Tools \& Methodologies}{: Git, Jira, Jenkins, CI/CD, Agile, Scrum, Terraform, Ansible} \\
    }}

    
 \end{itemize}


%-----------EDUCATION-----------
\section{Education}
  \resumeSubHeadingListStart
    \resumeSubheading
      {Georgian College - Ontario, Canada}{Jan 2024 – Aug 2024}
    {Post-Graduation in Artificial Intelligence}{GPA: 8.9 (Dean's List)}
    \resumeSubheading
      {Georgian College - Ontario, Canada}{May 2023 -- Dec 2023}
      {Post-Graduation in Mobile Application Development} {GPA: 8.8 (Dean's List)}
      \resumeSubheading
        {Gujarat Technological University - Gujarat, India}{Aug 2018 -- May 2021}
        {Bachelor of Engineering - Computer Engineering} {GPA:8.6}

  \resumeSubHeadingListEnd
%-------------------------------------------
\end{document}

    """)

    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, latex_code, fontsize=20, ha='center', va='center')
    ax.axis('off')

    output = BytesIO()
    plt.savefig(output, format='png')
    plt.close(fig)
    output.seek(0)

    return send_file(output, mimetype='image/png')

@resume_parser_bp.route('/latex_preview', methods=['GET', 'POST'])
def latex_preview_form():
    if request.method == 'POST':
        latex_code = request.form['latex']
        img_url = url_for('resume_parser.latexPreview', latex=latex_code)
        return render_template_string('''
            <!doctype html>
            <title>Render LaTeX</title>
            <h1>Render LaTeX to Image</h1>
            <form method="post">
                <textarea name="latex" rows="10" cols="50">{{ latex_code }}</textarea>
                <br>
                <input type="submit" value="Render">
            </form>
            {% if img_url %}
                <h2>Rendered Image:</h2>
                <img src="{{ img_url }}" alt="LaTeX Image">
            {% endif %}
        ''', img_url=img_url, latex_code=latex_code)
    return render_template_string('''
        <!doctype html>
        <title>Render LaTeX</title>
        <h1>Render LaTeX to Image</h1>
        <form method="post">
            <textarea name="latex" rows="10" cols="50">\\frac{a}{b}</textarea>
            <br>
            <input type="submit" value="Render">
        </form>
    ''')


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
    app.secret_key = 'supersecretkey'
    app.register_blueprint(resume_parser_bp, url_prefix='/resume_parser')
    app.run(debug=True)
