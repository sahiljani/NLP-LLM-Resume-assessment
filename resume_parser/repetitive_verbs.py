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

    text = ' '.join([
        json_str,
        data["Skills"],
        ' '.join(proj["Description"] for proj in data["Projects"]),
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


# Example JSON string
json_str = """
{
    "Education": [
        {
            "Degree": "Post-Graduation in Artificial Intelligence",
            "End Year": "Aug 2024",
            "Institution": "Georgian College",
            "Location": "Ontario, Canada",
            "Start Year": "Jan 2024"
        },
        {
            "Degree": "Post-Graduation in Mobile Application Development",
            "End Year": "Dec 2023",
            "Institution": "Georgian College",
            "Location": "Ontario, Canada",
            "Start Year": "May 2023"
        },
        {
            "Degree": "Bachelor of Engineering - Computer Engineering",
            "End Year": "May 2021",
            "Institution": "Gujarat Technological University",
            "Location": "Gujarat, India",
            "Start Year": "Aug 2017"
        }
    ],
    "Personal Info": {
        "Email": "iam@janisahil.com",
        "GitHub": null,
        "LinkedIn": null,
        "Location": "Ontario",
        "Name": "Sahil Jani",
        "Phone": "249-877-2908"
    },
    "Projects": [
        {
            "Description": "Resume Tailor |Python, React Mar 2024 - Apr 2024 •Implemented advanced filtering and matching algorithms in a Resume Analyzer & Job Matching Platform using NLP and LLM, with React interface and LaTeX integration for streamlined resume creation and PDF conversion. Investor Management System (Github )|PHP, MySQL Dec 2023 - Feb 2024 •Integrated over 15 advanced filters using MySQL and Eloquent ORM to match projects with ideal investors based on specific requirements, significantly enhancing the efficiency of project-investor matching. •Built Amazon SES email-sending feature to send up to 5,000 bulk emails at once. Utilized queue system for efficient processing, including open rate tracking and reporting for detailed insights. Custom Relational Database |Java Apr 2021 - May 2021 •Implemented a fully functional relational database from scratch in Java CLI (Maven) application with data parsers to store and retrieve metadata and raw data."
        }
    ],
    "Skills": "HTML\\nCSS\\nJavaScript\\nTypescript\\nNext.js\\nPHP\\nJava\\nPython\\nNode.js\\nSpring Boot\\nLaravel\\nDatabase\\nSQL\\nMySQL\\nPostgreSQL\\nNoSQL\\nMongoDB\\nAzure\\nDocker\\nKubernetes\\nPostman\\nAPI",
    "Work Experience": [
        {
            "company": "Leasey",
            "date_range": "Jul 2023 – Dec 2023",
            "job_title": "Web Developer",
            "location": "British Columbia, Canada",
            "responsibilities": [
                "Directed transition from SaaS-based CMS to open-source CMS, reducing Subscription costs by 75% and enabling advanced functionalities.",
                "Executed custom PHP implementations for dynamic functionality, incorporating JavaScript and CSS for interactive features, achieving pixel-perfect website design and reducing bounce rate by 25%."
            ]
        },
        {
            "company": "ManticLabs Web Solutions Pvt. Ltd.",
            "date_range": "Jun 2021 – Mar 2023",
            "job_title": "Software Developer",
            "location": "Gujarat, India",
            "responsibilities": [
                "Directed end-to-end software development and coordinated with cross-functional teams, developing 15+ high performance, maintainable applications using Node.js, JavaScript, HTML, and CSS.",
                "Built dynamic, responsive user interfaces with React, enhancing user experience across multiple devices.",
                "Administered SQL and NoSQL databases, optimizing queries and indexing for optimal performance.",
                "Ensured high-quality standards and reliability through comprehensive quality assurance practices.",
                "Implemented Scrum methodologies, enhancing team responsiveness and productivity. Managed application deployment with Git and CI/CD pipelines, ensuring smooth transitions from development to production.",
                "Implemented scalable, secure cloud infrastructure with AWS services, improving application performance."
            ]
        }
    ]
}
"""


# print(repetitive_verbs(json_str))