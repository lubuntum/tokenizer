import customtkinter as ctk

from styles.UITheme import UITheme


class UIComponents:
    """UI component builders to keep main app clean"""

    def __init__(self, theme: UITheme):
        self.theme = theme

    def create_header(self, parent, controller):
        """Create header with title and theme selector"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))

        # Title container
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(side="left", fill="x", expand=True)

        title_label = ctk.CTkLabel(
            title_container,
            text="Token Counter",
            font=self.theme.title_font(),
            text_color=self.theme.title_color,
            anchor="w"
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            title_container,
            text="Analyze token usage in your codebase",
            font=self.theme.subtitle_font(),
            text_color=self.theme.get("subtitle", "color"),
            anchor="w"
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))

        # Theme selector
        theme_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        theme_container.pack(side="right", padx=(10, 0))

        theme_menu = ctk.CTkOptionMenu(
            theme_container,
            values=self.theme.get_available_themes(),
            command=controller.switch_theme,
            width=130,
            height=32,
            font=ctk.CTkFont(size=12),
            fg_color=self.theme.get("entry", "background"),
            button_color=self.theme.get("dropdown", "button"),
            button_hover_color=self.theme.get("dropdown", "hover"),
            text_color=self.theme.get("entry", "text"),
            dropdown_fg_color=self.theme.get("dropdown", "menu_background"),
            dropdown_hover_color=self.theme.get("dropdown", "menu_hover"),
            dropdown_text_color=self.theme.get("dropdown", "menu_text"),
            corner_radius=self.theme.get("buttons", "corner_radius")
        )
        theme_menu.pack(side="right")
        theme_menu.set("default_theme")

        return theme_menu

    def create_path_section(self, parent, browse_command):
        """Create path input section"""
        path_frame = ctk.CTkFrame(parent, fg_color="transparent")
        path_frame.pack(fill="x", padx=30, pady=(20, 5))

        path_label = ctk.CTkLabel(
            path_frame,
            text="Project Path:",
            font=self.theme.label_font(),
            text_color=self.theme.get("labels", "color")
        )
        path_label.pack(anchor="w")

        path_entry_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_entry_frame.pack(fill="x", pady=(5, 0))

        path_entry = ctk.CTkEntry(
            path_entry_frame,
            placeholder_text="Drop folder here or browse...",
            height=self.theme.get("entry", "height"),
            font=self.theme.entry_font(),
            fg_color=self.theme.get("entry", "background"),
            border_color=self.theme.get("entry", "border"),
            text_color=self.theme.get("entry", "text"),
            placeholder_text_color=self.theme.get("entry", "placeholder")
        )
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = ctk.CTkButton(
            path_entry_frame,
            text="Browse",
            command=browse_command,
            width=100,
            height=self.theme.get("buttons", "height"),
            fg_color=self.theme.get("buttons", "browse", "background"),
            hover_color=self.theme.get("buttons", "browse", "hover"),
            font=self.theme.button_font(),
            corner_radius=self.theme.get("buttons", "corner_radius")
        )
        browse_btn.pack(side="right")

        return path_entry

    def create_model_section(self, parent, models_list, default_model):
        """Create model selection section"""
        model_frame = ctk.CTkFrame(parent, fg_color="transparent")
        model_frame.pack(fill="x", padx=30, pady=(15, 5))

        model_label = ctk.CTkLabel(
            model_frame,
            text="Tokenizer Model:",
            font=self.theme.label_font(),
            text_color=self.theme.get("labels", "color")
        )
        model_label.pack(anchor="w")

        model_menu = ctk.CTkOptionMenu(
            model_frame,
            values=models_list,
            height=self.theme.get("entry", "height"),
            font=self.theme.entry_font(),
            fg_color=self.theme.get("dropdown", "background"),
            button_color=self.theme.get("dropdown", "button"),
            button_hover_color=self.theme.get("dropdown", "hover"),
            text_color=self.theme.get("dropdown", "text"),
            dropdown_fg_color=self.theme.get("dropdown", "menu_background"),
            dropdown_hover_color=self.theme.get("dropdown", "menu_hover"),
            dropdown_text_color=self.theme.get("dropdown", "menu_text"),
            corner_radius=self.theme.get("buttons", "corner_radius")
        )
        model_menu.pack(fill="x", pady=(5, 0))
        model_menu.set(default_model)

        return model_menu

    def create_analyze_button(self, parent, analyze_command):
        """Create analyze button"""
        analyze_btn = ctk.CTkButton(
            parent,
            text="Analyze Tokens",
            command=analyze_command,
            height=self.theme.get("buttons", "height"),
            font=self.theme.button_font(),
            fg_color=self.theme.get("buttons", "analyze", "background"),
            hover_color=self.theme.get("buttons", "analyze", "hover"),
            corner_radius=self.theme.get("buttons", "corner_radius")
        )
        analyze_btn.pack(fill="x", padx=30, pady=(20, 10))

        return analyze_btn

    def create_results_section(self, parent):
        """Create results section with cards"""
        results_label = ctk.CTkLabel(
            parent,
            text="Results",
            font=ctk.CTkFont(
                size=self.theme.get("results", "title_size"),
                weight="bold"
            ),
            text_color=self.theme.get("results", "title_color")
        )
        results_label.pack(pady=(10, 10))

        results_container = ctk.CTkFrame(parent, fg_color="transparent")
        results_container.pack(fill="x", padx=30, pady=(0, 20))

        # Folder name card
        folder_card = self.create_result_card(results_container, "📁 Folder")

        # Model card
        model_card = self.create_result_card(results_container, "AI Model")

        # Stats row
        stats_frame = ctk.CTkFrame(results_container, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(10, 0))

        # Create stat cards
        tokens_card = self.create_stat_card(stats_frame, "📈 Total Tokens", 0)
        files_card = self.create_stat_card(stats_frame, "📁 Files Scanned", 1)
        extensions_card = self.create_stat_card(stats_frame, "🔤 Extensions", 2)

        return {
            'container': results_container,
            'folder_card': folder_card,
            'model_card': model_card,
            'tokens_card': tokens_card,
            'files_card': files_card,
            'extensions_card': extensions_card,
            'stats_frame': stats_frame
        }

    def create_result_card(self, parent, label_text):
        """Create a result card with label and value"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.theme.get("cards", "background"),
            corner_radius=self.theme.get("cards", "corner_radius")
        )
        card.pack(fill="x", pady=5)

        label = ctk.CTkLabel(
            card,
            text=label_text,
            font=self.theme.card_label_font(),
            text_color=self.theme.get("cards", "label_color")
        )
        label.pack(side="left", padx=15, pady=10)

        value_label = ctk.CTkLabel(
            card,
            text="—",
            font=self.theme.card_value_font(),
            text_color=self.theme.get("cards", "value_color")
        )
        value_label.pack(side="right", padx=15, pady=10)

        return value_label

    def create_stat_card(self, parent, label_text, column):
        """Create a stat card for the stats row"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.theme.get("stat_cards", "background"),
            corner_radius=self.theme.get("stat_cards", "corner_radius")
        )
        card.grid(row=0, column=column, padx=5, sticky="nsew")

        parent.grid_columnconfigure(column, weight=1)

        value_label = ctk.CTkLabel(
            card,
            text="—",
            font=self.theme.stat_value_font(),
            text_color=self.theme.get("stat_cards", "value_color")
        )
        value_label.pack(pady=(15, 5))

        label = ctk.CTkLabel(
            card,
            text=label_text,
            font=self.theme.stat_label_font(),
            text_color=self.theme.get("stat_cards", "label_color")
        )
        label.pack(pady=(0, 15))

        return value_label

    def create_progress_bar(self, parent):
        """Create progress bar"""
        progress_bar = ctk.CTkProgressBar(
            parent,
            fg_color=self.theme.get("progress_bar", "background"),
            progress_color=self.theme.get("progress_bar", "color"),
            height=self.theme.get("progress_bar", "height"),
            width=400
        )
        progress_bar.pack(pady=(0, 10))
        progress_bar.set(0)
        progress_bar.pack_forget()

        return progress_bar