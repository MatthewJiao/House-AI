from flask import Flask, render_template, request
import tasks
import app as prediction_app

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/submit_sepsis', methods=['POST'])
def my_form_post():
    text = request.form['text']
    result = prediction_app.single_work(input=text, frontend=True)
    return result

  

if __name__ == '__main__':
  app.run(debug=True)