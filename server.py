from flask import Flask, render_template
from data_handler import *

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')



@app.route("/list")
def display_questions_list():
    list_of_questions = open_question_file()
    list_of_questions = data_sorting(list_of_questions, True)
    return render_template('questions_list.html', table_headers=TABLE_HEADERS, list_of_questions=list_of_questions)


if __name__ == "__main__":
    app.run()
