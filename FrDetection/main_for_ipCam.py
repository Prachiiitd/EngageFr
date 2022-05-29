import asyncio
import sys

import requests
from faceRecognition import faceRec, getIps, clearIPS
from faceDetector import get_face_detector, find_faces, draw_faces
import numpy as np
import imutils
from io import BytesIO
import cv2

face_model = get_face_detector()


class VideoStream:
	def __init__(self, _url, _add):
		"""
			Initialize the camera stream object
			:param _url: url of the camera
			:param _add: address of the camera
		"""

		self.url = _url
		self.address = _add

	def getResponse(self):
		"""
			Get the response of the camera
			:return: image response
		"""
		try:  # get the response of the camera and convert it to numpy array format for further processing.
			img_resp = requests.get(self.url)  # get the response of the camera
			img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)  # convert the response to numpy array
			img = cv2.imdecode(img_arr, -1)  # convert the numpy array to image
			img = imutils.resize(img, width=400, height=800)  # resize the image

			faces = find_faces(img, face_model)  # find the faces in the image
			ret, faces = draw_faces(img, faces)  # check if the image have faces

			if ret:  # check if the image have faces:
				try:
					faceRec(BytesIO(faces), self.address)
				except Exception as e:
					print(e)

			else:  # if the image have no faces, print the message
				print("No faces found in the image:", self.address)

			cv2.imshow(self.url, img)  # show the image

		except Exception as er:  # if the image could not be processed, raise the error.
			raise er  # raise the error

	async def getStream(self):
		"""
			Asynchronous function to get the stream of the camera
			:return: None
		"""
		# If image response is received, print the camera in use and process images from the camera
		print("Using CameraIP:-", self.url, "with address:-", self.address)  # print the camera ip and address

		try:  # try to process the image from the camera
			while True:
				self.getResponse()  # invoke the getResponse function to process the image from the camera par
				await asyncio.sleep(0.00000000000000000000000000000001)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break  # if the user presses q, break the loop

		except Exception as er:  # if the image could not be processed, print and raise the error.
			print("Could not get image response for CameraId:-", self.address, er)
			raise er  # raise the error


def main():
	# urls = ["http://192.168.16.122:8080/shot.jpg", "http://192.168.156.122:8080/shot.jpg"]
	# add = ""

	cameraIp = getIps()
	if len(cameraIp) == 0:
		print("No Camera IPs found")
		sys.exit(0)

	loop = asyncio.get_event_loop()

	try:
		resp = None
		for ip in cameraIp:
			add, ipAdd = ip
			url = f"http://{ipAdd}/shot.jpg"
			try:
				resp = requests.get(url, timeout=10)
				stream = VideoStream(url, add)
				asyncio.ensure_future(stream.getStream())
			except Exception as er:
				print("Camera not found:-", url, er)
				continue

		if resp is not None:
			loop.run_forever()

	except (KeyboardInterrupt, Exception) as er:
		print("Shutdown requested...exiting")
		raise er

	finally:
		loop.close()  # close the loop
		s = input("Clear the IPs(Y/n):-").lower()
		if s == 'y':
			clearIPS()  # clear the camera ip list
		print("Shutdown ...exiting")
		sys.exit(0)  # exit the program


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(e)
		sys.exit(0)
