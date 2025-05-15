import pyttsx3 as pyt
import speech_recognition as sr
import datetime
import webbrowser
import pyjokes

def speech():
    input = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        input.adjust_for_ambient_noise(source)
        audio = input.listen(source)
        try:
            print("Recognizing....")
            data = input.recognize_google(audio)
            print("You Said: ",data.capitalize())
            return data.lower()
        except sr.UnknownValueError:
            print("I can't understand that")
            return None


def txtspeech(x):
    engine = pyt.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate',150)
    engine.say(x)
    engine.runAndWait()

def process_command(command):
    if "hello" in command:

        txtspeech("Hello! How can I help you?")
    
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        txtspeech(f"The time is {current_time}")

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        txtspeech(f"Today's date is {current_date}")

    elif "open youtube" in command:
        txtspeech("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "search for" in command or "who is" in command or "what is" in command:
        txtspeech("Searching the web for your query.")
        query = command.replace("search for", "").replace("who is", "").replace("what is", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            txtspeech("Please say what you want to search for.")

    elif "open google" in command:
        txtspeech("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "tell me a joke" in command:
        joke = pyjokes.get_joke()
        txtspeech(joke)
        print(joke)

    elif "exit" in command or "bye" in command:
        txtspeech("Goodbye! Have a great day.")
        exit()

    else:
        print("Please repeat")


def main():
    txtspeech("Hello! I am Jarvis. How can I assist you?")
    while True:
        command = speech() 
        if command:
            process_command(command) 
if __name__ == "__main__":
    main()