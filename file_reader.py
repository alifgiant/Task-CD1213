def get_target(file_path):
    file_text = open(file_path)
    target = list()
    for line in file_text:
        line = line.split('\n')
        target.append(line[0].split(' ')[-1])
    return target
