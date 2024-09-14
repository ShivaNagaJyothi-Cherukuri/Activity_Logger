import tkinter as tk
from tkinter import simpledialog
from tkinter import PhotoImage
import time
from datetime import datetime, timedelta
from playsound import playsound
import sqlite3
import threading

# database setup
def db_setup():
    conn = sqlite3.connect('data/activity_logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            activity TEXT
        )
    ''')
    conn.commit()
    return conn,cursor

# logging the activity to the Database
def log_activity(activity):
    cursor.execute('INSERT INTO activity_logs (activity) VALUES (?)', (activity,))
    conn.commit()
    print(f'Logged activity: {activity}')

# play notification sound
def play_notification_sound():
    playsound('sounds/notification_sound.mp3')

# creating a pop up window for entering the activity using Tkinter
def popup_window():

    # Calculating current time and previous hour time
    now = datetime.now()
    previous_hour = now - timedelta(hours=1)
    current_time_str = now.strftime('%Y-%m-%d %H:%M:%S')
    previous_hour_str = previous_hour.strftime('%H:%M:%S')
    
    # Creating the popup window
    popup = tk.Toplevel()
    popup.title('Log Your Activity')

    # Set window size and background color
    popup.geometry('300x200')  # Width x Height
    popup.configure(bg='#f0f0f0')  # Light gray background

     # Add a frame to organize widgets
    frame = tk.Frame(popup, bg='#f0f0f0')
    frame.pack(padx=20, pady=20, expand=True)

    # Displaying the current date and time at the top
    time_label = tk.Label(frame, text=f'Current Time: {current_time_str}',
                          font=('Helvetica', 18, 'bold'),
                          bg='#f0f0f0',
                          fg='#333333')  # Dark gray text
    time_label.pack(pady=(0, 20))

    # Add an image to the frame
    img = PhotoImage(file='time_track.png')  # image path
    img_label = tk.Label(frame, image=img, bg='#f0f0f0')
    img_label.image = img  # Keeping a reference to avoid garbage collection
    img_label.pack(pady=(0, 10))

    # Adding a label with custom font and color
    label = tk.Label(frame, text=f'Enter the Activity you have Done (from {previous_hour_str}):', 
                     font=('Helvetica', 12, 'bold'),
                     bg='#f0f0f0',
                     fg='#333333')  # Dark gray text
    label.pack(pady=(0,10)) # bottom padding

    # Adding an entry widget for user input
    entry = tk.Entry(frame,
                     font=('Helvetica', 12),
                     width=30)
    entry.pack(pady=(0, 20))  # Add bottom padding

    # Function to handle submit button click
    def on_submit(entry, popup):
        activity = entry.get()
        if activity.strip():
            log_activity(activity)
        popup.destroy()

     # Adding a submit button with custom style
    submit_btn = tk.Button(frame,
                           text='Submit',
                           font=('Helvetica', 12, 'bold'),
                           bg='#4CAF50',  # Green background
                           fg='#FFFFFF',  # White text
                           relief='raised',
                           command=lambda: on_submit(entry, popup))
    submit_btn.pack()

# Timer function to wait and trigger notifications
def timer():
    while True:
        play_notification_sound()
        # Run the popup window in the Tkinter main loop
        root.after(0,popup_window)
        # Calculate time to wait until the next hour
        seconds_to_next_hour = 3600 - time.time() % 3600
        time.sleep(seconds_to_next_hour)

# main function to run the application
def main():
    global conn, cursor
    conn, cursor = db_setup()

    global root

    root = tk.Tk()
    root.withdraw() #hides the root window

    try:
        # Starting the timer in a separate thread
        timer_thread = threading.Thread(target=timer, daemon=True)
        timer_thread.start()
        # Keeping the main thread running to allow Tkinter to operate
        root.mainloop()
    except KeyboardInterrupt:
        print('Application Interrupted and Stopped.')
    finally:
        conn.close()

if __name__ =="__main__":
    main()