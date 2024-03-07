import csv
from typing import Optional


class Transform:
    def __init__(self, source, name: str, delimiter: str = ',', separator: str = ":", position: Optional[int] = 1, jump: Optional[int] = 1):
        # ARGUMENTS:
        # source:    > source file in txt/csv format written in csv columns
        # name:      > name of output file
        # delimiter: > what delimiter is used in source file
        # position:  > put position index of column what you want to modify
        # jump:      > number of characters after which the string in column is divided by the separator
        self.source = source
        self.name = name
        self.delimiter = delimiter
        self.separator = separator
        self.position = position
        self.jump = jump
        # Automatic loading
        self.load_data()

        # Probes:


    def load_data(self):
        with open(self.source, "r", newline='') as data_source:
            self.datalines = [line.rstrip() for line in data_source.readlines()]
            print(f"Reading of {self.source} was sucessfull")

    def show_data(self):
        if self.datalines:
            return self.datalines
        else:
            print("Nothing to show !")

    def transform(self):
        self.tokens_dump = []
        for line in self.datalines:
            self.tokens = self.tokenize(line)
            self.to_change = self.tokens[self.position]
            self.tokens[self.position] = self.separator.join(self.to_change[i:i + self.jump] for i in range(0, len(self.to_change), self.jump))
            self.tokens_dump.append(self.tokens)
        self.throw_to_csv(self.tokens_dump)
        print("Tranformation of", self.name.split('.')[0], "has been done !")


    # Iterating throught one line and dividing line into strings based on the delimiter
    def tokenize(self, line):
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
                self.final_word = line[self.end:len(line) - 1]
                self.line_tokens.append(self.final_word)

        return self.line_tokens
    
    
    def throw_to_csv(self, dump):
        with open(self.name + "_output.csv", "w", newline="") as output:
            writer = csv.writer(output)
            for line in dump:
                writer.writerow(line)

    def __str__(self):
        self.to_show = self.show_data()
        return str(self.to_show)



#if __name__ == "__main__":
    #sources = ["source.txt"]
    #for file in sources:
        #job = Parser(file, file.split('.')[0], ",", "<", 1)
        #job.manage_parser()
        #print("Tranformation of", file.split('.')[0], "has been done !")

    
