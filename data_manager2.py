from typing import Dict, Optional

import connection2
import os
from datetime import datetime

UPLOAD_FOLDER = 'static/images/'


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


@connection2.connection_handler
def route_edit_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})

    question_to_edit = cursor.fetchall()
    return question_to_edit[0]


@connection2.connection_handler
def edit_question(cursor, question_id, edited_title, edited_message):
    cursor.execute("""
                    UPDATE question
                    SET title = %(edited_title)s, message = %(edited_message)s
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id,
                    'edited_title': edited_title,
                    'edited_message': edited_message})


@connection2.connection_handler
def route_edit_answer(cursor, answer_id, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(answer_id)s AND question_id = %(question_id)s;
                    """,
                   {'answer_id': answer_id,
                    'question_id': question_id})
    answer_to_edit = cursor.fetchall()
    return answer_to_edit[0]


@connection2.connection_handler
def edit_answer(cursor, answer_id, question_id, edited_message):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(edited_message)s
                    WHERE id = %(answer_id)s AND question_id = %(question_id)s;
                    """,
                   {'answer_id': answer_id,
                    'question_id': question_id,
                    'edited_message': edited_message})

@connection2.connection_handler
def save_picture(cursor, file1, path, i_d):
    file1.save(os.path.join(path))
    table = path.split('/')[-1][0]
    if table == 'A':
        cursor.execute("""
                            UPDATE answer
                            SET image = %(p)s
                            WHERE id = %(i_d)s;
                            """,
                       {'p': path,
                        'i_d': i_d})
    else:
        cursor.execute("""
                                    UPDATE question
                                    SET image = %(p)s
                                    WHERE id = %(i_d)s;
                                    """,
                       {'p': path,
                        'i_d': i_d})


def delete_question(question_id):
    delete_img_from_all_answer(question_id)
    delete_img_from_question(question_id)
    delete_all_answer_from_db(question_id)
    delete_question_from_db(question_id)


@connection2.connection_handler
def delete_question_from_db(cursor, question_id):
    cursor.execute("""
                DELETE  FROM question_tag
                WHERE question_id = %(question_id)s;
                DELETE  FROM comment
                WHERE question_id = %(question_id)s;
                DELETE  FROM question
                WHERE id = %(question_id)s;
                """,
                   {'question_id': question_id})


@connection2.connection_handler
def delete_all_answer_from_db(cursor, q_id):
    cursor.execute("""
                DELETE FROM comment
                WHERE answer_id = %(question_id)s;
                DELETE FROM answer
                WHERE question_id = %(question_id)s;
                """,
                   {'question_id': q_id})


@connection2.connection_handler
def delete_an_answer(cursor, id):
    cursor.execute("""
                DELETE  FROM comment
                WHERE answer_id = %(id)s;
                DELETE  FROM answer
                WHERE id = %(id)s;
                """,
                   {'id': id})


@connection2.connection_handler
def delete_img_from_question(cursor, question_id):
    cursor.execute("""
                SELECT image FROM question
                WHERE id = %(question_id)s AND image IS NOT NULL;
                """,
                   {'question_id': question_id})
    file_path = cursor.fetchall()
    file_path = file_path[0]['image']
    if os.path.exists(file_path):
        os.remove(file_path)


@connection2.connection_handler
def delete_img_from_all_answer(cursor, q_id):
    cursor.execute("""
                SELECT image FROM answer
                WHERE question_id = %(q_id)s AND image IS NOT NULL;
                """,
                   {'q_id': q_id})
    target_list = cursor.fetchall()
    for file_path in target_list:
        if os.path.exists(file_path['image']):
            os.remove(file_path)


@connection2.connection_handler
def delete_an_img_from_answer(cursor, a_id):
    cursor.execute("""
                SELECT image FROM answer
                WHERE id = %(aid)s AND image IS NOT NULL;
                """,
                   {'aid': a_id})
    file_path = cursor.fetchall()
    if file_path != [] and os.path.exists(file_path[0]['image']):
        os.remove(file_path)


@connection2.connection_handler
def delete_a_comment(cursor, c_id):
    cursor.execute("""
                    DELETE  FROM comment
                    WHERE id = %(cid)s;
                    """,
                   {'cid': c_id})


@connection2.connection_handler
def get_edit_comment(cursor, comment_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE id = %(c_id)s;
                    """,
                   {'c_id': comment_id})
    comment_to_edit = cursor.fetchall()
    return comment_to_edit[0]


@connection2.connection_handler
def edit_comment(cursor, comment_id, edited_message, sub_time, edited_counter):
    cursor.execute("""
                    UPDATE comment
                    SET message = %(edited_message)s, submission_time = %(s_time)s, edited_count = %(edit_counter)s
                    WHERE id = %(c_id)s;
                    """,
                   {'c_id': comment_id,
                    'edited_message': edited_message,
                    's_time': sub_time,
                    'edit_counter': edited_counter})


def get_submission_time_for_comment():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


@connection2.connection_handler
def get_edited_counter_for_comment(cursor, comment_id):
    cursor.execute("""
                        SELECT edited_count FROM comment
                        WHERE id = %(c_id)s;
                        """,
                   {'c_id': comment_id})
    edited_count = cursor.fetchall()
    edited_count = 1 if edited_count[0]['edited_count'] == None else edited_count[0]['edited_count'] + 1
    return edited_count


@connection2.connection_handler
def add_new_data_to_table(cursor, data: Dict[str, str], table_name: str) -> None:
    """
    table_name:  = 'question' or 'answer' or 'comment'
    """

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


@connection2.connection_handler
def get_comment(cursor, key_id: str):
    query = """
            SELECT * FROM comment
            WHERE question_id = %(key_id)s
            """
    cursor.execute(query, {'key_id': int(key_id)})
    comments = cursor.fetchall()
    return comments


def save_question_picture(file1, path):
    file1.save(os.path.join(path))


def save_answer_picture(answerfile, file_name, max_id, upload_folder):
    answerfile.save(os.path.join(upload_folder, "A" + max_id + file_name))


@connection2.connection_handler
def get_new_id(cursor, table):
    if table == 'q':
        cursor.execute("""
                SELECT id FROM question
                ORDER BY id DESC
                LIMIT 1;
                """)
    else:
        cursor.execute("""
                        SELECT id FROM answer
                        ORDER BY id DESC
                        LIMIT 1;
                        """)
    answers = cursor.fetchall()[0]["id"]
    return answers


@connection2.connection_handler
def get_question_id_from_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(answer_id)s""",
                   {'answer_id': answer_id})
    return cursor.fetchall()[0]


@connection2.connection_handler
def get_comments_from_answers(cursor, current_answers):
    if len(current_answers) > 0:
        answer_ids = tuple(answer['id'] for answer in current_answers)
        cursor.execute("""
                        SELECT * FROM comment
                        WHERE answer_id IN %(answer_ids)s""",
                       {'answer_ids': answer_ids})
        return cursor.fetchall()
    else:
        return None


@connection2.connection_handler
def get_searched_question(cursor, search):
    cursor.execute("""
                SELECT question.* FROM question LEFT JOIN answer
                ON question.id = answer.question_id
                WHERE question.message LIKE %(search)s
                OR question.title LIKE %(search)s
                OR answer.message LIKE %(search)s
GROUP BY question.id;
    """,
                   {'search': '%' + search + '%'})
    questions = cursor.fetchall()
    return questions


@connection2.connection_handler
def get_tags(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM tag
                    JOIN question_tag
                    ON tag.id = question_tag.tag_id
                    WHERE question_id = %(question_id)s""",
                   {'question_id': question_id})
    return cursor.fetchall()


@connection2.connection_handler
def get_all_tags(cursor):
    cursor.execute("""SELECT * FROM tag""")
    return cursor.fetchall()


@connection2.connection_handler
def get_tag_id(cursor, tag: str) -> int:
    cursor.execute("""SELECT id FROM tag WHERE name LIKE %(tag)s""", {'tag': tag})
    return cursor.fetchall()[0]['id']


@connection2.connection_handler
def add_new_tag(cursor, new_tag: str, question_id) -> None:
    tags = [tag['name'] for tag in get_all_tags()]
    if new_tag not in tags:
        cursor.execute("""
                        INSERT INTO tag (name)
                        VALUES (%(new_tag)s)""",
                       {'new_tag': new_tag})
    tag_id = get_tag_id(new_tag)
    cursor.execute("""
                    INSERT INTO question_tag (question_id, tag_id)
                    VALUES (%(question_id)s, %(tag_id)s)
                    """,
                   {'question_id': question_id, 'tag_id': tag_id})


@connection2.connection_handler
def list_of_best_memes(cursor):
    b_list = []
    cursor.execute("""SELECT vote_number, image, id as question_id FROM question
                    WHERE image IS NOT NULL
                    ORDER BY vote_number DESC
                        LIMIT 5;
    """)
    a_list = cursor.fetchall()
    for i in range(len(a_list)):
        b_list.append((a_list[i]['image'], a_list[i]['question_id'], a_list[i]['vote_number']))
    cursor.execute("""SELECT vote_number, image, question_id FROM answer
                        WHERE image IS NOT NULL
                        ORDER BY vote_number DESC
                            LIMIT 5;
        """)
    a_list = cursor.fetchall()
    for i in range(len(a_list)):
        b_list.append((a_list[i]['image'], a_list[i]['question_id'], a_list[i]['vote_number']))
    return sorted(b_list, key=lambda x: x[2], reverse=True)[:5]



@connection2.connection_handler
def tag_delete_from_question(cursor, question_id, tag_id):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id = %(question_id)s
                    AND tag_id = %(tag_id)s
                    """,
                   {'question_id': question_id, 'tag_id': tag_id})

