"""
Enhanced Movie Ticket Booking System - Frontend
Features: Improved UI, validation, error handling, and user feedback
"""

from tkinter import *
from tkinter import ttk, messagebox
import movie_backend as backend

class MovieManagementSystem:
    """Main application class for movie management"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Management System")
        self.root.geometry("1400x800+50+50")
        self.root.config(bg="#1a1a1a")
        self.root.resizable(True, True)
        
        # StringVars for form fields
        self.movie_id = StringVar()
        self.movie_name = StringVar()
        self.release_date = StringVar()
        self.director = StringVar()
        self.cast = StringVar()
        self.budget = StringVar()
        self.duration = StringVar()
        self.rating = StringVar()
        
        # Track selected record
        self.selected_record = None
        
        # Initialize database
        backend.MovieData()
        
        # Build UI
        self.create_widgets()
        self.refresh_movie_list()
    
    def create_widgets(self):
        """Create all UI components"""
        
        # Title Frame
        title_frame = Frame(self.root, bg="#1a1a1a", bd=0)
        title_frame.pack(side=TOP, fill=X, padx=20, pady=10)
        
        title_label = Label(
            title_frame,
            text="🎬 MOVIE MANAGEMENT SYSTEM",
            font=("Arial", 42, "bold"),
            bg="#1a1a1a",
            fg="#FF8C00"
        )
        title_label.pack()
        
        # Main Content Frame
        content_frame = Frame(self.root, bg="#1a1a1a")
        content_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Left Frame - Input Form
        left_frame = LabelFrame(
            content_frame,
            text="  Movie Information  ",
            font=("Arial", 16, "bold"),
            bg="#2a2a2a",
            fg="#FF8C00",
            bd=3,
            relief=RIDGE
        )
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        
        # Create input fields
        self.create_input_fields(left_frame)
        
        # Right Frame - Movie List
        right_frame = LabelFrame(
            content_frame,
            text="  Movie Database  ",
            font=("Arial", 16, "bold"),
            bg="#2a2a2a",
            fg="#FF8C00",
            bd=3,
            relief=RIDGE
        )
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
        
        # Create treeview for movie list
        self.create_movie_treeview(right_frame)
        
        # Button Frame
        button_frame = Frame(self.root, bg="#1a1a1a", bd=2)
        button_frame.pack(side=BOTTOM, fill=X, padx=20, pady=20)
        
        # Create buttons
        self.create_buttons(button_frame)
        
        # Status bar
        self.create_status_bar()
    
    def create_input_fields(self, parent):
        """Create input form fields"""
        fields = [
            ("Movie ID:", self.movie_id),
            ("Movie Name:", self.movie_name),
            ("Release Date:", self.release_date),
            ("Director:", self.director),
            ("Cast:", self.cast),
            ("Budget (Crores INR):", self.budget),
            ("Duration (Hrs):", self.duration),
            ("Rating (1-5):", self.rating)
        ]
        
        for idx, (label_text, var) in enumerate(fields):
            # Label
            label = Label(
                parent,
                text=label_text,
                font=("Arial", 14, "bold"),
                bg="#2a2a2a",
                fg="#FF8C00",
                anchor=W
            )
            label.grid(row=idx, column=0, sticky=W, padx=15, pady=12)
            
            # Entry
            entry = Entry(
                parent,
                textvariable=var,
                font=("Arial", 14),
                bg="#3a3a3a",
                fg="white",
                insertbackground="white",
                relief=FLAT,
                bd=5
            )
            entry.grid(row=idx, column=1, sticky=EW, padx=15, pady=12)
        
        parent.grid_columnconfigure(1, weight=1)
    
    def create_movie_treeview(self, parent):
        """Create treeview to display movies"""
        # Scrollbars
        vsb = Scrollbar(parent, orient=VERTICAL)
        hsb = Scrollbar(parent, orient=HORIZONTAL)
        
        # Treeview
        self.tree = ttk.Treeview(
            parent,
            columns=("ID", "Movie ID", "Name", "Date", "Director", "Cast", "Budget", "Duration", "Rating"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=20
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Define columns
        columns = {
            "ID": 50,
            "Movie ID": 80,
            "Name": 180,
            "Date": 100,
            "Director": 120,
            "Cast": 150,
            "Budget": 80,
            "Duration": 80,
            "Rating": 60
        }
        
        for col, width in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=CENTER if col in ["ID", "Rating", "Budget", "Duration"] else W)
        
        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#3a3a3a",
            foreground="white",
            fieldbackground="#3a3a3a",
            font=("Arial", 11)
        )
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#FF8C00", foreground="black")
        style.map("Treeview", background=[("selected", "#FF8C00")])
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_movie_select)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)
        vsb.grid(row=0, column=1, sticky=NS)
        hsb.grid(row=1, column=0, sticky=EW)
        
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
    
    def create_buttons(self, parent):
        """Create action buttons"""
        buttons = [
            ("➕ Add New", self.add_movie, "#28a745"),
            ("🔄 Update", self.update_movie, "#007bff"),
            ("🗑️ Delete", self.delete_movie, "#dc3545"),
            ("🔍 Search", self.search_movies, "#ffc107"),
            ("📋 Display All", self.refresh_movie_list, "#17a2b8"),
            ("🧹 Clear", self.clear_fields, "#6c757d"),
            ("❌ Exit", self.exit_application, "#343a40")
        ]
        
        for idx, (text, command, color) in enumerate(buttons):
            btn = Button(
                parent,
                text=text,
                font=("Arial", 14, "bold"),
                width=12,
                height=1,
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                command=command,
                cursor="hand2",
                relief=RAISED,
                bd=3
            )
            btn.grid(row=0, column=idx, padx=8, pady=5)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = Label(
            self.root,
            text="Ready",
            font=("Arial", 10),
            bg="#FF8C00",
            fg="black",
            anchor=W,
            relief=SUNKEN,
            bd=1
        )
        self.status_bar.pack(side=BOTTOM, fill=X)
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=message)
        self.root.after(3000, lambda: self.status_bar.config(text="Ready"))
    
    def validate_fields(self):
        """Validate required fields"""
        if not self.movie_id.get().strip():
            messagebox.showerror("Validation Error", "Movie ID is required!")
            return False
        if not self.movie_name.get().strip():
            messagebox.showerror("Validation Error", "Movie Name is required!")
            return False
        
        # Validate rating if provided
        if self.rating.get().strip():
            try:
                rating_val = float(self.rating.get())
                if rating_val < 0 or rating_val > 5:
                    messagebox.showerror("Validation Error", "Rating must be between 0 and 5!")
                    return False
            except ValueError:
                messagebox.showerror("Validation Error", "Rating must be a number!")
                return False
        
        return True
    
    def add_movie(self):
        """Add a new movie to database"""
        if not self.validate_fields():
            return
        
        success, message = backend.db.add_movie(
            self.movie_id.get().strip(),
            self.movie_name.get().strip(),
            self.release_date.get().strip(),
            self.director.get().strip(),
            self.cast.get().strip(),
            self.budget.get().strip(),
            self.duration.get().strip(),
            self.rating.get().strip()
        )
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_fields()
            self.refresh_movie_list()
            self.update_status("Movie added successfully")
        else:
            messagebox.showerror("Error", message)
    
    def update_movie(self):
        """Update selected movie"""
        if not self.selected_record:
            messagebox.showwarning("Warning", "Please select a movie to update!")
            return
        
        if not self.validate_fields():
            return
        
        success, message = backend.db.update_movie(
            self.selected_record[0],
            self.movie_id.get().strip(),
            self.movie_name.get().strip(),
            self.release_date.get().strip(),
            self.director.get().strip(),
            self.cast.get().strip(),
            self.budget.get().strip(),
            self.duration.get().strip(),
            self.rating.get().strip()
        )
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_fields()
            self.refresh_movie_list()
            self.update_status("Movie updated successfully")
        else:
            messagebox.showerror("Error", message)
    
    def delete_movie(self):
        """Delete selected movie"""
        if not self.selected_record:
            messagebox.showwarning("Warning", "Please select a movie to delete!")
            return
        
        response = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{self.selected_record[2]}'?"
        )
        
        if response:
            success, message = backend.db.delete_movie(self.selected_record[0])
            if success:
                messagebox.showinfo("Success", message)
                self.clear_fields()
                self.refresh_movie_list()
                self.update_status("Movie deleted successfully")
            else:
                messagebox.showerror("Error", message)
    
    def search_movies(self):
        """Search movies based on input fields"""
        results = backend.SearchMovieData(
            self.movie_id.get().strip(),
            self.movie_name.get().strip(),
            self.release_date.get().strip(),
            self.director.get().strip(),
            self.cast.get().strip(),
            self.budget.get().strip(),
            self.duration.get().strip(),
            self.rating.get().strip()
        )
        
        self.display_movies(results)
        self.update_status(f"Found {len(results)} movie(s)")
    
    def refresh_movie_list(self):
        """Refresh the movie list display"""
        movies = backend.ViewMovieData()
        self.display_movies(movies)
        stats = backend.db.get_statistics()
        self.update_status(f"Total Movies: {stats['total_movies']} | Avg Rating: {stats['average_rating']}")
    
    def display_movies(self, movies):
        """Display movies in treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert movies
        for movie in movies:
            self.tree.insert("", END, values=movie)
    
    def on_movie_select(self, event):
        """Handle movie selection from treeview"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_record = item['values']
            
            # Populate fields
            self.movie_id.set(self.selected_record[1])
            self.movie_name.set(self.selected_record[2])
            self.release_date.set(self.selected_record[3])
            self.director.set(self.selected_record[4])
            self.cast.set(self.selected_record[5])
            self.budget.set(self.selected_record[6])
            self.duration.set(self.selected_record[7])
            self.rating.set(self.selected_record[8])
    
    def clear_fields(self):
        """Clear all input fields"""
        self.movie_id.set("")
        self.movie_name.set("")
        self.release_date.set("")
        self.director.set("")
        self.cast.set("")
        self.budget.set("")
        self.duration.set("")
        self.rating.set("")
        self.selected_record = None
        self.update_status("Fields cleared")
    
    def exit_application(self):
        """Exit the application"""
        response = messagebox.askyesno(
            "Exit Application",
            "Are you sure you want to exit?"
        )
        if response:
            self.root.destroy()


def main():
    """Main entry point"""
    root = Tk()
    app = MovieManagementSystem(root)
    root.mainloop()


if __name__ == '__main__':
    main()