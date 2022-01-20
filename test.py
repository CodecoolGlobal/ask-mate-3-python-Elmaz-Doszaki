def write_file(data, filepath="test.csv"):
    with open(filepath, 'w') as workfile:
        for item in data:
            item = item.replace("\r\n", "Ł@&")
            row = ";".join(item)
            workfile.write(row + '\n')



def read_file(filepath):
    with open(filepath) as workfile:
        row = workfile.readlines()
        data = [item.replace('\n', '').replace("Ł@&", "\r\n").split(";") for item in row]
    return data

list1 = ['0; rtee']
write_file(list1)
print(read_file("test.csv"))
