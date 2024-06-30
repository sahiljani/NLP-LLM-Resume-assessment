from pylatex import Document, Section, Subsection, Command, Tabular, NewLine, LineBreak
from pylatex.utils import NoEscape


def generate_resume():
    data = {
    "Education": [],
    "Personal Info": {
        "Email": "divyapatel4572@gmail.com",
        "GitHub": "github.com/DivyaPatel304",
        "LinkedIn": "linkedin.com/in/iamdivyapatel",
        "Location": "Canada",
        "Name": "Divya Patel",
        "Phone": "437-799-2908"
    },
    "Projects": [
        {
            "Description": "Music Recommendation System |Python, TensorFlow, Flask Feb 2024 - Apr 2024 \u2022Built a music recommendation system using Python and TensorFlow, handling a database of 120,000+ songs with recommendations generated in just 300ms. \u2022Implemented content-based filtering and cosine similarity for tailored song recommendations. Georgian College Auto Show |React Native, Firebase, Google Maps API May 2023 \u2013 Aug 2023 \u2022Led the development of an advanced mobile app for Georgian College\u2019s auto shows using React Native, Firebase, and Google Maps API, featuring dynamic ticketing, interactive location viewing, and real-time event notifications. \u2022Maintained proactive client communication to ensure alignment and successful project deployment. Push Notification Platform |Node.js, React.js, Google Firebase May 2021 - Aug 2021 \u2022Developed an innovative SaaS push notification platform using PHP, Next.js, and Google Firebase Cloud Messaging, designed to deliver targeted notifications efficiently. \u2022Achieved under 100 milliseconds latency and over 98% delivery success rate through optimized algorithms."
        }
    ],
    "Skills": "",
    "Work Experience": [
        {
            "company": "Cyberstrek Technologies",
            "dateRange": "Jun 2021 - Jan 2023",
            "jobTitle": "Web Developer",
            "location": "Ahmedabad - India",
            "responsibilities": [
                "Leveraged Node.js for backend development and MySQL for database optimization to boost server-side processes by 40% and elevate application performance by 30%.",
                "Directed the entire process from gathering client requirements to crafting tailored solutions, deploying, monitoring, and debugging multiple web applications.",
                "Sustained ongoing support for 20 web applications, ensuring 95% client satisfaction through rapid issue resolution."
            ]
        },
        {
            "company": "Euroteck India",
            "dateRange": "Dec 2021 - May 2021",
            "jobTitle": "Software Developer - Internship",
            "location": "Ahmedabad - India",
            "responsibilities": [
                "Developed an advanced ERP system for Euroteck India using MySQL and Flask; increased resource allocation accuracy by 35% and reduced inventory discrepancies by 20%, optimizing overall workflow.",
                "Seamlessly transitioned paper-based workflows into the ERP within 6 months, significantly improving efficiency.",
                "Advanced continuous improvement processes by regularly updating based on comprehensive bug analytics and client feedback, resulting in a 70% reduction in client-reported issues."
            ]
        }
    ]
}

    doc = Document()
    
    # Personal Info
    with doc.create(Section('Personal Information')):
        doc.append(f"Name: {data['Personal Info']['Name']}")
        doc.append(LineBreak())
        doc.append(f"Location: {data['Personal Info']['Location']}")
        doc.append(LineBreak())
        doc.append(f"Phone: {data['Personal Info']['Phone']}")
        doc.append(LineBreak())
        doc.append(f"Email: {data['Personal Info']['Email']}")
        doc.append(LineBreak())
        doc.append(f"GitHub: {data['Personal Info']['GitHub']}")
        doc.append(LineBreak())
        doc.append(f"LinkedIn: {data['Personal Info']['LinkedIn']}")

    # Work Experience
    with doc.create(Section('Work Experience')):
        for experience in data['Work Experience']:
            with doc.create(Subsection(experience['company'])):
                doc.append(f"Job Title: {experience['jobTitle']} ({experience['dateRange']})")
                doc.append(LineBreak())
                doc.append(f"Location: {experience['location']}")
                doc.append(LineBreak())
                doc.append("Responsibilities:")
                doc.append(LineBreak())
                for responsibility in experience['responsibilities']:
                    doc.append(f"- {responsibility}")
                    doc.append(LineBreak())

    # Projects
    with doc.create(Section('Projects')):
        for project in data['Projects']:
            doc.append(project['Description'].replace("\u2022", "-").replace("\u2013", "-"))
            doc.append(LineBreak())
    # Generate PDF
    doc.generate_pdf('resume', clean_tex=False)
    print("Resume generated successfully")

