import re
from resume_parser.personal_info_extractor import extract_personal_info
from resume_parser.education_extractor import extract_education
from resume_parser.work_experience_extractor import extract_work_experience
from resume_parser.projects_extractor import extract_projects  
from resume_parser.skills_extractor import extract_skills  
import time
def parse_resume(resume_text):
    sections = {'Profile': '', 'Education': '', 'Projects': '', 'Work Experience': '', 'Skills': ''}
    section_patterns = {
        'Profile': r'^(Profile|Summary):?',
        'Education': r'^(Education|Academic Background):?',
        'Projects': r'^(Projects|Portfolio):?',
        'Work Experience': r'^(Experience|Work Experience|Professional Background):?',
        'Skills': r'^(Technical Skills|Skills):?'
    }

    resume_text = resume_text.replace('\r', '\n').strip()
    lines = resume_text.split('\n')
    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        matched = False
        for section, pattern in section_patterns.items():
            if re.match(pattern, line, re.IGNORECASE):
                current_section = section
                matched = True
                break
        if not matched and current_section:
            sections[current_section] += line + '\n'

    personal_info = extract_personal_info(resume_text)

    education = extract_education(sections.get('Education', ''))
    work_experience = extract_work_experience(sections.get('Work Experience', ''))
    projects = extract_projects(sections.get('Projects', ''))
    skills = extract_skills(sections.get('Skills', ''))

    # print(projects)
    data = {
        'Personal Info': personal_info,
        'Education': education,
        'Work Experience': work_experience,
        'Projects': projects,
        'Skills': skills
       
    }

    # timestamp = time.strftime("%Y%m%d%H%M%S")
    # file_name = f'parsed_resume_{timestamp}.txt'

    # # Save to a text file
    # with open(file_name, 'w', encoding='utf-8') as file:
    #     for key, value in data.items():
    #         file.write(f'{key}:\n{value}\n\n')
    
    # print(f"Resume parsed and saved to '{file_name}.txt'")

    return data
