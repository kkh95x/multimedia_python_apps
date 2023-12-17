import cv2
import numpy as np
import matplotlib.pyplot as plt

def polar_to_cartesian(theta, a, b, k):
    r = np.sin(k * theta)
    x = a * r * np.cos(theta)
    y = b * r * np.sin(theta)
    return x, y

def rotate_image(image, angle):
    center = tuple(np.array(image.shape[1::-1]) / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return rotated_image

img_size = 500
img = np.zeros((img_size, img_size, 3), dtype=np.uint8)

# Set parameters for the rose curve
a = 8
b = 5
k = 7

# Set rotation angle increment
rotation_angle = 1

num_frames = 360
output_file = 'rotating_rose_animation.mp4'

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, 30.0, (img_size, img_size))

# Generate and save frames for the animation
for frame in range(num_frames):
    # Draw the rose curve
    theta_values = np.linspace(0, 2 * np.pi, 1000)
    x_values, y_values = polar_to_cartesian(theta_values, a, b, k)

    # Scale and translate the curve to fit the image
    x_values = (x_values + max(x_values)) * (img_size / (2 * max(x_values)))
    y_values = (y_values + max(y_values)) * (img_size / (2 * max(y_values)))

    # Convert to integer coordinates
    points = np.array(list(zip(x_values.astype(int), y_values.astype(int))), np.int32)
    points = points.reshape((-1, 1, 2))

    # Draw the rose on the image
    img.fill(0)
    cv2.polylines(img, [points], isClosed=False, color=(0, 0, 255), thickness=2)

    # Rotate the image for the current frame
    rotated_img = rotate_image(img, frame * rotation_angle)

    # Write the frame to the video file
    video_writer.write(rotated_img)

# Release the VideoWriter object
video_writer.release()
cv2.destroyAllWindows()
