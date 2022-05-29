from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import pyodbc
from datetime import datetime
import json

"""
    credential: Stores credentials for azure face api and database
    face_client: Stores the client for azure face api
    db: Stores the connection to the database
    connctStr: Stores the connection string for the database

    *NOTE: The credentials are stored in the credentials.json file
    Face API: https://docs.microsoft.com/en-us/azure/cognitive-services/face/
    Database: https://docs.microsoft.com/en-us/azure/sql-database/sql-database-python-getstarted

    API_KEY: Stores the API key for azure face api
    ENDPOINT: Stores the endpoint for azure face api

    server: Stores the server name for the database
    host: Stores the host for the database
    database: Stores the database name for the database
    user: Stores the user for the database
    password: Stores the password for the mssql database
    driver: Stores the odbc driver for the mssql database
"""

credential = json.load(open('AzureCloudKeys.json'))  # load the keys from AzureCloudKeys.json

API_KEY = credential['API_KEY']  # replace with your own key
ENDPOINT = credential['ENDPOINT']  # replace with your own key

server = credential['server']  # replace with your own key
database = credential['database']  # replace with your own key
username = credential['username']  # replace with your own key
password = credential['password']  # replace with your own key
driver = credential['driver']  # replace with your own key
host = credential['host']  # replace with your own key

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

connectStr = f'DRIVER={driver}; SERVER={server}; DATABASE={database}; UID={username}; PWD={password}'
db = pyodbc.connect(connectStr)


def execute(query, read=False):
    """
    Executes a query on the database
    :param query: The query to be executed
    :param read: If the query is a read query or not
    :return: The result of the query
    """
    try:  # try to execute the query
        res = "Updated"  # default result

        cursor = db.cursor()  # create a cursor for the database.
        cursor.execute(query)  # execute the query on the database

        if read:  # if the query is a read query then fetch the result and store for returning later.
            res = cursor.fetchall()  # fetch the result from the database and store it for returning later.

        db.commit()  # commit the changes to the database.
        cursor.close()  # close the cursor.
        return res  # return the result.

    except pyodbc.Error as err:  # if an error occurs then print the error and return None.
        print(err)  # print the error.
        return None  # return None.


def clearIPS():
    """
    DELETE all the cameraIp from database.
    :return: None
    """

    query = "DELETE FROM CameraIP"  # query to delete all the cameraIp from the database.
    execute(query)  # execute the query.


def getIps():
    """
    Gets the ip addresses of the devices that are connected to the network and
     stores them in a list called ips and returns it.
    :return: The list of ip addresses of the devices that are stored in the database.
    """

    query = "SELECT address, ipaddress FROM CameraIP"  # query to get the ip addresses of the devices.
    ips = execute(query, read=True)  # execute the query and store the result in ips.
    return ips  # return the list of ip addresses.


def knownFace():
    """
    Gets the face ids of the known faces and the app ids of the known faces and returns them.
    :return: The face ids and the app ids of the known faces.
    """

    query = "SELECT appId, images FROM Application"  # query to get the face ids and the app ids of the known faces.
    applications = execute(query, read=True)  # execute the query and store the result in applications.
    faceEncodings = []  # create a list to store the face encodings of the known faces.
    appId = []  # create a list to store the app ids of the known faces.

    for app in applications:  # for each application in the list of applications
        _appId = app[0]  # store the app id of the application in _appId
        image = host + app[1]  # store the image of the application in image

        source_face = face_client.face.detect_with_url(  # detect the face in the image
            url=image,  # store the image in the url
            detection_model='detection_03',   # use detection_03 model
            recognition_model='recognition_04'  # use recognition_04 model
        )

        # append the face id of the face in the image to the list of face encodings.
        faceEncodings.append(source_face[0].face_id)
        appId.append(_appId)  # append the app id of the face in the image to the list of app ids.

    return faceEncodings, appId  # return the list of face encodings and the list of app ids.


def updateDatabase(face_id, address):  # update the database with the face id and the address of the device.
    """
    Updates the database with the face id and the address of the device.
    :param face_id: The face id of the face in the image.
    :param address: The address of the device.
    :return: None
    """

    # query to update the database with the face id and the address of the device.
    query = f"""UPDATE Application SET found = 'true', lastTrackDate='{datetime.now()}',
                lastTrackLoc='{address}' WHERE appId = {face_id};"""
    print(query)  # print the query to the console.
    execute(query)  # execute the query.


def faceRec(stream, address):
    """
    Detects the face in the image and updates the database if the face is found.
    :param stream: The image stream of the device.
    :param address: The address of the device.
    :return: None
    """
    sourceFaceIds, appId = knownFace()  # get the face ids and the app ids of the known faces.

    detectionImageFaces = face_client.face.detect_with_stream( # detect the face in the image
        image=stream,  # store the image in the image
        detection_model='detection_03',  # use detection_03 model
        recognition_model='recognition_04'  # use recognition_04 model
    )
    print("detectionImageFaces", detectionImageFaces)  # print the detectionImageFaces to the console.

    if len(detectionImageFaces) == 0:  # if no face is detected then return.
        print("No face detected")  # print the message to the console.
        print()
        return

    detectionFaceIds = [face.face_id for face in detectionImageFaces]  # get the face ids of the faces in the image.
    print("sourceFaceId: ", sourceFaceIds)  # print the sourceFaceIds to the console.
    print("detectionFaceIds", detectionFaceIds)  # print the detectionFaceIds to the console.

    # check if the face in the image is in the list of known faces and if it is then update the database.
    for sourceFaceId in sourceFaceIds:  # for each sourceFaceId in the list of sourceFaceIds
        matchedFaces = face_client.face.find_similar(
            face_id=sourceFaceId,  # store the sourceFaceId in the face_id
            face_ids=detectionFaceIds  # store the detectionFaceIds in the face_ids
        )

        if len(matchedFaces) > 0:  # if there is a match then update the database.
            matchedFace = matchedFaces[0]  # store the matched face in the matchedFace
            if matchedFace.confidence > 0.7:  # if the confidence of the match is greater than 0.7 then update the database.
                print("Matched face: ", matchedFace)  # print the matched face to the console.
                resIndex = sourceFaceIds.index(sourceFaceId) # get the index of the matched face in the list of known faces.
                matchedAppId = appId[resIndex]  # get the app id of the matched face.
                updateDatabase(matchedAppId, address)  # update the database with the matched face id and the address of the device.
                print("Matched AppId: ", matchedAppId)  # print the matched app id to the console.
                print()
                return

    print("No face matched")  # print the message to the console.
    print()
    return  # return.


if __name__ == "__main__":
    query = "SELECT * FROM Customer"  # query to get all the applications in the database.
    customers = execute(query, read=True)  # execute the query and store the result in customers.
    print(customers)  # print the customers to the console.
