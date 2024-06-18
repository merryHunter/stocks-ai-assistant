from flask import Flask, request, jsonify
from app.stocks import answer_stock_question 
from flask_cors import CORS
from flask import send_from_directory

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'Hello'


@app.route('/home')
def send_report():
    return send_from_directory('.', 'index.html')
    
@app.route("/ask", methods=["POST"])
def ask():
    try:
        question = request.json["question"]
        answer = answer_stock_question(question)
        return jsonify({"answer":answer})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
