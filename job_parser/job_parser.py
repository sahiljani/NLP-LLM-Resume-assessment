import spacy
import nltk
import jsonlines
import re
import os
import ssl

from spacy.pipeline import EntityRuler
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag, ne_chunk

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')



# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load skill patterns from jsonl file
def load_skill_patterns(file_path):
    skill_patterns = []
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            skill_patterns.append(obj)
    return skill_patterns

# Function to parse job description
def jd_parser(JD):

    skill_patterns = load_skill_patterns(os.path.join("data", "skill_patterns.jsonl"))

    # Check if 'entity_ruler' already exists in the pipeline
    if 'entity_ruler' not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before="ner")
    else:
        ruler = nlp.get_pipe("entity_ruler")
    
    ruler.add_patterns(skill_patterns)

    # Process the job description
    doc = nlp(JD)

    # Tokenization using spaCy and NLTK
    tokens_spacy = [token.text for token in doc]
    nltk_tokens = word_tokenize(JD)

    # Part-of-Speech (POS) Tagging using spaCy and NLTK
    pos_tags_spacy = [(token.text, token.pos_) for token in doc]
    nltk_pos_tags = pos_tag(nltk_tokens)

    # Named Entity Recognition (NER) using spaCy
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Chunking using NLTK
    nltk_chunks = ne_chunk(nltk_pos_tags)

    # Extract years of experience using regular expressions
    experience_pattern = re.compile(r'(\d+)\s+years? of experience')
    years_of_experience = experience_pattern.findall(JD)

    # Extract skills from the job description
    skills = []
    for ent in doc.ents:
        if "SKILL" in ent.label_:
            skills.append(ent.text)

    # Create a dictionary for the extracted information
    parsed_data = {
        "tokens_spacy": tokens_spacy,
        "tokens_nltk": nltk_tokens,
        "pos_tags_spacy": pos_tags_spacy,
        "pos_tags_nltk": nltk_pos_tags,
        "entities": entities,
        "nltk_chunks": str(nltk_chunks),
        "years_of_experience": years_of_experience,
        "skills": skills
    }
    # only return skills and remove duplication
    parsed_data = list(set(parsed_data['skills']))

    return parsed_data

# # Call the jd_parser function and store the result
# data = jd_parser()

# # Print the parsed data
# print(data)
