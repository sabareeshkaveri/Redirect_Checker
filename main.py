import tkinter as tk
from Controller import RedirectCheckerController

def main():
    root = tk.Tk()
    controller = RedirectCheckerController(root)
    controller.run_authorConsole()  # Display author information in the console
    root.state('zoomed')  # Maximize the window

    root.focus_force()  # Force focus on the window
    root.mainloop()

if __name__ == "__main__":
    main()