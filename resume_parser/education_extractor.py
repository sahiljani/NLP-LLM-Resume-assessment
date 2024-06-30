import re

from resume_parser.gemini import generate_structured_json

# def extract_education(education_text):
#     print(education_text)
#     print("Extracting education")
    
#     pattern = re.compile(r"([\w\s]+)\s+([\w\s]+),\s+([A-Za-z\s]+)\s+(\d{4})\s+[-–]\s+(\w+)", re.MULTILINE)
#     matches = pattern.findall(education_text)
#     educations = [{
#         'Institution': m[0].strip(),
#         'Location': m[1].strip(),
#         'Degree': m[2].strip(),
#         'Start Year': m[3],
#         'End Year': m[4]
#     } for m in matches]
#     return educations


def extract_education(education_text):
    prompt = f"""
    Extract Education from the following text:
    Given the following Educations text, convert each education entry into a structured JSON format with keys for 
    Institution, Location, Degree, Start Year, and End Year 
    " {education_text} "

    MUST RETURN JSON WITH GIVEN FORMAT 
    """
    
    response = generate_structured_json(prompt)
    print(response)
    return response
