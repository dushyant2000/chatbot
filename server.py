from flask import Flask, render_template, request, redirect, jsonify
import sys

app = Flask(__name__)
 
# @app.route('/chatbot/<string:question>/<string:background>/<string:history>', methods = ['GET'])
@app.route('/chatbot/<string:question>', methods = ['GET'])
def get_answer(question):
    try:
        print(question, file=sys.stdout)
        import sample
        response = jsonify(sample.get_answer(question))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print(e, file=sys.stdout)
        return (str(e))
 
# Regular Server
if __name__ == "__main__":
    app.run(debug=True)
 
# Smooth server
# def create_app():
   # return app
