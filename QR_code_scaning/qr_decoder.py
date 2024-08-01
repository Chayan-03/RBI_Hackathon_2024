"""
import cv2
image_path = "Scripts/QR_code_scaning/Untitled 1.png"
def decode_qr_code(image_path):
    # Load the image
    img = cv2.imread(image_path)
    
    # Initialize the QRCode detector
    detector = cv2.QRCodeDetector()
    
    # Detect and decode the QR code
    data, vertices_array, _ = detector.detectAndDecode(img)
    
    if vertices_array is not None:
        # If a QR code is detected, return the data
        return data
    else:
        # If no QR code is detected
        return None
"""
"""
import cv2
 
image = cv2.imread('Scripts/QR_code_scaning/Untitled 1.png')
 
qrCodeDetector = cv2.QRCodeDetector()
 
decodedText, points, _ = qrCodeDetector.detectAndDecode(image)
 
if points is not None:
 
    nrOfPoints = len(points)
    print(nrofPoints)
    for i in range(nrOfPoints):
        nextPointIndex = (i+1) % nrOfPoints
        cv2.line(image, tuple(points[i][0]), tuple(points[nextPointIndex][0]), (255,0,0), 5)
 
    print(decodedText)    
 
    #cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
     
 
else:
    print("QR code not detected")
    """
import cv2
import os

# Define the image path
image_path = 'Untitled.png'

# Check if the file exists
if not os.path.exists(image_path):
    print(f"File not found: {image_path}")
else:
    # Load the image
    image = cv2.imread(image_path)

    # Check if the image is loaded correctly
    if image is None:
        print("Error: Image not loaded properly.")
    else:
        # Initialize the QR code detector
        qrCodeDetector = cv2.QRCodeDetector()

        # Detect and decode the QR code
        decodedText, points, _ = qrCodeDetector.detectAndDecode(image)

        if points is not None:
            points = points[0]  # Extract the points array from the nested array
            nrOfPoints = len(points)
            #print(nrOfPoints)
            for i in range(nrOfPoints):
                nextPointIndex = (i + 1) % nrOfPoints
                pt1 = (int(points[i][0]), int(points[i][1]))
                pt2 = (int(points[nextPointIndex][0]), int(points[nextPointIndex][1]))
                cv2.line(image, pt1, pt2, (255, 0, 0), 5)

            print(decodedText)

            # Display the image with detected QR code
            #cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("QR code not detected")
