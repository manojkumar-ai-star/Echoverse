    
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
from PyPDF2 import PdfReader
import pygame

def get_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def browse_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(0, file_path)

def generate_audio():
    text = text_box.get("1.0", tk.END).strip()
    pdf_path = pdf_entry.get().strip()
    
    if pdf_path:
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", "PDF file not found!")
            return
        text = get_text_from_pdf(pdf_path)
    
    if not text:
        messagebox.showerror("Error", "Please provide text or PDF.")
        return

    language = lang_var.get().lower()
    gender = gender_var.get().lower()
    expression = expression_var.get().lower()
    
    lang_map = {
        "english": "en",
        "tamil": "ta",
        "hindi": "hi",
        "telugu": "te",
        "malayalam": "ml"
    }

    # Ask user where to save the audio
    output_file = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3 files", "*.mp3")],
        title="Save Audio As"
    )

    if not output_file:  # User cancelled
        return

    # Generate speech
    tts = gTTS(text=text, lang=lang_map.get(language, "en"))
    tts.save(output_file)
    messagebox.showinfo("Success", f"Audio saved as {output_file}")

    # Play audio using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

# GUI setup
root = tk.Tk()
root.title("Text/PDF to Speech with Audio Playback")

tk.Label(root, text="Enter Text:").grid(row=0, column=0, sticky="w")
text_box = tk.Text(root, width=60, height=10)
text_box.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

tk.Label(root, text="Or select PDF:").grid(row=2, column=0, sticky="w")
pdf_entry = tk.Entry(root, width=40)
pdf_entry.grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_pdf).grid(row=2, column=2)

tk.Label(root, text="Language:").grid(row=3, column=0, sticky="w")
lang_var = tk.StringVar(value="english")
tk.OptionMenu(root, lang_var, "english", "tamil", "hindi", "telugu", "malayalam").grid(row=3, column=1)

tk.Label(root, text="Voice Gender:").grid(row=4, column=0, sticky="w")
gender_var = tk.StringVar(value="male")
tk.OptionMenu(root, gender_var, "male", "female").grid(row=4, column=1)

tk.Label(root, text="Expression:").grid(row=5, column=0, sticky="w")
expression_var = tk.StringVar(value="neutral")
tk.OptionMenu(root, expression_var, "neutral", "happy", "sad", "angry").grid(row=5, column=1)

tk.Button(root, text="Generate Audio", command=generate_audio, bg="green", fg="white").grid(row=6, column=0, columnspan=3, pady=10)

root.mainloop()
