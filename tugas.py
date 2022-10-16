from datetime import datetime
from distutils.log import error
from logging import exception
from logging.config import listen
from msilib.schema import AppId
from multiprocessing.connection import Listener
from re import search
from unittest import result
from urllib import response
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
activationWord = 'computer'

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

appId = '5R4937-J888YX9J2V'
wolframClinet = wolframalpha.Clinet(appId)


def speak(text, rate=120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


def parseCommand():
    Listener = sr.Recognizer()
    print('Listening for a command')

    with sr.Microphone() as source:
        Listener.pause_threshold = 2
        input_speech = Listener.listen(source)

    try:
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'The input speech was : {query}')

    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'

    return query

    def search_wikipedia(query=''):
        searchResults = wikipedia.search(query)
        if not searchResults:
            print('No wikipedia result')
            return 'no result received'
        try:
            wikipedia = wikipedia.page(searchResults[0])

        except wikipedia.DisambiguationError as error:
            wikiPage = wikipedia.page(error.options[0])
        print(wikiPage.title)
        wikiSummary = str(wikiPage.summary)
        return wikiSummary

    def listOrDict(var):
        if isinstance(var, list):
            return var[0]['plaintext']
        else:
            return var['plaintext']

    def search_wolfframAlpha(query=''):
        response = wolframClinet.query(query)

        if response['@success'] == 'false':
            return 'Could not compute'

        else:
            result = ''

            pod0 = response['pod'][0]
            pod1 = response['pod'][1]

            if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
                result = listOrDict(pod1['subpod'])
                return result.split('(')[0]
            else:
                question = listOrDict(pod0['subpod'])
                return question.split('(')[0]
                speak('Computation failed. Querying universal databank.')
                return search_wikipedia(question)


# main loop
if __name__ == '__main__':
    speak('All systems nominal.')

    while True:
        query = parseCommand().lower().split()
        # list command
        if query[0] == 'say':
            if 'hello' in query:
                speak('Greetings,all.')
            else:
                query.pop(0)
                speech = ''.join(query)

        # Navigation
        if query[0] == 'go' and query[1] == 'to':
            speak('Opening...')
            query = ''.join(query[2:1])
            webbrowser.get('chrome').open_new(query)

        # Wikipedia
        if query[0] == 'wikipedia':
            query = ''.join(query[1:])
            speak('Querying the universal databank.')
            speak(search_wikipedia(query))

        # wolfram alpha
        if query[0] == 'compute' or query[0] == 'computer':
            query = ''.join(query[1:])
            speak('Computing')
            try:
                result = search_wolframAlpha(query)
                speak(result)
            except:
                speak('Unable to compute.')

        # Note taking
        if query[0] == 'log':
            speak('Ready to record your note')
            newNote = parseCommand().lower()
            now = datetime.now().strftime('%Y=%m-%d-%H-%M-%S')
            with open('note_%s.txt' % now, 'W') as newFile:
                newFile.write(newNote)
            speak('Note written')

        if query[0] == 'exit':
            speak('Goodbye')
            break
