from flask import Flask, request, jsonify
from Spellchecker import SpellChecker
app = Flask(__name__)

sc = SpellChecker('./wordList.txt')

@app.route('/')
def index():
    return {
        "status": "Healthy and dat"
    }

@app.route('/word', methods=['GET'])
def word():
    if(request.method == 'GET'):
        result = []
        
        if(request.json['words']):
            for word in request.json['words']:
                for uncutWord in sc.query(word):
                    result.append(uncutWord[0].strip())
            
        return jsonify(result)
        
        
if __name__ == '__main__':
    app.run(debug=True)