from flask import Flask, request
import requests
import socket

# Retrieves the current IP Address of the RaspberryPi
import AI_Preprocessor
import SNConnector
from CarPickerAI import CarPickerAI


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    ipAddress = s.getsockname()[0]
    s.close()
    return ipAddress


SNConnector.updateIP("x_ntt47_genericcar_ai_server", getIP(), SNConnector.getAIServer())


# Defines and starts the webserver
def startWebserver():
    try:
        app = Flask(__name__)
        ai = CarPickerAI()

        @app.route('/predict_car', methods=['POST'])
        def predict_car():
            userID = request.args.get("userID")
            relationship = request.args.get("relationship")
            friends = AI_Preprocessor.convertStringToBoolean(request.args.get("friends"))
            hiking = AI_Preprocessor.convertStringToBoolean(request.args.get("hiking"))
            party = AI_Preprocessor.convertStringToBoolean(request.args.get("party"))
            city = AI_Preprocessor.convertStringToBoolean(request.args.get("city"))
            mountainbiking = AI_Preprocessor.convertStringToBoolean(request.args.get("mountainbiking"))
            skiing = AI_Preprocessor.convertStringToBoolean(request.args.get("skiing"))
            family = AI_Preprocessor.convertStringToBoolean(request.args.get("family"))
            dogs = AI_Preprocessor.convertStringToBoolean(request.args.get("dogs"))
            cars = AI_Preprocessor.convertStringToBoolean(request.args.get("cars"))
            shared_mobility = AI_Preprocessor.convertStringToBoolean(request.args.get("shared_mobility"))
            two_wheels = AI_Preprocessor.convertStringToBoolean(request.args.get("two_wheels"))
            style = int(request.args.get("style"))
            plan = int(request.args.get("plan"))
            budget = int(request.args.get("budget"))
            birthday = int(request.args.get("birthday"))
            yearly_drive = int(request.args.get("yearly_drive"))

            prediction = ai.predict(relationship, friends, hiking, party, city, mountainbiking, skiing, family, dogs, cars,
                                shared_mobility, two_wheels, style, plan, budget, birthday, yearly_drive)
            SNConnector.sendPredictionToInstance('x_ntt47_genericcar_survey_result', userID, prediction)

            return 'Success'

        # Starts the webserver
        if __name__ == '__main__':
            app.run(debug=False, host="0.0.0.0")

    # Stops the Server on Interrupt
    except KeyboardInterrupt:
        print("Keyboardinterrupt")
    finally:
        print("Cleaning...")


startWebserver()
