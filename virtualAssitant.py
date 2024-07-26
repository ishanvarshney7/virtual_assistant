from deepface import DeepFace
import cv2
import pyttsx3 #python text to speech
import pyaudio
import os
import wikipedia #for wikipedia search
import datetime
import randfacts
import random
import smtplib #for emails sending
import webbrowser #for open browser-build in module
import requests #for news reading
from requests import get
import speech_recognition as sr

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
#print(voices[1].id) #female voice-voices[1].id
engine.setProperty('voice',voices[1].id)
rate=engine.getProperty('rate')
#print(rate) #rate of speed of assistent is 200 here
engine.setProperty('rate',150) #we slow speed of assistent here

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour=int(datetime.datetime.now().hour)
    if hour >=0 and hour<12:
        speak("Good morning")
    elif hour>=12 and hour<18:
        speak("Good afternoon")
    else:
        speak("Good evening")
        
    speak("Hello! I am your assistant, Chhotu, please tell me how may I help you?") 

def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('ishanvarshney4@gmail.com', 'Ishan@123456789')
    server.sendmail('ishanvarshney4@gmail.com', to, content)
    server.close()

def takecommand(): #it takes microphone input from user and return string output
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        #r.adjust_for_ambient_noise(source)
        #r.pause_threshold=1  to hold some time for the assistant before taking any command from the user
        r.energy_threshold=20000 #it can detect very low voice too
        audio= r.listen(source,phrase_time_limit=8)

        try:
            print("Recognizing......")
            query=r.recognize_google(audio,language='en-in')
            print(f"User Said:{query}\n")
            return query
        
        except Exception as e:
            print(e)
            print("say that again please....")
            return "None" #return a simple stament of word name


if __name__ == '__main__':
    wishme()
    while True:
        query=takecommand().lower()    #logic for executing task based on query

        if 'wikipedia' in query:
            speak('searching wikipedia...')
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query,sentences=2)
            speak("According to wikipedia ")
            print(results)
            speak(results)

        elif 'facts' in query or 'fact' in query:
            speak("Here some random facts ")
            x=randfacts.get_fact()
            print(x)
            speak(f"did you know{x}?")
            y = randfacts.get_fact()
            print(y)
            speak(y)
            z = randfacts.get_fact()
            print(z)
            speak(z)

        elif 'ip address' in query:
            ip=get('https://api.ipify.org').text
            print(f"your ip address is {ip}")
            speak(f"your ip address is {ip}")

        elif "current date" in query:
            today_date=datetime.datetime.now() #%d-day of month,%B-month,%y=year
            speak("today is"+today_date.strftime("%d")+"of"+today_date.strftime("%B")+"and its currently"+today_date.strftime("%Y"))
            print(today_date.strftime("%d %B %Y"))

        elif 'current time' in query:
            today_time=datetime.datetime.now()
            speak("currently time is "+today_time.strftime("%H")+"hours "+today_time.strftime("%M")+"minutes and "+today_time.strftime("%S")+"seconds at "+today_time.strftime("%p"))
            print("currently time is "+today_time.strftime("%H")+"hours "+today_time.strftime("%M")+"minutes and "+today_time.strftime("%S")+"seconds at "+today_time.strftime("%p"))

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'open college official site' in query or 'college website' in query:
            webbrowser.open("https://aith.ac.in/")

        elif 'open instagram' in query:
            webbrowser.open("https://www.instagram.com/")

        elif 'facebook'in query:
            webbrowser.open("https://www.facebook.com/")

        elif 'open linkedin' in query:
            webbrowser.open("https://in.linkedin.com/")

        elif 'temp' in query or 'temperature' in query:
            url = "http://api.weatherapi.com/v1/forecast.json?key=440aeb0539ea418eb1734341220204&q=meerut&days=1&aqi=yes&alerts=yes"
            json_data = requests.get(url).json()
            temp = (json_data["current"]["temp_c"])
            last_up = json_data["current"]["last_updated"]
            description = json_data["current"]["condition"]["text"]
            print(f"Current temperature in Meerut is: {temp} degree celcius and day is {description}.(last updated at: {last_up})")
            speak(f"Current temperature in Meerut is: {temp} degree celcius and day is {description}.(last updated at: {last_up})")

        elif 'news'  in query:
            speak("sure sir, now i will read some news for you.")
            news_api_address="https://newsapi.org/v2/top-headlines?country=in&apiKey=0b631146289b487f95ec9e3fe92b6f64"
            ar=[]
            json_data=requests.get(news_api_address).json()#converting api data to json file
            def news():
                for i in range(3):
                    ar.append("Number"+str(i+1)+","+json_data["articles"][i]["title"]+".")
                return ar
            arr=news()
            for i in range(len(arr)):
                print(arr[i])
                speak(arr[i])

        elif 'send an email' in query:
            try:
                speak("what should i say")
                content=takecommand()
                to="ishanvarshney7@gmail.com"
                send_email(to,content)
                speak("email has been sent")

            except Exception as e:
                print(e)
                speak("Sorry unable to send email")

        elif 'my mood' in query:
            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                cap = cv2.VideoCapture(1)
            if not cap.isOpened():
                raise IOError("Cannot open webcam")
            t = []

            while True:
                ret, frame = cap.read()
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                # print(result)
                # print(result[0]['dominant_emotion'])
                t.append(result[0]['dominant_emotion'])  # all emotions are stored in a list t
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,result[0]['dominant_emotion'],(50, 50),font, 3,(0, 0, 255),2,cv2.LINE_4)
                cv2.imshow('demo video', frame)
                #print(t)
                if cv2.waitKey(2) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
            print("your emotion is :", max(set(t), key=t.count))  # line to find dominant emotion in the given time\

        elif 'quit' in query:
            break
        
        elif query=='':
            speak("Please say that again")

print("Thank you for using this assistant. \nHave a good day")
speak("Thank you for using this assistant. Have a good day")