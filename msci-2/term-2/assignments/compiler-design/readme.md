# Compiler Design Coursework Documentation
## Installation
To run this program you will need
* `python` (download [here](https://www.python.org/downloads/release/python-374/))
* `graphviz`; (download [here](https://graphviz.gitlab.io/download/)) and
* `anytree` (with the above packages installed, run `pip install anytree`).

## Running the program

The python script `main.py` takes three arguments:
* the input file name is the name of the text file containing 
    the sets of symbols and formula;
* the output grammar file is the name of the text file the program will write the
    corresponding grammar to; and
* the output abstract syntax tree file name is the name of the file the program should 
    write the abstract syntax tree to (must end in `.png`).

These files must be in the same directory as `main.py`.
You call the program using the following syntax.
```
python main.py input_file output_grammar_file output_tree_file
```

For example, if the input file was called `input.txt` and I wanted the
program to write to `grammar.txt` and `ast.png` I would execute the following command.
```
python main.py input.txt grammar.txt ast.png
```

## Outputs

Note that if parsing is unsuccessful, the program will not generate a
grammar or abstract syntax tree file. 

### Grammar file
The grammar file will outline the symbols and production rules of the grammar.
It will show the
* non-terminalgi symbols;
* terminal symbols;
* production rules; and
* the starting symbol.

### Abstract syntax tree
The abstract syntax tree file is an image of the abstract syntax tree of the
provided grammar, given that it is valid.

### Log file
Given that the program arguments are valid, the program will generate a log file.
If the parsing is successful, it will state as such.
If parsing was unsuccessful, it will report a syntax error.

## Examples
The files
* `example-1.txt`;
* `example-2.txt`;
* `example-3.txt`; and
* `example-4.txt`

are example inputs to the program with valid formula.