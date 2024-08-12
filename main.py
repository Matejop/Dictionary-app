import dictionary_app

class Main(): #Runs dictionary_app.py
    app = dictionary_app.DictionaryApp()
    app.Run("devn't") #Mode argument tells the app if to run with waitress or on flask dev server