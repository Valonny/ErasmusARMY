# ErasmusARMY Recruitment FAQ AI Agent (Enhanced Version with Web Interface and Website)
from flask import Flask, request, jsonify, render_template_string
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

class MilitaryFAQAgent:
    def __init__(self):
        self.faq = {
            "What are the basic requirements to join?": "You must meet age, citizenship, education, and physical fitness standards.",
            "How old do I have to be to join?": "Typically between 17 and 34 years old, depending on the branch.",
            "Do I need a high school diploma?": "Yes, a high school diploma or equivalent (GED) is usually required.",
            "Can I join if I have a criminal record?": "Some offenses may disqualify you, but waivers are available for certain cases.",
            "How long is basic training?": "Basic training usually lasts between 8 to 12 weeks depending on the branch.",
            "Do I have to pass a fitness test?": "Yes, you must pass a physical fitness assessment before and during training.",
            "What jobs are available?": "There are hundreds of roles available, ranging from combat to logistics, intelligence, medical, and technical fields.",
            "Is prior military experience required?": "No, prior experience is not required for enlistment.",
            "What benefits will I receive?": "Benefits typically include salary, healthcare, education assistance, and retirement plans.",
            "How do I start the enlistment process?": "You should contact a recruiter, schedule an interview, and prepare for testing and physical exams."
        }
        self.required_documents = []

    def answer_question(self, question):
        for key, answer in self.faq.items():
            if any(word in key.lower() for word in question.lower().split()):
                return answer
        return "I'm sorry, I don't have an answer for that. Please contact a recruiter for more details."

    def attach_document(self, document_name):
        self.required_documents.append(document_name)
        return f"Document '{document_name}' has been successfully attached."

    def list_documents(self):
        if not self.required_documents:
            return "No documents attached yet."
        return "Attached Documents: " + ", ".join(self.required_documents)

agent = MilitaryFAQAgent()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ErasmusARMY Recruitment FAQ</title>
    <style>
        
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; 
         background-color : "4b5320"}
        .logo { margin-bottom: 20px; }
        form { margin: 20px auto; width: 300px; }
    </style>
</head>
<body>
    <div class="logo">
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/50/Army_star_logo.png" alt="ErasmusARMY Logo" width="100">
    </div>
    <h1>ErasmusARMY Recruitment FAQ Assistant</h1>
    <form action="/ask" method="post">
        <label for="question">Ask a Question:</label><br>
        <input type="text" id="question" name="question"><br><br>
        <input type="submit" value="Ask">
    </form>

    <form action="/attach" method="post">
        <label for="document_name">Attach Required Document:</label><br>
        <input type="text" id="document_name" name="document_name"><br><br>
        <input type="submit" value="Attach">
    </form>

    <form action="/documents" method="get">
        <input type="submit" value="View Attached Documents">
    </form>

    {% if answer %}
        <h3>Answer:</h3>
        <p>{{ answer }}</p>
    {% endif %}

    {% if message %}
        <h3>Message:</h3>
        <p>{{ message }}</p>
    {% endif %}

    {% if documents %}
        <h3>Attached Documents:</h3>
        <p>{{ documents }}</p>
    {% endif %}

    <p><a href="/">Back to ErasmusARMY Home</a></p>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask_question():
    if request.is_json:
        question = request.get_json().get('question', '')
    else:
        question = request.form.get('question', '')
    answer = agent.answer_question(question)
    return render_template_string(HTML_TEMPLATE, answer=answer)

@app.route('/attach', methods=['POST'])
def attach_document():
    if request.is_json:
        document_name = request.get_json().get('document_name', '')
    else:
        document_name = request.form.get('document_name', '')
    message = agent.attach_document(document_name)
    return render_template_string(HTML_TEMPLATE, message=message)

@app.route('/documents', methods=['GET'])
def list_documents():
    documents = agent.list_documents()
    return render_template_string(HTML_TEMPLATE, documents=documents)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
