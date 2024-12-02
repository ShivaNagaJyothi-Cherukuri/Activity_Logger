import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import pygame
import mysql.connector
import threading
import time
from datetime import datetime, timedelta

# Global variables for time range
start_time = datetime.strptime('12:00 AM', '%I:%M %p').time()
end_time = datetime.strptime('11:59 PM', '%I:%M %p').time()

def db_setup():
    """Set up the database and create the activity_logs table if it doesn't exist."""
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='qaz123',
        database='activity_logger'
    )
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS activity_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Log_day VARCHAR(20),
        Log_date DATE,
        Log_hour VARCHAR(10),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        activity TEXT
    )''')
    conn.commit()
    return conn, cursor

def log_activity(conn, cursor, activity):
    """Log the activity to the database."""
    now = datetime.now()
    Log_day = now.strftime('%A')
    Log_date = now.strftime('%Y-%m-%d')
    Log_hour = now.strftime('%I:%M %p')

    try:
        cursor.execute('''
            INSERT INTO activity_logs (Log_day, Log_date, Log_hour, activity)
            VALUES (%s, %s, %s, %s)
        ''', (Log_day, Log_date, Log_hour, activity))
        conn.commit()
        print(f'Logged activity: {activity}')
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

def play_notification_sound():
    """Play the notification sound in a separate thread."""
    def play_sound():
        try:
            pygame.mixer.init()
            pygame.mixer.music.load('sounds/notification_sound.mp3')
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing sound: {e}")

    sound_thread = threading.Thread(target=play_sound, daemon=True)
    sound_thread.start()

def get_time_range():
    """Prompt the user to enter the start and end times."""
    global start_time, end_time

    time_window = tk.Tk()
    time_window.withdraw()  # Hide the main window

    start_time_str = simpledialog.askstring("Start Time", "Enter start time (HH:MM AM/PM):")
    end_time_str = simpledialog.askstring("End Time", "Enter end time (HH:MM AM/PM):")
    
    try:
        start_time = datetime.strptime(start_time_str, '%I:%M %p').time()
        end_time = datetime.strptime(end_time_str, '%I:%M %p').time()
    except ValueError:
        print("Invalid time format. Use HH:MM AM/PM.")
        time_window.destroy()
        exit()

    time_window.destroy()

def popup_window(conn, cursor):
    """Create a popup window for entering the activity."""
    now = datetime.now()
    previous_hour = now - timedelta(hours=1)
    current_time_str = now.strftime('%Y-%m-%d %I:%M %p')
    current_day = now.strftime('%A')
    current_date = now.strftime('%Y-%m-%d')
    current_hour = now.strftime('%I:%M %p')
    previous_hour_str = previous_hour.strftime('%I:%M %p')

    popup = tk.Toplevel()
    popup.title('Log Your Activity')
    popup.geometry('300x300')  # Increased height for better layout
    popup.configure(bg='#f0f0f0')

    frame = tk.Frame(popup, bg='#f0f0f0')
    frame.pack(padx=20, pady=20, expand=True)

    time_label = tk.Label(frame, text=f'{current_date} - {current_day} \n {current_hour}',
                          font=('Helvetica', 18, 'bold'),
                          bg='#f0f0f0',
                          fg='#333333')
    time_label.pack(pady=(0, 20))

    img_path = 'Track_image.png'
    try:
        img = Image.open(img_path)
        img = img.resize((300, 300), Image.LANCZOS)  # Adjusted size for better layout
        img_tk = ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image: {e}")
        img_tk = None

    if img_tk:
        img_label = tk.Label(frame, image=img_tk, bg='#f0f0f0')
        img_label.image = img_tk
        img_label.pack(pady=(0, 10))
    else:
        tk.Label(frame, text="Failed to load image", bg='#f0f0f0').pack(pady=(0, 10))

    label = tk.Label(frame, text=f'Enter the Activity you have Done (from {previous_hour_str} to {current_hour}):', 
                     font=('Helvetica', 12, 'bold'),
                     bg='#f0f0f0',
                     fg='#333333')
    label.pack(pady=(0, 10))

    entry = tk.Entry(frame,
                     font=('Helvetica', 12),
                     width=30)
    entry.pack(pady=(0, 20))

    def on_submit():
        activity = entry.get()
        if activity.strip():
            log_activity(conn, cursor, activity)
        popup.destroy()

    submit_btn = tk.Button(frame,
                           text='Submit',
                           font=('Helvetica', 12, 'bold'),
                           bg='#4CAF50',
                           fg='#FFFFFF',
                           relief='raised',
                           command=on_submit)
    submit_btn.pack()

    popup.protocol('WM_DELETE_WINDOW', lambda: (popup.destroy(), root.quit()))

def timer(conn, cursor):
    """Timer function to wait and trigger notifications."""
    now = datetime.now()
    
    # Combine the current date with the provided start time
    start_time_today = datetime.combine(now.date(), start_time)
    end_time_today = datetime.combine(now.date(), end_time)
    
    # If the current time is already past the start time, schedule the first notification one hour later
    if now.time() >= start_time:
        next_notification_time = start_time_today + timedelta(hours=1)
    else:
        # If the current time is before the start time, wait until the start time
        next_notification_time = start_time_today
    
    while True:
        now = datetime.now()
        current_time = now.time()

        # Check if the current time is after the end time and exit the loop
        if now >= end_time_today:
            # Trigger one last notification exactly at end_time
            if now <= end_time_today + timedelta(minutes=1):  # Allow small delay margin
                play_notification_sound()
                root.after(0, lambda: popup_window(conn, cursor))  # Show the popup window

            print("End time reached. Exiting program.")
            root.quit() # Stop the Tkinter event loop
            break  # Exit the loop and end the program
        
        # Check if current time is within the specified range
        if start_time <= current_time <= end_time:
            # Check if it's time for the next notification
            if now >= next_notification_time:
                play_notification_sound()
                root.after(0, lambda: popup_window(conn, cursor))  # Show the popup window from main thread

                # Schedule the next notification one hour from the current notification time
                next_notification_time += timedelta(hours=1)
        
        # Calculate time to wait until the next notification
        time_to_next_notification = max((next_notification_time - now).total_seconds(), 0)
        print(f"Sleeping for {time_to_next_notification} seconds until the next notification...")
        time.sleep(time_to_next_notification)

def main():
    global root

    conn, cursor = db_setup()
    get_time_range()

    root = tk.Tk()
    root.withdraw()  # Hide the root window

    try:
        timer_thread = threading.Thread(target=lambda: timer(conn, cursor), daemon=True)
        timer_thread.start()
        root.mainloop()
    except KeyboardInterrupt:
        print('Application Interrupted and Stopped.')
    finally:
        conn.close()
        root.quit()

if __name__ == "__main__":
    main()
