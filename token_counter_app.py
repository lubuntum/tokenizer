import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD

from services.token_counter_service import TOKENIZERS, count_project_tokens
from styles.UITheme import UITheme
from ui_components import UIComponents
from config.Config import Config


class TokenCounterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)

        # Load saved theme or use default
        saved_theme = Config.get("theme", "default_theme")

        # Initialize theme and UI components
        self.theme = UITheme(saved_theme)
        self.ui = UIComponents(self.theme)
        self.current_theme = saved_theme

        # Window configuration
        self.title("Token Counter Pro")
        self.geometry(self.theme.window_size)
        self.configure(fg_color=self.theme.window_bg)

        # Create GUI elements
        self.create_widgets()

        # Enable drag-drop
        self.path_entry.drop_target_register(DND_FILES)
        self.path_entry.dnd_bind('<<Drop>>', self.drop_path)

    def switch_theme(self, theme_name):
        """Switch application theme and save preference"""
        if theme_name == self.current_theme:
            return

        self.current_theme = theme_name
        self.theme.switch_theme(theme_name)

        # Save theme preference
        Config.set("theme", theme_name)

        # Update window background
        self.configure(fg_color=self.theme.window_bg)

        # Recreate widgets
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

        # Re-enable drag-drop
        self.path_entry.drop_target_register(DND_FILES)
        self.path_entry.dnd_bind('<<Drop>>', self.drop_path)

    def drop_path(self, event):
        path = event.data.strip('{}')
        self.path_entry.delete(0, "end")
        self.path_entry.insert(0, path)

    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = ctk.CTkFrame(
            self,
            fg_color=self.theme.main_frame_bg,
            corner_radius=self.theme.main_frame_corner
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with title and theme selector
        self.theme_menu = self.ui.create_header(main_frame, self)
        self.theme_menu.set(self.current_theme)  # Set current theme in dropdown

        # Path section
        self.path_entry = self.ui.create_path_section(main_frame, self.browse_path)

        # Model section
        self.model_menu = self.ui.create_model_section(
            main_frame,
            list(TOKENIZERS.keys()),
            "gpt-4o"
        )

        # Analyze button
        self.ui.create_analyze_button(main_frame, self.analyze_tokens)

        # Results section
        results = self.ui.create_results_section(main_frame)
        self.folder_card = results['folder_card']
        self.model_card = results['model_card']
        self.tokens_card = results['tokens_card']
        self.files_card = results['files_card']
        self.extensions_card = results['extensions_card']
        self.results_container = results['container']
        self.stats_frame = results['stats_frame']

        # Progress bar
        self.progress_bar = self.ui.create_progress_bar(main_frame)

        # Initially hide results
        self.hide_results()

    def hide_results(self):
        """Hide all result cards"""
        self.folder_card.master.pack_forget()
        self.model_card.master.pack_forget()
        self.stats_frame.pack_forget()

    def show_results(self):
        """Show all result cards"""
        self.folder_card.master.pack(fill="x", pady=5)
        self.model_card.master.pack(fill="x", pady=5)
        self.stats_frame.pack(fill="x", pady=(10, 0))

    def browse_path(self):
        """Browse for folder"""
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)

    def analyze_tokens(self):
        """Analyze tokens in selected path"""
        path = self.path_entry.get().strip()

        if not path:
            messagebox.showerror("Error", "Please provide a project path")
            return

        if not os.path.exists(path):
            messagebox.showerror("Error", "Path does not exist")
            return

        model = self.model_menu.get()

        # Show progress bar
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0.5)
        self.progress_bar.start()

        # Run analysis in background
        def run_analysis():
            try:
                result = count_project_tokens(path, model)
                total_tokens, extensions, file_count = result
                self.after(0, self.update_results, total_tokens, extensions, file_count, path, model)
            except Exception as e:
                self.after(0, self.show_error, str(e))

        threading.Thread(target=run_analysis, daemon=True).start()

    def update_results(self, total_tokens, extensions, file_count, path, model):
        """Update results display"""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

        # Get folder name from path
        folder_name = os.path.basename(os.path.normpath(path))

        # Update values
        self.folder_card.configure(text=folder_name)
        self.model_card.configure(text=model)
        self.tokens_card.configure(text=f"{total_tokens:,}")
        self.files_card.configure(text=str(file_count))
        self.extensions_card.configure(text=f"{len(extensions)} types")

        # Show results
        self.show_results()

    def show_error(self, error_message):
        """Show error message"""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        messagebox.showerror("Error", f"Analysis failed: {error_message}")


if __name__ == "__main__":
    app = TokenCounterApp()
    app.mainloop()