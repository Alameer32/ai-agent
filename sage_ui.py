import customtkinter as ctk
import threading
from sage_backend import ask_ollama  # We'll connect this to your existing backend

# Initialize customtkinter theme
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
conversation = []

class SageApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SAGE - Your AI Assistant")
        self.geometry("600x700")

        # Chat Display
        self.chat_display = ctk.CTkTextbox(self, width=560, height=500, wrap="word")
        self.chat_display.pack(padx=20, pady=20)
        self.chat_display.insert("end", "🤖 SAGE: Hello, I am ready to assist you.\n")
        self.chat_display.configure(state="disabled")

        # User Input Field
        self.user_input = ctk.CTkEntry(self, width=400, placeholder_text="Type your request here...")
        self.user_input.pack(pady=10)
        self.user_input.bind("<Return>", self.handle_user_input)

        # Send Button
        self.send_button = ctk.CTkButton(self, text="Send", command=self.handle_user_input)
        self.send_button.pack(pady=10)

    def handle_user_input(self, event=None):
        user_text = self.user_input.get()
        if user_text.strip() == "":
            return

        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n🧑 You: {user_text}\n")
        self.chat_display.configure(state="disabled")
        self.user_input.delete(0, 'end')

        # Run AI response in a thread to avoid freezing UI
        threading.Thread(target=self.get_response, args=(user_text,)).start()

    def get_response(self, user_input):
        try:
            response = ask_ollama(user_input,conversation)
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"🤖 SAGE: {response}\n")
            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")
        except Exception as e:
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"[Error]: {e}\n")
            self.chat_display.configure(state="disabled")

if __name__ == "__main__":
    app = SageApp()
    app.mainloop()
