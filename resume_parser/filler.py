import spacy

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

# # Example text
# text = """
# {
#     "Education": [
#         {
#             "Degree": "Post-Graduation in Artificial Intelligence",
#             "End Year": "2024",
#             "Institution": "Georgian College",
#             "Location": "Ontario, Canada",
#             "Start Year": "2024"
#         },
#         {
#             "Degree": "Post-Graduation in Mobile Application Development",
#             "End Year": "2023",
#             "Institution": "Georgian College",
#             "Location": "Ontario, Canada",
#             "Start Year": "2023"
#         },
#         {
#             "Degree": "Bachelor of Engineering - Computer Engineering",
#             "End Year": "2021",
#             "Institution": "Gujarat Technological University",
#             "Location": "Gujarat, India",
#             "Start Year": "2017"
#         }
#     ],
#     "Personal Info": {
#         "Email": "iam@janisahil.com",
#         "GitHub": null,
#         "LinkedIn": null,
#         "Location": "Ontario",
#         "Name": "Sahil Jani",
#         "Phone": "249-877-2908"
#     },
#     "Projects": [
#         {
#             "Description": "Resume Tailor |Python, React Mar 2024 - Apr 2024 •Implemented advanced filtering and matching algorithms in a Resume Analyzer & Job Matching Platform using NLP and LLM, with React interface and LaTeX integration for streamlined resume creation and PDF conversion. Investor Management System (Github )|PHP, MySQL Dec 2023 - Feb 2024 •Integrated over 15 advanced filters using MySQL and Eloquent ORM to match projects with ideal investors based on specific requirements, significantly enhancing the efficiency of project-investor matching. •Built Amazon SES email-sending feature to send up to 5,000 bulk emails at once. Utilized queue system for efficient processing, including open rate tracking and reporting for detailed insights. Custom Relational Database |Java Apr 2021 - May 2021 •Implemented a fully functional relational database from scratch in Java CLI (Maven) application with data parsers to store and retrieve metadata and raw data."
#         }
#     ],
#     "Skills": "HTML\nCSS\nJavaScript\nTypescript\nNext.js\nPHP\nJava\nPython\nNode.js\nSpring Boot\nLaravel\nDatabase\nSQL\nMySQL\nPostgreSQL\nNoSQL\nMongoDB\nAzure\nDocker\nKubernetes\nPostman\nAPI",
#     "Work Experience": [
#         {
#             "company": "Leasey",
#             "date_range": "Jul 2023 – Dec 2023",
#             "job_title": "Web Developer",
#             "location": "British Columbia, Canada",
#             "responsibilities": [
#                 "Directed as needed transition from SaaS-based CMS to open-source CMS, reducing Subscription costs by 75% and enabling advanced functionalities.",
#                 "Executed custom PHP implementations for dynamic functionality, incorporating JavaScript and CSS for interactive features, achieving pixel-perfect website design and reducing bounce rate by 25%."
#             ]
#         },
#         {
#             "company": "ManticLabs Web Solutions Pvt. Ltd.",
#             "date_range": "Jun 2021 – Mar 2023",
#             "job_title": "Software Developer",
#             "location": "Gujarat, India",
#             "responsibilities": [
#                 "Directed end-to-end software development and coordinated with cross-functional teams, developing 15+ high performance, maintainable applications using Node.js, JavaScript, HTML, and CSS.",
#                 "Built dynamic, responsive user interfaces with React, enhancing user experience across multiple devices.",
#                 "Administered SQL and NoSQL databases, optimizing queries and indexing for optimal performance.",
#                 "Ensured high-quality standards and reliability through comprehensive quality assurance practices.",
#                 "Implemented Scrum methodologies, enhancing team responsiveness and productivity.",
#                 "Managed application deployment with Git and CI/CD pipelines, ensuring smooth transitions from development to production.",
#                 "Implemented scalable, secure cloud infrastructure with AWS services, improving application performance."
#             ]
#         }
#     ]
# }
# """

# # Detect filler words in the text
# detected_fillers = detect_filler_words(text)
# print("Detected filler words/phrases:", detected_fillers)
