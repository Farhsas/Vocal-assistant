from sense_hat import SenseHat
import rhasspy 
import datetime
import time
import crypto
import os

sense = SenseHat()

sense.show_letter("A")
print("Begin trainning")
rhasspy.train_intent_files("/home/pi/sentences.ini")
print("Trainning done!")

rhasspy.text_to_speech("Hello, I'm Bud, your vocal assistant")

while True:
    intent = rhasspy.speech_to_intent()
    print(intent)

    sense.show_message("Command : {}".format(intent["name"]), scroll_speed=0.05)

    command = "{}".format(intent["name"])

    if command == "GetTime" :
        now = datetime.datetime.now()
        sense.show_message("%s h %d" % (now.strftime('%H'), now.minute))
        rhasspy.text_to_speech("%s hours %d" % (now.strftime('%H'), now.minute))
    
    elif command == "GetDate":
        today = datetime.date.today()
        date = today.strftime("%d/%m/%Y")
        sense.show_message("Date: " + date)
        rhasspy.text_to_speech("We are the" + date)

    elif command == "GetWeather":
        humidity = sense.get_humidity()
        temperature = sense.get_temperature()
        pressure = sense.get_pressure()

        sense.show_message("Humidity: " + str(humidity), text_colour =[255, 0, 0])
        time.sleep(2)
        rhasspy.text_to_speech("The humidity is " + str(humidity))

        sense.show_message("Temperature : " + str(temperature), text_colour =[255, 0, 0])
        time.sleep(2)
        rhasspy.text_to_speech("The temperature" + str(temperature))

        sense.show_message("Atmospheric pressure: " + str(pressure), text_colour =[255, 0, 0])
        time.sleep(2)
        rhasspy.text_to_speech("The atmospheric pressure is " + str(pressure))

    elif command == "GetPIN":
        getmdp = "{}".format(intent["variables"]["mot de passe"])
        getmdpHACHE = crypto.hashing(getmdp)
        filePin = "PIN.txt"
        fileMdp = "MDP.txt"
        with open(filePin ,'r') as PIN :
            if os.stat(filePin).st_size != 0:
                VpinC =PIN.read()
                with open(fileMdp,'r') as MDP :
                     VmdpH =MDP.read()
                if getmdpHACHE == VmdpH :
                #donc le mot de passe dit par l'utilisateur(lors de la tentative) est egale au mot de passe hache
                    pinDECODE = crypto.decode(getmdp,VpinC)
                    rhasspy.text_to_speech("Your PIN is"+pinDECODE)
                else :
                    rhasspy.text_to_speech("The password you gave is incorrect")
            else:
                rhasspy.text_to_speech("No PIN registered") 

        

    elif command == "AddPIN":
        filePin = "PIN.txt"
        fileMdp = "MDP.txt" 

        pin = "{}".format(intent["variables"]["PIN"])
        mdp = "{}".format(intent["variables"]["mot de passe"])

        pinCHIFFRE = crypto.encode(mdp,pin)
        mdpHACHE = crypto.hashing(mdp)

        fichierPIN = open(filePin, "a")
        fichierPIN.truncate(0)

        fichierPIN.write(pinCHIFFRE)
        fichierPIN.close()
 
        fichierMdp = open(fileMdp,"a")
        fichierMdp.truncate(0)
        fichierMdp.write(mdpHACHE)
        fichierMdp.close()

    elif command == "DeletePIN":

        deletemdp = "{}".format(intent["variables"]["mot de passe"])
        deletemdpHACHE = crypto.hashing(deletemdp)

        filePin = "PIN.txt"
        fileMdp = "MDP.txt"
        with open(fileMdp,'r') as MDP :
                     VmdpH =MDP.read()
                     if deletemdpHACHE == VmdpH :
                         with open(fileMdp,'w') as MDP :
                            MDP.truncate(0)

                            with open(filePin, 'w') as Pin:
                                Pin.truncate(0)
                            
                            rhasspy.text_to_speech("Your password has been succesfuly deleted")
                     else :
                         rhasspy.text_to_speech("You gave the wrong password")
                    



    elif command == "AddItem":

        filename = "list.txt"

        produit = "{}".format(intent["variables"]["produit"])
        nombre = "{}".format(intent["variables"]["nombre"])
        unite = "{}".format(intent["variables"]["unité"])

        with open(filename, 'a') as liste:
            liste.writelines("\n" + nombre + " " + unite + " de " + produit)

    elif command == "ReadList":

        filename = "list.txt"

        with open(filename, 'r') as liste:
            if os.stat(filename).st_size == 0:
                rhasspy.text_to_speech("Your shopping list is empty")
            else:
                rhasspy.text_to_speech(liste.read())

    elif command == "DeleteList":
        filename = "liste.txt"
        with open(filename, 'a') as liste:
            if os.stat(filename).st_size == 0:

                rhasspy.text_to_speech("Your shopping list is already empty")
            else:
                liste.truncate(0)
                rhasspy.text_to_speech("Your shopping list has been succesfuly deleted")

    elif command == "Flashlight":
        X = [255, 255, 255]
        flashlight =[
            X, X, X, X, X, X, X, X,
            X, X, X, X, X, X, X, X, 
            X, X, X, X, X, X, X, X, 
            X, X, X, X, X, X, X, X, 
            X, X, X, X, X, X, X, X, 
            X, X, X, X, X, X, X, X, 
            X, X, X, X, X, X, X, X, 
            X, X, X, X, X, X, X, X,
        ]
        sense.set_pixels(flashlight)

    elif command == "FlashlightOff":
        X = [0, 0, 0]
        flashlight =[
            X, X, X, X, X, X, X, X,
            X, X, X, X, X, X, X, X, 
            X, X, X, X, X, X, X, X, 
            X, X, X, X, X, X, X, X, 
            X, X, X, X, X, X, X, X, 
            X, X, X, X, X, X, X, X, 
            X, X, X, X, X, X, X, X, 
            X, X, X, X, X, X, X, X,
        ]
        sense.set_pixels(flashlight)

    elif commande == "FallDetected":
        global fall_detected 
        fall_detected = O
        while True:
            accelerometer = sense.get_accelerometer_raw().values()
            x = accelerometer[round('x')]
            y = accelerometer['y']
            z = accelerometer['z']

            if x < -1 :
                sense.show_message("Fall detected", text_colour = [255, 0, 0])
                rhasspy.text_to_speech("Fall detected")
                time.sleep(5)
                sense.show_message("Do you feel OK? Press the joystick to confirm", text_colour = [255, 0, 0])
                rhasspy.text_to_speech("Do you feel OK? Press the joystick to confirm")
                time.sleep(5)

                fall_detected += 1
                
                for event in sense.stick.get_events():
                    if event.action == "pressed" :
                        sense.show_message("You are fine", text_colour=[255, 0, 0])
                        rhasspy.text_to_speech("You are fine")
                    
                    else:
                        sense.show_message("Somebody call an ambulance!", text_colour = [255, 0, 0])
                        X = [255, 0, 0]
                        rhasspy.text_to_speech("Somebody call an ambulance!")

                        if event.action == "pressed":
                            break
            if x >= -1:
                break
    
    elif commande == "FallCount":
            sense.show_message("Number of falls:" + fall_detected, text_colour = [255, 0, 0])
            rhasspy.text_to_speech("The number of falls is" + fall_detected)