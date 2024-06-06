import PySimpleGUI as sg
import os
import subprocess

def convert_to_mp4(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', output_file]
    subprocess.run(command)

def download_youtube(link, destination, quality, window, progress_bar):
    base_command = ['yt-dlp', '-o', os.path.join(destination, '%(title)s.%(ext)s')]
    
    if quality == 'Highest Quality':
        command = base_command + ['-f', 'bestvideo+bestaudio', '--merge-output-format', 'mp4', link]
    elif quality == 'Medium Quality':
        command = base_command + ['-f', 'bestvideo[height<=720]+bestaudio', '--merge-output-format', 'mp4', link]
    elif quality == 'Lowest Quality':
        command = base_command + ['-f', 'worst', '--merge-output-format', 'mp4', link]
    else:  # No Video (MP3 only)
        command = base_command + ['-x', '--audio-format', 'mp3', link]

    subprocess.run(command)
    
    # Post-processing to ensure proper mp4 conversion
    if quality != 'No Video (MP3 Only)':
        downloaded_files = [f for f in os.listdir(destination) if f.endswith('.mp4')]
        for file in downloaded_files:
            input_file = os.path.join(destination, file)
            output_file = os.path.join(destination, os.path.splitext(file)[0] + '_converted.mp4')
            convert_to_mp4(input_file, output_file)
            os.remove(input_file)  # Remove the original file
            os.rename(output_file, input_file)  # Rename the converted file back to original name

    progress = 100
    window[progress_bar].update(progress)

# Custom color definitions
background_color = '#000000'
text_color = '#ffffff'  # White color
input_text_color = '#ffffff'  # White color for input text
button_color = ('black', '#00ffff')  # Text, Background
progress_bar_color = ('#f2f2f2', '#00ffff')  # (border_color, bar_color)

# Set the theme colors for the window
sg.theme('Dark')
sg.set_options(
    background_color=background_color,
    text_element_background_color=background_color,
    element_background_color=background_color,
    input_elements_background_color=background_color,  # Use background color for input elements
    progress_meter_color=progress_bar_color,
    button_color=button_color,
    text_color=text_color,
    input_text_color=input_text_color,
    scrollbar_color=None
)

# Define the layout of the GUI
layout = [
    [sg.Text('YouTube Link:', text_color=text_color), sg.InputText(key='YT_LINK', text_color=input_text_color, background_color=background_color)],
    [sg.Text('Destination Folder:', text_color=text_color), sg.InputText(key='DEST_FOLDER', text_color=input_text_color, background_color=background_color), sg.FolderBrowse(target='DEST_FOLDER', button_color=button_color)],
    [sg.Text('Quality:', text_color=text_color), sg.Combo(['Highest Quality', 'Medium Quality', 'Lowest Quality', 'No Video (MP3 Only)'], default_value='Highest Quality', key='QUALITY', text_color=input_text_color, background_color=background_color)],
    [sg.Button('Download', button_color=button_color), sg.Button('Exit', button_color=button_color)],
    [sg.Text('Progress:', text_color=text_color), sg.ProgressBar(max_value=100, orientation='h', size=(20, 20), key='progressbar', bar_color=progress_bar_color)]
]

# Create the window
window = sg.Window('YouTube Downloader', layout, grab_anywhere=True)

# Event loop to process events and get input values
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Download':
        link = values['YT_LINK']
        destination = values['DEST_FOLDER']
        quality = values['QUALITY']
        download_youtube(link, destination, quality, window, 'progressbar')

# Close the window
window.close()
