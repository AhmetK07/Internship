from fileinput import filename
import os
import glob
import shutil

src_folder = "/home/ahmet/Desktop/Ayvos_Assignment - I/AyvosAssignment-2/cornetto_ask_atesi_second/"
dst_folder = "/home/ahmet/Desktop/Ayvos_Assignment - I/AyvosAssignment-2/Destination//"

jpgPattern = "*.jpg"
jpgFiles = glob.glob(src_folder + jpgPattern , recursive=False)


for file in jpgFiles:

    file_name = file.split("/")[-1].split(".")[0] 
    print(file_name)
        
    if os.path.exists(src_folder+ file_name + ".json"):

        continue  
    else:
        shutil.move(file, dst_folder + file_name + ".jpg")
        print('Moved:', file)