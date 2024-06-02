<h1>Cthulhuglyphs</h1>


A little Tool that creates a riddle out of the <a href="https://lovecraftzine.com/wp-content/uploads/2013/04/lovecraft-bestiary.jpg"> Cthulhu Symbols</a>.
Best used in the PenAndPaper Call of Cthulhu:

<h2>How to use</h2>
<h3>Creating a riddle:</h3>
- Change the Words in the file sentences.csv<br>
  - You can write max. 6 Word Groups, made out of exactly 3 Words each<br>
  - Example: <br>
  NORTH;WEST;CLOSE<br>
  NEARBY;UNDER;LAND <br>
  MADNESS;BOTH;ELDRITCH<br>
  - empty sentences are gonna be filled up with random words<br>
  - You can only use the words from the file language/useful_words.txt<br>
  - if you want to use other words check how to create a new dictionary<br>
- now run main.py<br>
- it should create a riddle.svg and a translation.svg in the export folder<br>

<h3>Using the Riddle:</h3>
- Print out the exported SVG files<br>
  - (export them to png  or jpeg for better printing results)<br>
- cut out the 2 triangles from the riddle.svg<br>
- when you lay the 2 triangles on top of each other, they either form a triangle or a Star of David<br>
- the symbols then complement each other and can be translated with the translation file <br>

<h3>Creating a dictionary:</h3>
- if you want to change the meaning of the symbols you can change the dictionary<br>
- simply change the language/useful_words.txt file and fill it up with the words you want to use (max. 256)<br>
- then run createDictionary.py<br>
- this prints out the content for language/dictionary.csv in the terminal<br>
- just copy and paste it into the file and now you can use your new words <br>

