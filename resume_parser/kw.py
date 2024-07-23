import spacy
import json

nlp = spacy.load("en_core_web_sm")

def suggest_verbs(text):

    verb_pairs = {
    "help": ["Facilitated", "Enabled"],
    "work": ["Collaborated", "Engineered"],
    "do": ["Executed", "Achieved"],
    "make": ["Developed", "Generated"],
    "use": ["Utilized", "Leveraged"],
    "manage": ["Directed", "Orchestrated"],
    "assist": ["Supported", "Contributed"],
    "support": ["Advocated", "Championed"],
    "handle": ["Administered", "Oversaw"],
    "conduct": ["Executed", "Performed"],
    "complete": ["Accomplished", "Finalized"],
    "create": ["Designed", "Formulated"],
    "prepare": ["Organized", "Devised"],
    "provide": ["Supplied", "Delivered"],
    "implement": ["Instituted", "Established"],
    "improve": ["Enhanced", "Optimized"],
    "learn": ["Mastered", "Acquired"],
    "teach": ["Educated", "Instructed"],
    "involve": ["Engaged", "Incorporated"],
    "participate": ["Contributed", "Engaged"],
    "lead": ["Spearheaded", "Directed"],
    "see": ["Observed", "Noticed"],
    "start": ["Initiated", "Launched"],
    "build": ["Constructed", "Created"],
    "say": ["Communicated", "Expressed"],
    "write": ["Authored", "Composed"],
    "show": ["Demonstrated", "Illustrated"],
    "find": ["Discovered", "Uncovered"],
    "fix": ["Resolved", "Rectified"],
    "sell": ["Marketed", "Negotiated"],
    "buy": ["Purchased", "Acquired"],
    "give": ["Presented", "Distributed"],
    "get": ["Received", "Obtained"],
    "choose": ["Selected", "Elected"],
    "talk": ["Discussed", "Conversed"],
    "arrange": ["Coordinated", "Organized"],
    "change": ["Modified", "Transformed"],
    "reduce": ["Decreased", "Minimized"],
    "save": ["Conserved", "Preserved"],
    "spend": ["Allocated", "Invested"],
    "design": ["Conceptualized", "Outlined"],
    "decide": ["Determined", "Concluded"],
    "understand": ["Grasped", "Comprehended"],
    "examine": ["Inspected", "Analyzed"],
    "explain": ["Clarified", "Elucidated"],
    "win": ["Secured", "Achieved"],
    "lose": ["Forfeited", "Misplaced"],
    "deliver": ["Implemented", "Executed"],
    "test": ["Evaluated", "Assessed"],
    "review": ["Analyzed", "Appraised"],
    "research": ["Investigated", "Explored"],
    "share": ["Distributed", "Disseminated"],
    "influence": ["Persuaded", "Shaped"],
    "exceed": ["Surpassed", "Outperformed"],
    "pitch": ["Proposed", "Presented"],
    "forecast": ["Predicted", "Projected"],
    "identify": ["Recognized", "Diagnosed"],
    "plan": ["Strategized", "Mapped"],
    "solve": ["Resolved", "Addressed"],
    "streamline": ["Simplified", "Optimized"],
    "train": ["Mentored", "Guided"],
    "spearhead": ["Led", "Directed"],
    "audit": ["Examined", "Reviewed"],
    "strengthen": ["Reinforced", "Bolstered"],
    "clarify": ["Elucidated", "Explained"],
    "eliminate": ["Eradicated", "Removed"],
    "achieve": ["Accomplished", "Attained"],
    "update": ["Revised", "Refreshed"],
    "monitor": ["Tracked", "Supervised"],
    "oversee": ["Supervised", "Directed"],
    "maximize": ["Optimized", "Enhanced"],
    "negotiate": ["Bargained", "Arranged"],
    "complete": ["Finalized", "Concluded"]
}

    doc = nlp(text)
    
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]

    suggestions = {}
    matched_verbs = []
    for verb in verbs:
        if verb in verb_pairs:
            matched_verbs.append(verb)
            suggestions[verb] = verb_pairs[verb]
    
    return {
        "matched_verbs": matched_verbs,
        "suggestions": suggestions
    }



text = """
{
    "Education": [
        {
            "Degree": "Post-Graduation in Artificial Intelligence",
            "End Year": "2024",
            "Institution": "Georgian College",
            "Location": "Ontario, Canada",
            "Start Year": "2024"
        },
        {
            "Degree": "Post-Graduation in Mobile Application Development",
            "End Year": "2023",
            "Institution": "Georgian College",
            "Location": "Ontario, Canada",
            "Start Year": "2023"
        },
        {
            "Degree": "Bachelor of Engineering - Computer Engineering",
            "End Year": "2021",
            "Institution": "Gujarat Technological University",
            "Location": "Gujarat, India",
            "Start Year": "2017"
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
    "Skills": "HTML\nCSS\nJavaScript\nTypescript\nNext.js\nPHP\nJava\nPython\nNode.js\nSpring Boot\nLaravel\nDatabase\nSQL\nMySQL\nPostgreSQL\nNoSQL\nMongoDB\nAzure\nDocker\nKubernetes\nPostman\nAPI",
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
                "Implemented Scrum methodologies, enhancing team responsiveness and productivity.",
                "Managed application deployment with Git and CI/CD pipelines, ensuring smooth transitions from development to production.",
                "Implemented scalable, secure cloud infrastructure with AWS services, improving application performance."
            ]
        }
    ]
}
"""

# result = suggest_verbs(text, verb_pairs)
# print(json.dumps(result['suggestions'], indent=6))