import tkinter as tk

def test_tkinter():
    root = tk.Tk()
    root.title('Test Tkinter')

    label = tk.Label(root, text='If you see this window, Tkinter is working!')
    label.pack(padx=20, pady=20)

    button = tk.Button(root, text='Close', command=root.destroy)
    button.pack(padx=20, pady=20)

    root.mainloop()

if __name__ == '__main__':
    test_tkinter()
