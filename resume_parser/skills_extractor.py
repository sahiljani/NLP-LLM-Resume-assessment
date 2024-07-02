import spacy
import json
import os
# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Read skill patterns from jsonl file
skill_patterns = []
# write path that start from root directory root/skill_patterns.jsonl

with open(os.path.join("data", "skill_patterns.jsonl"), 'r') as file:
    for line in file:
        pattern = json.loads(line.strip())
        skill_patterns.append(pattern)

# Add patterns to the EntityRuler
ruler = nlp.add_pipe('entity_ruler', before='ner')
ruler.add_patterns(skill_patterns)

# Function to extract skills from the skills section text
def extract_skills(skills_section):
    doc = nlp(skills_section)
    skills = [ent.text for ent in doc.ents if ent.label_.startswith("SKILL")]
    return '\n'.join(skills)
