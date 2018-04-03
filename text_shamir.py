"""Contains methods to convert from string to a concatenated ascii integer and back"""

''' Converts text to ascii.
Returns concatendated ascii integers
and a list of the number of digits for each individual ascii integer'''
def text_to_ascii(text):
    ascii_string = ""
    digits_per_c = []
    for c in text:
        ascii_char = str(ord(c))
        ascii_string = ascii_string + ascii_char
        digits_per_c.append(len(ascii_char))
    return int(ascii_string), digits_per_c

''' Converts concatenated ascii integer to text
using a list of the # of digits for each integer.
returns the converted text'''
def ascii_to_text(num, digits):
    num_list = [n for n in str(num)]
    converted_text = ""
    for d in digits:
        ascii_num = ""
        for i in range(d):
            ascii_num = ascii_num + num_list.pop(0)
        char = chr(int(ascii_num))
        converted_text = converted_text + char
    return converted_text

secret = "Ah ha"
secret, digits = text_to_ascii(secret)
print (type(secret))
print (secret)
print (digits)

print (ascii_to_text(secret, digits))