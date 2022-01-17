TABLE_HEADERS = [
    '#ID',
    'Submission time',
    'View number',
    'Vote number',
    'Title',
    'Message',
    'View',
    'Delete',
    'Vote Up',
    'Vote Down'
]
QUESTIONS_FILE = "sample_data/question.csv"
ANSWERS_FILE = "sample_data/answer.csv"


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
