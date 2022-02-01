import data_manager2
from flask import Flask, render_template, request, redirect
from data_manager import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/'


@app.route("/")
def hello():
    return render_template('index.html', list_of_best_memes=best_memes())


@app.route("/list")
def display_questions_list():
    args = request.args
    order_by = args.get('order_by', default='submission_time', type=str)
    order_direction = args.get('order_direction', default='desc')
    questions = data_manager2.list_questions(order_by, order_direction)
    return render_template('questions_list.html',
                           table_headers=TABLE_HEADERS,
                           list_of_questions=questions,
                           order_by=order_by,
                           order_direction=order_direction)


@app.route('/questions/<question_id>')
def display_question(question_id):
    data_manager2.increase_view_number(question_id)
    return render_template('question.html',
                           current_question=data_manager2.display_question(question_id),
                           answer_header=ANSWER_HEADERS,
                           current_answers=data_manager2.get_answers_for_question(question_id),
                           question_id=question_id)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    else:
        question_id = str(data_manager2.new_questionid())
        file1 = request.files['file1']
        if request.files['file1'].filename == "":
            path = ""
        else:
            path = data_manager2.UPLOAD_FOLDER + "Q" + question_id + file1.filename
        data = {'title': request.form['title'], 'message': request.form['question'], 'image': path}
        data_manager2.add_new_data_to_table(data, 'question')
        if path != "":
            data_manager2.save_question_picture(file1, path)

        return redirect('/questions/'+question_id)


@app.route('/question/<q_id>/new-answer', methods=['POST'])
def display_answer(q_id):
    question_id = q_id
    return render_template('answer_form.html', question_id=question_id)


@app.route('/question/new-answer', methods=['POST'])
def add_new_answer():
    data = read_file(ANSWERS_FILE)
    max_id = 0
    if len(data) > 0:
        max_id = max(int(i[0]) for i in data)
    max_id = str(max_id+1)
    if request.files['answerfile'].filename == "":
        path = "0"
    else:
        answerfile = request.files['answerfile']
        file_name = answerfile.filename
        path = UPLOAD_FOLDER + "A" + max_id + file_name
        upload_folder = app.config['UPLOAD_FOLDER']
        data_manager2.save_answer_picture(answerfile, file_name, max_id, upload_folder)
    append_new_answer(max_id, path)
    return redirect("/questions/" + request.form['question_id'])


def append_new_answer(max_id, path):
    data = [max_id, get_time_stamp(), '0', request.form['question_id'], request.form['answer_message'], path]
    append_file(data, ANSWERS_FILE)


@app.route('/question/<q_id>/delete', methods=['POST'])
def delete_question(q_id):
    data_manager2.delete_question(q_id)
    return redirect('/list')


@app.route('/answer/<a_id>/delete', methods=['POST'])
def delete_answer(a_id):
    data_manager2.delete_an_img_from_answer(a_id)
    data_manager2.delete_an_answer(a_id)
    return redirect("/questions/" + request.form['question_id'])


@app.route('/question/<q_id>/edit', methods=['POST', 'GET'])
def route_edit(q_id):
    if request.method == 'GET':
        message, title = data_for_question_edit(q_id)
        return render_template('edit-question.html', title=title, message=message, q_id=q_id)
    else:
        title = request.form['title']
        message = request.form['message']
        edit_question(message, q_id, title)
        return redirect('/questions/' + q_id)


@app.route('/question/<q_id>/vote-up', methods=['POST'])
def vote_up_question(q_id):
    vote_question(q_id, 'up')
    return redirect('/list')


@app.route('/question/<q_id>/vote-down', methods=['POST'])
def vote_down_question(q_id):
    vote_question(q_id, 'down')
    return redirect('/list')


@app.route('/answer/<answer_id>/vote-up', methods=['POST'])
def vote_up_answer(answer_id):
    vote_answer(answer_id, 'up')
    return redirect('/questions/' + request.form['question_id'])


@app.route('/answer/<answer_id>/vote-down', methods=['POST'])
def vote_down_answer(answer_id):
    vote_answer(answer_id, 'down')
    return redirect('/questions/' + request.form['question_id'])


if __name__ == "__main__":
    app.run(debug=True)
