import tkinter as tk
import random
import sys
import os
import re
from PIL import Image, ImageTk

EMOJI_PATTERN = re.compile(
    r'['
    '\U0001F600-\U0001F64F'
    '\U0001F300-\U0001F5FF'
    '\U0001F680-\U0001F6FF'
    '\U0001F700-\U0001F77F'
    '\U0001F780-\U0001F7FF'
    '\U0001F800-\U0001F8FF'
    '\U0001F900-\U0001F9FF'
    '\U0001FA00-\U0001FA6F'
    '\U0001FA70-\U0001FAFF'
    '\U00002702-\U000027B0'
    '\U000024C2-\U0001F251'
    ']+'
    '|'
    r'(?:<3|:\)|:-\)|:\(|:-\(|;\)|;-\)|:D|:P|:p|:o|:O|:\||:\*|:s|:S|:x|:X|:Z|:z|:o|:O|:\||:-\*|:-x|:-X|:-Z|:-z|:-o|:-O|:-<|:\'\(|:\'-\(|>_<|\^_\^|=D|:3)'
)

def copy_to_clipboard():
    try:
        global output_text
        root.clipboard_clear()
        text_to_copy = output_text.get("1.0", tk.END).strip()
        if text_to_copy:
            root.clipboard_append(text_to_copy)
            status_label.config(text="Text copied to clipboard!")
        else:
            status_label.config(text="No text to copy.")
    except Exception as e:
        status_label.config(text=f"Error copying to clipboard: {e}")

def clear_text_boxes():
    global output_text
    global text_input
    text_input.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    status_label.config(text="Text boxes cleared.")
    
LIGHT_THEME = {
    "bg": "SystemButtonFace",
    "fg": "black",
    "text_bg": "white",
    "text_fg": "black",
    "button_bg": "SystemButtonFace",
    "button_fg": "black",
    "checkbox_select": "SystemButtonFace"
}

DARK_THEME = {
    "bg": "#2e2e2e",
    "fg": "#e0e0e0",
    "text_bg": "#3c3c3c",
    "text_fg": "#e0e0e0",
    "button_bg": "#4a4a4a",
    "button_fg": "#e0e0e0",
    "checkbox_select": "#5c5c5c"
}

def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

def setup_main_app_ui(root_window):
    global status_label
    global text_input
    global output_text
    enter_to_convert = tk.BooleanVar(value=True)
    auto_clear_output = tk.BooleanVar(value=True)
    dark_mode_enabled = tk.BooleanVar(value=True)
    
    root_window.title("Home")

    def apply_theme():
        is_dark = dark_mode_enabled.get()
        theme = DARK_THEME if is_dark else LIGHT_THEME

        root_window.config(bg=theme["bg"])
        filler_frame.config(bg=theme["bg"])
        button_frame.config(bg=theme["bg"])

        author_label.config(bg=theme["bg"], fg=theme["fg"])
        input_label.config(bg=theme["bg"], fg=theme["fg"])
        output_label.config(bg=theme["bg"], fg=theme["fg"])
        status_label.config(bg=theme["bg"], fg=theme["fg"])

        text_input.config(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["fg"])
        output_text.config(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["fg"])

        submit_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
        clear_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
        settings_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
        copy_button.config(bg=theme["button_bg"], fg=theme["button_fg"])

        if settings_window is not None and settings_window.winfo_exists():
            settings_window.config(bg=theme["bg"])
            for widget in settings_window.winfo_children():
                if isinstance(widget, (tk.Label, tk.Checkbutton, tk.Button)):
                    try:
                        widget.config(bg=theme["bg"], fg=theme["fg"])
                        if isinstance(widget, tk.Checkbutton):
                            widget.config(selectcolor=theme["checkbox_select"])
                    except tk.TclError:
                        pass
    
    def convert_text(text):
        parts_regex = re.compile(
            r'(?P<asterisk>\*.*?\*)|'
            r'(?P<emoji>' + EMOJI_PATTERN.pattern + r')|'
            r'(?P<word>\w+)|'
            r'(?P<punct>[^\w\s])|'
            r'(?P<space>\s+)'
        )
        
        converted_parts = []
        for match in parts_regex.finditer(text):
            if match.group('asterisk'):
                converted_parts.append(match.group('asterisk'))
            elif match.group('emoji'):
                converted_parts.append(match.group('emoji'))
            elif match.group('word'):
                word = match.group('word')
                if random.choice([True, False]):
                    word = f"{word[0]}-{word.lower()}"
                if random.choice([True, False, False]):
                    word += random.choice(["...", ".."])
                if random.choice([True, False, False]):
                    word += random.choice(["~", "~~"])
                converted_parts.append(word)
            elif match.group('punct'):
                converted_parts.append(match.group('punct'))
            elif match.group('space'):
                converted_parts.append(match.group('space'))
        
        return "".join(converted_parts)

    def submit_button_clicked():
        text = text_input.get("1.0", tk.END).strip()
        converted_text = convert_text(text)
        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", converted_text)
        status_label.config(text="")

    def on_enter(event):
        if enter_to_convert.get():
            submit_button_clicked()
            return "break"
        
    def open_settings():
        nonlocal settings_window
        if settings_window is not None and settings_window.winfo_exists():
            settings_window.lift()
            return

        settings_window = tk.Toplevel(root_window)
        settings_window.title("Settings")
        win_width = 600
        win_height = 500
        screen_width = settings_window.winfo_screenwidth()
        screen_height = settings_window.winfo_screenheight()
        x = (screen_width // 2) - (win_width // 2)
        y = (screen_height // 2) - (win_height // 2)
        settings_window.geometry(f"{win_width}x{win_height}+{x}+{y}")

        settings_label = tk.Label(settings_window, text="Settings", font=("Arial", 18))
        settings_label.pack(pady=10)

        enter_checkbox = tk.Checkbutton(
            settings_window,
            text="Press Enter to convert text",
            variable=enter_to_convert,
            font=("Arial", 20)
        )
        enter_checkbox.pack(pady=10)

        auto_clear_checkbox = tk.Checkbutton(
            settings_window,
            text="Auto-clear converted text when input is empty",
            variable=auto_clear_output,
            font=("Arial", 20)
        )
        auto_clear_checkbox.pack(pady=10)

        dark_mode_checkbox = tk.Checkbutton(
            settings_window,
            text="Enable Light Mode",
            variable=dark_mode_enabled,
            command=apply_theme,
            font=("Arial", 20)
        )
        dark_mode_checkbox.pack(pady=10)
        
        def on_close():
            nonlocal settings_window
            settings_window.destroy()
            settings_window = None

        settings_window.protocol("WM_DELETE_WINDOW", on_close)

        is_dark = dark_mode_enabled.get()
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        settings_window.config(bg=current_theme["bg"])
        settings_label.config(bg=current_theme["bg"], fg=current_theme["fg"])
        enter_checkbox.config(bg=current_theme["bg"], fg=current_theme["fg"], selectcolor=current_theme["checkbox_select"])
        auto_clear_checkbox.config(bg=current_theme["bg"], fg=current_theme["fg"], selectcolor=current_theme["checkbox_select"])
        dark_mode_checkbox.config(bg=current_theme["bg"], fg=current_theme["fg"], selectcolor=current_theme["checkbox_select"])

    settings_window = None

    author_label = tk.Label(
        root_window,
        text="Fridge's\n𝓕𝓻𝓮𝓪𝓴𝔂  Text Generator",
        font=("Arial", 20)
    )
    author_label.pack()

    filler_frame = tk.Frame(root_window)
    filler_frame.pack(pady=10)

    input_label = tk.Label(
        root_window,
        text="Your text here (Input):",
        font=("Arial", 15)
    )
    input_label.pack()

    text_input = tk.Text(
        root_window,
        width=100,
        height=4,
        font=("Arial", 20)
    )
    text_input.pack(pady=10)
    text_input.focus_set()
    text_input.bind('<Return>', on_enter)

    output_label = tk.Label(
        root_window,
        text="Result (Output):",
        font=("Arial", 15)
    )
    output_label.pack()

    output_text = tk.Text(
        root_window,
        width=100,
        height=4,
        font=("Arial", 20)
    )
    output_text.pack(pady=10)

    button_frame = tk.Frame(root_window)
    button_frame.pack(pady=5)
    
    submit_button = tk.Button(
        button_frame,
        text="Convert",
        font=("Arial", 20),
        command=submit_button_clicked
    )
    submit_button.pack(side=tk.LEFT, padx=5)

    clear_button = tk.Button(
        button_frame,
        text="Clear All",
        font=("Arial", 20),
        command=clear_text_boxes
    )
    clear_button.pack(side=tk.LEFT, padx=5)
    
    copy_button = tk.Button(
        button_frame,
        text="Copy to Clipboard",
        font=("Arial", 15),
        command=copy_to_clipboard
    )
    copy_button.pack(side=tk.LEFT, padx=5)

    settings_button = tk.Button(
        root_window,
        text="Settings",
        font=("Arial", 15),
        command=open_settings
    )
    settings_button.place(relx=1.0, rely=0.0, anchor="ne")

    status_label = tk.Label(root_window, text="", font=("Arial", 12))
    status_label.pack(pady=5)
    
    apply_theme()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def start_app():
    clear_window(root)
    root.geometry("1920x1080")
    setup_main_app_ui(root)

root = tk.Tk()
root.title("Welcome")
root.geometry("1920x1800")
root.config(bg=DARK_THEME["bg"])

tk.Label(root, 
         text="Hello! Welcome to Fridge's 𝓕𝓻𝓮𝓪𝓴𝔂 Text Generator.\nExample: Hello World ----> H-hello... world..~\nAll you need to do is put whatever text in the input, press enter (Can be changed in settings to manually click convert) and your 𝓯𝓻𝓮𝓪𝓴𝔂 text will be displayed in the output!",
         font=("Arial", 14), wraplength=680, justify="left",
         bg=DARK_THEME["bg"], fg=DARK_THEME["fg"]).pack(pady=20)
print("Looking for:", resource_path("blinking_bear.jpeg"))
print("Looking for:", resource_path("modified_bear.png"))
try:
    img1 = Image.open(resource_path("blinking_bear.jpeg"))
    img1 = img1.resize((120, 120), Image.Resampling.LANCZOS)
    img1 = ImageTk.PhotoImage(img1)
except FileNotFoundError:
    img1 = None
    print("[ERROR] blinking_bear.jpeg not found")

try:
    img2 = Image.open(resource_path("modified_bear.png"))
    img2 = img2.resize((120, 120), Image.Resampling.LANCZOS)
    img2 = ImageTk.PhotoImage(img2)
except FileNotFoundError:
    img2 = None
    print("[ERROR] modified_bear.png not found")

img_frame = tk.Frame(root, bg=DARK_THEME["bg"])
img_frame.pack(pady=10)

if img1:
    tk.Label(img_frame, image=img1, bg=DARK_THEME["bg"]).pack(side="left", padx=10)
if img2:
    tk.Label(img_frame, image=img2, bg=DARK_THEME["bg"]).pack(side="left", padx=10)

root.img1 = img1
root.img2 = img2

start_button = tk.Button(root, text="Start", font=("Arial", 16), command=start_app,
                         bg=DARK_THEME["button_bg"], fg=DARK_THEME["button_fg"])
start_button.pack()

root.mainloop()