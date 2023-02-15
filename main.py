import os
import datetime
import pyttsx3
import speech_recognition


# инициализация инструмента синтеза речи
tts = pyttsx3.init('sapi5')
voices = tts.getProperty('voices')
tts.setProperty('voice', voices[2].id)

rate = tts.getProperty('rate')
tts.setProperty('rate', 200)

def speak(audio):
    tts.say(audio)
    tts.runAndWait()  # Без этой команды мы не услышим речь


def record_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        # использование online-распознавания через Google
        try:
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит выброс ошибки
        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")

        return recognized_data


if __name__ == "__main__":
    speak('Этого хватит, Джарвис. Смысл в том, что это невозможно. Я это знал ещё ребёнком.')

    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    while True:
        # старт записи речи с последующим выводом распознанной речи
        # и удалением записанного в микрофон аудио
        voice_input = record_audio()
        os.remove("microphone-results.wav")
        print(voice_input)

        # отделение комманд от дополнительной информации (аргументов)
        voice_input = voice_input.split(" ")
        command = voice_input[0]

        if command == "привет":
            speak("Привет, меня зовут Лео")

        if command == "время":
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Сейчас: {strTime}')

        if command == "браузер":
            codePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
            os.startfile(codePath)

        if command == 'пока' or command == 'Пока':
            speak('Пока!')
            break
