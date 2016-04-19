def get_target(file_path):
    file_text = open(file_path)
    target = list()
    for line in file_text:
        target.append(line.split(' ')[2][:-2])
    return target
