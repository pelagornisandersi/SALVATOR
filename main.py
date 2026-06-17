import tkinter as tk
from tkinter import ttk
from analyzer import analyze_message
from tkinter import filedialog
from ocr import extract_text
import customtkinter as ctk

class ScamShieldAI:

    def __init__(self, root):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.root = root
        self.root.title("Salvator")
        self.root.geometry("1200x900")

        self.build_ui()


    def upload_image(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg")
            ]
        )

        if not file_path:
            return

        try:

            text = extract_text(file_path)

            self.input_box.delete(
                "1.0",
                tk.END
            )

            self.input_box.insert(
                tk.END,
                text
            )

            self.analyze()

        except Exception as e:

            self.input_box.delete(
                "1.0",
                tk.END
            )

            self.input_box.insert(
                tk.END,
                f"OCR Error:\n{e}"
            )

    def build_ui(self):

        title_label = ctk.CTkLabel(
            root,
            text="Salvator\nAI-Powered Scam Detection",
            font=("Chesna grotesk", 28, "bold")
        )
        title_label.pack(pady=10)

        subtitle = ctk.CTkLabel(
            self.root,
            text="Analyze messages for scams and phishing attempts",
            font=("Montserrat", 20, "bold")

        )
        subtitle.pack()

        ctk.CTkLabel(
            self.root,
            text="Paste a suspicious message here or upload a screenshot...",
            font=("Arial", 18)
        ).pack(anchor="w", padx=10, pady=(20, 5))

        self.input_box = ctk.CTkTextbox(
            self.root,
            width=700,
            height=180,
            corner_radius=20
        )
        self.input_box.pack(
            fill="x",
            padx=10
        )

        self.analyze_btn = ctk.CTkButton(
            self.root,
            text="Analyze",
            command=self.analyze,
            width=200,
            height=40,
            corner_radius=20
        )
        self.analyze_btn.pack(
            pady=15
        )

        self.upload_btn = ctk.CTkButton(
            self.root,
            text="Upload Screenshot",
            command=self.upload_image,
            width=200,
            height=40,
            corner_radius=20
        )

        self.upload_btn.pack(pady=5)


        self.risk_label = ctk.CTkLabel(
            self.root,
            text="Awaiting Analysis",
            font=("Segoe UI", 32, "bold")
        )

        self.risk_label.pack(pady=10)

        ctk.CTkLabel(
            self.root,
            text="Results:",
            font=("Arial", 18)
        ).pack(anchor="w", padx=10)

        self.output_box = ctk.CTkTextbox(
            self.root,
            width=700,
            height=250,
            corner_radius=10
        )
        self.output_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.output_box.configure(
           state="disabled"
        )

    def analyze(self):

        text = self.input_box.get(
            "1.0",
            tk.END
        ).strip()

        self.output_box.configure(
           state="normal"
        )

        self.output_box.delete(
            "1.0",
            tk.END
        )

        if not text:

            self.output_box.insert(
                tk.END,
                "Please enter a message."
            )

            self.output_box.configure(
                state="disabled"
            )

            return

        try:

            data = analyze_message(text)
            tactics = data.get(
                "manipulation_tactics",
                []
            )

            if tactics:
                tactics_text = "\n".join(
                    f"⚠ {t}"
                    for t in tactics
                )
            else:
                tactics_text = "None Detected"

            score = float(data["risk_score"])

            if score < 30:
                risk_level = "LOW RISK"
                self.risk_label.configure(
                    text=risk_level,
                    text_color="#22C55E"
                )

            elif score < 70:
                risk_level = "SUSPICIOUS"
                self.risk_label.configure(
                    text=risk_level,
                    text_color="#F59E0B"
                    
                )

            else:
                risk_level = "HIGH RISK"
                self.risk_label.configure(
                    text=risk_level,
                    text_color="#EF4444"
                )

            filled = min(10, round(score / 10))
            empty = 10 - filled

            meter = "█" * filled + "░" * empty

            self.output_box.insert(
                tk.END,
            
                f"""
            
            {risk_level}

            ══════════════════════════════

            Risk Meter:
            [{meter}] {score}/100

            Risk Score: {data['risk_score']}
            Verdict: {data['verdict']}
            Category: {data['category']}

            ══════════════════════════════

            Manipulation Tactics:
            {tactics_text}

            ══════════════════════════════

            Red Flags:
            {chr(10).join('- ' + flag for flag in data['red_flags'])}

            ══════════════════════════════

            Explanation:
            {data['explanation']}

            ══════════════════════════════

            Recommended Action:
            {data['recommended_action']}
            """
            )

            self.output_box.configure(
                state="disabled"
            )

        except Exception as e:

            self.output_box.insert(
                tk.END,
                f"Error:\n{e}"
            )


root = ctk.CTk()
app = ScamShieldAI(root)
root.mainloop()