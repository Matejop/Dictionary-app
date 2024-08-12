from flask import Flask, request, jsonify
from waitress import serve
import random
import math

class DictionaryApp(): 

    def Run(self, mode): #Run method called by main. Defines endpoints and runs the app. Mode is a variable that defines app run mode
        self.mode = mode
        self.app = Flask(__name__)

        @self.app.route("/filter_words", methods=["GET","POST"])
        def call_filter_words():
            return self.FilterWords()

        @self.app.route("/filter_pairs", methods=["GET","POST"])
        def call_filter_pairs():
            return self.FilterPairs()

        @self.app.route("/filter_counts", methods=["GET","POST"])
        def call_filter_counts():
            return self.FilterCounts()

        if __name__ == "dictionary_app": #Kept dev mode since it was useful during development
            if self.mode == "dev":
                self.app.run(debug=True)
            else:
                serve(self.app, host='0.0.0.0', port=50100, threads=1)

    def GetDictionary(self): #Gets refactored version of the wamerican
        file = open("american-english-huge-refactored.csv")
        content = file.read()
        file.close()
        dictionary = content.split(',')

        for i in range(len(dictionary)):
            dictionary[i] = dictionary[i].strip('\"')

        return dictionary
   
    def RefactorInput(self, input): #Returns refactored list of words from input in the same format as words in refactored wamerican
        input = input.replace("\n\r", ' ')
        input = input.replace('\n', ' ')

        input_words = input.split()
                     
        for i in range(len(input_words)): 
            input_words[i] = list(input_words[i])
            for j in range(len(input_words[i])):
                if input_words[i][j].isalpha() or input_words[i][j] == '\'' or input_words[i][j] == ' ':
                    continue
                else:
                    input_words[i][j] = ' '
            input_words[i] = ''.join(input_words[i])

        input_words = ' '.join(input_words)
        input_words = input_words.split()
        return input_words
    
    def GetUndefinedWords(self): #Returns list of unique words not found in the wamerican
        input = request.get_data(as_text=True) #Gets body of request
        input_words = self.RefactorInput(input)
        dictionary = self.GetDictionary()
        undefined_words = []
        
        for word in input_words: 
            found = self.BinarySearch(word, dictionary)
            for undefined_word in undefined_words:
                if undefined_word == word:
                    found = True
                    break
            if not found:
                undefined_words.append(word)
        
        return undefined_words
       
    def BinarySearch(self, word, word_list): #Searches the wamerican (word_list) and returns true if the argument word was found, false if not
        word = word.lower()
        lower_bound = 0
        upper_bound = len(word_list) - 1
        found = False

        while lower_bound <= upper_bound:
            mid = math.floor(lower_bound + (upper_bound  -  lower_bound) / 2)
            if word == word_list[mid]:
                found = True
                break
            elif word < word_list[mid]:
                upper_bound = mid - 1
            else:
                lower_bound = mid + 1

        return found
    
    def FilterWords(self): #Returns response: Words not defined in the wamerican
        if request.method == "POST":
            return jsonify({"filter_words": self.GetUndefinedWords()}), 200 
        else:
            return jsonify("Not valid input"), 400 #Wasn't sure what to return if endpoint received GET request

    def FilterPairs(self): #Returns response: Pairs of defined and not defined words
        if request.method == "POST":
            input = request.get_data(as_text=True)
            input_words = self.RefactorInput(input)
            undefined_words = self.GetUndefinedWords()
            pairs = []

            for text_word in input_words:
                for undefined_word in undefined_words:
                    if text_word == undefined_word:
                        input_words.remove(text_word)
            for undefined_word in undefined_words:
                random_int = random.randint(0, len(input_words) - 1)
                pairs.append([undefined_word, input_words[random_int]])

            return jsonify({"filter_pairs": pairs}), 200 
        else:
            return jsonify("Not valid input"), 400 #Wasn't sure what to return if endpoint received GET request

    def FilterCounts(self): #Returns response: Count of undefined words and defined words in the request text
        if request.method == "POST":
            input = request.get_data(as_text=True)
            input_words = self.RefactorInput(input)
            undefined_words = self.GetUndefinedWords()
            return jsonify({"filter_counts": {"dict_words": len(input_words) - len(undefined_words), "non-dict_words": len(undefined_words)}}), 200
        else: 
            return jsonify("Not valid input"), 400 #Wasn't sure what to return if endpoint received GET request