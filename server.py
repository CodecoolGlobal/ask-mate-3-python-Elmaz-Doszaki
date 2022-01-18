from flask import Flask, render_template, request, redirect
from data_handler import *

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/list")
def display_questions_list():
    list_of_questions = read_file(QUESTIONS_FILE)
    list_of_questions = data_sorting(list_of_questions, True)
    return render_template('questions_list.html', table_headers=TABLE_HEADERS, list_of_questions=list_of_questions)


@app.route('/questions/<question_id>')
def display_question(question_id):
    list_of_questions = read_file(QUESTIONS_FILE)
    current_question = []
    for row in list_of_questions:
        if row[ID] == question_id:
            row[VIEW] = str(int(row[VIEW]) + 1)
            current_question.append(row[ID])
            current_question.append(row[TITLE])
            current_question.append(row[MESSAGE])
            write_file(list_of_questions, QUESTIONS_FILE)
    answer_list = read_file(ANSWERS_FILE)
    current_answers = []
    for row in answer_list:
        if row[QUESTION_ID_IN_ANSWERS] == question_id:
            answers = [row[ID], row[ANSWER_MESSAGE]]  # row[img]
            current_answers.append(answers)
    return render_template('question.html',
                           current_question=current_question,
                           current_answers=current_answers,
                           question_id=question_id)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    else:
        id = str(new_id(QUESTIONS_FILE))
        data = [id, get_time_stamp(), "0", "0", request.form['title'], request.form['question']]
        append_file(data, QUESTIONS_FILE)
        return redirect('/questions/'+id)


@app.route('/question/<q_id>/new-answer', methods=['POST'])
def display_answer(q_id=None):
    """
        Displays the answer form page.
    """
    question_id = q_id
    return render_template('answer_form.html', question_id=question_id)


@app.route('/question/new-answer', methods=['POST'])
def add_new_answer():
    """
    Add the new answer to database.
    """
    data = read_file(ANSWERS_FILE)
    max_id = 0
    if len(data) > 0:
        max_id = max(int(i[0]) for i in data)
    current_time = str(int(time.time()))
    decoded_time = str(datetime.datetime.fromtimestamp(float(current_time)).strftime('%Y-%m-%d %H:%M:%S'))
    data = [str(max_id+1), current_time, '0', request.form['question_id'], request.form['answer_message']]

    append_file(data, ANSWERS_FILE)
    return redirect("/questions/" + request.form['question_id'])


@app.route('/question/<q_id>/delete', methods=['POST'])
def delete_question(q_id):
    question_data = read_file(QUESTIONS_FILE)
    for row in question_data:
        if row[ID] == q_id:
            question_data.remove(row)
    write_file(question_data, QUESTIONS_FILE)

    answer_data = read_file(ANSWERS_FILE)
    for row in answer_data:
        if row[QUESTION_ID_IN_ANSWERS] == q_id:
            answer_data.remove(row)
    write_file(answer_data, ANSWERS_FILE)
    return redirect('/list')

@app.route('/answer/<a_id>/delete', methods=['POST'])
def delete_answer(a_id):
    answer_data = read_file(ANSWERS_FILE)
    for row in answer_data:
        if row[ID] == a_id:
            answer_data.remove(row)
    write_file(answer_data, ANSWERS_FILE)
    return redirect("/questions/" + request.form['question_id'])

@app.route('/question/<q_id>/vote-up', methods=['POST'])
def vote_up_question(q_id):
    data = read_file(QUESTIONS_FILE)
    for row in data:
        if row[ID] == q_id:
            row[VOTE] = str(int(row[VOTE])+1)
    write_file(data, QUESTIONS_FILE)
    return redirect('/list')


@app.route('/question/<q_id>/vote-down', methods=['POST'])
def vote_down_question(q_id):
    data = read_file(QUESTIONS_FILE)
    for row in data:
        if row[ID] == q_id:
            row[VOTE] = str(int(row[VOTE])-1)
    write_file(data, QUESTIONS_FILE)
    return redirect('/list')

if __name__ == "__main__":
    app.run(debug=True)
