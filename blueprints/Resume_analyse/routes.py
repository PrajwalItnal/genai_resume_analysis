from flask import Blueprint,json, render_template, request, redirect, url_for, flash
from .Gemini_API.API import ChatBot
import re

analyse = Blueprint('analyse', __name__, template_folder='template')

@analyse.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        file = request.files.get('file')
        role = request.form.get('Role')
        quesummary = extract_text(file) + f"""
            Read the above resume and return ONLY one single valid JSON object with this exact schema:

            1. is_resume: true or false
            2. name: candidate name
            3. email: candidate email
            4. phone: candidate phone number
            5. education: object with keys matrix, post_matrix, UG, PG, other 
            (each containing degree, duration, institution, aggregate; use null if missing)
            6. skills: object with keys backend, frontend, database, soft_skills, core, tools, other 
            (arrays of strings)
            7. experience: array of objects with company name, role, duration, work done; use empty array if missing
            8. points: analisis in this resume and get the percentage how much points it is gets based on the role:{role} main things only in integer format
            9. description : analysis in ths resome and give the descition in 20 words in sentence format based on the role:{role} main things only
            10. missing_skills : analysis in this resume provide the missing skills based on the role:{role} in array format main things only
            11. drawbacks : analysis in this resume and provide the drawbacks in 20 words sentance format based on the role:{role} main things only
            12. improvements : analysis in this resume and provide the improvements in 20 words sentance format based on the role:{role} main things only
            13. summary : based on all above things give the summary in sentence format in 200 words based on the role:{role} main things only
            14. short_education : provide the education based on the above resume in a short format 10 tokens
            15. key_skills : provide the key skills based on the above resume in a short format 10 tokens in a array format
            16. resume_highlights : provide the short summary based on above resume in 20 tokens
            ⚠️ Rules:
            - Do not return anything other than JSON.
            - Do not add explanations, comments, or formatting.
            - Missing values must be null (not "null").
            - Return only one valid JSON object, nothing else.
            """


        summary = generate_response(quesummary, -1).strip().replace('"null"', 'null')
        resume_valid = True
        report = {}

        if summary == "false":
            flash('Unable to get response from API. Please try again later.', 'error')
            return redirect(url_for('analyse.index'))

        if not summary == "false":
            try:
                # Remove anything before first "{" and after last "}"
                cleaned = re.search(r'\{.*\}', summary, re.DOTALL)
                if cleaned:
                    summary = cleaned.group(0)
                else:
                    raise ValueError("No JSON object found in response")

                # Replace "null" (as string) with null
                summary = summary.replace('"null"', 'null')

                # Parse JSON safely
                summary = json.loads(summary)

                report = {
                "name" : summary.get("name"),
                "points" : summary.get("points"),
                "description" : summary.get("description"),
                "missing_skills" : summary.get("missing_skills"),
                "drawbacks" : summary.get("drawbacks"),
                "improvements" : summary.get("improvements"),
                "experience" : summary.get("experience"),
                "key_skills" : summary.get("key_skills"),
                "summary" : summary.get("resume_highlights"),
                "education" : summary.get("short_education")
                 }
                print("Final JSON:", summary,"\n")
                print("Report:", report)


            except Exception as e:
                print("Error decoding JSON:", e)
            
                
        #Check the Data is valid or not
        try:
             resume_valid = summary.get("is_resume") == True
        except Exception as e:
            print(e)
            resume_valid = False
        
        
        if resume_valid:
            return render_template('checker.html',report = report)
        else:
            flash('Upload the valid Resume', 'error')
            return redirect(url_for('analyse.index'))


#Extracting text from file
import pdfplumber
def extract_text(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"     
    return text



def generate_response(user_input, budget=50):
    retries = 3
    
    for i in range(retries):
        try:
            respons = ChatBot(user_input, budget)
            return respons
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            if i < retries -1:
                continue
            else:
                print("Unable to get the response")
                return "false"
