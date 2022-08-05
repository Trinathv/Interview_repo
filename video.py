#!/usr/bin/env python
# coding: utf-8

# In[1]:


#try:
    #from moviepy.editor import VideoFileClip
#except:
    #get_ipython().system('pip install -q moviepy')


# In[1]:


# creating the video clips
import time
from datetime import datetime, timedelta
from moviepy.editor import *

os.makedirs('video_clips', exist_ok=True)
# loading video
video = 'test.mp4'
clip = VideoFileClip(video)

count = 0
while 1:
    print(count)
    # getting only 60 seconds
    sub_clip = clip.subclip(count, 60 + count)
    # saving the clips
    sub_clip.write_videofile(verbose=False, audio=False, logger=None, filename=f"./video_clips/clip_{count}.mp4")
    count = count + 60
    if (60 + count) > clip.duration:
        break


# In[2]:


from moviepy.editor import VideoFileClip
import os
import datetime
import pandas as pd


d = []
video_path = 'video_clips/'
for i in os.listdir(video_path):
    if i.endswith(('.mp4', '.mov')):
        d.append((
                  i.split('.')[0],
                  i.split('.')[-1],
                  VideoFileClip(video_path + i).duration,
                  os.path.abspath(video_path + i),
                  datetime.datetime.now()
                 ))

# create dataframe
columns=['clip_name', 'clip_file_extension', 'clip_duration', 'clip_location', 'insert_timestamp']
video_data = pd.DataFrame(d, columns=columns[0:5])
video_data


# In[3]:


os.makedirs('./report', exist_ok=True)
video_data.to_csv('./report/generated_video_files.csv')


# In[4]:


import pandas as pd

## connect to database
import sqlite3

conn = sqlite3.connect("pythonsqlite.db")

##push the dataframe to sql
video_data.to_sql("video_data", conn, if_exists="replace")

##create the table
conn.execute(
    """
    create table IF NOT EXISTS video_table as 
    select * from video_data
    """)


# In[5]:


cur = conn.cursor()
cur.execute('select * from video_data;')
cur.fetchall()


# In[6]:


for i in cur.execute('select * from video_data;'):
    print(i)


# In[7]:


conn.close()


# In[ ]:




