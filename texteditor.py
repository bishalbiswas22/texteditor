import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser

class TextEditor:

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Text Editor")
        self.root.geometry("800x600")

        self.text_area = tk.Text(self.root, wrap='word', undo=True)
        self.text_area.pack(expand='yes', fill='both')

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_editor)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo_text)
        self.edit_menu.add_command(label="Redo", command=self.redo_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.find_text)
        self.edit_menu.add_command(label="Replace", command=self.replace_text)

        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Font", command=self.choose_font)
        self.format_menu.add_command(label="Text Color", command=self.choose_text_color)
        self.format_menu.add_command(label="Background Color", command=self.choose_background_color)
        self.format_menu.add_command(label="Highlight Text", command=self.highlight_text)

        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_checkbutton(label="Show/Hide Status Bar", command=self.toggle_status_bar)
        self.view_menu.add_checkbutton(label="Show/Hide Line Numbers", command=self.toggle_line_numbers)

        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Word Count", command=self.word_count)
        self.tools_menu.add_command(label="Character Count", command=self.character_count)
        self.tools_menu.add_command(label="Text Alignment", command=self.choose_text_alignment)
        self.tools_menu.add_separator()
        self.tools_menu.add_command(label="Insert Image", command=self.insert_image)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.help_menu.add_command(label="Help Documentation", command=self.show_help)

        self.status_bar = tk.Label(self.root, text="Status: Ready", anchor='w')
        self.status_bar.pack(side='bottom', fill='x')

        self.file_path = None

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.update_status("New File")

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                               filetypes=[("All Files", "*.*"),
                                                          ("Text Files", "*.txt"),
                                                          ("Python Files", "*.py")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())
            self.file_path = file_path
            self.update_status(f"Opened File: {file_path}")

    def save_file(self):
        if self.file_path:
            if messagebox.askokcancel("Save", "Do you want to overwrite the current file?"):
                with open(self.file_path, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.update_status(f"Saved File: {self.file_path}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("All Files", "*.*"),
                                                            ("Text Files", "*.txt"),
                                                            ("Python Files", "*.py")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.file_path = file_path
            self.update_status(f"Saved As File: {file_path}")

    def exit_editor(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")
        self.update_status("Cut Text")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")
        self.update_status("Copied Text")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")
        self.update_status("Pasted Text")

    def undo_text(self):
        self.text_area.event_generate("<<Undo>>")
        self.update_status("Undid Last Action")

    def redo_text(self):
        self.text_area.event_generate("<<Redo>>")
        self.update_status("Redid Last Action")

    def find_text(self):
        find_string = simpledialog.askstring("Find", "Enter text to find:")
        if find_string:
            start_pos = '1.0'
            while True:
                start_pos = self.text_area.search(find_string, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(find_string)}c"
                self.text_area.tag_add('highlight', start_pos, end_pos)
                start_pos = end_pos
                self.text_area.tag_config('highlight', background='yellow')
            self.update_status(f"Found '{find_string}'")

    def replace_text(self):
        find_string = simpledialog.askstring("Find", "Enter text to find:")
        replace_string = simpledialog.askstring("Replace", "Enter replacement text:")
        if find_string and replace_string:
            content = self.text_area.get(1.0, tk.END)
            new_content = content.replace(find_string, replace_string)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, new_content)
            self.update_status(f"Replaced '{find_string}' with '{replace_string}'")

    def choose_font(self):
        font_family = simpledialog.askstring("Font", "Enter font family (e.g., Arial):")
        font_size = simpledialog.askinteger("Font Size", "Enter font size (e.g., 12):")
        if font_family and font_size:
            self.text_area.config(font=(font_family, font_size))
            self.update_status(f"Font changed to {font_family} {font_size}")

    def choose_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.config(fg=color)
            self.update_status("Text color changed")

    def choose_background_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.config(bg=color)
            self.update_status("Background color changed")

    def highlight_text(self):
        color = colorchooser.askcolor()[1]
        if color:
            try:
                current_tags = self.text_area.tag_names(tk.SEL_FIRST)
                if "highlight" in current_tags:
                    self.text_area.tag_delete("highlight")
                else:
                    self.text_area.tag_add("highlight", tk.SEL_FIRST, tk.SEL_LAST)
                    self.text_area.tag_config("highlight", background=color)
                self.update_status("Highlighted text")
            except tk.TclError:
                messagebox.showerror("Error", "No text selected")

    def toggle_status_bar(self):
        if self.status_bar.winfo_ismapped():
            self.status_bar.pack_forget()
            self.update_status("Status Bar Hidden")
        else:
            self.status_bar.pack(side='bottom', fill='x')
            self.update_status("Status Bar Shown")

    def toggle_line_numbers(self):
        # Example implementation: Add line numbers as a tag to the text area
        pass

    def word_count(self):
        content = self.text_area.get(1.0, tk.END)
        words = content.split()
        word_count = len(words)
        messagebox.showinfo("Word Count", f"Total Words: {word_count}")

    def character_count(self):
        content = self.text_area.get(1.0, tk.END)
        char_count = len(content.replace('\n', '').replace(' ', ''))
        messagebox.showinfo("Character Count", f"Total Characters: {char_count}")

    def choose_text_alignment(self):
        alignment = simpledialog.askstring("Text Alignment", "Enter text alignment (left, center, right):")
        if alignment in ['left', 'center', 'right']:
            self.text_area.tag_configure('align', justify=alignment)
            self.text_area.tag_add('align', '1.0', 'end')
            self.update_status(f"Text aligned {alignment}")

    def insert_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            image = tk.PhotoImage(file=file_path)
            self.text_area.image_create(tk.END, image=image)
            self.update_status(f"Inserted Image: {file_path}")

    def show_about(self):
        messagebox.showinfo("About", "Advanced Text Editor\nVersion 1.0\nCreated by Your Name")

    def show_help(self):
        # Provide help documentation here
        pass

    def update_status(self, message):
        self.status_bar.config(text=f"Status: {message}")

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
