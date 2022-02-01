from typing import Dict, Optional

import connection2


@connection2.connection_handler
def list_questions(cursor, order_by, order):
    cursor.execute(f"""
                    SELECT * FROM question 
                    ORDER BY {order_by} {order};
                    """)
    questions = cursor.fetchall()
    return questions


@connection2.connection_handler
def display_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    question = cursor.fetchall()
    return question


@connection2.connection_handler
def get_answers_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s
                    ORDER BY vote_number DESC;
                    """,
                   {'question_id': question_id})
    answers = cursor.fetchall()
    return answers


@connection2.connection_handler
def increase_view_number(cursor, question_id):
    cursor.execute("""
                   UPDATE question
                   SET view_number = view_number + 1
                   WHERE id = %(question_id)s;
                   """,
                   {'question_id': question_id})


@connection2.connection_handler
def add_new_data_to_table(cursor, data: Dict[str, str], table_name: str) -> None:
    """
    table_name:  = 'question' or 'answer' or 'comment'
    """
    from datetime import datetime
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")

    if table_name == 'question':
        cursor.execute("""
                        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                        VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);
                        """,
                       {'submission_time': dt,
                        'view_number': 0,
                        'vote_number': 0,
                        'title': data['title'],
                        'message': data['message'],
                        'image': data['image']})
    elif table_name == 'answer':
        cursor.execute("""
                        INSERT INTO answer(submission_time, vote_number, question_id, message, image)
                        VALUES(%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s);
                        """,
                       {'submission_time': dt,
                        'vote_number': 0,
                        'question_id': data['question_id'],
                        'message': data['message'],
                        'image': data['image']})
    elif table_name == 'comment':
        cursor.execute("""
                        INSERT INTO comment(question_id, answer_id, message, submission_time, edited_count)
                        VALUES(%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s);
                        """,
                       {'question_id': data['question_id'],
                        'answer_id': data['answer_id'],
                        'message': data['message'],
                        'submission_time': dt,
                        'edited_count': data['edited_count']})
