import asyncio
import tkinter as tk
from tkinter import messagebox
from truecallerpy import login, verify_otp, search_phonenumber, bulk_search
import threading

class TruecallerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Truecaller API Interaction")
        self.root.geometry("500x400")

        self.phone_number = None
        self.otp = None
        self.installation_id = None

        self.create_phone_frame()
        self.create_otp_frame()
        self.create_search_frame()

    def create_phone_frame(self):
        self.phone_frame = tk.Frame(self.root)
        self.phone_frame.pack(fill="both", expand=True)

        tk.Label(self.phone_frame, text="Phone Number (e.g., +1234567890):").pack(pady=10)
        self.phone_number_entry = tk.Entry(self.phone_frame, width=30)
        self.phone_number_entry.pack()

        tk.Button(self.phone_frame, text="Request OTP", command=self.start_request_otp).pack(pady=10)

    def create_otp_frame(self):
        self.otp_frame = tk.Frame(self.root)

        tk.Label(self.otp_frame, text="OTP:").pack(pady=5)
        self.otp_entry = tk.Entry(self.otp_frame, width=30)
        self.otp_entry.pack()

        tk.Button(self.otp_frame, text="Login", command=self.start_verify_otp).pack(pady=10)

    def create_search_frame(self):
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(fill="both", expand=True)
        self.search_frame.pack_forget()

        tk.Label(self.search_frame, text="Search Number (e.g., +9876543210):").pack(pady=10)
        self.search_number_entry = tk.Entry(self.search_frame, width=30)
        self.search_number_entry.pack()

        tk.Label(self.search_frame, text="Search Country Code (e.g., US, IN):").pack(pady=5)
        self.search_country_entry = tk.Entry(self.search_frame, width=30)
        self.search_country_entry.pack()

        tk.Label(self.search_frame, text="Bulk Numbers (comma separated, e.g., +1234567890,+9876543210):").pack(pady=10)
        self.bulk_numbers_entry = tk.Entry(self.search_frame, width=30)
        self.bulk_numbers_entry.pack()

        tk.Label(self.search_frame, text="Bulk Country Code (e.g., US, IN):").pack(pady=5)
        self.bulk_country_entry = tk.Entry(self.search_frame, width=30)
        self.bulk_country_entry.pack()

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.start_search, state=tk.DISABLED)
        self.search_button.pack(pady=10)

        self.bulk_search_button = tk.Button(self.search_frame, text="Bulk Search", command=self.start_bulk_search, state=tk.DISABLED)
        self.bulk_search_button.pack(pady=10)

        self.results_text = tk.Text(self.search_frame, height=10, width=50)
        self.results_text.pack(pady=10)

    def start_request_otp(self):
        self.run_async(self.request_otp)

    def start_verify_otp(self):
        self.run_async(self.verify_otp)

    def start_search(self):
        self.run_async(self.search)

    def start_bulk_search(self):
        self.run_async(self.bulk_search)

    def run_async(self, func):
        threading.Thread(target=asyncio.run, args=(func(),)).start()

    async def request_otp(self):
        self.phone_number = self.phone_number_entry.get()

        if not self.phone_number:
            self.show_message("Error", "Please enter the phone number.")
            return

        # Step 1: Request OTP from Truecaller
        self.update_results("Requesting OTP from Truecaller...")
        login_response = await login(self.phone_number)
        self.update_results(login_response)

        if login_response['status_code'] != 200:
            self.show_message("Error", "Failed to request OTP. Please try again.")
            return

        self.phone_frame.pack_forget()
        self.otp_frame.pack(fill="both", expand=True)

    async def verify_otp(self):
        self.otp = self.otp_entry.get()

        if not self.otp:
            self.show_message("Error", "Please enter the OTP.")
            return

        # Step 2: OTP Verification
        self.update_results("Verifying OTP with Truecaller...")
        verify_response = await verify_otp(self.phone_number, {}, self.otp)
        self.update_results(verify_response)

        if verify_response['status_code'] != 200:
            self.show_message("Error", "Failed to verify OTP. Please try again.")
            return

        installation_data = verify_response.get('data', {})
        self.installation_id = installation_data.get('installationId')
        if not self.installation_id:
            self.show_message("Error", "Failed to get installationId from verification response.")
            return

        # Switch to search frame
        self.otp_frame.pack_forget()
        self.search_frame.pack(fill="both", expand=True)

        # Enable search and bulk search buttons
        self.enable_search_buttons()

    async def search(self):
        search_number = self.search_number_entry.get()
        search_country = self.search_country_entry.get()

        if not search_number or not search_country:
            self.show_message("Error", "Please enter both search number and country code.")
            return

        # Step 3: Search for a Phone Number
        search_response = await search_phonenumber(search_number, search_country, self.installation_id)
        self.update_results(search_response)

    async def bulk_search(self):
        bulk_numbers = self.bulk_numbers_entry.get()
        bulk_country = self.bulk_country_entry.get()

        if not bulk_numbers or not bulk_country:
            self.show_message("Error", "Please enter both bulk numbers and country code.")
            return

        # Step 4: Bulk Phone Number Search
        bulk_search_response = await bulk_search(bulk_numbers, bulk_country, self.installation_id)
        self.update_results(bulk_search_response)

    def update_results(self, response):
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, f"Response: {response}\n\n")

    def enable_search_buttons(self):
        self.search_button.config(state=tk.NORMAL)
        self.bulk_search_button.config(state=tk.NORMAL)

    def show_message(self, title, message):
        messagebox.showerror(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = TruecallerUI(root)
    root.mainloop()
