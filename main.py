# -*- coding: utf-8 -*-
from collections import defaultdict
from collections import defaultdict
import operator

MORSE_CODE =\
{
'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
'Y': '-.--', 'Z': '--..',

'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.', 'Д': '-..', 'Е': '.', 'Ё': '.', 'Ж': '...-', 'З': '--..',
'И': '..', 'Й': '.---', 'К': '-.-', 'Л': '.-..', 'М': '--', 'Н': '-.', 'О': '---', 'П': '.--.', 'Р': '.-.',
'С': '...', 'Т': '-', 'У': '..-', 'Ф': '..-.', 'Х': '....', 'Ц': '-.-.', 'Ч': '---.', 'Ш': '----',
'Щ': '--.-', 'Ъ': '.--.-.', 'Ы': '-.--', 'Ь': '-..-', 'Э': '..-..', 'Ю': '..--', 'Я': '.-.-',

'0': '-----','1': '.----', '2': '..---','3': '...--','4': '....-','5': '.....','6': '-....','7': '--...','8': '---..','9': '----.',

'.': '.-.-.-',',': '--..--','?': '..--..','!': '-.-.--', '-': '-....-', '(': '-.--.', ')': '-.--.-',
':': '---...', ';': '-.-.-.', '"': '.-..-.', ' ': '/'
}

def encode(text):
    encoded_text = []
    for char in text:
        if char.upper() in MORSE_CODE:
            encoded_text.append(MORSE_CODE[char.upper()])
        else:
            encoded_text.append(char)
    return ' '.join(encoded_text)

def decode(code):
    decoded_text = []
    words = code.split('  ')
    for word in words:
        letters = word.strip().split()
    for letter in letters:
        for key, value in MORSE_CODE.items():
            if value == letter:
                decoded_text.append(key)
                break
        decoded_text.append(' ')
    return ''.join(decoded_text)

input_text = "In the конце теста was 4 вопроса!!"
print("----------Исходный текст----------\n", input_text)
encoded = encode(input_text)
print("\n----------На азбуке Морзе----------\n", encoded)

decoded = decode(encoded)
print("\n----------Транслит или на втором языке----------\n", decoded)