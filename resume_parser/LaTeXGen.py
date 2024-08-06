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

    \newcommand{\resumeProjectHeading}[4]{
        \item
        \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
          \textbf{#1} & #2 \\
          \textit{\small#3} & \textit{\small #4} \\
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
            job_title = job.get("jobTitle", "")
            latex_code += r'''
            \resumeSubheading
              {''' + escape_latex_special_chars(job_title) + r'''}{''' + escape_latex_special_chars(job.get("dateRange", "")) + r'''}
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
            project_title = escape_latex_special_chars(project.get("Project_title", ""))
            project_dates = escape_latex_special_chars(project.get("Project_dates", ""))
            project_links = escape_latex_special_chars(project.get("Project_links", ""))
            project_description = project.get("Project_description", "").split("\n")
            
            latex_code += r'''
            \resumeSubheading
              {''' + project_title + r'''}{''' + project_dates + r'''}
              {''' + project_links + r'''}{}
              \resumeItemListStart
            '''
            for detail in project_description:
                if detail.strip():
                    latex_code += r'''
                    \resumeItem{''' + escape_latex_special_chars(detail.strip()) + r'''}
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

# Example JSON data
data = {
    "Personal Info": [
        {
            "Email": "iam@janisahil.com",
            "GitHub": "github.com/sahiljani",
            "LinkedIn": "linkedin.com/in/jani-sahil",
            "Location": "Ontario",
            "Name": "Sahil Jani",
            "Phone": "249-877-2908"
        }
    ],
    "Work Experience": [
        {
            "company": "Leasey.AI",
            "dateRange": "Jul 2023 – Dec 2023",
            "jobTitle": "Web Developer (Contract)",
            "location": "Vancouver, Canada",
            "responsibilities": [
                "Led migration from SaaS to open-source CMS, cutting costs by 75% and adding advanced functionalities.",
                "Engineered custom PHP solutions for dynamic functionality, enhancing interactivity with JavaScript and CSS, and achieved a 25% reduction in bounce rate.",
                "Implemented PhpRedis for caching in the PHP environment, boosting application speed by 40%."
            ]
        },
        {
            "company": "ManticLabs Web Solutions Pvt. Ltd.",
            "dateRange": "Jun 2021 – May 2023",
            "jobTitle": "Software Developer",
            "location": "Gujarat, India",
            "responsibilities": [
                "Enhanced system performance by 40% and supported over 100,000 users through designing, developing, and maintaining software applications.",
                "Showcased proficiency in Java, PHP, and JavaScript, implementing over 15 scalable solutions, and mastered SQL and NoSQL database management.",
                "Wrote unit tests using PHPUnit to ensure code reliability and reduce bugs.",
                "Implemented agile methodologies which reduced project turnaround times by 25%, fostering a more responsive development environment and enhancing overall team productivity."
            ]
        },
        {
            "company": "Cyberstrek Technologies",
            "dateRange": "Nov 2020 – May 2021",
            "jobTitle": "Web Developer - Internship",
            "location": "Gujarat, India",
            "responsibilities": [
                "Developed CRM features using PHP and MySQL, meeting industry standards for clean, efficient solutions.",
                "Seamlessly integrated backend functionalities, improving data processing efficiency by 20%.",
                "Designed responsive interfaces using HTML, CSS, and JavaScript to enhance user experience."
            ]
        }
    ],
    "Projects": [
        {
            "Project_dates": "Mar 2024 – Apr 2024",
            "Project_links": "Github",
            "Project_title": "Investor Management System",
            "project_skills": "",
            "Project_description": "Developed and integrated over 15 advanced filters using MySQL and Eloquent ORM to match projects with ideal investors based on specific requirements, enhancing project-investor matching efficiency.\nIntegrated an Amazon SES email sending feature to send up to 2,000 bulk emails at once, utilizing Laravel Queue for efficient processing, with open rate tracking and reporting."
        },
        {
            "Project_dates": "Oct 2023 - Dec 2023",
            "Project_links": "Github",
            "Project_title": "Incentive-based Quiz Website",
            "project_skills": "",
            "Project_description": "Developed a React and Laravel-based quiz website with Adsense monetization and Google Analytics integration, increasing monthly ad revenue by 50%."
        },
        {
            "Project_dates": "May 2023 - Jul 2023",
            "Project_links": "wssurgical.com",
            "Project_title": "Website Design & Content Management System",
            "project_skills": "",
            "Project_description": "Transformed Figma designs into a responsive web app with Tailwind CSS and Alpine.js, boosting user engagement by 30%, and built a CMS with Laravel, increasing lead generation by 20% through a new submission system."
        }
    ],
    "Education": [
        {
            "Institution": "Some University",
            "Start Year": "2018",
            "End Year": "2022",
            "Degree": "Bachelor of Science in Computer Science"
        }
    ],
    "Skills": "HTML\nCSS\nJavaScript\nTypescript\nNext.js\nPHP\nJava\nPython\nNode.js\nLaravel\nDatabase\nSQL\nMySQL\nNoSQL\nMongoDB\nAzure\nDocker\nGit\nJenkins\nTerraform\nAnsible"
}

latex_code = generate_latex_from_json(data)
pdf_path = latex_to_pdf(latex_code, 'resume.pdf')
print(f"PDF generated at: {pdf_path}")
