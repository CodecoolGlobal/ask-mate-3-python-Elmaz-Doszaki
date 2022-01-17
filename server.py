from flask import Flask, render_template, request
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


@app.route('/questions/<question_id>')
def display_question(question_id):
    list_of_questions = open_question_file()
    current_question = []
    for row in list_of_questions:
        if row[ID] == question_id:
            row[VIEW] = str(int(row[VIEW]) + 1)
            current_question.append(row[ID])
            current_question.append(row[TITLE])
            current_question.append(row[MESSAGE])
            write_question_to_file(list_of_questions)
    answer_list = read_answer_file()
    current_answers = []
    for row in answer_list:
        if row[QUESTION_ID_IN_ANSWERS] == question_id:
            answers = [row[ID], row[ANSWER_MESSAGE], row[IMG]]
            current_answers.append(answers)
    return render_template('question.html',
                           current_question=current_question,
                           current_answers=current_answers,
                           )


if __name__ == "__main__":
    app.run()
