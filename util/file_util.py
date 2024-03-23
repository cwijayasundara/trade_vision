import os


def save_file(file, directory):
    with open(os.path.join(directory, file), "wb") as f:
        f.write(file.getbuffer())
    return os.path.join(directory, file)


def read_file(file):
    with open(file, "rb") as f:
        return f.read()
