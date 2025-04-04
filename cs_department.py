import sqlite3

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect('cs_department.db')
cursor = conn.cursor()

# Create table for storing responses
cursor.execute('''
CREATE TABLE IF NOT EXISTS responses (
    intent TEXT PRIMARY KEY,
    response TEXT NOT NULL
)
''')

# Insert sample responses
responses = [
    ("courses_offered", "Programs Offered by the CS Department:\n"
                        "• Postgraduate Programs:\n"
                        "  - MSc Computer Science (MSc CS)\n"
                        "  - MSc Data Science (MSc DS)\n"
                        "  - MSc Artificial Intelligence (MSc AI)\n"
                        "• Research Programs:\n"
                        "  - MPhil in Computer Science\n"
                        "  - PhD in Computer Science"),
    
    ("about_cs_department", "• The Department of Computer Science was established in 2005.\n"
                         "• It has dedicated faculty, technical staff, and students.\n"
                         "• Offers MSc, MPhil, and PhD programs.\n"
                         "• Known for its discipline and research excellence."),
    
    ("cs_research_labs", "• Data Analytics and AI Research: Text, image, healthcare data analytics.\n"
                      "• Bioinformatics & Speech Recognition: Protein analysis, speech enhancement.\n"
                      "• IoT & Wireless Networks: Remote sensing, medical image analysis."),
    
    ("department_milestones", "• Publishes International Journal of Scientific Research in Computing (IJSRC).\n"
                   "• RUSA Phase-I project with Rs.20 crores budget.\n"
                   "• Online ERP for admissions, finance, and exams."),
    
    ("department_features", "• Covers software, hardware, databases, security, and AI.\n"
                               "• Offers fellowships from INSPIRE, RGNF, and URF.\n"
                               "• High-quality research publications."),
    
    ("msc_data_science_eligibility", "• A Pass in B.Sc. Statistics / Mathematics / CS / BCA / IT or equivalent."),
    ("msc_data_science_strength", "• 30 students per batch."),
    ("msc_data_science_duration", "• Duration: 2 Years."),
    ("msc_data_science_syllabus", "Here is the syllabus:\n"
                                   "(https://drive.google.com/file/d/1CnX1mIv93QEq-SwWi73GDG0pfRSGZ_Li/view)"),
    
    ("msc_cs_eligibility", "• A Pass in B.Sc. Computer Science, B.C.A., B.Sc. (IT), or equivalent."),
    ("msc_cs_strength", "• 40 students per batch."),
    ("msc_cs_duration", "• Duration: 2 Years."),
    ("msc_cs_syllabus", "Here is the syllabus:\n"
                        "(https://drive.google.com/file/d/1RrRgDe43OWkyuAu12AnZnwWwQl1x2ZOp/view)"),
    
    ("msc_ai_eligibility", "• A Pass in B.Sc. Computer Science / IT / Computer Applications or equivalent."),
    ("msc_ai_strength", "• 30 students per batch."),
    ("msc_ai_duration", "• Duration: 2 Years."),
    ("msc_ai_syllabus", "Here is the syllabus:\n"
                        "(https://drive.google.com/file/d/16fSEBJsyC8W1yYNPkqQYudWaqQG_ttWB/view)"),
    
    ("mphil_eligibility", "• Candidates with a Master’s degree from Bharathiar University or equivalent."),
    ("mphil_exclusions", "• Candidates with M.E., M.Tech., Medicine, Law, Agriculture are **not eligible**."),
    ("mphil_key_requirements", "• Only candidates with a PG degree and 17 years of study duration are eligible."),
    
    ("phd_eligibility", "• Candidates must have completed a PG degree with a total of 17 years of study."),
    ("phd_exclusions", "• Candidates with M.E., M.Tech., Medicine, Law, Agriculture are **not eligible**."),
    ("phd_key_requirements", "• Only candidates with a PG degree and 17 years of study duration are eligible."),
    
    ("unknown", "I'm not sure about that. Can you rephrase your question?")
    
]

cursor.executemany("INSERT OR REPLACE INTO responses (intent, response) VALUES (?, ?)", responses)

# Commit and close
conn.commit()
conn.close()

print("Database setup complete!")
