import tkinter as tk
from tkinter import simpledialog
import time
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
    popup = tk.Toplevel()
    popup.title('Log Your Activity')

    label = tk.Label(popup, text='Enter the Activity you have Done:')
    label.pack(padx=10, pady=10)

    entry = tk.Entry(popup)
    entry.pack(padx=10, pady=10)

    def on_submit():
        activity = entry.get()
        if activity.strip():
            log_activity(activity)
            popup.destroy()

    submit_btn = tk.Button(popup, text='Submit', command=on_submit)
    submit_btn.pack(padx=10, pady=10)

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