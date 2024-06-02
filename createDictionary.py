import xml.etree.ElementTree as ET
import random


def find_group_in_symbols(elements, typ):
    namespace = {'inkscape': 'http://www.inkscape.org/namespaces/inkscape'}

    elements = elements.findall(f'.//{{http://www.w3.org/2000/svg}}g[@inkscape:label = "{typ}"]/*', namespace)

    return elements

def main():

    print("Searching Symbols: ")

    symbol_types = ['1','2','3']


    svg_symbolTree = ET.parse(f"language/symbols.svg")
    symbols_root = svg_symbolTree.getroot()
    dictionary = {}

    for typ in symbol_types:
        group = find_group_in_symbols(symbols_root, f'typ{typ}')
        words = []

        for child in group:
            label = child.attrib['{http://www.inkscape.org/namespaces/inkscape}label']
            words.append(label)
            #print(f"Found in Typ {typ}: {label}")

        dictionary[f"typ{typ}"] = words

    print("Found the following Symbols:")
    word_count = 0
    for key,value in dictionary.items():
        combinations = len(value)*len(value)
        word_count += combinations
        print(key, f"Possible Combinations: {combinations}", value)

    print(f"Max. Words: {word_count}")

    word_array = []
    with open("language/useful_words.txt", 'r') as file:
        for line in file:
            word = line.strip()  # Remove leading/trailing whitespace and newline characters
            word_array.append(word)

    if len(word_array) <= word_count:
        print(f"Found {len(word_array)} words to translate")
    else:
        len_word = len(word_array)
        word_array = word_array[:word_count]
        print(f"Found {len_word} words to translate. Caping to {len(word_array)} words")

    random.shuffle(word_array)

    print("Printing Dictionary:")
    print("")
    print("NAME-TOP;NAME-BOTTOM;TRANSLATION;TYP")
    i = 0
    for key,value in dictionary.items():

        typ = key.replace("typ","")

        for symbol1 in value:
            for symbol2 in value:
                if i < (len(word_array)):
                    print(f"{symbol1.upper()};{symbol2.upper()};{word_array[i].upper()};{typ}")
                    i += 1
                else:
                    break





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
