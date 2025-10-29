import cv2
import os

def load_and_display_images(folder1, folder2):
    try:
        # Load images from cam1 folder
        cam1_images = [cv2.imread(os.path.join(folder1, img)) for img in os.listdir(folder1) if img.endswith('.jpeg')]
        
        # Load images from cam2 folder
        cam2_images = [cv2.imread(os.path.join(folder2, img)) for img in os.listdir(folder2) if img.endswith('.jpeg')]
        
        # Check if any images were loaded
        if not cam1_images:
            raise ValueError("No images found in cam1 folder.")
        if not cam2_images:
            raise ValueError("No images found in cam2 folder.")

        # Resize images to have the same height (assuming images have same height)
        max_height = max(img.shape[0] for img in cam1_images + cam2_images)
        cam1_images_resized = [cv2.resize(img, (int(img.shape[1]*max_height/img.shape[0]), max_height)) for img in cam1_images]
        cam2_images_resized = [cv2.resize(img, (int(img.shape[1]*max_height/img.shape[0]), max_height)) for img in cam2_images]

        # Stack images horizontally
        stacked_images = cv2.hconcat(cam1_images_resized + cam2_images_resized)

        # Display stacked images
        cv2.imshow('Stacked Images', stacked_images)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except FileNotFoundError:
        print("One or both folders not found.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print("An error occurred:", str(e))

# Example usage:
cam1_folder = 'cam1'
cam2_folder = 'cam2'
load_and_display_images(cam1_folder, cam2_folder)
