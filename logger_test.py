import tkinter as tk
from tkinter import PhotoImage
from tkinter import simpledialog
from PIL import Image, ImageTk
import time
from datetime import datetime, timedelta
from playsound import playsound
import mysql.connector
import threading

# Initialize global variables
start_time = datetime.strptime('12:00 AM', '%I:%M %p').time()
end_time = datetime.strptime('11:59 PM', '%I:%M %p').time()

# database setup
def db_setup():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='qaz123',
        database='activity_logger'
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Log_day VARCHAR(20),
            Log_date DATE,
            Log_hour VARCHAR(10),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            activity TEXT
        )
    ''')
    conn.commit()
    return conn,cursor

# logging the activity to the Database
def log_activity(activity):
    now = datetime.now()
    Log_day = now.strftime('%A')
    Log_date = now.strftime('%Y-%m-%d')
    Log_hour = now.strftime('%I:%M %p')

    cursor.execute('''
        INSERT INTO activity_logs (Log_day, Log_date, Log_hour, activity)
        VALUES (%s, %s, %s, %s)
    ''', (Log_day, Log_date, Log_hour, activity))
    conn.commit()
    print(f'Logged activity: {activity}')

# play notification sound
def play_notification_sound():
    playsound('sounds/notification_sound.mp3')

def get_time_range():
    global start_time, end_time

    time_window = tk.Tk()
    time_window.withdraw() # Hide the main window

    start_time_str = simpledialog.askstring("Start Time", "Enter start time (HH:MM AM/PM):")
    end_time_str = simpledialog.askstring("End Time", "Enter end time (HH:MM AM/PM):")
    
    # Convert to datetime objects
    try:
        start_time = datetime.strptime(start_time_str, '%I:%M %p').time()
        end_time = datetime.strptime(end_time_str, '%I:%M %p').time()
    except ValueError:
        print("Invalid time format. Use HH:MM AM/PM.")
        time_window.destroy()
        exit()

    time_window.destroy()

# creating a pop up window for entering the activity using Tkinter
def popup_window():

    # Calculating current time and previous hour time
    now = datetime.now()
    previous_hour = now - timedelta(hours=1)
    current_time_str = now.strftime('%Y-%m-%d %I:%M %p')
    current_day = now.strftime('%A')
    current_date = now.strftime('%Y-%m-%d')
    current_hour = now.strftime('%I:%M %p')
    previous_hour_str = previous_hour.strftime('%I:%M %p')
    
    # Creating the popup window
    popup = tk.Toplevel()
    popup.title('Log Your Activity')
    popup.geometry('300x200')  # window size (Width x Height)
    popup.configure(bg='#f0f0f0')  # Light gray background
    
     # Add a frame to organize widgets
    frame = tk.Frame(popup, bg='#f0f0f0')
    frame.pack(padx=20, pady=20, expand=True)

    # Displaying the current date and time at the top
    time_label = tk.Label(frame, text=f'{current_date} - {current_day} \n {current_hour}',
                          font=('Helvetica', 18, 'bold'),
                          bg='#f0f0f0',
                          fg='#333333')  # Dark gray text
    time_label.pack(pady=(0, 20))

    # Open and resize the image using Pillow
    img_path = 'Track_image.png'  # image path (can be .jpg, .png, .gif, .bmp, .tiff, .tif, .ico.)
    try:
        img = Image.open(img_path)
        img = img.resize((600, 600), Image.LANCZOS)  # Resize image to 800x800 pixels
        img_tk = ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image: {e}")
        img_tk = None

    if img_tk:
        img_label = tk.Label(frame, image=img_tk, bg='#f0f0f0')
        img_label.image = img_tk  # Keep a reference to avoid garbage collection
        img_label.pack(pady=(0, 10))
    else:
        tk.Label(frame, text="Failed to load image", bg='#f0f0f0').pack(pady=(0, 10))

    # Adding a label with custom font and color
    label = tk.Label(frame, text=f'Enter the Activity you have Done (from {previous_hour_str} to {current_hour}):', 
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

    # Bind keys to functions for terminating the app
    def terminate_app(event=None):
        print('Terminating application.')
        popup.destroy()  # Close the popup
        #terminate_event.set()
        root.quit()  # Exit the main loop

    # Ensure the popup window will also terminate the application
    popup.protocol('WM_DELETE_WINDOW', terminate_app)

# Timer function to wait and trigger notifications
def timer():
    while True:
        now = datetime.now()
        current_time = now.time()

        # Check if current time is within the specified range
        if start_time <= current_time <= end_time:
            play_notification_sound()
            root.after(0, popup_window)  # Show the popup window
            
        # Calculate time to wait until the next hour
        seconds_to_next_hour = 3600 - (now.minute * 60 + now.second)
        time.sleep(seconds_to_next_hour)

# main function to run the application
def main():
    global conn, cursor, root

    conn, cursor = db_setup()
    get_time_range()  # Ensure time range is set before starting the timer

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
        root.quit()

if __name__ =="__main__":
    main()