from tkinter import filedialog
import tkinter as tk
import streamlit as st
import os

st.set_page_config(
    page_title="Spotify Downloader",
    page_icon=":shark:",
    menu_items={
        'About': "# This is a header. This is an *extremely* cool app!",
        'Get Help': 'https://portfolio.denvernoell.com',
        'Report a bug': "https://denvernoell.com/unit-convertor",
    })

st.title('Spotify Downloader')


# import libraries

# Set up tkinter
root = tk.Tk()
root.withdraw()

# Make folder picker dialog appear on top of other windows
root.wm_attributes('-topmost', 1)

# Folder picker button
# st.title('Folder Picker')
# st.write('Please select a folder:')

# if st.button('Folder Picker'):
#     dirname = st.text_input(
#         'Selected folder:', filedialog.askdirectory(master=root))
URI = st.text_input('URI')

if st.button('Download'):
    dirname = st.text_input(
        'Selected folder:', filedialog.askdirectory(master=root))

    # F = st.file_uploader('Folder')

    os.system(f"cd {dirname}")

    # os.system(f"spotdl {URI}"
    #           + r" --ffmpeg C:\Users\dnoell\Documents\ShareX\Tools\ffmpeg.exe")
    os.system(f"spotdl {URI}")
    #   + r" --ffmpeg C:\Users\dnoell\Documents\ShareX\Tools\ffmpeg.exe")
    #       " --path-template '{artist}/{album}/{title}.{ext}'"
    st.success("Downloaded")
