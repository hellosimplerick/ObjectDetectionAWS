""" test """
import io
from PIL import Image, ImageDraw, ImageFont
import boto3

def draw_bounding_boxes(image_path):
    """
    Detects objects in an image file and draws bounding boxes and labels around them.
    """
    # Initialize the AWS Rekognition client
    rekognition = boto3.client('rekognition', region_name='us-east-1')

    # Load the image from the given path
    with open(image_path, 'rb') as image_file:
        source_bytes = image_file.read()

    # Detect objects in the image
    detect_objects = rekognition.detect_labels(Image={'Bytes': source_bytes})

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
    points = [(left, top), (left + width, top), (
        left + width, top + height), (left, top + height), (left, top)]
    draw.line(points, width=5, fill="#69f5d9")

    # Draw rectangle for the label's background
    shape = [(left - 2, top - 35), (left + width + 2, top)]
    draw.rectangle(shape, fill="#69f5d9")

    # Load font and draw label
    font = ImageFont.truetype("arial.ttf", 30)
    draw.text((left + 6, top - 30), label, font=font, fill='#000000')

# Replace 'rome.jpg' with the path to your image file
draw_bounding_boxes('rome.jpg')
