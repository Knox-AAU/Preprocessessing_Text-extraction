""" Main file """
from flask import Flask, request, jsonify
from spell_checking.spell_checker import SpellChecker
app = Flask(__name__)

sc = SpellChecker('./wordList.txt')

@app.route('/')
def index():
    """ Status check for api to ensure its running """
    return {
        "status": "Healthy and dat"
    }

@app.route('/word', methods=['GET'])
def word():
    """ returns a array of words """
    result = []

    if request.json['words']:
        for words in request.json['words']:
            for uncut_word in sc.query(words):
                result.append(uncut_word[0].strip())

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
