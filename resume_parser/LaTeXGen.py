import subprocess
import os
import re

def escape_latex_special_chars(text):
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}'
    }
    regex = re.compile('|'.join(re.escape(key) for key in special_chars.keys()))
    return regex.sub(lambda match: special_chars[match.group()], text)

def generate_latex_from_json(data):
    latex_code = r'''
    \UseRawInputEncoding

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

    \pagestyle{fancy}
    \fancyhf{} % clear all header and footer fields
    \fancyfoot{}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}

    \addtolength{\oddsidemargin}{-0.5in}
    \addtolength{\evensidemargin}{-0.5in}
    \addtolength{\textwidth}{1in}
    \addtolength{\topmargin}{-.5in}
    \addtolength{\textheight}{1.0in}

    \urlstyle{same}

    \raggedbottom
    \raggedright
    \setlength{\tabcolsep}{0in}

    \titleformat{\section}{
      \vspace{-4pt}\scshape\raggedright\large
    }{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

    \pdfgentounicode=1

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

    \begin{document}
    '''

    # Personal Info Section
    personal_info_list = data.get("Personal Info", [])
    if personal_info_list:
        personal_info = personal_info_list[0]  # Assuming only one set of personal info
        latex_code += r'''
        \begin{center}
            \textbf{\Huge \scshape ''' + escape_latex_special_chars(personal_info.get("Name", "")) + r'''} \\ \vspace{1pt}
            \small ''' + escape_latex_special_chars(personal_info.get("Phone", "")) + r''' $|$ \href{mailto:''' + escape_latex_special_chars(personal_info.get("Email", "")) + r'''}{\underline{''' + escape_latex_special_chars(personal_info.get("Email", "")) + r'''}} $|$ ''' + escape_latex_special_chars(personal_info.get("Location", "")) + r''' $|$ 
            \href{''' + escape_latex_special_chars(personal_info.get("LinkedIn", "")) + r'''}{\underline{''' + escape_latex_special_chars(personal_info.get("LinkedIn", "")) + r'''}} $|$
            \href{''' + escape_latex_special_chars(personal_info.get("GitHub", "")) + r'''}{\underline{''' + escape_latex_special_chars(personal_info.get("GitHub", "")) + r'''}} 
        \end{center}
        '''

    # Work Experience Section
    work_experience = data.get("Work Experience", [])
    if work_experience:
        latex_code += r'''
        \section{Experience}
          \resumeSubHeadingListStart
        '''
        for job in work_experience:
            latex_code += r'''
            \resumeSubheading
              {''' + escape_latex_special_chars(job.get("job_title", "")) + r'''}{''' + escape_latex_special_chars(job.get("dateRange", "")) + r'''}
              {''' + escape_latex_special_chars(job.get("company", "")) + r'''}{''' + escape_latex_special_chars(job.get("location", "")) + r'''}
              \resumeItemListStart
            '''
            for responsibility in job.get("responsibilities", []):
                latex_code += r'''
                \resumeItem{''' + escape_latex_special_chars(responsibility) + r'''}
                '''
            latex_code += r'''
              \resumeItemListEnd
            '''
        latex_code += r'''
          \resumeSubHeadingListEnd
        '''

    # Projects Section
    projects = data.get("Projects", [])
    if projects:
        latex_code += r'''
        \section{Projects}
          \resumeSubHeadingListStart
        '''
        for project in projects:
            descriptions = project.get("Description", "").split("•")
            project_title = escape_latex_special_chars(descriptions[0].strip())
            project_details = descriptions[1:]
            latex_code += r'''
            \resumeProjectHeading
              {''' + project_title + r'''}{}
              \resumeItemListStart
            '''
            for detail in project_details:
                if detail.strip():
                    latex_code += r'''
                    \resumeItem{''' + escape_latex_special_chars(detail.strip()).replace("(", r"\href{").replace(")", r"}{\underline{Github}}") + r'''}
                    '''
            latex_code += r'''
              \resumeItemListEnd
            '''
        latex_code += r'''
          \resumeSubHeadingListEnd
        '''

    # Skills Section
    skills = data.get("Skills", "")
    if skills:
        latex_code += r'''
        \section{Technical Skills}
        \begin{itemize}[leftmargin=0.15in, label={}]
            \small{\item{
             \textbf{Skills}: ''' + escape_latex_special_chars(skills).replace("\n", ", ") + r'''
            }}
        \end{itemize}
        '''

    # Education Section
    education = data.get("Education", [])
    if education:
        latex_code += r'''
        \section{Education}
          \resumeSubHeadingListStart
        '''
        for edu in education:
            latex_code += r'''
            \resumeSubheading
              {''' + escape_latex_special_chars(edu.get("Institution", "")) + r'''}{''' + escape_latex_special_chars(edu.get("Start Year", "") + " -- " + escape_latex_special_chars(edu.get("End Year", ""))) + r'''}
              {''' + escape_latex_special_chars(edu.get("Degree", "")) + r'''}{}
            '''
        latex_code += r'''
          \resumeSubHeadingListEnd
        '''

    latex_code += r'''
    \end{document}
    '''
    
    return latex_code

def latex_to_pdf(latex_code, output_pdf, output_folder='output'):
    output_folder = "app/newoutput"
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Create a temporary LaTeX file
    temp_tex_path = os.path.join(output_folder, 'temp.tex')
    with open(temp_tex_path, 'w') as f:
        f.write(latex_code)

    try:
        # Run pdflatex to compile the LaTeX file into a PDF
        subprocess.run(['pdflatex', '-output-directory', output_folder, temp_tex_path], check=True)
        
        # Rename the output PDF to the desired output name
        temp_pdf_path = os.path.join(output_folder, 'temp.pdf')
        final_pdf_path = os.path.join(output_folder, output_pdf)
        os.rename(temp_pdf_path, final_pdf_path)
        
        return final_pdf_path
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Clean up temporary files
        for ext in ['aux', 'log', 'tex']:
            temp_file = os.path.join(output_folder, f'temp.{ext}')
            if os.path.exists(temp_file):
                os.remove(temp_file)