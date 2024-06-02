# This is a sample Python script.
import xml.etree.ElementTree as ET
import random
import copy


# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def get_unique_random_choice(word_array, target_array):
    while True:
        random_word = random.choice(word_array)
        if random_word not in target_array:
            return random_word


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

        replace_word = find_symbol_in_symbols(symbols, symbol, direction)

        if replace_word:

            for child in list(template_word):
                template_word.remove(child)

            replace_word.set("label", f"{symbol}-{direction}-{sentence}-{word}")

            template_word.append(replace_word)


def add_translation(template, dictionary, symbols, word, i):

    transform = "matrix(0.44396914,0,0,0.44396914,-33.31881,-7.1430661)"
    transformY = -10 + (i%13 * 21)
    transformX = -20 + (i//13 * 60)
    transform = f"matrix(0.44396914,0,0,0.44396914,{transformX},{transformY})"


    word = find_word_in_dictionary(dictionary, word)

    symbol_top = find_symbol_in_symbols(symbols, word[0], "top")
    symbol_bottom = find_symbol_in_symbols(symbols, word[1], "bottom")

    template_translation = find_symbol_in_symbols(template,"words","template")

    new_translation = copy.deepcopy(template_translation)


    # Find the <tspan> element within the <text> element
    text_element = new_translation.find("./{http://www.w3.org/2000/svg}text/{http://www.w3.org/2000/svg}tspan")

    new_text = word[2].replace(" ","\n")
    new_text = new_text.replace("-","-\n")
    text_element.text = new_text

    namespace = {'inkscape': 'http://www.inkscape.org/namespaces/inkscape'}
    symbol_element = new_translation.find("./{http://www.w3.org/2000/svg}g[ @inkscape:label = 'symbol']", namespace)

    if symbol_element:

        for child in list(symbol_element):
            symbol_element.remove(child)

        symbol_element.append(symbol_top)
        symbol_element.append(symbol_bottom)

    # Change the ID of the copied element
    new_translation.set('id', f'translation-{i}')
    new_translation.set('transform', transform)


    template.append(new_translation)




def main():
    # Use a breakpoint in the code line below to debug your script.
    print("loading Template")

    template_tree = ET.parse("templates/template.svg")
    template_root = template_tree.getroot()

    svg_symbolTree = ET.parse(f"language/symbols.svg")
    symbols_root = svg_symbolTree.getroot()

    sentence_file = open("sentences.csv", 'r')
    sentences = []
    for line in sentence_file:
        sentences.append(line.strip())
    sentence_file.close()

    dictionary = load_dictionary()

    important_words = []
    print("############ PREP: ##############")
    print(f"Found the following Sentences ({len(sentences)}):")
    for sentence in sentences:
        print(sentence)

        words = sentence.strip().split(';')
        for word in words:
            important_words.append(word)

    if len(sentences) <= 6:
        print("Filling sentences up to 6 with the following random generated ones:")

        word_array = []
        with open("language/useful_words.txt", 'r') as file:
            for line in file:
                word = line.strip()  # Remove leading/trailing whitespace and newline characters
                word_array.append(word)

        while (len(sentences) < 6):
            new_sentence = f"{random.choice(word_array)};{random.choice(word_array)};{random.choice(word_array)}"
            sentences.append(new_sentence)
            print(new_sentence)

    random.shuffle(sentences)

    print("############ WRITING ##############")
    i = 0
    if len(sentences) <= 6:
        for sentence in sentences:
            words = sentence.strip().split(';')

            if (len(words) == 3):
                i += 1
                j = 0
                # print(f"### Sentence {i} ###")
                # print(f"Start Writing Sentence: " + sentence)
                for word in words:
                    j += 1
                    print_text = f"Word: {word}"

                    symbol = find_word_in_dictionary(dictionary, word)
                    if symbol:

                        print_text += f"; Typ: {symbol[3]}; Top: {symbol[0]}; Bottom: {symbol[1]}"


                        write_symbol(template_root, symbols_root, "textTop", i, j, symbol[0], "top")
                        write_symbol(template_root, symbols_root, "textBottom", i, j, symbol[1], "bottom")


                        # print(print_text)
                    else:
                        print(f"ERROR: No Symbol found for: {word}")
                        pass

            else:
                print("Only 3 Words allowed, skipping: " + sentence)
    else:
        print("Max. 6 Sentences, skipping all")

    template_tree.write("export/riddle.svg")

    print("############ TRANSLATIOn ##############")

    words_used = []

    for sentence in sentences:
        words = sentence.strip().split(';')

        for word in words:

            if word in important_words:
                words_used.append(word)

            else:

                if random.choice([True, False]):
                    words_used.append(word)

    print("Important Words: ", important_words)
    words_for_confusion = ['NORTH','EAST','WEST','SOUTH','DOWN','UNDER','NEAR','FAR']
    print("add the following words: ", words_for_confusion)
    for word in words_for_confusion:
        if word not in words_used:
            words_used.append(word)

    while (len(words_used) < 39):
        words_used.append(get_unique_random_choice(word_array, words_used))

    print("All Words: ",words_used)

    translation_tree = ET.parse("templates/translation-table.svg")
    translation_root = translation_tree.getroot()

    random.shuffle(words_used)

    i = 0
    for word in words_used:
        add_translation(translation_root, dictionary, symbols_root, word, i)
        i += 1

    element_to_delete = translation_root.find(".//*[@id='layer2']")
    translation_root.remove(element_to_delete)

    translation_tree.write("export/translation.svg")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
