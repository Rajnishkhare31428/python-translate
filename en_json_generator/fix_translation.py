import os

path = 'en_json_generator'

# Returns all html files in a directory recursively
def get_all_html_files(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.html' in file:
                files.append(os.path.join(r, file))
    return files
