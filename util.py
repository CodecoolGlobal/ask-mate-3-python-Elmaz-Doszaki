from data_manager import *
import datetime
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


def sort_data(data, order_by, order_direction):
    if order_by == 'title':
        order_by = TITLE
    elif order_by == 'submission_time':
        order_by = TIME
    elif order_by == 'message':
        order_by = MESSAGE
    elif order_by == 'number_of_views':
        order_by = VIEW
    elif order_by == 'number_of_votes':
        order_by = VOTE
    if order_direction == 'asc':
        order_direction = False
    else:
        order_direction = True
    data = sorted(
        data, key=lambda data: data[order_by], reverse=order_direction)
    return data


def time_stamp_decode(data):
    for row in data:
        row[1] = str(datetime.datetime.fromtimestamp(float(row[1])).strftime('%Y-%m-%d %H:%M:%S'))
    return data


def get_new_id(data):
    try:
        new_id = int(data[-1][0]) + 1
    except:
        new_id = 0
    return new_id


def question_vote(data, question_id, vote):
    for row in data:
        if row[ID] == question_id:
            if vote == 'down':
                row[VOTE] = str(int(row[VOTE]) - 1)
            else:
                row[VOTE] = str(int(row[VOTE]) + 1)


def answer_vote(answer_id, data, vote):
    for row in data:
        if row[ID] == answer_id:
            if vote == 'down':
                row[ANSWER_VOTE] = str(int(row[ANSWER_VOTE]) - 1)
            else:
                row[ANSWER_VOTE] = str(int(row[ANSWER_VOTE]) + 1)


def get_answers_for_question(answer_list, question_id):
    current_answers = []
    for row in answer_list:
        if row[QUESTION_ID_IN_ANSWERS] == question_id:
            answers = [row[ID], row[TIME], row[ANSWER_VOTE], row[ANSWER_MESSAGE], row[IMG]]
            current_answers.append(answers)
    return current_answers
