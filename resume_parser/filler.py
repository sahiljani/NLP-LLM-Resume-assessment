import spacy
import json


# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# List of filler words/phrases
filler_words = [
    "in order to", "as needed", "responsible for", "worked with", "participated in", 
    "assisted in", "in charge of", "was involved in", "took part in", "engaged in", 
    "in the process of", "due to the fact that", "for the purpose of", "a variety of", 
    "as a result of", "at this point in time", "in the event that", "in terms of", 
    "with regard to", "on a regular basis", "at all times", "in the near future", 
    "in the course of", "have the ability to", "as a means of", "for all intents and purposes", 
    "for the most part", "as a matter of fact", "to be honest", "at the present time", 
    "each and every", "at this juncture", "by means of", "for the time being", 
    "have a tendency to", "in my opinion", "in the final analysis", "in the first place", 
    "in the meantime", "in the midst of", "in the process of", "it should be noted that", 
    "needless to say", "on a daily basis", "on a monthly basis", "on a weekly basis", 
    "over the course of", "the fact that", "there is no doubt that", "until such time as", 
    "with respect to", "with the exception of", "with this in mind", "despite the fact that", 
    "in light of the fact that", "in order that", "until such time as", "during the time that", 
    "under the circumstances", "with reference to"
]

# Function to detect filler words
def detect_filler_words(text):
    doc = nlp(text.lower())
    detected_fillers = []
    
    for filler in filler_words:
        if filler in doc.text:
            detected_fillers.append(filler)
    
    return detected_fillers



# Function to check consistency
def check_consistency(json_data):
    data = json.loads(json_data)
    issues = []

    # Check for consistent capitalization in job titles and institutions
    if 'Work Experience' in data:
        job_titles = [exp.get('job_title', '') for exp in data['Work Experience']]
        for title in job_titles:
            if title and title.lower() != title and title.upper() != title and title.title() != title:
                issues.append({
                    'type': 'consistency',
                    'message': f'Inconsistent capitalization in job title: "{title}"'
                })

    if 'Education' in data:
        institutions = [edu.get('Institution', '') for edu in data['Education']]
        for institution in institutions:
            if institution and institution.lower() != institution and institution.upper() != institution and institution.title() != institution:
                issues.append({
                    'type': 'consistency',
                    'message': f'Inconsistent capitalization in institution name: "{institution}"'
                })

    # Check for consistent use of terms
    term_usage = {}
    for exp in data.get('Work Experience', []):
        for responsibility in exp.get('responsibilities', []):
            words = responsibility.split()
            for word in words:
                word_lower = word.lower()
                if word_lower not in term_usage:
                    term_usage[word_lower] = set()
                term_usage[word_lower].add(word)

    for term, variations in term_usage.items():
        if len(variations) > 1:
            issues.append({
                'type': 'consistency',
                'message': f'Inconsistent use of the term "{term}": {", ".join(variations)}'
            })

    return issues

# Function to check tone
def check_tone(json_data):
    data = json.loads(json_data)
    issues = []
    informal_words = {'stuff', 'things', 'cool', 'awesome', 'nice', 'great'}

    def check_text(text):
        words = text.split()
        for word in words:
            if word.lower() in informal_words:
                issues.append({
                    'type': 'tone',
                    'message': f'Informal word "{word}" found. Consider using more professional language.'
                })

    for exp in data.get('Work Experience', []):
        for responsibility in exp.get('responsibilities', []):
            check_text(responsibility)

    for project in data.get('Projects', []):
        check_text(project.get('Description', ''))

    return issues