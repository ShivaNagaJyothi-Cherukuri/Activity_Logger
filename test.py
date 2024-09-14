import tkinter as tk

def popup_window():
    popup = tk.Toplevel()
    popup.title('Log Your Activity')

    label = tk.Label(popup, text='Enter your activity:')
    label.pack(padx=10, pady=10)

    entry = tk.Entry(popup)
    entry.pack(padx=10, pady=10)

    def on_submit():
        print("Activity submitted:", entry.get())
        popup.destroy()

    submit_btn = tk.Button(popup, text='Submit', command=on_submit)
    submit_btn.pack(padx=10, pady=10)

root = tk.Tk()
root.withdraw()  # Hide the root window

popup_window()
root.mainloop()
