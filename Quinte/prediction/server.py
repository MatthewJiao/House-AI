from flask import Flask, render_template, request
import tasks
import app as prediction_app

app = Flask(__name__, template_folder = "sepsis_front_end")

@app.route('/')
def index():
  return render_template('index.ejs')


@app.route('/', methods=['POST'])
def my_form_post():
    text = ""
    text = request.form['values']
    if text == "":
        result = "Please enter some values"
        return render_template('index.ejs', result=result)
    else:
      result = prediction_app.single_work(input=text, frontend=True)
      return render_template('index.ejs', result=result)

  

if __name__ == '__main__':
  app.run(debug=True)