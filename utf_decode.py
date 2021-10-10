import encodings
string_ex = '\u092a\u094d\u0930\u0915\u093e\u0930'

print((bytes(string_ex, 'utf-8')).decode('utf8'))