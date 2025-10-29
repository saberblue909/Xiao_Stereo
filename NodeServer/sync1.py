import os
from datetime import datetime

def find_closest_images(cam1_folder, cam2_folder, slop_ms=100):
    cam1_files = sorted(os.listdir(cam1_folder))
    cam2_files = sorted(os.listdir(cam2_folder))
    
    closest_pairs = []

    for cam1_file in cam1_files:
        cam1_timestamp = int(cam1_file.split('_')[1].split('.')[0])
        cam1_time = datetime.utcfromtimestamp(cam1_timestamp)
        
        closest_diff = float('inf')
        closest_cam2_file = None
        
        for cam2_file in cam2_files:
            cam2_timestamp = int(cam2_file.split('_')[1].split('.')[0])
            cam2_time = datetime.utcfromtimestamp(cam2_timestamp)
            
            time_diff = abs((cam1_time - cam2_time).total_seconds() * 1000)
            if time_diff <= slop_ms and time_diff < closest_diff:
                closest_diff = time_diff
                closest_cam2_file = cam2_file
        
        if closest_cam2_file:
            closest_pairs.append((cam1_file, closest_cam2_file))
    
    return closest_pairs

# Example usage:
cam1_folder = "/Users/isabelafaistauer/ThatProject/ESP32CAM_Projects/ESP32_CAM_LocalServer/NodeServer/images/cam1"
cam2_folder = "/Users/isabelafaistauer/ThatProject/ESP32CAM_Projects/ESP32_CAM_LocalServer/NodeServer/images/cam2"
closest_pairs = find_closest_images(cam1_folder, cam2_folder)

for cam1_file, cam2_file in closest_pairs:
    print(f"Closest pair: {cam1_file} and {cam2_file}")
