import cv2
import numpy as np

def test_image_format(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Check if the image is loaded successfully
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Check the format (shape and dtype)
    print(f"Image shape: {gray.shape}, dtype: {gray.dtype}")

    # Ensure it's an 8-bit grayscale image
    if gray.dtype != np.uint8:
        print("Warning: The image is not in 8-bit grayscale format. Converting...")
        gray = gray.astype(np.uint8)

    # Display the original and grayscale images
    cv2.imshow("Original Image", image)
    cv2.imshow("Grayscale Image", gray)
    
    # Wait for a key press and close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = 'A00147_front.jpg'  # Replace with the path to your image
test_image_format(image_path)
