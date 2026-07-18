import customtkinter as ctk
import threading
from main import load_docs, retrieve_relevant_doc, fetch_scryfall, ask_claude
from sentence_transformers import SentenceTransformer

# Load docs and vectors once at startup
model = SentenceTransformer("all-MiniLM-L6-v2")
docs = load_docs()
doc_texts = list(docs.values())
doc_vectors = model.encode(doc_texts)

chat_history = []

def handle_question():
    question = input_box.get("1.0", "end").strip()
    if not question:
        return

    submit_btn.configure(state="disabled", text="Thinking...")
    answer_box.configure(state="normal")
    answer_box.configure(state="disabled")

    def run():
        relevant_doc = retrieve_relevant_doc(question, docs, doc_vectors)
        card_context = fetch_scryfall(question)
        answer = ask_claude(question, relevant_doc + "\n\n" + card_context)
        chat_history.append({"question": question, "answer":answer})

        answer_box.configure(state="normal")
        answer_box.insert("end", f"You: {question}\n\n")
        answer_box.insert("end", f"Assistant: {answer}\n\n")
        answer_box.insert("end", "─" * 30 + "\n\n")
        answer_box.configure(state="disabled")
        submit_btn.configure(state="normal", text="Ask")

    threading.Thread(target=run, daemon=True).start()


# App setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("MTG Rules Assistant")
app.geometry("800x600")
app.resizable(True, True)

main_frame = ctk.CTkFrame(app, fg_color="#2e1c08")
main_frame.pack(fill="both", expand=True)

# Title
title_label = ctk.CTkLabel(main_frame, text="MTG Rules Assistant", font=ctk.CTkFont(family="MedievalSharp", size=20, weight="bold"), text_color="#f0c060")
title_label.pack(pady=(20, 10))

# Input box
input_box = ctk.CTkTextbox(main_frame, height=80, width=700, fg_color="#c8a96e", text_color="#1a1200")
input_box.pack(pady=(0, 10))
input_box.insert("end", "")

# Submit button
submit_btn = ctk.CTkButton(main_frame, text="Ask", command=handle_question, fg_color="#c8922a", hover_color="#e6a832", text_color="#1a0f00")
submit_btn.pack(pady=(0, 10))

# Answer box
answer_box = ctk.CTkTextbox(main_frame, height=380, width=700, state="disabled", wrap="word", fg_color="#c8a96e", text_color="#1a1200")
answer_box.pack(pady=(0, 20))

app.mainloop()

