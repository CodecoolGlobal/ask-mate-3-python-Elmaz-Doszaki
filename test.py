def write_file(data, filepath="test.csv"):
    # data = base64_encoder(data)
    # data = time_stamp_encode(data)
    # data = time_stamp_decode(data)
    with open(filepath, 'w') as workfile:
        for item in data:
            item = item.replace("\r\n", "Ł@&")
            row = ";".join(item)
            workfile.write(row + '\n')


def append_file(data, filepath="test.csv"):
    # data = base64_encoder(data)
    # data = time_stamp_encode([data])
    # data = time_stamp_decode(data)
    with open(filepath, 'a', newline='\n') as workfile:
        row = ";".join(data)
        workfile.write(row + '\n')


def read_file(filepath):
    with open(filepath) as workfile:
        row = workfile.readlines()
        data = [item.replace('\n', '').replace(
            "Ł@&", "\r\n").split(";") for item in row]
        # data = time_stamp_decode(data)
        # data = time_stamp_encode(data)
        # data = base64_decoder_ans(data)
        return data


write_file(['0', 'ddd, 'kkk'])
read_file("test.csv")
