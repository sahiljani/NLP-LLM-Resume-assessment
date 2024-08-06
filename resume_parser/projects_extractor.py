import re
from resume_parser.gemini import generate_structured_json


def extract_projects(projects_text):
    prompt = f"""
    Extract Projects from the following text:
    Given the following Projects text, convert each project entry into a structured JSON format with keys for 
    Project_title, Project_description, Project_links, Project_dates, and project_skills 
    " {projects_text} "

    MUST RETURN JSON WITH GIVEN FORMAT 
    """
    
    response = generate_structured_json(prompt)
    print(response)
    return response


# def extract_projects(projects_text):
#     projects = []
#     current_project = {}
#     lines = projects_text.split('\n')

#     project_title_pattern = re.compile(r'^\s*(Project|Title|Name):?\s*(.*)', re.IGNORECASE)
#     date_pattern = re.compile(r'^\s*(Date|Duration):?\s*(.*)', re.IGNORECASE)
#     description_pattern = re.compile(r'^\s*(Description|Details):?\s*(.*)', re.IGNORECASE)
#     responsibility_pattern = re.compile(r'^\s*(Responsibilities|Tasks):?\s*(.*)', re.IGNORECASE)

#     for line in lines:
#         line = line.strip()
#         if not line:
#             continue

#         title_match = project_title_pattern.match(line)
#         date_match = date_pattern.match(line)
#         description_match = description_pattern.match(line)
#         responsibility_match = responsibility_pattern.match(line)

#         if title_match:
#             if current_project:
#                 projects.append(current_project)
#                 current_project = {}
#             current_project['Title'] = title_match.group(2).strip()
#         elif date_match:
#             current_project['Date'] = date_match.group(2).strip()
#         elif description_match:
#             current_project['Description'] = description_match.group(2).strip()
#         elif responsibility_match:
#             current_project['Responsibilities'] = responsibility_match.group(2).strip()
#         else:
#             if 'Description' in current_project:
#                 current_project['Description'] += ' ' + line
#             else:
#                 current_project['Description'] = line

#     if current_project:
#         projects.append(current_project)

#     return projects