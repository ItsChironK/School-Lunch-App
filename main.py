import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
from datetime import datetime
from tkcalendar import DateEntry

MENU = {
    "Cheeseburger": 5.00,
    "Pizza Slice": 4.00,
    "Chicken Sandwich": 4.50,
    "Fries": 2.50,
    "Milk": 1.00,
    "Juice": 1.50,
    "Water": 1.00,
    "Apple": 1.25,
    "Salad": 3.50,
    "Brownies": 2.00
}

START_BALANCE = 15.00

class Colors:
    BG_PRIMARY = "#F8F8F8"      # Light background
    BG_SECONDARY = "#FFFFFF"    # Card background
    SURFACE = "#F2F2F7"         # Surface
    
    PRIMARY = "#007AFF"          # iOS Blue
    PRIMARY_LIGHT = "#34C759"    # iOS Green accent
    ACCENT = "#FF3B30"           # Red for warnings
    SUCCESS = "#34C759"          # Green
    
    TEXT_PRIMARY = "#000000"     # Black text
    TEXT_SECONDARY = "#6E6E73"   # Gray text
    TEXT_TERTIARY = "#C7C7CC"    # Light gray
    
    SHADOW = "rgba(0, 0, 0, 0.08)"
    BORDER = "#E5E5EA"

# CUSTOM WIDGETS

class RoundedFrame(tk.Canvas):
    """Canvas-based rounded rectangle for shadow effects"""
    def __init__(self, parent, bg="#FFFFFF", radius=12, **kwargs):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0, **kwargs)
        self.bg_color = bg
        self.radius = radius

    def draw_rounded_rect(self):
        self.delete("bg")
        w = self.winfo_width()
        h = self.winfo_height()
        if w > 1 and h > 1:
            # Draw shadow
            self.create_oval(5, 5, 5+20, 5+20, fill="#00000015", outline="", tags="bg")
            # Draw main rounded rectangle
            self.create_round_rectangle(
                2, 2, w-2, h-2,
                radius=self.radius,
                fill=self.bg_color,
                outline="",
                tags="bg"
            )
            self.tag_lower("bg")

    def create_round_rectangle(self, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs)

class CardFrame(tk.Frame):
    """iOS-style card with shadow and rounded corners"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=Colors.BG_SECONDARY, **kwargs)
        self.configure(
            relief="flat",
            bd=0,
            highlightthickness=0
        )

class ModernButton(tk.Frame):
    """Premium iOS-style button with hover effects"""
    def __init__(self, parent, text="Button", command=None, variant="primary", **kwargs):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0, **kwargs)
        
        self.variant = variant
        self.command = command
        self.hovered = False
        
        # Color mapping
        if variant == "primary":
            self.bg_normal = Colors.PRIMARY
            self.bg_hover = "#0051D0"
            self.text_color = "white"
        elif variant == "secondary":
            self.bg_normal = Colors.SURFACE
            self.bg_hover = Colors.BORDER
            self.text_color = Colors.TEXT_PRIMARY
        elif variant == "success":
            self.bg_normal = Colors.SUCCESS
            self.bg_hover = "#2EBD57"
            self.text_color = "white"
        
        # Button container
        self.button_frame = tk.Frame(
            self,
            bg=self.bg_normal,
            highlightthickness=0,
            relief="flat"
        )
        self.button_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Button label
        self.label = tk.Label(
            self.button_frame,
            text=text,
            font=("Helvetica Neue", 17, "bold"),
            bg=self.bg_normal,
            fg=self.text_color,
            padx=20,
            pady=16
        )
        self.label.pack(fill="both", expand=True)
        
        # Bindings
        self.button_frame.bind("<Enter>", self._on_enter)
        self.button_frame.bind("<Leave>", self._on_leave)
        self.button_frame.bind("<Button-1>", self._on_click)
        self.label.bind("<Enter>", self._on_enter)
        self.label.bind("<Leave>", self._on_leave)
        self.label.bind("<Button-1>", self._on_click)

    def _on_enter(self, event):
        if not self.hovered:
            self.hovered = True
            self.button_frame.config(bg=self.bg_hover)
            self.label.config(bg=self.bg_hover)

    def _on_leave(self, event):
        self.hovered = False
        self.button_frame.config(bg=self.bg_normal)
        self.label.config(bg=self.bg_normal)

    def _on_click(self, event):
        if self.command:
            self.command()

# MAIN APPLICATION

class SchoolLunchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("School Lunch")
        self.geometry("420x900")
        self.resizable(False, False)
        self.configure(bg=Colors.BG_PRIMARY)
        
        # Configure styles
        self.setup_styles()
        
        # State
        self.balance = START_BALANCE
        self.student = {}
        self.order = []
        
        # Container
        self.container = tk.Frame(self, bg=Colors.BG_PRIMARY)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        self.current_frame = None
        
        # Create all frames
        for FrameClass in (LoginPage, ConfirmPage, MenuPage, CheckoutPage):
            frame = FrameClass(self.container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(LoginPage)
    
    def setup_styles(self):
        """Configure fonts"""
        self.font_title = tkFont.Font(family="Helvetica Neue", size=32, weight="bold")
        self.font_subtitle = tkFont.Font(family="Helvetica Neue", size=17, weight="bold")
        self.font_body = tkFont.Font(family="Helvetica Neue", size=16)
        self.font_small = tkFont.Font(family="Helvetica Neue", size=15)
        self.font_caption = tkFont.Font(family="Helvetica Neue", size=13)
    
    def show_frame(self, frame_class):
        """Bring frame to front"""
        frame = self.frames[frame_class]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

# LOGIN PAGE

class LoginPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=Colors.BG_PRIMARY)
        self.app = app
        
        # Header
        header = tk.Frame(self, bg=Colors.BG_PRIMARY)
        header.pack(fill="x", padx=20, pady=(40, 10))
        
        tk.Label(
            header,
            text="School Lunch",
            font=("Helvetica Neue", 40, "bold"),
            bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_PRIMARY
        ).pack(anchor="w")
        
        tk.Label(
            header,
            text="Get your favorite meals",
            font=("Helvetica Neue", 16),
            bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_SECONDARY
        ).pack(anchor="w")
        
        # Form container with scroll
        form_container = tk.Frame(self, bg=Colors.BG_PRIMARY)
        form_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Input fields
        self.entries = {}
        fields = [
            ("County", "e.g., County Name"),
            ("School", "e.g., North Atlanta"),
            ("Student Name", "Your full name"),
            ("Lunch ID", "Your 10-digit ID")
        ]
        
        for field, placeholder in fields:
            self._create_input_field(form_container, field, placeholder)
        
        # Button area
        button_area = tk.Frame(self, bg=Colors.BG_PRIMARY)
        button_area.pack(fill="x", padx=20, pady=(20, 40))
        
        ModernButton(
            button_area,
            text="Continue",
            command=self.submit,
            variant="primary",
            height=60
        ).pack(fill="x")
    
    def _create_input_field(self, parent, label, placeholder):
        """Create a modern input field"""
        field_frame = tk.Frame(parent, bg=Colors.BG_PRIMARY)
        field_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            field_frame,
            text=label,
            font=("Helvetica Neue", 15, "bold"),
            bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 8))
        
        entry = tk.Entry(
            field_frame,
            font=("Helvetica Neue", 16),
            bg=Colors.SURFACE,
            fg=Colors.TEXT_PRIMARY,
            relief="flat",
            bd=0,
            insertbackground=Colors.PRIMARY
        )
        entry.pack(fill="x", ipady=12)
        entry.insert(0, placeholder)
        
        # Placeholder behavior
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=Colors.TEXT_PRIMARY)
        
        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg=Colors.TEXT_SECONDARY)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.config(fg=Colors.TEXT_SECONDARY)
        
        self.entries[label] = entry
    
    def submit(self):
        """Validate and submit"""
        for field, entry in self.entries.items():
            value = entry.get()
            if not value or value.startswith("e.g.,") or value.startswith("Your"):
                messagebox.showerror("Error", f"Please enter your {field.lower()}")
                return
        
        self.app.student = {
            "county": self.entries["County"].get(),
            "school": self.entries["School"].get(),
            "name": self.entries["Student Name"].get(),
            "id": self.entries["Lunch ID"].get()
        }
        
        self.app.show_frame(ConfirmPage)

# CONFIRM PAGE

class ConfirmPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=Colors.BG_PRIMARY)
        self.app = app
        
        # Header
        header = tk.Frame(self, bg=Colors.BG_PRIMARY)
        header.pack(fill="x", padx=20, pady=(40, 30))
        
        tk.Label(
            header,
            text="Confirm Details",
            font=("Helvetica Neue", 34, "bold"),
            bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_PRIMARY
        ).pack(anchor="w")
        
        # Info card
        self.info_frame = CardFrame(self)
        self.info_frame.pack(fill="x", padx=20, pady=(0, 30))
        
        self.info_frame.pack_configure(ipady=20, ipadx=20)
        
        # Buttons
        button_area = tk.Frame(self, bg=Colors.BG_PRIMARY)
        button_area.pack(fill="x", padx=20, pady=(20, 40))
        
        ModernButton(
            button_area,
            text="Looks Good",
            command=self.on_confirm,
            variant="success",
            height=60
        ).pack(fill="x", pady=(0, 12))
        
        ModernButton(
            button_area,
            text="Edit",
            command=self.on_edit,
            variant="secondary",
            height=60
        ).pack(fill="x")
    
    def on_show(self):
        """Update info when page shown"""
        for widget in self.info_frame.winfo_children():
            widget.destroy()
        
        for key, value in self.app.student.items():
            row = tk.Frame(self.info_frame, bg=Colors.BG_SECONDARY)
            row.pack(fill="x", pady=10)
            
            tk.Label(
                row,
                text=key.title(),
                font=("Helvetica Neue", 14),
                bg=Colors.BG_SECONDARY,
                fg=Colors.TEXT_SECONDARY
            ).pack(anchor="w")
            
            tk.Label(
                row,
                text=value,
                font=("Helvetica Neue", 17, "bold"),
                bg=Colors.BG_SECONDARY,
                fg=Colors.TEXT_PRIMARY
            ).pack(anchor="w", pady=(4, 0))
    
    def on_confirm(self):
        self.app.show_frame(MenuPage)
    
    def on_edit(self):
        self.app.show_frame(LoginPage)

# MENU PAGE

class MenuPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=Colors.BG_PRIMARY)
        self.app = app
        self.vars = {}
        self.item_frames = {}
        
        # Top bar with balance
        top_bar = tk.Frame(self, bg=Colors.BG_PRIMARY)
        top_bar.pack(fill="x", padx=20, pady=(20, 0))
        
        tk.Label(
            top_bar,
            text="Menu",
            font=("Helvetica Neue", 34, "bold"),
            bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_PRIMARY
        ).pack(anchor="w", side="left")
        
        self.balance_label = tk.Label(
            top_bar,
            text="",
            font=("Helvetica Neue", 15, "bold"),
            bg=Colors.BG_PRIMARY,
            fg=Colors.PRIMARY
        )
        self.balance_label.pack(anchor="e", side="right")
        
        # Scroll container
        scroll_frame = tk.Frame(self, bg=Colors.BG_PRIMARY)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Canvas for scrolling
        canvas = tk.Canvas(scroll_frame, bg=Colors.BG_PRIMARY, highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=Colors.BG_PRIMARY)
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Menu items
        for item, price in MENU.items():
            self._create_menu_item(scrollable, item, price)
        
        # Bottom button area
        button_area = tk.Frame(self, bg=Colors.BG_PRIMARY)
        button_area.pack(fill="x", padx=20, pady=(20, 40))
        
        ModernButton(
            button_area,
            text="Proceed to Checkout",
            command=self.checkout,
            variant="primary",
            height=60
        ).pack(fill="x")
    
    def _create_menu_item(self, parent, item, price):
        """Create a menu item card"""
        var = tk.IntVar()
        self.vars[item] = var
        
        card = CardFrame(parent)
        card.pack(fill="x", pady=10)
        card.pack_configure(ipady=14, ipadx=16)
        
        self.item_frames[item] = card
        
        # Checkbox
        check_frame = tk.Frame(card, bg=Colors.BG_SECONDARY)
        check_frame.pack(fill="x")
        
        checkbox = tk.Checkbutton(
            check_frame,
            text=item,
            variable=var,
            font=("Helvetica Neue", 16),
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_PRIMARY,
            activebackground=Colors.BG_SECONDARY,
            activeforeground=Colors.PRIMARY,
            selectcolor=Colors.BG_SECONDARY,
            highlightthickness=0
        )
        checkbox.pack(anchor="w", side="left")
        
        price_label = tk.Label(
            check_frame,
            text=f"${price:.2f}",
            font=("Helvetica Neue", 16, "bold"),
            bg=Colors.BG_SECONDARY,
            fg=Colors.PRIMARY
        )
        price_label.pack(anchor="e", side="right")
    
    def on_show(self):
        """Update balance when shown"""
        self.balance_label.config(text=f"Balance: ${self.app.balance:.2f}")
    
    def checkout(self):
        """Process checkout"""
        self.app.order = []
        total = 0
        
        for item, var in self.vars.items():
            if var.get():
                self.app.order.append(item)
                total += MENU[item]
        
        if not self.app.order:
            messagebox.showwarning("No Items", "Please select at least one item")
            return
        
        if total > self.app.balance:
            messagebox.showerror("Insufficient Funds", f"Not enough balance. Need ${total:.2f}, have ${self.app.balance:.2f}")
            return
        
        self.app.balance -= total
        self.app.show_frame(CheckoutPage)

# checkout page 

class CheckoutPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=Colors.BG_PRIMARY)
        self.app = app
        
        # Success icon area
        icon_frame = tk.Frame(self, bg=Colors.BG_PRIMARY)
        icon_frame.pack(pady=(60, 30))
        
        tk.Label(
            icon_frame,
            text="✓",
            font=("Helvetica Neue", 80, "bold"),
            bg=Colors.BG_PRIMARY,
            fg=Colors.SUCCESS
        ).pack()
        
        # Title
        tk.Label(
            self,
            text="Order Confirmed",
            font=("Helvetica Neue", 34, "bold"),
            bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_PRIMARY
        ).pack()
        
        tk.Label(
            self,
            text="Your order is ready",
            font=("Helvetica Neue", 17),
            bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_SECONDARY
        ).pack(pady=(4, 30))
        
        # Order summary
        self.summary_card = CardFrame(self)
        self.summary_card.pack(fill="x", padx=20, pady=(0, 30))
        self.summary_card.pack_configure(ipady=20, ipadx=20)
        
        # Message
        msg_frame = tk.Frame(self, bg=Colors.BG_PRIMARY)
        msg_frame.pack(fill="x", padx=20, pady=(0, 30))
        
        tk.Label(
            msg_frame,
            text="📣 Your name will be called at lunch",
            font=("Helvetica Neue", 15),
            bg=Colors.BG_PRIMARY,
            fg=Colors.TEXT_SECONDARY,
            wraplength=280,
            justify="center"
        ).pack()
        
        # Button area
        button_area = tk.Frame(self, bg=Colors.BG_PRIMARY)
        button_area.pack(fill="x", padx=20, pady=(0, 40))
        
        ModernButton(
            button_area,
            text="Start New Order",
            command=self.new_order,
            variant="primary",
            height=60
        ).pack(fill="x")
    
    def on_show(self):
        """Update summary when shown"""
        for widget in self.summary_card.winfo_children():
            widget.destroy()
        
        # Student name
        name_frame = tk.Frame(self.summary_card, bg=Colors.BG_SECONDARY)
        name_frame.pack(fill="x", pady=(0, 16))
        
        tk.Label(
            name_frame,
            text=self.app.student["name"],
            font=("Helvetica Neue", 20, "bold"),
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_PRIMARY
        ).pack(anchor="w")
        
        # Divider
        tk.Frame(self.summary_card, bg=Colors.BORDER, height=1).pack(fill="x", pady=16)
        
        # Items
        for item in self.app.order:
            item_frame = tk.Frame(self.summary_card, bg=Colors.BG_SECONDARY)
            item_frame.pack(fill="x", pady=6)
            
            tk.Label(
                item_frame,
                text="•",
                font=("Helvetica Neue", 18),
                bg=Colors.BG_SECONDARY,
                fg=Colors.PRIMARY
            ).pack(side="left", padx=(0, 12))
            
            tk.Label(
                item_frame,
                text=item,
                font=("Helvetica Neue", 16),
                bg=Colors.BG_SECONDARY,
                fg=Colors.TEXT_PRIMARY
            ).pack(anchor="w", side="left")
        
        # Divider
        tk.Frame(self.summary_card, bg=Colors.BORDER, height=1).pack(fill="x", pady=16)
        
        # Balance
        balance_frame = tk.Frame(self.summary_card, bg=Colors.BG_SECONDARY)
        balance_frame.pack(fill="x")
        
        tk.Label(
            balance_frame,
            text="Remaining Balance",
            font=("Helvetica Neue", 14),
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_SECONDARY
        ).pack(anchor="w")
        
        tk.Label(
            balance_frame,
            text=f"${self.app.balance:.2f}",
            font=("Helvetica Neue", 22, "bold"),
            bg=Colors.BG_SECONDARY,
            fg=Colors.SUCCESS
        ).pack(anchor="w", pady=(4, 0))
    
    def new_order(self):
        """Start a new order"""
        self.app.show_frame(MenuPage)

if __name__ == "__main__":
    app = SchoolLunchApp()
    app.mainloop()
