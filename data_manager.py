from connection import *
import time
import os
import util

UPLOAD_FOLDER = 'images/'
TABLE_HEADERS = ['#ID', 'Submission time', 'View number', 'Vote number', 'Title', '         Message       ', 'Photo', 'Delete', 'Vote Up', 'Vote Down']
ANSWER_HEADERS = ['#ID', 'Submission time', 'Vote number', '___________Message___________', '___________Photo___________', 'Delete', 'Vote Up', 'Vote Down', 'Edit']
QUESTIONS_FILE = "sample_data/question.csv"
ID = 0
TIME = 1
VIEW = 2
VOTE = 3
TITLE = 4
MESSAGE = 5
QUESTION_IMG_PATH = 6
ANSWERS_FILE = "sample_data/answer.csv"
ANSWER_VOTE = 2
QUESTION_ID_IN_ANSWERS = 3
ANSWER_MESSAGE = 4
IMG = 5


def get_questions() -> List[List[str]]:
    return util.time_stamp_decode(read_file(QUESTIONS_FILE))


def get_current_question(question_id):
    list_of_questions = read_file(QUESTIONS_FILE)
    current_question = []
    for row in list_of_questions:
        if row[ID] == question_id:
            row[VIEW] = str(int(row[VIEW]) + 1)
            data = row[ID], row[TIME], row[TITLE], row[MESSAGE], row[QUESTION_IMG_PATH]
            current_question.extend(data)
            write_file(list_of_questions, QUESTIONS_FILE)
    current_question = util.time_stamp_decode([current_question])
    current_question = current_question[0]
    return current_question


def get_current_answers(question_id):
    answer_list = read_file(ANSWERS_FILE)
    current_answers = util.get_answers_for_question(answer_list, question_id)
    if len(current_answers) > 0:
        current_answers = util.time_stamp_decode(current_answers)
    return current_answers


def delete_answer_to_question(question_id):
    answer_data = read_file(ANSWERS_FILE)
    for row in answer_data:
        if row[QUESTION_ID_IN_ANSWERS] == question_id:
            delete_file(row[-1])
            answer_data.remove(row)
    write_file(answer_data, ANSWERS_FILE)


def delete_question_from_file(question_id):
    question_data = read_file(QUESTIONS_FILE)
    for row in question_data:
        if row[ID] == question_id:
            delete_file(row[-1])
            question_data.remove(row)
    write_file(question_data, QUESTIONS_FILE)


def data_for_question_edit(question_id):
    data = read_file(QUESTIONS_FILE)
    for row in data:
        if row[ID] == question_id:
            title = row[TITLE]
            message = row[MESSAGE]
    return message, title


def save_question_picture(file1, file_name, question_id, upload_folder):
    file1.save(os.path.join(upload_folder, "Q" + question_id + file_name))


def save_answer_picture(answerfile, file_name, max_id, upload_folder):
    answerfile.save(os.path.join(upload_folder, "A" + max_id + file_name))


def append_new_question(path, question, question_id, title):
    data = [question_id, get_time_stamp(), "0", "0", title, question, path]
    append_file(data, QUESTIONS_FILE)


def edit_question(message, question_id, title):
    data = read_file(QUESTIONS_FILE)
    for index in range(len(data)):
        if data[index][ID] == question_id:
            data[index] = [question_id, get_time_stamp(), '0', '0', title, message, data[index][QUESTION_IMG_PATH]]
    write_file(data, QUESTIONS_FILE)


def delete_an_answer(answer_id):
    answer_data = read_file(ANSWERS_FILE)
    for row in answer_data:
        if row[ID] == answer_id:
            delete_file(row[-1])
            answer_data.remove(row)
    write_file(answer_data, ANSWERS_FILE)


def data_sorting(data, order_by, order_direction):
    return util.sort_data(data, order_by, order_direction)


def delete_file(file_path):
    file_path = file_path[1:]
    if os.path.exists(file_path):
        os.remove(file_path)


def new_id(filepath):
    return util.get_new_id(read_file(filepath))


def get_time_stamp():
    return str(int(time.time()))


def vote_question(question_id, vote):
    data = read_file(QUESTIONS_FILE)
    util.question_vote(data, question_id, vote)
    write_file(data, QUESTIONS_FILE)


def vote_answer(answer_id, vote):
    data = read_file(ANSWERS_FILE)
    util.answer_vote(answer_id, data, vote)
    write_file(data, ANSWERS_FILE)


# def best_memes():
#     import os
#
#     cwd = os.getcwd()  # Get the current working directory (cwd)
#     files = os.listdir(cwd)  # Get all the files in that directory
#     print("Files in %r: %s" % (cwd, files))
#
#
#     pics = []
#     pic_list = read_file(ANSWERS_FILE)
#     pic_list = sorted(pic_list, key=lambda x: int(x[ANSWER_VOTE]), reverse=True)[:3]
#     for i in pic_list:
#         if i[IMG] != "0":
#             pics.append((i[ANSWER_VOTE], i[IMG]))
#     pic_list = read_file(QUESTIONS_FILE)
#     pic_list = sorted(pic_list, key=lambda x: int(x[VOTE]), reverse=True)[:3]
#     for i in pic_list:
#         if i[QUESTION_IMG_PATH] != "0":
#             pics.append((i[VOTE], i[QUESTION_IMG_PATH]))
#     return sorted(pics, key=lambda x: int(x[0]), reverse=True)[:3]
