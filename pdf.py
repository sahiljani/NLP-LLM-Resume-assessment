
import os
import subprocess

# LaTeX document content
content = r'''

%-------------------------
% Resume in Latex
% Author : Jake Gutierrez
% Based off of: https://github.com/sb2nov/resume
% License : MIT
%------------------------

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

'''

# Write LaTeX content to cover.tex
with open('cover.tex', 'w') as f:
    f.write(content)

# Run pdflatex to create the PDF
cmd = ['pdflatex', '-interaction', 'nonstopmode', 'cover.tex']
proc = subprocess.Popen(cmd)
proc.communicate()

# Check for errors and handle output
retcode = proc.returncode
if not retcode == 0:
    os.unlink('cover.pdf')
    raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))

# Clean up auxiliary files
os.unlink('cover.tex')
os.unlink('cover.log')
os.unlink('cover.aux')

# Display the generated PDF
from IPython.display import FileLink, display
display(FileLink('cover.pdf'))
