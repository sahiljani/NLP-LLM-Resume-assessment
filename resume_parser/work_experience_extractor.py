import re
from resume_parser.gemini import generate_structured_json

def extract_work_experience(work_text):
    prompt = f"""
    Extract work experience from the following text:
    Given the following work experience text, convert each job entry into a structured JSON format with keys for job title, date range, company, location, and bullet points describing responsibilities and achievements: 
    " {work_text} "
    """

    response = generate_structured_json(prompt)
    return response



# def extract_work_experience(work_text):
#     jobs = []
#     pattern = re.compile(r"([^\n]+)\s+(\w+\s+\d{4})\s+[-–]\s+(\w+\s+\d{4}|\w+)\s+([^\n]+)\n([^\n]+)")
    
#     for match in pattern.finditer(work_text):
#         job_info = {
#             'Job Title': match.group(1).strip(),
#             'Duration': f"{match.group(2)} - {match.group(3)}",
#             'Company': match.group(4).strip(),
#             'Location': match.group(5).strip(),
#             'Details': []
#         }
#         start_index = match.end()
#         bullet_pattern = re.compile(r"•\s+(.+)")
        
#         while start_index < len(work_text):
#             bullet_match = bullet_pattern.match(work_text, start_index)
#             if bullet_match:
#                 job_info['Details'].append(bullet_match.group(1).strip())
#                 start_index = bullet_match.end()
#             else:
#                 break
        
#         jobs.append(job_info)
    
#     return jobs