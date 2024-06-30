import re
import spacy

nlp = spacy.load('en_core_web_sm')

def extract_personal_info(text):
    name = None
    phone = None
    email = None
    linkedin = None
    github = None
    location = None

    phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    linkedin_pattern = re.compile(r'linkedin\.com/in/[A-Za-z0-9_-]+')
    github_pattern = re.compile(r'github\.com/[A-Za-z0-9_-]+')

    phone_match = phone_pattern.search(text)
    if phone_match:
        phone = phone_match.group()

    email_match = email_pattern.search(text)
    if email_match:
        email = email_match.group()

    linkedin_match = linkedin_pattern.search(text)
    if linkedin_match:
        linkedin = linkedin_match.group()

    github_match = github_pattern.search(text)
    if github_match:
        github = github_match.group()

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON' and not name:
            name = ent.text.strip()
        elif ent.label_ == 'GPE' and not location:
            location = ent.text.strip()

    return {
        'Name': name,
        'Phone': phone,
        'Email': email,
        'LinkedIn': linkedin,
        'GitHub': github,
        'Location': location
    }