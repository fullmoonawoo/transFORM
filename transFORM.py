import csv
import sys, os
import argparse
from argparse import ArgumentParser
from typing import Optional


# HOW TO CALL THAT: >> python be.py -m 'T' -s 'source.txt' -d '-' -sb '*' -p '2,3,4'
# BUGs: when in source file is line without any delimiter like just slovo1


class Transform:
    def __init__(self, mode: str, source, delimiter: str = ',', symbol: str = ":", position: Optional[int] = None, jump: Optional[int] = 1):
        # ARGUMENTS:
        # mode:        > choose the required mode: -T - transform - modify data on some position with choosen symbol, -R - replace - only replace existing delimiter with the substitutor, -C - change character on position - replace index of existing character on selected position with substitutor
        # source:      > source file in txt/csv format written in csv columns
        # delimiter:   > what delimiter is used in source file
        # symbol:      > symbol what will be add between characters [function: transform]
        # position:    > put position index of column what you want to modify
        # jump:        > number of characters after which the string in column is divided by the separator
        self.mode = mode
        self.source = source
        self.delimiter = delimiter
        self.separator = symbol
        self.position = False
        if position:
            self.position = [int(x) for x in position.split(',')]
        #self.position = position - 1
        self.jump = int(jump)
        # File name
        self.file_name = source.split('.')[0]
        self.script_real_path = os.path.realpath(source)
        self.script_folder = os.path.dirname(self.script_real_path)
        #print(self.script_real_path)
        #print(self.script_folder)
        self.datalines = []
        # Automatic loading
        self.load_data()

        # Probes:


    def load_data(self):
        with open(self.source, "r", newline='') as data_source:
            self.datalines = [line.rstrip() for line in data_source.readlines()]
            print('DATALINES: ', self.datalines)
            print(f"Reading of {self.source} was sucessfull")

    def show_data(self):
        if self.datalines:
            return self.datalines
        else:
            print("Nothing to show !")

    def check_lenght(self):
        self.lenghts = []
        for line in self.datalines:
            self.lenghts.append(line.count(self.delimiter))

        self.most_frequent = max(self.lenghts)
        self.nonvalid = []
        for index, numb in enumerate(self.lenghts):
            if numb != self.most_frequent:
                self.nonvalid.append(str(index + 1))
        
        if len(self.nonvalid) != 0:
            return self.nonvalid
        else:
            print("False")
            return False


    def transform(self, path):
        self.file_path = self.file_name + '_output.txt'
        self.tokens_dump = []
        for line in self.datalines:
            self.tokens = self.tokenize(line)
            for word_position in range(len(self.tokens)):
                if self.position and (word_position in self.position):
                    self.to_change = self.tokens[word_position]
                    self.tokens[word_position] = self.separator.join(self.to_change[i:i + self.jump] for i in range(0, len(self.to_change), self.jump))
                    
                elif not self.position:
                    self.to_change = self.tokens[word_position]
                    self.tokens[word_position] = self.separator.join(self.to_change[i:i + self.jump] for i in range(0, len(self.to_change), self.jump))

            self.tokens_dump.append(self.tokens)
                
        
        # Export to the txt file
        self.throw_to_txt(self.tokens_dump, self.file_path)
        # clean token_dump
        self.tokens_dump = []


    def change_position(self, path):
        self.file_path = self.file_name + '_output_CP.txt'
        self.tokens_dump = []
        for line in self.datalines:
            self.tokens = self.tokenize(line)
            self.to_change = self.tokens[self.position]
            self.newstring = ""
            for x in range(len(self.to_change)):
                if x == self.jump - 1:
                    self.tokens[self.position] = self.newstring + self.separator + self.to_change[self.jump:]
                    break
                else:
                    self.newstring += self.to_change[x]
            self.tokens_dump.append(self.tokens)

        # Export to the txt file
        self.throw_to_txt(self.tokens_dump, self.file_path)
        # clean token_dump
        self.tokens_dump = []


    def replace_delimiter(self, path):
        self.file_path = self.file_name + '_output_C.txt'
        self.tokens_dump = []
        for line in self.datalines:
            self.tokens = self.tokenize(line)
            self.to_change = self.tokens[self.position]
            print('TO CHANGE: ', self.to_change)
            self.tokens[self.position] = self.to_change.replace(self.delimiter, self.separator)
            self.tokens_dump.append(self.tokens)
        
        # Export to the txt file
        self.throw_to_txt(self.tokens_dump, self.file_path, self.separator)
        # clean token_dump
        self.tokens_dump = []

    # Iterating throught one line and dividing line into strings based on the delimiter
    def tokenize(self, line) -> list:  # slovo1-slovo2
        self.line_tokens = []
        self.start = 0
        self.end = None
        self.last = len(line) - 1
        
        for x in range(len(line)):
            if line[x] == self.delimiter:
                self.end = x
                self.line_tokens.append(line[self.start:self.end])
                self.start = x + 1
            elif x == self.last:
                self.end += 1
                self.final_word = line[self.end:len(line)]  # -1 removed
                #self.final_word = line[self.start:len(line)]  # does not matter if this line will be executed or line above
                self.line_tokens.append(self.final_word)

        return self.line_tokens

    def throw_to_txt(self, dump, path, new_delimiter=","):
        with open(path, "w") as output:
            for line in dump:
                output.writelines(new_delimiter.join(line))
                output.writelines("\n")


    def throw_to_csv(self, dump, path):
        with open(path, "w", newline="") as output:
            writer = csv.writer(output)
            for line in dump:
                writer.writerow(line)

    def __str__(self):
        self.to_show = self.show_data()
        return str(self.to_show)
    
    
def get_cli_arguments():
    cli_parser = argparse.ArgumentParser(prog=sys.argv[0], description="Tool for transforming structured data files. Script can modify data on some position with periodic insert of selected symbol, replace delimiter or replace character in specific column and column index")

    # ARGUMENTS:
        # mode:        > choose the required mode: -T - transform - modify data on some position with choosen symbol, -R - replace - only replace existing delimiter with the substitutor, -C - change character on position - replace index of existing character on selected position with substitutor
        # source:      > source file in txt/csv format written in csv columns
        # delimiter:   > what delimiter is used in source file
        # symbol:      > symbol what will be add between characters
        # position:    > put position index of column what you want to modify
        # jump:        > number of characters after which the string in column is divided by the separator
        # output:      > choose output format of the file [txt or csv]
    cli_parser.add_argument('-m', '--mode', choices=['T', 'R', 'C'], 
                            help="Three available modes: \n"
                            "T - transform - modify data on some position with choosen symbol\n" 
                            "R - replace - only replace existing delimiter with the substitutor\n" 
                            "C - change character on position - replace index of existing character on selected position with substitutor\n")
    cli_parser.add_argument('-s', '--source_file', help='Source file')
    cli_parser.add_argument('-d', '--delimiter', help='Existing delimiter in source file')
    cli_parser.add_argument('-sb', '--symbol', help='Transformation mode: symbol which modify data in specific columns')
    cli_parser.add_argument('-p', '--position', help='In case we want to modify only data on some row position in dataset')
    cli_parser.add_argument('-j', '--jump', help='Transformation mode: Gap for a between placed symbols')

    if len(sys.argv) <= 1:
        cli_parser.print_usage()
        sys.exit()

    args = cli_parser.parse_args()
    return args


if __name__ == "__main__":
    session_args = get_cli_arguments()
    job = Transform(mode=session_args.mode, source=session_args.source_file, delimiter=session_args.delimiter, symbol=session_args.symbol, position=session_args.position, jump=session_args.jump)
    #job.check_lenght()
    job.transform('/home/fma44/Documents/python_projects/transFORM_backup')
    #job.change_position('/home/fma44/Documents/python_projects/transFORM_backup')
    #job.replace_delimiter('/home/fma44/Documents/python_projects/transFORM_backup')

