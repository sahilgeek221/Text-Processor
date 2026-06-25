import customtkinter as ctk
from tkinter import filedialog, messagebox
from collections import Counter
import re

# Set the global UI theme and color scheme for CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def compute_word_frequency(text):
    # Extract all valid words using regex, preserving apostrophes
    words = re.findall(r"\b[a-z']+\b", text.lower())
    # Return a dictionary-like Counter object of word frequencies
    return Counter(words)

def is_palindrome_core(s):
    # Create a new string containing only lowercase alphanumeric characters
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    # Check if the string reads the same forwards and backwards
    return cleaned == cleaned[::-1]

def caesar_transform(text, shift):
    # Initialize an empty list to store shifted characters
    result_chars = []
    # Iterate through every character in the input text
    for ch in text:
        # Check if the character is a letter
        if ch.isalpha():
            # Determine the ASCII base value depending on case
            base = ord('A') if ch.isupper() else ord('a')
            # Calculate the new shifted character using modulo arithmetic
            shifted = chr((ord(ch) - base + shift) % 26 + base)
            # Append the new character to the list
            result_chars.append(shifted)
        else:
            # Append non-alphabet characters exactly as they are
            result_chars.append(ch)
    # Join the list into a single string and return it
    return "".join(result_chars)

class WordFrequencyTab(ctk.CTkFrame):
    def __init__(self, parent):
        # Initialize the frame with a transparent background to match the tab
        super().__init__(parent, fg_color="transparent")
        
        # Create a container frame for the top controls
        control_frame = ctk.CTkFrame(self)
        # Place the control frame at the top, stretching horizontally
        control_frame.pack(fill="x", pady=(0, 10))
        
        # Initialize a string variable to store the file path
        self.filename_var = ctk.StringVar()
        # Create an entry widget tied to the filename variable
        self.file_entry = ctk.CTkEntry(control_frame, textvariable=self.filename_var, placeholder_text="Select a file...")
        # Place the entry widget on the left, letting it expand
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        # Create and place the Browse button
        ctk.CTkButton(control_frame, text="Browse...", width=80, command=self.browse_file).pack(side="left", padx=5)
        # Create and place the Analyze button
        ctk.CTkButton(control_frame, text="Analyze", width=80, command=self.analyze).pack(side="left", padx=5)
        # Create and place the Clear button
        ctk.CTkButton(control_frame, text="Clear", width=80, fg_color="transparent", border_width=1, command=self.clear).pack(side="left", padx=(5, 10))

        # Create a textbox for output using a monospaced font for tabular alignment
        self.output_box = ctk.CTkTextbox(self, font=("Consolas", 14), wrap="none")
        # Place the textbox so it fills the remaining space
        self.output_box.pack(fill="both", expand=True)

    def browse_file(self):
        # Open a file dialog restricted to text-based files
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt *.md *.csv"), ("All files", "*.*")])
        # Update the entry variable if a file was selected
        if filename:
            self.filename_var.set(filename)

    def analyze(self):
        # Get the current string from the filename entry
        filename = self.filename_var.get().strip()
        # Abort if the filename is empty
        if not filename:
            messagebox.showwarning("No filename", "Please select a file.")
            return
            
        try:
            # Open and read the entire file contents
            with open(filename, "r", encoding="utf-8") as f:
                raw_text = f.read()
        except Exception as e:
            # Show an error dialog if the file fails to open
            messagebox.showerror("File error", f"Could not open file:\n{e}")
            return

        # Calculate word frequencies from the raw text
        counter = compute_word_frequency(raw_text)
        # Clear the current textbox output
        self.clear(keep_filename=True)
        
        # Check if the text contained no valid words
        if not counter:
            self.output_box.insert("end", "No words found in the file.")
            return

        # Create header strings for the output
        header = f"{'WORD':<30} | COUNT\n"
        divider = "-" * 45 + "\n"
        # Insert the headers into the textbox
        self.output_box.insert("end", header + divider)

        # Iterate through the top 1000 most common words
        for word, count in counter.most_common(1000):
            # Format each row with specific padding and insert it
            self.output_box.insert("end", f"{word:<30} | {count}\n")

    def clear(self, keep_filename=False):
        # Delete all text inside the output box
        self.output_box.delete("1.0", "end")
        # Clear the filename entry if keep_filename is False
        if not keep_filename:
            self.filename_var.set("")

class PalindromeTab(ctk.CTkFrame):
    def __init__(self, parent):
        # Initialize the frame with a transparent background
        super().__init__(parent, fg_color="transparent")
        
        # Create and place a label prompting user input
        ctk.CTkLabel(self, text="Enter text to check:", font=("Segoe UI", 14)).pack(anchor="w", pady=(0, 5))
        # Create an entry widget for the string to check
        self.pal_input = ctk.CTkEntry(self, width=400, placeholder_text="e.g., Racecar")
        # Place the entry widget
        self.pal_input.pack(fill="x", pady=(0, 15))
        
        # Create a container frame for the buttons
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        # Place the button container
        btn_row.pack(fill="x")
        
        # Create and place the Check button
        ctk.CTkButton(btn_row, text="Check", command=self.check).pack(side="left", padx=(0, 10))
        # Create and place the Clear button
        ctk.CTkButton(btn_row, text="Clear", fg_color="transparent", border_width=1, command=lambda: self.pal_input.delete(0, "end")).pack(side="left")
        
        # Create a label to display the result, initially empty
        self.result_label = ctk.CTkLabel(self, text="", font=("Segoe UI", 18, "bold"))
        # Place the result label below the buttons
        self.result_label.pack(anchor="w", pady=20)

    def check(self):
        # Retrieve the text from the entry widget
        s = self.pal_input.get()
        # Abort if the input is entirely whitespace or empty
        if not s.strip():
            self.result_label.configure(text="Please enter some text.", text_color="gray")
            return
            
        # Check if the string is a palindrome
        if is_palindrome_core(s):
            # Update the label text and color for success
            self.result_label.configure(text="✓ Palindrome", text_color="#2ECC71")
        else:
            # Update the label text and color for failure
            self.result_label.configure(text="✗ Not a palindrome", text_color="#E74C3C")

class CaesarTab(ctk.CTkFrame):
    def __init__(self, parent):
        # Initialize the frame with a transparent background
        super().__init__(parent, fg_color="transparent")
        
        # Create and place the input label
        ctk.CTkLabel(self, text="Input text:").pack(anchor="w", pady=(0, 5))
        # Create a textbox for multi-line user input
        self.text_input = ctk.CTkTextbox(self, height=100)
        # Place the input textbox
        self.text_input.pack(fill="both", expand=True, pady=(0, 15))

        # Create a container frame for controls
        shift_row = ctk.CTkFrame(self, fg_color="transparent")
        # Place the controls container
        shift_row.pack(fill="x", pady=(0, 15))
        
        # Create and place the shift label
        ctk.CTkLabel(shift_row, text="Shift (integer):").pack(side="left", padx=(0, 10))
        
        # Initialize a string variable for the shift number
        self.shift_var = ctk.StringVar(value="3")
        # Create and place an entry widget for the shift number
        ctk.CTkEntry(shift_row, textvariable=self.shift_var, width=60).pack(side="left", padx=(0, 20))

        # Create and place the Encrypt button, passing 1 as the multiplier
        ctk.CTkButton(shift_row, text="Encrypt →", command=lambda: self.process(1)).pack(side="left", padx=5)
        # Create and place the Decrypt button, passing -1 as the multiplier
        ctk.CTkButton(shift_row, text="Decrypt ←", command=lambda: self.process(-1)).pack(side="left", padx=5)
        # Create and place the Clear button
        ctk.CTkButton(shift_row, text="Clear", fg_color="transparent", border_width=1, command=self.clear).pack(side="left", padx=(15, 0))

        # Create and place the output label
        ctk.CTkLabel(self, text="Result:").pack(anchor="w", pady=(0, 5))
        # Create a textbox for the processed output text
        self.text_output = ctk.CTkTextbox(self, height=100)
        # Place the output textbox
        self.text_output.pack(fill="both", expand=True)

    def process(self, direction_multiplier):
        try:
            # Convert the shift input to an integer and multiply by direction (1 or -1)
            shift = int(self.shift_var.get()) * direction_multiplier
        except ValueError:
            # Show an error dialog if the input is not a valid number
            messagebox.showerror("Invalid shift", "Please enter a valid integer for shift.")
            return

        # Retrieve text from the input box, stripping the trailing newline Tkinter adds
        text = self.text_input.get("1.0", "end-1c")
        # Abort if the input box is empty
        if not text:
            messagebox.showinfo("No input", "Enter text to process.")
            return
            
        # Delete existing text in the output box
        self.text_output.delete("1.0", "end")
        # Process the text and insert it into the output box
        self.text_output.insert("end", caesar_transform(text, shift))

    def clear(self):
        # Delete text in the input box
        self.text_input.delete("1.0", "end")
        # Delete text in the output box
        self.text_output.delete("1.0", "end")

class App(ctk.CTk):
    def __init__(self):
        # Initialize the main CustomTkinter window
        super().__init__()
        # Set the window title
        self.title("Text & String Tools")
        # Set the initial window dimensions
        self.geometry("750x550")

        # Create the tabview container
        self.tabview = ctk.CTkTabview(self)
        # Place the tabview to fill the entire window with padding
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Create the three individual tabs
        tab_1 = self.tabview.add("Word Frequency")
        tab_2 = self.tabview.add("Palindrome Checker")
        tab_3 = self.tabview.add("Caesar Cipher")

        # Instantiate the Word Frequency frame inside tab 1
        self.wf_frame = WordFrequencyTab(tab_1)
        # Expand the frame to fill tab 1
        self.wf_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Instantiate the Palindrome frame inside tab 2
        self.pal_frame = PalindromeTab(tab_2)
        # Expand the frame to fill tab 2
        self.pal_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Instantiate the Caesar frame inside tab 3
        self.caesar_frame = CaesarTab(tab_3)
        # Expand the frame to fill tab 3
        self.caesar_frame.pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == "__main__":
    # Create the application instance
    app = App()
    # Start the main event loop
    app.mainloop()