from psycopg2.sql import NULL
import data_manager2
from flask import Flask, render_template, request, redirect, url_for
from data_manager import *
import data_manager2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/'


@app.route("/")
def hello():
    return render_template('index.html')


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
                           question_id=question_id,
                           answer_comments=data_manager2.get_comment(question_id))


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


@app.route('/question/<question_id>/new-answer', methods=['POST'])
def display_answer(question_id):
    return render_template('answer_form.html', question_id=question_id)

@app.route('/question/new-answer', methods=['POST'])
def add_new_answer():
    question_id = request.form['question_id']
    new_answer = {'vote_number': 0,
                  'question_id': question_id,
                  'message': request.form['answer_message'],
                  'image': None}
    data_manager2.add_new_data_to_table(new_answer, 'answer')
    return redirect(url_for("display_question", question_id=question_id))


@app.route('/question/<q_id>/delete', methods=['POST'])
def delete_question(q_id):
    data_manager2.delete_question(q_id)
    return redirect('/list')


@app.route('/answer/<a_id>/delete', methods=['POST'])
def delete_answer(a_id):
    data_manager2.delete_an_img_from_answer(int(a_id))
    data_manager2.delete_an_answer(int(a_id))
    return redirect("/questions/" + request.form['question_id'])

@app.route('/delete_comment/<q_id>/<c_id>')
def delete_comment(q_id, c_id):
    data_manager2.delete_a_comment(c_id)
    return redirect('/questions/' + q_id)

@app.route('/edit_comment/<q_id>/<c_id>', methods=['GET', 'POST'])
def edit_comment(q_id, c_id):
    if request.method == 'GET':
        comment_to_edit = data_manager2.get_comment(c_id)
        return render_template('edit_comment.html', comment=comment_to_edit)
    else:
        sub_time = data_manager2.get_submission_time_for_comment()
        edited_counter = data_manager2.get_edited_counter_for_comment(c_id)
        data_manager2.edit_comment(c_id, request.form['message'], sub_time, edited_counter)
        return redirect('/questions/' + q_id)


@app.route('/question/<q_id>/edit', methods=['POST', 'GET'])
def route_edit(q_id):
    if request.method == 'GET':
        question_to_edit = data_manager2.route_edit_question(q_id)
        message = question_to_edit["message"]
        title = question_to_edit["title"]
        return render_template('edit-question.html', title=title, message=message, q_id=q_id)
    else:
        title = request.form['title']
        message = request.form['message']
        data_manager2.edit_question(q_id, title, message)
        return redirect('/questions/' + q_id)


@app.route('/question/<q_id>/vote-up', methods=['POST'])
def vote_up_question(q_id):
    vote_number = data_manager2.get_question_vote_number(q_id)
    modify_vote_number = util.vote_up_or_down(vote_number, 'up')
    data_manager2.update_question_vote_number(q_id, modify_vote_number)
    return redirect('/list')


@app.route('/question/<q_id>/vote-down', methods=['POST'])
def vote_down_question(q_id):
    vote_number = data_manager2.get_question_vote_number(q_id)
    modify_vote_number = util.vote_up_or_down(vote_number, 'down')
    data_manager2.update_question_vote_number(q_id, modify_vote_number)
    return redirect('/list')


@app.route('/answer/<answer_id>/vote-up', methods=['POST'])
def vote_up_answer(answer_id):
    question_id = request.form['question_id']
    vote_number = data_manager2.get_answer_vote_number(question_id, answer_id)
    modify_vote_number = util.vote_up_or_down(vote_number, 'up')
    data_manager2.update_answer_vote_number(question_id, answer_id, modify_vote_number)
    return redirect('/questions/' + request.form['question_id'])


@app.route('/answer/<answer_id>/vote-down', methods=['POST'])
def vote_down_answer(answer_id):
    question_id = request.form['question_id']
    vote_number = data_manager2.get_answer_vote_number(question_id, answer_id)
    modify_vote_number = util.vote_up_or_down(vote_number, 'down')
    data_manager2.update_answer_vote_number(question_id, answer_id, modify_vote_number)
    return redirect('/questions/' + request.form['question_id'])


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'GET':
        return render_template('add-comment.html', question_id=question_id,
                               current_question=data_manager2.display_question(question_id))
    if request.method == 'POST':
        data_manager2.add_new_data_to_table(
            data={'question_id': question_id, 'answer_id': None, 'message': request.form['message'],
                  'edited_count': None},
            table_name='comment')
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/answer/<answer_id>/edit', methods=['POST', 'GET'])
def route_edit_answer(answer_id):
    if request.method == 'GET':
        q_id = request.args.get('question_id')
        answer_to_edit = data_manager2.route_edit_answer(answer_id, q_id)
        message = answer_to_edit["message"]
        return render_template('edit-answer.html', message=message, q_id=q_id, answer_id=answer_id)
    else:
        q_id = request.form['question_id']
        message = request.form['message']
        data_manager2.edit_answer(answer_id, q_id, message)
        return redirect('/questions/' + q_id)


if __name__ == "__main__":
    app.run(debug=True)
