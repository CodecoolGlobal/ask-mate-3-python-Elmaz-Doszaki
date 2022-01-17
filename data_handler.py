TABLE_HEADERS = [
    '#ID',
    'Submission time',
    'View number',
    'Vote number',
    'Title',
    'Message',
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

ANSWERS_FILE = "sample_data/answer.csv"
ANSWER_VOTE = 2
QUESTION_ID_IN_ANSWERS = 3
ANSWER_MESSAGE = 4
IMG = 5


def open_question_file():
    '''
        Opens the question.csv file,
        reads it content as rows.
        Minden sor egy lista lesz
    '''
    filepath = QUESTIONS_FILE
    with open(filepath) as workfile:
        row = workfile.readlines()
        data = [item.replace('\n', '').split(',') for item in row]
        # data = time_stamp_decode(data)
        # data = base64_decoder(data)
        return data


def data_sorting(data, rev_opt):
    '''
        Sorts the questions by time in descanding order
        Order can be reveresed with rev_opt.
    '''
    data = sorted(data, key=lambda data: data[1], reverse=rev_opt)
    return data


def write_question_to_file(data):
    filepath = QUESTIONS_FILE
    # data = base64_encoder(data)
    #     # data = time_stamp_encode(data)
    with open(filepath, 'w') as workfile:
        for item in data:
            row = ','.join(item)
            workfile.write(row + '\n')


def read_answer_file():
    filepath = ANSWERS_FILE
    with open(filepath) as workfile:
        row = workfile.readlines()
        data = [item.replace('\n', '').split(',') for item in row]
        # data = time_stamp_decode(data)
        # data = base64_decoder_ans(data)
        return data

