text = '<!-- Modal -->'



def print_comment_end(text: str):
    print(text[len(text) - 3:len(text)])

def print_comment_start(text: str):
    print(text[0:4])


print_comment_start(text)
print_comment_end(text)
print(len(text))