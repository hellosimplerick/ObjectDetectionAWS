"""
S3 version of the kid's code
"""

import io
from PIL import Image, ImageDraw, ImageFont
import boto3

def draw_bounding_boxes(bucket_name, image_key):
    """
    Detects objects in an image stored in an S3 bucket and
    draws bounding boxes and labels around them.
    """
    # Initialize AWS clients for Rekognition and S3
    rekognition = boto3.client('rekognition', region_name='us-east-1')
    s3 = boto3.client('s3')

    # Retrieve the image from S3
    s3_response = s3.get_object(Bucket=bucket_name, Key=image_key)
    source_bytes = s3_response['Body'].read()

    # Detect objects in the image using Rekognition
    detect_objects = rekognition.detect_labels(Image=
                     {'S3Object': {'Bucket': bucket_name, 'Name': image_key}})

    # Load the image for drawing
    image = Image.open(io.BytesIO(source_bytes))
    draw = ImageDraw.Draw(image)

    # Loop through detected labels to draw bounding boxes
    for label in detect_objects['Labels']:
        print(label["Name"], "Confidence:", label["Confidence"])

        for instance in label['Instances']:
            if 'BoundingBox' in instance:
                box = instance["BoundingBox"]
                draw_box(draw, box, image.width, image.height, label["Name"])

    # Display the image
    image.show()

def draw_box(draw, box, image_width, image_height, label):
    """
    Draws a single bounding box around a detected object.
    """
    left = image_width * box['Left']
    top = image_height * box['Top']
    width = image_width * box['Width']
    height = image_height * box['Height']

    # Define the four corners of the bounding box
    points = [(left, top), (left + width, top),
              (left + width, top + height), (left, top + height), (left, top)]
    draw.line(points, width=5, fill="#69f5d9")

    # Draw rectangle for the label's background
    shape = [(left - 2, top - 35), (left + width + 2, top)]
    draw.rectangle(shape, fill="#69f5d9")

    # Load font and draw label
    font = ImageFont.truetype("arial.ttf", 30)
    draw.text((left + 6, top - 30), label, font=font, fill='#000000')

# Specify the S3 bucket and image key
BUCKET_NAME = 'mlptestcanada'
IMAGE_KEY = 'chrisson.JPG'

draw_bounding_boxes(BUCKET_NAME, IMAGE_KEY)
