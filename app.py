import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


# Define the main application class
class FederatedLearningApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Federated Learning for Healthcare")
        self.geometry("1024x720")

        # Initialize UI components
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Federated Learning for Healthcare",
                                        font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)

        # User Authentication
        self.auth_frame = ctk.CTkFrame(self)
        self.auth_frame.pack(pady=10, padx=20, fill="x")

        self.username_label = ctk.CTkLabel(self.auth_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = ctk.CTkEntry(self.auth_frame, width=200)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = ctk.CTkLabel(self.auth_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = ctk.CTkEntry(self.auth_frame, show="*", width=200)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = ctk.CTkButton(self.auth_frame, text="Login", command=self.authenticate_user,
                                          fg_color="#1e90ff", hover_color="#4682b4")
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Dataset Upload
        self.dataset_frame = ctk.CTkFrame(self)
        self.dataset_frame.pack(pady=10, padx=20, fill="x")

        self.upload_button = ctk.CTkButton(self.dataset_frame, text="Upload Dataset", command=self.upload_dataset,
                                           fg_color="#32cd32", hover_color="#228b22")
        self.upload_button.pack(side="left", padx=10, pady=10)

        self.dataset_label = ctk.CTkLabel(self.dataset_frame, text="No dataset uploaded.", anchor="w")
        self.dataset_label.pack(side="left", fill="x", padx=10, pady=10)

        # Training Progress
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.pack(pady=10, padx=20, fill="x")

        self.start_training_button = ctk.CTkButton(self.progress_frame, text="Start Training",
                                                   command=self.start_training,
                                                   fg_color="#ff4500", hover_color="#cd3700")
        self.start_training_button.pack(side="left", padx=10, pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=400)
        self.progress_bar.pack(side="left", padx=10, pady=10)

        # Performance Dashboard
        self.dashboard_frame = ctk.CTkFrame(self)
        self.dashboard_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.dashboard_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome to the Federated Learning Platform!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def upload_dataset(self):
        file_path = filedialog.askopenfilename(title="Select Dataset", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            encrypted_file = self.encrypt_file(file_path)
            self.dataset_label.configure(text=f"Dataset Encrypted: {encrypted_file}")
        else:
            self.dataset_label.configure(text="No dataset uploaded.")

    def encrypt_file(self, file_path):
        key = os.urandom(32)  # AES-256 key
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.EAX(os.urandom(16)), backend=backend)
        encryptor = cipher.encryptor()

        with open(file_path, 'rb') as f:
            plaintext = f.read()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, 'wb') as ef:
            ef.write(encryptor.tag + ciphertext)

        return encrypted_file_path

    def start_training(self):
        self.progress_bar.set(0)
        self.training_thread = threading.Thread(target=self.simulate_training)
        self.training_thread.start()

    def simulate_training(self):
        for i in range(101):
            time.sleep(0.1)
            self.progress_bar.set(i / 100.0)
            self.update_training_graph(i)

    def update_training_graph(self, step):
        self.ax.clear()
        self.ax.plot(range(step), [x ** 0.5 for x in range(step)], label="Training Accuracy")
        self.ax.set_title("Model Performance")
        self.ax.set_xlabel("Epochs")
        self.ax.set_ylabel("Accuracy")
        self.ax.legend()
        self.canvas.draw()


# Run the application
if __name__ == "__main__":
    app = FederatedLearningApp()
    app.mainloop()
