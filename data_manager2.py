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
def get_question_vote_number(cursor, question_id):
    cursor.execute("""
                    SELECT vote_number FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    vote_number = cursor.fetchall()
    return vote_number[0]


@connection2.connection_handler
def update_question_vote_number(cursor, question_id, vote_number):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = %(vote_number)s
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id,
                    'vote_number': vote_number})


@connection2.connection_handler
def get_answer_vote_number(cursor, question_id, answer_id):
    cursor.execute("""
                    SELECT vote_number FROM answer
                    WHERE question_id = %(question_id)s AND id = %(answer_id)s;
                    """,
                   {'question_id': question_id,
                    'answer_id': answer_id})
    vote_number = cursor.fetchall()
    return vote_number[0]


@connection2.connection_handler
def update_answer_vote_number(cursor, question_id, answer_id, vote_number):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = %(vote_number)s
                    WHERE question_id = %(question_id)s AND id = %(answer_id)s;
                    """,
                   {'question_id': question_id,
                    'answer_id': answer_id,
                    'vote_number': vote_number})