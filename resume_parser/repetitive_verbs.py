import json
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet
import re

# Download required NLTK data files
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def get_wordnet_pos(treebank_tag):
    """
    Convert treebank POS tags to WordNet POS tags
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def repetitive_verbs(json_str):

    data = json.loads(json_str)

    # Concatenate text from all relevant sections
    text = ' '.join([
        json_str,
        data["Skills"],
        ' '.join(proj["Project_description"] for proj in data["Projects"]),
        ' '.join(' '.join(exp.get("responsibilities", "")) for exp in data.get("Work Experience", []))
    ])

    # Remove special characters and brackets
    cleaned_text = re.sub(r'[^A-Za-z\s]', '', text)

    # Tokenize the cleaned text
    tokens = word_tokenize(cleaned_text)

    # POS tagging
    pos_tags = pos_tag(tokens)

    # Filter for verbs and count repetitions
    verb_counts = {}
    for word, tag in pos_tags:
        wn_tag = get_wordnet_pos(tag)
        if wn_tag == wordnet.VERB:
            verb_counts[word] = verb_counts.get(word, 0) + 1

    # Identify repetitive verbs with count > 4
    repetitive_verbs = {verb: count for verb, count in verb_counts.items() if count > 4}

    # Return all verbs as JSON
    result = {
        "all_verbs": verb_counts,
        "repetitive_verbs": repetitive_verbs
    }
    return result['repetitive_verbs']