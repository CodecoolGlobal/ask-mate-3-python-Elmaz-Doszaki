import time
import datetime
import os

UPLOAD_FOLDER = '/static/'

TABLE_HEADERS = [
    '#ID',
    'Submission time',
    'View number',
    'Vote number',
    'Title',
    '         Message       ',
    'Photo',
    'Delete',
    'Vote Up',
    'Vote Down'
]
ANSWER_HEADERS = [
    '#ID',
    'Submission time',
    'Vote number',
    '___________Message___________',
    '___________Photo___________',
    'Delete',
    'Vote Up',
    'Vote Down'
]
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
SEPARATOR = ';'

NEW_LINE_SEPARATOR = "a6z?k@LLa&"


def data_sorting(data, order_by, order_direction):
    """
        Sorts the questions by time in descanding order
        Order can be reveresed with rev_opt.
    """
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


def write_file(data, filepath):
    with open(filepath, 'w') as workfile:
        for item in range(len(data)):
            for i in range(len(data[item])):
                data[item][i] = data[item][i].replace("\r\n", NEW_LINE_SEPARATOR)
            row = SEPARATOR.join(data[item])
            workfile.write(row + '\n')

def append_file(data, filepath):
    with open(filepath, 'a') as workfile:
        for item in range(len(data)):
            data[item] = data[item].replace("\r\n", NEW_LINE_SEPARATOR)
        row = SEPARATOR.join(data)
        workfile.write(row + '\n')


def read_file(filepath):
    with open(filepath, 'r') as workfile:
        row = workfile.readlines()
        data = [item.replace('\n', '') for item in row]
        data = [item.replace(NEW_LINE_SEPARATOR, "\r\n").split(SEPARATOR) for item in data]
        return data


def delete_file(file_path):
    file_path = file_path[1:]
    if os.path.exists(file_path):
        os.remove(file_path)


def time_stamp_decode(data):
    """
        Decodes the UNIX timestamp to readable string format.
    """
    for row in data:
        row[1] = str(datetime.datetime.fromtimestamp(float(row[1])).strftime('%Y-%m-%d %H:%M:%S'))
    return data


def time_stamp_encode(data):
    """
        Encodes the string time format to UNIX timestamp.
    """
    for row in data:
        row[1] = str(int(datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').strftime("%s")))
    return data


def new_id(filepath):
    data = read_file(filepath)
    try:
        new_id = int(data[-1][0]) + 1
    except:
        new_id = 0
    return new_id


def get_time_stamp():
    current_time = str(int(time.time()))
    decoded_time = str(datetime.datetime.fromtimestamp(
        float(current_time)).strftime('%Y-%m-%d %H:%M:%S'))
    return current_time


def vote_question(q_id, vote):
    data = read_file(QUESTIONS_FILE)
    for row in data:
        if row[ID] == q_id:
            if vote == 'down':
                row[VOTE] = str(int(row[VOTE])-1)
            else:
                row[VOTE] = str(int(row[VOTE])+1)
    write_file(data, QUESTIONS_FILE)


def vote_answer(a_id, vote):
    data = read_file(ANSWERS_FILE)
    for row in data:
        if row[ID] == a_id:
            if vote == 'down':
                row[ANSWER_VOTE] = str(int(row[ANSWER_VOTE]) - 1)
            else:
                row[ANSWER_VOTE] = str(int(row[ANSWER_VOTE]) + 1)
    write_file(data, ANSWERS_FILE)


def best_memes():
    pics = []
    pic_list = read_file(ANSWERS_FILE)
    pic_list = sorted(pic_list, key=lambda x: int(x[ANSWER_VOTE]), reverse= True)[:3]
    for i in pic_list:
        if i[IMG] != "0":
            pics.append((i[ANSWER_VOTE], i[IMG]))
    pic_list = read_file(QUESTIONS_FILE)
    pic_list = sorted(pic_list, key=lambda x: int(x[VOTE]), reverse= True)[:3]
    for i in pic_list:
        if i[QUESTION_IMG_PATH] != "0":
            pics.append((i[VOTE], i[QUESTION_IMG_PATH]))
    return sorted(pics, key=lambda x: int(x[0]), reverse= True)[:3]