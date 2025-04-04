import sqlite3
import spacy
from flask import Flask, request, jsonify
from sklearn.metrics import classification_report
from fuzzywuzzy import fuzz

# Load SpaCy NLP Model
nlp = spacy.load("en_core_web_lg")

# Initialize Flask App
app = Flask(__name__)

# Expanded keyword training data (10+ variations per intent)
KEYWORDS = {
    "courses_offered": [
        "what courses do you offer?", "list of programs", "degrees available",
        "what can I study here?", "available postgraduate courses",
        "tell me about CS programs", "options after graduation",
        "what are the research programs?", "MSc specializations",
        "do you offer data science?", "computer science courses",
        "what masters programs are available?", "PG courses in CS"
    ],
    
    "about_cs_department": [
        "tell me about the department", "history of CS department",
        "what makes this department special?", "faculty information",
        "when was the department established?", "overview of computer science dept",
        "strengths of this department", "research areas",
        "achievements of the department", "why choose this department?",
        "department background", "information about CS department"
    ],

    "cs_research_labs": [
        "what research labs are available?", "list of research facilities",
        "tell me about your labs", "research areas in the department",
        "what kind of research do you do?", "AI research facilities",
        "data analytics labs", "bioinformatics research",
        "IoT research capabilities", "wireless networks lab",
        "healthcare data research", "speech recognition labs"
    ],

    "msc_data_science_eligibility": [
        "requirements for MSc DS", "who can apply for data science?",
        "eligibility criteria for MSc Data Science", "qualifications needed",
        "can I apply with a math degree?", "minimum marks for MSc DS",
        "does BCA qualify for data science?", "required background","tell me who are eligible for msc data science"
        "is statistics mandatory?", "admission requirements for DS",
        "what degree do I need for data science?", "can I join MSc DS with IT background?"
    ],

    "msc_cs_eligibility": [
        "who can apply for MSc CS?", "eligibility for computer science master's",
        "requirements for MSc Computer Science", "CS MSc admission criteria",
        "what qualifications are needed for MSc CS?", "do I need a CS degree?",
        "can IT students apply for MSc CS?", "minimum marks required for CS MSc","tell me who are eligible for msc cs"
        "eligibility for MSc in computer science?", "does BSc in physics qualify for MSc CS?",
        "is programming knowledge required for MSc CS?", "who is eligible for CS master's?"
    ],

    "msc_ai_eligibility": [
        "who can apply for MSc AI?", "eligibility for artificial intelligence master's",
        "requirements for MSc Artificial Intelligence", "AI MSc admission criteria",
        "what qualifications are needed for MSc AI?", "do I need a CS degree for AI?",
        "can IT students apply for MSc AI?", "minimum marks required for MSc AI","tell me who are eligible for msc ai",
        "eligibility for MSc in artificial intelligence?", "does a non-CS background qualify for MSc AI?",
        "is machine learning knowledge required for MSc AI?", "who is eligible for MSc AI?"
    ],

    "msc_cs_duration": [
        "how long is the MSc cs program?", "duration of MSc cs course?",
        "what is the time frame for MSc cs studies?", "length of MSc cs courses?",
        "MSc cs program length in years",
        "total duration of MSc cs program?",
        "time required to complete MSc cs?", "how long to finish MSc cs?",
        "what is the study period for MSc cs?",
    ],
    
    "msc_data_science_duration": [
        "how long is the MSc ds program?", "duration of MSc ds courses?",
        "what is the time frame for MSc ds studies?", "length of MSc ds courses?",
        "MSc ds program length in years",
        "total duration of MSc ds program?",
        "time required to complete MSc ds?", "how long to finish MSc ds?",
        "what is the study period for MSc ds?",
    ],

    "msc_ai_duration": [
        "how long is the MSc ai program?", "duration of MSc ai courses?",
        "what is the time frame for MSc ai studies?", "length of MSc ai courses?",
        "MSc ai program length in years",
        "total duration of MSc ai program?",
        "time required to complete MSc ai?", "how long to finish MSc ai?",
        "what is the study period for MSc ai?",
    ],

    "msc_cs_strength": [
        "what is the student intake for MSc cs?", "how many students per MSc cs batch?",
        "strength of MSc cs program?", "number of seats for MSc CS?",
        "student capacity for MSc cs?", "what is the batch size for MSc cs?",
        "total seats available in MSc cs programs", "how many students are admitted for MSc cs?",
        "maximum student strength in MSc cs?", "admission limit for MSc cs course?",
        "average class size for MSc cs program?", "student intake per MSc cs course?"
    ],

    "msc_data_science_strength": [
        "what is the student intake for MSc ds?", "how many students per MSc ds batch?",
        "strength of MSc ds program?", "number of seats for MSc ds?",
        "student capacity for MSc ds?", "what is the batch size for MSc ds?",
        "total seats available in MSc ds programs", "how many students are admitted for MSc ds?",
        "maximum student strength in MSc ds?", "admission limit for MSc ds course?",
        "average class size for MSc ds program?", "student intake per MSc ds course?"
    ],

    "msc_ai_strength": [
        "what is the student intake for MSc ai?", "how many students per MSc ai batch?",
        "strength of MSc ai program?", "number of seats for MSc ai?",
        "student capacity for MSc ai?", "what is the batch size for MSc ai?",
        "total seats available in MSc ai programs", "how many students are admitted for MSc ai?",
        "maximum student strength in MSc ai?", "admission limit for MSc ai course?",
        "average class size for MSc ai program?", "student intake per MSc ai course?"
    ],

    "msc_data_science_syllabus": [
        "what is the syllabus for MSc ds programs?", "course structure of MSc ds?",
        "MSc ds curriculum details", "subjects covered in MSc ds course?",
        "can I get the MSc ds syllabus PDF?", "detailed syllabus for MSc dS?",
        "data science MSc syllabus?",
        "topics included in MSc ds program?", "modules in MSc ds course?",
        "MSc ds course outline", "send me the MSc ds syllabus document"
    ],

    "msc_cs_syllabus": [
        "what is the syllabus for MSc cs programs?", "course structure of MSc cs?",
        "MSc cs curriculum details", "subjects covered in MSc cs course?",
        "can I get the MSc cs syllabus PDF?", "detailed syllabus for MSc cS?",
        "computer science MSc syllabus?",
        "topics included in MSc cs program?", "modules in MSc cs course?",
        "MSc cs course outline", "send me the MSc cs syllabus document"
    ],

    "msc_ai_syllabus": [
        "what is the syllabus for MSc ai programs?", "course structure of MSc ai?",
        "MSc ai curriculum details", "subjects covered in MSc ai course?",
        "can I get the MSc ai syllabus PDF?", "detailed syllabus for MSc ai?",
        "artificial intelligence MSc syllabus?",
        "topics included in MSc ai program?", "modules in MSc ai course?",
        "MSc ai course outline", "send me the MSc ai syllabus document"
    ],

    "mphil_eligibility": [
        "who can apply for MPhil?",
        "what are the criteria for Mphil admission?", "MPhil application requirements?",
        "qualifications needed for MPhil?", "minimum marks for Mphil admission?",
        "can MSc graduates apply for Mphil?", "who is eligible for MPhil?",
        "Mphil admission process and criteria?","tell me who are eligible for mphil",
        "requirements for joining MPhil?", "academic qualifications for MPhil?"
    ],

    "mphil_exclusions": [
        "who cannot apply for MPhil?", "exclusions in Mphil admissions?",
        "disqualifications for MPhil?",
        "who is ineligible for Mphil?", "does work experience matter for Mphil admission?",
        "can BSc students apply for Mphil?", "who is restricted from MPhil enrollment?",
        "limitations for mphil applicants?", "age limits for MPhil admissions?",
        "what conditions exclude MPHIL applicants?", "MPhil eligibility restrictions?"
    ],

    "mphil_key_requirements": [
        "what documents are needed for MPhil admission?", "requirements for MPhil research?",
        "mandatory qualifications for Mphil?", "how to apply for MPhil?",
        "list of documents for Mphil application?",
        "what exams are required for MPHIL?", "key requirements for MPhil enrollment?",
        "minimum CGPA for Mphil?", "MPhil research proposal requirements?",
        "do I need a thesis for Mphil admission?", "what are the academic requirements for Mphil?"
    ],
    "phd_eligibility": [
        "who can apply for PhD?",
        "what are the criteria for PhD admission?", "PhD application requirements?",
        "qualifications needed for PhD?", "minimum marks for PhD admission?",
        "can MSc graduates apply for PhD?", "who is eligible for Phd?",
        "PhD admission process and criteria?","tell me who are eligible for phd",
        "requirements for joining Phd?", "academic qualifications for PhD?"
    ],

    "phd_exclusions": [
        "who cannot apply for PhD?", "exclusions in PhD admissions?",
        "disqualifications for Phd?",
        "who is ineligible for PhD?", "does work experience matter for PhD admission?",
        "can BSc students apply for PhD?", "who is restricted from Phd enrollment?",
        "limitations for PhD applicants?", "age limits for PhD admissions?",
        "what conditions exclude PhD applicants?", "PHD eligibility restrictions?"
    ],

    "phd_key_requirements": [
        "what documents are needed for PhD admission?", "requirements for Phd research?",
        "mandatory qualifications for PhD?", "how to apply for Phd?",
        "list of documents for PhD application?",
        "what exams are required for PhD?", "key requirements for PhD enrollment?",
        "minimum CGPA for PhD?", "Phd research proposal requirements?",
        "do I need a thesis for PhD admission?", "what are the academic requirements for PhD?"
    ],

    "department_features": [
        "what are the best features of this department?", "why is this CS department special?",
        "highlights of the computer science department", "what makes your department unique?",
        "strengths of your department?", "facilities available in the CS department?",
        "key advantages of this department?", "why should I choose this CS department?",
        "important aspects of this department?", "what benefits does the department offer?",
        "top features of the CS faculty?", "what makes this department stand out?"
    ],

    "department_milestones": [
        "what are the achievements of this department?", "important milestones of the CS department?",
        "biggest accomplishments of your department?", "what are the key successes of the CS faculty?",
        "notable research contributions from this department?", "recognitions received by the CS faculty?",
        "awards won by the department?", "historical successes of this department?",
        "departmental honors and achievements?", "research breakthroughs in this department?",
        "major recognitions in the CS department?", "success stories from the faculty?"
    ]

}

# Database connection
def get_db_connection():
    conn = sqlite3.connect('cs_department.db')
    conn.row_factory = sqlite3.Row
    return conn

# Intent classification using similarity scoring
def classify_intent(user_input):
    user_input = user_input.lower().strip()
    if not user_input:
        return "unknown"
    
    doc = nlp(user_input)
    best_match = None
    highest_score = 0.7  # Minimum threshold
    
    for intent, phrases in KEYWORDS.items():
        for phrase in phrases:
            phrase_doc = nlp(phrase)
            similarity = doc.similarity(phrase_doc)
            # Fuzzy Matching for typo handling
            fuzzy_score = fuzz.ratio(user_input, phrase) / 100
            combined_score = (similarity * 0.7) + (fuzzy_score * 0.3)
            
            if similarity > highest_score:
                highest_score = similarity
                best_match = intent
                
    if not best_match:
        log_unmatched_query(user_input)  # Log unknown queries for analysis
    return best_match if best_match else "unknown"

# Fetch response from database
def get_response(intent):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT response FROM responses WHERE intent = ?", (intent,))
        result = cursor.fetchone()
        conn.close()
        return result['response'] if result else None
    except Exception as e:
        print(f"Database error: {e}")
        return None

# Model evaluation
def evaluate_model():
    test_cases = [
        ("what courses are available?", "courses_offered"),
        ("tell me about MSc DS eligibility", "msc_data_science_eligibility"),
        ("what are the research facilities?", "cs_research_labs"),
        ("how long is the MSc cs program?", "msc_cs_duration"),
        ("tell me about department features", "department_features"),
        ("tell me about MSc AI eligibility","msc_ai_eligibility"),
        ("tell me about MSc CS eligibility","msc_cs_eligibility"),
        ("what are the achievements of this department?","department_milestones"),
        ("what are the best features of this department?","department_features"),
        ("tell me about the department","about_cs_department"),
        ("duration of MSc cs course?","msc_cs_eligibility"),
        ("duration of MSc ds course?","msc_data_science_eligibility"),
        ("duration of MSc ai course?","msc_ai_eligibility"),
        
    ]
    
    y_true = []
    y_pred = []
    
    for test_input, expected_intent in test_cases:
        predicted_intent = classify_intent(test_input)
        y_true.append(expected_intent)
        y_pred.append(predicted_intent)
    
    print("\nModel Evaluation Report:")
    print(classification_report(y_true, y_pred, zero_division=0))

# Flask API endpoint
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"response": "Please enter a valid message"}), 400
            
        intent = classify_intent(user_message)
        response = get_response(intent) or get_response("unknown")
        
        return jsonify({
            "response": response,
            "detected_intent": intent
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Running model evaluation...")
    evaluate_model()
    print("\nStarting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=False)
