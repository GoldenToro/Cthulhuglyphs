# This is a sample Python script.
import xml.etree.ElementTree as ET
import random


# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def find_word_in_dictionary(dictionary, search_string):
    # Iterate over each row in the CSV file
    for row in dictionary:

        # Check if the row has at least three columns
        if len(row) >= 3:
            # Check if the value in the third column matches the search string
            if row[2] == search_string:
                # If found, return the strings of the first two columns
                return row

    # If search string is not found, return None
    return None


def find_word_in_template(elements, layer, sentence, word):
    namespace = {'inkscape': 'http://www.inkscape.org/namespaces/inkscape'}

    elements = elements.find(f'.//{{http://www.w3.org/2000/svg}}g[@inkscape:label = "{layer}"]//{{http://www.w3.org/2000/svg}}g[@inkscape:label = "{sentence}"]//{{http://www.w3.org/2000/svg}}g[@inkscape:label = "{word}"]', namespace)

    return elements


def find_symbol_in_symbols(elements, symbol, direction):
    namespace = {'inkscape': 'http://www.inkscape.org/namespaces/inkscape'}

    elements = elements.find(f'.//{{http://www.w3.org/2000/svg}}g[@inkscape:label = "{symbol}"]//{{http://www.w3.org/2000/svg}}g[@inkscape:label = "{direction}"]', namespace)

    return elements


def load_dictionary():
    dictionary = open("language/dictionary.csv", 'r')
    csv_data = []

    # Iterate over each row in the CSV file
    for row in dictionary:
        # Append the row to the list as a 2D array
        csv_line = []

        words = row.strip().split(';')

        for word in words:
            csv_line.append(word)

        csv_data.append(csv_line)

    dictionary.close()
    return csv_data


def write_symbol(template, symbols, layer, sentence, word, symbol, direction):
    template_word = find_word_in_template(template, layer, f"sentence{sentence}", f"word{word}")

    if word:
        print("Found Word in Template")

        replace_word = find_symbol_in_symbols(symbols, symbol, direction)

        if replace_word:
            print("Found Symbol")

            for child in list(template_word):
                template_word.remove(child)

            template_word.append(replace_word)


def main():
    # Use a breakpoint in the code line below to debug your script.
    print("loading Template")

    template_tree = ET.parse("template/template.svg")
    template_root = template_tree.getroot()

    svg_symbolTree = ET.parse(f"language/symbols.svg")
    symbols_root = svg_symbolTree.getroot()

    sentences = open("sentences.csv", 'r')
    dictionary = load_dictionary()

    i = 0
    for sentence in sentences:
        words = sentence.strip().split(';')

        print("###########################")
        if (len(words) == 3):
            i += 1
            j = 0
            print(f"Start Writing Sentence {i}: " + sentence)
            for word in words:
                j += 1
                print("########")
                print(f"Start Writing Word {j}: " + word)
                symbol = find_word_in_dictionary(dictionary, word)
                if symbol:
                    print("Found Symbol: " + str(symbol))

                    if random.choice([True, False]):

                        write_symbol(template_root, symbols_root, "textTop", i, j, symbol[0], "top")
                        write_symbol(template_root, symbols_root, "textBottom", i, j, symbol[0], "bottom")

                    else:

                        write_symbol(template_root, symbols_root, "textTop", i, j, symbol[0], "bottom")
                        write_symbol(template_root, symbols_root, "textBottom", i, j, symbol[0], "top")








                else:
                    pass
        else:
            print("Skipping Sentence: " + sentence)

    template_tree.write("export/riddle.svg")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
