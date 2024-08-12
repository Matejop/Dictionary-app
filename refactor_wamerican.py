#Makes a .csv file that the app can work with

file = open("american-english-huge")
content = file.read()
file.close()
content = content.lower()
dictionary = sorted(content.splitlines())
refactor_file = open("american-english-huge-refactoreds.csv", "a")

for i in range(len(dictionary)):
    dictionary[i] = '\"' + dictionary[i] + '\"'

refactor_file.write(",".join(dictionary))
refactor_file.close()
        