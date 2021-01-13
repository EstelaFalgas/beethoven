import music21 as m21
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import zipfile
import seaborn as sns
import os


#All our data is in a folder called beethoven. This folder contains different folders for each composition category (canons, sonatas...) and inside these we have zip files.

#unzipping all files

for dirname, _, filenames in os.walk("beethoven"):
    for filename in filenames:
        file = (os.path.join(dirname, filename))
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall("unzipped") #droping into folder called unzipped


#unzipping we see we have unwanted files and our wanted midi files thus we filter the data to get only the midi files and save them in a new folder.

#extracting ALL midis from unzipped files
import shutil
for dirname, _, filenames in os.walk("unzipped"):
        for filename in filenames:
            file = (os.path.join(dirname, filename))
            if "mid" in file:
                shutil.copy2(file, "beethoven_allMIDIS") #droping into folder called "bethoven_allMIDIS"


#TO COUNT THE TOTAL NUMBER OF COMPOSITIONS WE HAVE: 1230
count=0
for dirname, _, filenames in os.walk("beethoven_allMIDIS"):
        for filename in filenames:
            count+=1
print(count)


#we now prefer to extract midis by category, so we start by unzipping again by folder and then putting midis into different folders, according to the folder they where extracted from.  
#canons --> canons_midis, chamber_music---> chamber_music_midis, ...


#creating a list of folder names to later get . 

beet_file_list=[]
for dirname, _, filenames in os.walk("beethoven"):
    for i in _:
        beet_file_list.append(i)


#unzipping and extracting midis by folder. droping into respective new folder.

for i in beet_file_list:
    for dirname, _, filenames in os.walk("beethoven"):
        for filename in filenames:
            file = (os.path.join(dirname, filename))
            if i in file:
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall("unZ")

    for dirname, _, filenames in os.walk("unZ"):
        for filename in filenames:
            file = (os.path.join(dirname, filename))
            if "mid" in file:
                shutil.move(file, f"beethoven_MIDIS\\{i}_midis")  


#This is only to be run once as if it tries to move the midi files to the folder specified where they already exist it will raise an error.



