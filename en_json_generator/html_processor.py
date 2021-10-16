f = open('en_json_generator/file.html', 'r')
html = f.read()

def get_camel_case(string: str):
    vector = string.split(' ')
    result = ''
    first_time = True
    for element in vector:
        if(first_time):
            result += element.lower()
            first_time = False
        else:
            result += element.capitalize()
    return result

def get_plain_text(html: str):
    plain_text = ''
    chevron_ongoing = False
    string_ongoing = False
    start_index = 0
    stop_index = 0
    plain_text_points = []
    index = 0
    for char in html:
        if(char == '<' and not string_ongoing):
            chevron_ongoing = True
            stop_index = index
            plain_text_points.append({
                'start_index': start_index,
                'stop_index': stop_index,
            })
        if(char == '>' and not string_ongoing):
            chevron_ongoing = False
            start_index = index + 1
        if(char == '\"' and chevron_ongoing):
            string_ongoing = not string_ongoing
        if(not chevron_ongoing):
            plain_text += char
        index += 1
    return plain_text_points

def get_l_spaces(text: str):
    new_string = ''
    for char in text:
        if(char == ' ' or char == '\n'):
            new_string += char
        else:
            return new_string
    return new_string

def get_r_spaces(text: str):
    new_string = ''
    for char in text[::1]:
        if(char == ' ' or char == '\n'):
            new_string += char
        else:
            return new_string
    return new_string

# plain_output = open('en_json_generator/plain.html', 'w')
# html_output = open('en_json_generator/html.html', 'w')
# plain_output.write(get_plain_text(html))

points = get_plain_text(html)
new_html = ''
for i in range(1, len(points)):
    new_html += html[points[i - 1]['stop_index']:points[i]['start_index']]
    interpolation_text = (html[points[i]['start_index']:points[i]['stop_index']])
    # l_spaces = get_l_spaces(interpolation_text)
    # r_spaces = get_r_spaces(interpolation_text)
    # if(interpolation_text.strip() == ''):
    #     new_html += (interpolation_text)
    # else:
    #     new_html += l_spaces + '{{ \'' + get_camel_case(interpolation_text).strip() + '\' | translate }}' + r_spaces
    new_html += (interpolation_text)
new_html += html[points[len(points) - 1]['stop_index']:]
out = open('en_json_generator/new-html.html', 'w')
out.write(new_html)