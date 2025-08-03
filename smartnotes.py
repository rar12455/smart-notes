import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import json
from datetime import datetime
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None
# API key will be loaded from config

# Notes management class
class NotesManager:
    def __init__(self, notes_file="smart_notes.json"):
        self.notes_file = notes_file
        self.notes = self.load_notes()

    def load_notes(self):
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        return []

    def save_notes(self):
        with open(self.notes_file, 'w') as file:
            json.dump(self.notes, file, indent=2)

    def add_note(self, title, content):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note_id = self._get_next_id()

        new_note = {
            "id": note_id,
            "title": title,
            "content": content,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        self.notes.append(new_note)
        self.save_notes()
        return note_id

    def _get_next_id(self):
        if not self.notes:
            return 1
        return max(note["id"] for note in self.notes) + 1

    def update_note(self, note_id, title=None, content=None):
        for note in self.notes:
            if note["id"] == note_id:
                if title is not None:
                    note["title"] = title
                if content is not None:
                    note["content"] = content
                note["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_notes()
                return True
        return False

    def delete_note(self, note_id):
        for i, note in enumerate(self.notes):
            if note["id"] == note_id:
                del self.notes[i]
                self.save_notes()
                return True
        return False

    def search_notes(self, query):
        query = query.lower()
        results = []

        for note in self.notes:
            if query in note["title"].lower() or query in note["content"].lower():
                results.append(note)

        return results

    def get_all_notes(self):
        return self.notes

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if note["id"] == note_id:
                return note
        return None

# Main application
class SmartNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry(f"{1280}x{720}")
        self.root.title("Personal Note-Taking App // A.K.A : smart notes")
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.current_theme = "dark"
        self.focus = None
        self.notes_manager = NotesManager()
        self.current_note_id = None
        self.api_key = self.load_api_key()

        # Initialize theme colors
        self.update_theme_colors()

        self.setup_ui()
        self.setup_bindings()
        self.refresh_notes_list()

    def update_theme_colors(self):
        """Update theme color variables based on current theme"""
        if self.current_theme == "light":
            self.bg_color = "#FFFFFF"
            self.fg_color = "#000000"
            self.top_frame_color = "#F5F5F5"
            self.sidebar_bg = "#FAFAFA"
            self.button_bg = "#FFFFFF"
            self.button_fg = "#000000"
            self.button_hover_bg = "#F5F5F5"
            self.tree_bg = "#FFFFFF"
            self.tree_fg = "#000000"
            self.tree_field_bg = "#F5F5F5"
            self.tree_select_bg = "#E3F2FD"
            self.entry_bg = "#FFFFFF"
            self.entry_fg = "#000000"
            self.scrollbar_bg = "#F5F5F5"
            self.textbox_border = "#E0E0E0"     # Light theme textbox border
        else:
            # Google Material Design Dark Theme colors
            self.bg_color = "#1F1F1F"           # Main background - rich dark gray
            self.fg_color = "#E8EAED"           # Primary text - soft white
            self.top_frame_color = "#2D2D30"    # Toolbar - slightly lighter dark
            self.sidebar_bg = "#252526"         # Sidebar - medium dark gray
            self.button_bg = "#3C3C3C"          # Button background
            self.button_fg = "#E8EAED"          # Button text
            self.button_hover_bg = "#464647"    # Button hover state
            self.tree_bg = "#252526"            # Tree background
            self.tree_fg = "#CCCCCC"            # Tree text
            self.tree_field_bg = "#2D2D30"      # Tree field background
            self.tree_select_bg = "#094771"     # Tree selection - Google blue
            self.entry_bg = "#3C3C3C"           # Entry field background
            self.entry_fg = "#E8EAED"           # Entry field text
            self.scrollbar_bg = "#3E3E42"       # Scrollbar background
            self.textbox_border = "#404040"     # Textbox border color

    def setup_ui(self):
        # Set root window background
        self.root.config(bg=self.bg_color)

        # Top frame for buttons
        self.top_frame = tk.Frame(self.root, bg=self.top_frame_color, relief=tk.FLAT, bd=1)
        self.top_frame.grid(row=0, column=0, sticky="ew")
        self.top_frame.columnconfigure(tuple(range(9)), weight=1)

        # Main content frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.grid(row=1, column=0, sticky="nsew")

        # Set up the main frame with 3 columns
        # Column 0: Notes sidebar
        # Column 1: Text editor
        # Column 2: AI assistant
        self.main_frame.columnconfigure(0, weight=1)  # Sidebar
        self.main_frame.columnconfigure(1, weight=3)  # Main editor
        self.main_frame.columnconfigure(2, weight=2)  # AI section
        self.main_frame.rowconfigure(0, weight=1)

        # Notes sidebar frame
        self.sidebar_frame = tk.Frame(self.main_frame, bg=self.sidebar_bg)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=2, pady=5)
        self.sidebar_frame.rowconfigure(0, weight=0)  # Search row
        self.sidebar_frame.rowconfigure(1, weight=1)  # Notes list
        self.sidebar_frame.columnconfigure(0, weight=1)

        # Search in sidebar
        self.search_frame = tk.Frame(self.sidebar_frame, bg=self.sidebar_bg)
        self.search_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.search_notes())
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var,
                                    bg=self.entry_bg, fg=self.entry_fg, font="Helvetica 13",
                                    insertbackground=self.entry_fg, relief=tk.FLAT, bd=8,
                                    highlightthickness=1, highlightcolor="#1A73E8")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Notes list with Treeview
        self.notes_list_frame = tk.Frame(self.sidebar_frame, bg=self.sidebar_bg)
        self.notes_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.notes_list_frame.rowconfigure(0, weight=1)
        self.notes_list_frame.columnconfigure(0, weight=1)

        # Create style for treeview
        style = ttk.Style()
        style.configure("Treeview",
                        background=self.tree_bg,
                        foreground=self.tree_fg,
                        fieldbackground=self.tree_field_bg,
                        borderwidth=0)
        style.map('Treeview', background=[('selected', self.tree_select_bg)])

        self.notes_list = ttk.Treeview(self.notes_list_frame, columns=("title",), show="tree")
        self.notes_list.grid(row=0, column=0, sticky="nsew")
        self.notes_list.column("#0", width=30)
        self.notes_list.column("title", width=170)
        self.notes_list.bind("<<TreeviewSelect>>", self.on_note_select)

        # Main text editor with frame
        self.main_editor_frame = tk.Frame(self.main_frame, bg=self.textbox_border, relief=tk.FLAT, bd=2)
        self.main_editor_frame.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=5, pady=5)
        self.main_editor_frame.grid_rowconfigure(0, weight=1)
        self.main_editor_frame.grid_columnconfigure(0, weight=1)

        self.txtBox = tk.Text(self.main_editor_frame, wrap=tk.WORD, font="Helvetica 15",
                             bg=self.bg_color, fg=self.fg_color, insertbackground=self.fg_color,
                             relief=tk.FLAT, bd=0, highlightthickness=0, selectbackground=self.tree_select_bg)
        self.txtBox.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.txtBox.bind("<FocusIn>", self.focus_changed)

        # AI assistant section with frame
        self.ai_input_frame = tk.Frame(self.main_frame, bg=self.textbox_border, relief=tk.FLAT, bd=2)
        self.ai_input_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.ai_input_frame.grid_rowconfigure(0, weight=1)
        self.ai_input_frame.grid_columnconfigure(0, weight=1)

        tk.Label(self.ai_input_frame, text="AI Assistant Input", bg=self.textbox_border, fg=self.fg_color,
                font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="ew", padx=2, pady=(2,0))

        self.aitxtBox = tk.Text(self.ai_input_frame, wrap=tk.WORD, font="Helvetica 15",
                               bg=self.bg_color, fg=self.fg_color, insertbackground=self.fg_color,
                               relief=tk.FLAT, bd=0, highlightthickness=0, selectbackground=self.tree_select_bg)
        self.aitxtBox.grid(row=1, column=0, sticky="nsew", padx=2, pady=(0,2))
        self.aitxtBox.bind("<FocusIn>", self.focus_changed)

        # AI response bubble with frame
        self.ai_response_frame = tk.Frame(self.main_frame, bg=self.textbox_border, relief=tk.FLAT, bd=2)
        self.ai_response_frame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        self.ai_response_frame.grid_rowconfigure(0, weight=1)
        self.ai_response_frame.grid_columnconfigure(0, weight=1)

        tk.Label(self.ai_response_frame, text="AI Response", bg=self.textbox_border, fg=self.fg_color,
                font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="ew", padx=2, pady=(2,0))

        self.bubble = tk.Text(self.ai_response_frame, wrap=tk.WORD, font="Helvetica 15",
                             bg=self.bg_color, fg=self.fg_color, insertbackground=self.fg_color,
                             relief=tk.FLAT, bd=0, highlightthickness=0, selectbackground=self.tree_select_bg)
        self.bubble.grid(row=1, column=0, sticky="nsew", padx=2, pady=(0,2))
        self.bubble.bind("<FocusIn>", self.focus_changed)

        # Add buttons to top frame
        buttons = [
            ("About", self.about_app),
            ("Save", self.save_note),
            ("New Note", self.new_note),
            ("Clear", self.clear_notes),
            ("Tutorial", self.tutorial),
            ("AI", self.ai_assist),
            ("Assign API", self.assign_api),
            ("Theme", self.change_theme),
            ("Delete", self.delete_note),
            ("Export", self.export_note)
        ]

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(
                self.top_frame, text=text, bg=self.button_bg, fg=self.button_fg,
                command=command, width=9, height=1, relief=tk.FLAT, bd=0,
                font=("Segoe UI", 9), cursor="hand2",
                activebackground=self.button_hover_bg, activeforeground=self.button_fg
            )
            button.grid(row=0, column=i, sticky="ew", padx=1, pady=3)

    def setup_bindings(self):
        # Keyboard shortcuts
        self.root.bind("<Control-t>", lambda event: self.change_theme())
        self.root.bind("<Control-Alt-b>", lambda event: self.about_app())
        self.root.bind("<Control-s>", lambda event: self.save_note())
        self.root.bind("<Control-n>", lambda event: self.new_note())
        self.root.bind("<Control-Alt-c>", lambda event: self.clear_notes())
        self.root.bind("<Control-Alt-d>", lambda event: self.ai_assist())
        self.root.bind("<Control-Alt-f>", lambda event: self.create_sample_note())
        self.root.bind("<Control-Delete>", lambda event: self.delete_note())

    def focus_changed(self, event):
        focused_widget = event.widget
        if isinstance(focused_widget, tk.Text):
            if focused_widget == self.txtBox:
                self.focus = "a"
            elif focused_widget == self.aitxtBox:
                self.focus = "b"
            elif focused_widget == self.bubble:
                self.focus = "c"

    def refresh_notes_list(self, search_query=None):
        # Clear existing items
        self.notes_list.delete(*self.notes_list.get_children())

        # Get notes, either all or search results
        notes = self.notes_manager.search_notes(search_query) if search_query else self.notes_manager.get_all_notes()

        # Sort by most recently updated
        notes.sort(key=lambda x: x["updated_at"], reverse=True)

        # Add to treeview
        for note in notes:
            note_id = str(note["id"])
            self.notes_list.insert("", tk.END, note_id, text="", values=(note["title"],))

    def search_notes(self):
        query = self.search_var.get().strip()
        self.refresh_notes_list(query if query else None)

    def on_note_select(self, event):
        selected_items = self.notes_list.selection()
        if not selected_items:
            return

        note_id = int(selected_items[0])
        note = self.notes_manager.get_note_by_id(note_id)
        if note:
            self.current_note_id = note_id
            self.txtBox.delete(1.0, tk.END)
            self.txtBox.insert(tk.END, note["content"])

    def new_note(self):
        # Show a dialog to get the note title
        title_window = tk.Toplevel(self.root)
        title_window.title("New Note")
        title_window.geometry("300x120")
        title_window.configure(bg=self.bg_color)

        tk.Label(title_window, text="Enter note title:", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 11)).pack(pady=5)

        title_entry = tk.Entry(title_window, width=30, bg=self.entry_bg, fg=self.entry_fg,
                              insertbackground=self.entry_fg, relief=tk.FLAT, bd=5, font=("Segoe UI", 11))
        title_entry.pack(pady=5)
        title_entry.focus_set()

        def create_note():
            title = title_entry.get().strip()
            if title:
                note_id = self.notes_manager.add_note(title, "")
                self.current_note_id = note_id
                self.txtBox.delete(1.0, tk.END)
                self.refresh_notes_list()
                # Select the new note in the list
                self.notes_list.selection_set(str(note_id))
                title_window.destroy()
            else:
                tk.Label(title_window, text="Title cannot be empty!", fg="#FF6B6B", bg=self.bg_color, font=("Segoe UI", 10)).pack()

        tk.Button(title_window, text="Create", command=create_note, bg=self.button_bg, fg=self.button_fg,
                 relief=tk.FLAT, bd=0, font=("Segoe UI", 11), cursor="hand2",
                 activebackground=self.button_hover_bg, activeforeground=self.button_fg).pack(pady=10)

    def save_note(self):
        if self.current_note_id is None:
            # If no note is selected, create a new one
            self.new_note()
            return

        content = self.txtBox.get("1.0", tk.END).strip()
        success = self.notes_manager.update_note(self.current_note_id, content=content)

        if success:
            # Update the note in the list if needed
            self.refresh_notes_list()

    def delete_note(self):
        if self.current_note_id is None:
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?")
        if confirm:
            success = self.notes_manager.delete_note(self.current_note_id)
            if success:
                self.current_note_id = None
                self.txtBox.delete(1.0, tk.END)
                self.refresh_notes_list()

    def export_note(self):
        if self.current_note_id is None:
            messagebox.showinfo("Info", "No note selected to export")
            return

        file_path = filedialog.asksaveasfilename(
            initialdir=".",
            title="Export Note",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.txtBox.get("1.0", tk.END).strip())

    def about_app(self):
        about_window = tk.Toplevel(self.root)
        about_window.geometry("300x150")
        about_window.title("About App")
        about_window.configure(bg=self.bg_color)

        label = tk.Label(
            about_window,
            text="This app is made by RAR - dev_era\n\nVersion: 3.0\nAdded: Search & Notes sidebar",
            font=("Segoe UI", 13),
            bg=self.bg_color,
            fg=self.fg_color
        )
        label.pack(expand=True)
        label.pack(pady=20)

    def create_sample_note(self):
        self.txtBox.insert(tk.END, "\n# Create your first notes here!\n")

    def clear_notes(self):
        if self.focus == "a":
            self.txtBox.delete("1.0", tk.END)
        if self.focus == "b":
            self.aitxtBox.delete("1.0", tk.END)
        if self.focus == "c":
            self.bubble.delete("1.0", tk.END)

    def ai_assist(self):
        if not GENAI_AVAILABLE:
            self.bubble.delete("1.0", tk.END)
            self.bubble.insert(tk.END, "ERROR: Google Generative AI library not installed!\n\nPlease install it with:\npip install google-generativeai")
            return

        if not self.api_key:
            self.bubble.delete("1.0", tk.END)
            self.bubble.insert(tk.END, "ERROR: No API key configured!\n\nPlease click 'Assign API' to set up your Google Gemini API key.")
            return

        uinput = self.aitxtBox.get("1.0", tk.END)
        if not uinput.strip():
            return

        self.bubble.delete("1.0", tk.END)
        self.bubble.insert(tk.END, "Thinking...\n")
        self.root.update()

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(uinput)
            self.bubble.delete("1.0", tk.END)
            self.bubble.insert(tk.END, response.text)
        except Exception as e:
            self.bubble.delete("1.0", tk.END)
            self.bubble.insert(tk.END, f"Error: {str(e)}\n\nPlease check your API key using 'Assign API' button.")

    def load_api_key(self):
        """Load API key from config file"""
        config_file = "smartnotes_config.json"
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    api_key = config.get('api_key', '')
                    if api_key and GENAI_AVAILABLE:
                        genai.configure(api_key=api_key)
                    return api_key
        except Exception as e:
            print(f"Error loading API key: {e}")
        return ""

    def save_api_key(self, api_key):
        """Save API key to config file"""
        config_file = "smartnotes_config.json"
        try:
            config = {'api_key': api_key}
            with open(config_file, 'w') as f:
                json.dump(config, f)
            if GENAI_AVAILABLE:
                genai.configure(api_key=api_key)
            return True
        except Exception as e:
            print(f"Error saving API key: {e}")
            return False

    def assign_api(self):
        """Open API key assignment window"""
        api_window = tk.Toplevel(self.root)
        api_window.title("Assign Google Gemini API Key")
        api_window.geometry("500x300")
        api_window.configure(bg=self.bg_color)

        # Title label
        title_label = tk.Label(api_window, text="Google Gemini API Key Configuration",
                              bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 15, "bold"))
        title_label.pack(pady=10)

        # Instructions
        instructions = tk.Label(api_window,
                               text="Enter your Google Gemini API key below.\nYou can get it from: https://makersuite.google.com/app/apikey",
                               bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 11),
                               justify=tk.CENTER)
        instructions.pack(pady=5)

        # Current API key status
        status_text = "API Key Configured" if self.api_key else "No API Key Set"
        status_label = tk.Label(api_window, text=f"Current Status: {status_text}",
                               bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 11))
        status_label.pack(pady=5)

        # API key entry
        tk.Label(api_window, text="API Key:", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 11)).pack(pady=(10,0))

        api_entry = tk.Entry(api_window, width=60, bg=self.entry_bg, fg=self.entry_fg,
                            insertbackground=self.entry_fg, relief=tk.FLAT, bd=5, font=("Segoe UI", 11),
                            show="*")  # Hide API key with asterisks
        api_entry.pack(pady=5)

        if self.api_key:
            api_entry.insert(0, self.api_key)

        # Buttons frame
        button_frame = tk.Frame(api_window, bg=self.bg_color)
        button_frame.pack(pady=20)

        def save_api():
            new_api_key = api_entry.get().strip()
            if new_api_key:
                if self.save_api_key(new_api_key):
                    self.api_key = new_api_key
                    messagebox.showinfo("Success", "API key saved successfully!")
                    api_window.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save API key.")
            else:
                messagebox.showwarning("Warning", "Please enter a valid API key.")

        def test_api():
            if not GENAI_AVAILABLE:
                messagebox.showerror("Error", "Google Generative AI library not installed.\nPlease install: pip install google-generativeai")
                return

            test_key = api_entry.get().strip()
            if test_key:
                try:
                    genai.configure(api_key=test_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content("Hello, just testing the API")
                    messagebox.showinfo("Success", "API key is working correctly!")
                except Exception as e:
                    messagebox.showerror("Error", f"API key test failed: {str(e)}")
            else:
                messagebox.showwarning("Warning", "Please enter an API key to test.")

        # Save button
        save_btn = tk.Button(button_frame, text="Save API Key", command=save_api,
                            bg=self.button_bg, fg=self.button_fg, relief=tk.FLAT, bd=0,
                            font=("Segoe UI", 11), cursor="hand2",
                            activebackground=self.button_hover_bg, activeforeground=self.button_fg)
        save_btn.pack(side=tk.LEFT, padx=5)

        # Test button
        test_btn = tk.Button(button_frame, text="Test API Key", command=test_api,
                            bg=self.button_bg, fg=self.button_fg, relief=tk.FLAT, bd=0,
                            font=("Segoe UI", 11), cursor="hand2",
                            activebackground=self.button_hover_bg, activeforeground=self.button_fg)
        test_btn.pack(side=tk.LEFT, padx=5)

        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", command=api_window.destroy,
                              bg=self.button_bg, fg=self.button_fg, relief=tk.FLAT, bd=0,
                              font=("Segoe UI", 11), cursor="hand2",
                              activebackground=self.button_hover_bg, activeforeground=self.button_fg)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def tutorial(self):
        tuto_window = tk.Toplevel(self.root)
        tuto_window.geometry("630x740")
        tuto_window.title("How to use it")
        tuto_window.configure(bg=self.bg_color)

        tutorial_text = """
        # Smart Notes Tutorial

        ## Basic Usage:
        - Create new notes using the 'New Note' button
        - Write your content in the main text area
        - Save notes with the 'Save' button or Ctrl+S

        ## Notes Management:
        - View your notes in the sidebar on the left
        - Search through your notes using the search box
        - Click on any note to open it
        - Delete notes with the 'Delete' button

        ## AI Assistant:
        - Type your question in the right top box
        - Click 'AI' button to get a response
        - The AI response will appear in the box below

        ## Keyboard Shortcuts:
        - Ctrl+S: Save note
        - Ctrl+N: New note
        - Ctrl+T: Change theme
        - Ctrl+Alt+C: Clear current panel
        - Ctrl+Alt+D: Ask AI assistant
        - Ctrl+Delete: Delete current note
        """

        tutorial_label = tk.Text(tuto_window, wrap=tk.WORD, font=("Segoe UI", 11),
                                bg=self.bg_color, fg=self.fg_color, relief=tk.FLAT, bd=0,
                                selectbackground=self.tree_select_bg, highlightthickness=0)
        tutorial_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tutorial_label.insert(tk.END, tutorial_text)
        tutorial_label.config(state=tk.DISABLED)

    def change_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"

        # Update theme colors
        self.update_theme_colors()

        # Update root window
        self.root.config(bg=self.bg_color)

        # Update main frame
        self.main_frame.config(bg=self.bg_color)

        # Update text boxes and their frames
        self.txtBox.config(fg=self.fg_color, bg=self.bg_color, insertbackground=self.fg_color, selectbackground=self.tree_select_bg)
        self.aitxtBox.config(fg=self.fg_color, bg=self.bg_color, insertbackground=self.fg_color, selectbackground=self.tree_select_bg)
        self.bubble.config(fg=self.fg_color, bg=self.bg_color, insertbackground=self.fg_color, selectbackground=self.tree_select_bg)

        # Update textbox frames and labels
        self.main_editor_frame.config(bg=self.textbox_border)
        self.ai_input_frame.config(bg=self.textbox_border)
        self.ai_response_frame.config(bg=self.textbox_border)

        # Update frame labels
        for frame in [self.main_editor_frame, self.ai_input_frame, self.ai_response_frame]:
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg=self.textbox_border, fg=self.fg_color)

        # Update frames
        self.top_frame.config(bg=self.top_frame_color)
        self.sidebar_frame.config(bg=self.sidebar_bg)
        self.search_frame.config(bg=self.sidebar_bg)
        self.notes_list_frame.config(bg=self.sidebar_bg)

        # Update search entry
        self.search_entry.config(bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)

        # Update buttons
        for widget in self.top_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=self.button_bg, fg=self.button_fg,
                            activebackground=self.button_hover_bg, activeforeground=self.button_fg)

        # Update treeview
        style = ttk.Style()
        style.configure("Treeview",
                       background=self.tree_bg,
                       foreground=self.tree_fg,
                       fieldbackground=self.tree_field_bg)
        style.map('Treeview', background=[('selected', self.tree_select_bg)])
        style.configure("Treeview.Heading", background=self.top_frame_color, foreground=self.fg_color)

# Run application
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartNotesApp(root)
    root.mainloop()
