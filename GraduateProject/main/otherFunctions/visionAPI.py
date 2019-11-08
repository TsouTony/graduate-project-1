import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from .setPath import imgDirectoryPath

def getLabel(imgPath):
	imgPath = os.path.join(os.path.abspath(os.path.join(os.getcwd(),"media")),imgPath)
	# Instantiates a client
	client = vision.ImageAnnotatorClient()

	# The name of the image file to annotate
	file_name = os.path.abspath(imgPath)

	# Loads the image into memory
	with io.open(file_name, 'rb') as image_file:
	    content = image_file.read()

	image = types.Image(content=content)

	# Performs label detection on the image file
	response = client.label_detection(image=image)
	labels = response.label_annotations

	labelsList = []
	print('Labels:')
	for label in labels:
	    print(label.description)
	    labelsList.append(label.description)
	return labelsList
