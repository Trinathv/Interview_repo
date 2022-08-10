#!/usr/bin/env py

#
import time
from datetime import datetime, timedelta
#!pip install moviepy
from moviepy.editor import *
from moviepy.editor import VideoFileClip
import os
import datetime
import pandas as pd

os.makedirs('video_clips', exist_ok=True)
# loading the input  video file that needs to be split
# Goal: Split the intput video file into chunks.
video_input = 'test.mp4'
clip = VideoFileClip(video_input)

count = 0
#while 1:
while 1 < count:
    print(count)
    # getting only 60 seconds
    sub_clip = clip.subclip(count, 60 + count)
    # saving the clips
    sub_clip.write_videofile(verbose=False, audio=False, logger=None, filename=f"./video_clips/clip_{count}.mp4")
    count = count + 60
    #Exit condition:
    if (60 + count) > clip.duration:
        break

# Generate the CSV file. Input: All the files in folder 'video_clips/'
d = []
video_path = 'video_clips/'
for i in os.listdir(video_path):
    if i.endswith(('.mp4', '.mov')):
        #Sample Output:
        # i.split('.')[0]  :: clip_180
        # i.split('.')[-1] :: mp4
        d.append((
                  i.split('.')[0], #clip_180.mp4 -> clip_180
                  i.split('.')[1], #clip_180.mp4 -> .mp4
                  #Get the duration for the specific clip
                  VideoFileClip(video_path + i).duration, #video_clips/Users/trinathvemula/PycharmProjects/video/video_clips/clip_180.mp4'
                  os.path.abspath(video_path + i),
                  datetime.datetime.now()
                 ))

# create dataframe
columns=['clip_name', 'clip_file_extension', 'clip_duration', 'clip_location', 'insert_timestamp']
video_data = pd.DataFrame(d, columns=columns[0:5])
print(video_data)


# In[3]:


os.makedirs('./report', exist_ok=True)
#using pandas df, write as csv into a file
video_data.to_csv('./report/generated_video_files.csv')


# In[4]:


import pandas as pd

## connect to database
import sqlite3

#Connect to the default in memory database (used by c, pandas)
conn = sqlite3.connect("pythonsqlite.db")

##push the dataframe to sql
#Save the df to the context 'conn'. similar to insert
video_data.to_sql("video_data", conn, if_exists="replace")

##create the table
conn.execute(
    """
    create table IF NOT EXISTS video_table as 
    select * from video_data
    """)

cur = conn.cursor()
#Select rows from the in memory table
cur.execute('select * from video_data;')
cur.fetchall()

for i in cur.execute('select * from video_data;'):
    print(i)

conn.close()




