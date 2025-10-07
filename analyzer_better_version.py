import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import PyPDF2, re, nltk, matplotlib.pyplot as plt
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Download stopwords
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# ------------ Helper Functions ------------
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return ""

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = [word for word in text.split() if word not in stop_words and len(word) > 2]
    return " ".join(tokens)

def get_keywords(text, top_n=20):
    words = text.split()
    freq = Counter(words)
    return [word for word, count in freq.most_common(top_n)]

def calculate_similarity(text1, text2):
    cv = CountVectorizer().fit_transform([text1, text2])
    similarity = cosine_similarity(cv)[0][1]
    return round(similarity * 100, 2)

def plot_skill_overlap(jd_keywords, res_keywords):
    both = len(jd_keywords & res_keywords)
    only_jd = len(jd_keywords - res_keywords)
    only_res = len(res_keywords - jd_keywords)

    categories = ['Overlap', 'Only JD', 'Only Resume']
    values = [both, only_jd, only_res]

    plt.figure(figsize=(5,4))
    plt.bar(categories, values, color=['#008080','#66CCCC','#004D40'])
    plt.title("Skill Overlap Summary", fontsize=12)
    plt.ylabel("Count of Keywords")
    plt.tight_layout()
    plt.show()

def export_report(similarity, jd_keywords, res_keywords, missing):
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
    if not save_path:
        return

    c = canvas.Canvas(save_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 80, "Resume vs Job Description Analysis Report")

    c.setFont("Helvetica", 12)
    y = height - 120
    lines = [
        f"Similarity Score: {similarity}%",
        "",
        f"Job Description Keywords: {', '.join(jd_keywords)}",
        "",
        f"Resume Keywords: {', '.join(res_keywords)}",
        "",
        f"Missing Keywords in Resume: {', '.join(missing) if missing else 'None! Excellent match!'}"
    ]

    for line in lines:
        c.drawString(80, y, line)
        y -= 20
    c.save()
    messagebox.showinfo("Success", f"Report saved successfully at:\n{save_path}")


# ------------ GUI Functions ------------
def upload_job_desc():
    global job_desc_path
    job_desc_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt")])
    if job_desc_path:
        job_desc_label.config(text=f"Uploaded: {job_desc_path.split('/')[-1]}", fg="#004D40")

def upload_resume():
    global resume_path
    resume_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt")])
    if resume_path:
        resume_label.config(text=f"Uploaded: {resume_path.split('/')[-1]}", fg="#004D40")

def analyze_documents():
    global last_similarity, last_jd_keywords, last_res_keywords, last_missing

    try:
        jd_text = extract_text(job_desc_path)
        res_text = extract_text(resume_path)

        if not jd_text or not res_text:
            messagebox.showwarning("Warning", "Please upload valid files.")
            return

        jd_clean = preprocess(jd_text)
        res_clean = preprocess(res_text)

        jd_keywords = set(get_keywords(jd_clean))
        res_keywords = set(get_keywords(res_clean))

        similarity = calculate_similarity(jd_clean, res_clean)
        missing = jd_keywords - res_keywords

        # Save for export
        last_similarity, last_jd_keywords, last_res_keywords, last_missing = similarity, jd_keywords, res_keywords, missing

        result_box.config(state='normal')
        result_box.delete('1.0', tk.END)
        result_box.insert(tk.END, f"✅ Similarity Score: {similarity}%\n\n")
        result_box.insert(tk.END, f"🧠 Job Description Keywords:\n{', '.join(jd_keywords)}\n\n")
        result_box.insert(tk.END, f"👤 Resume Keywords:\n{', '.join(res_keywords)}\n\n")
        result_box.insert(tk.END, f"❌ Missing Keywords in Resume:\n{', '.join(missing) if missing else 'None! Great Match!'}")
        result_box.config(state='disabled')

        # Show skill overlap chart
        plot_skill_overlap(jd_keywords, res_keywords)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def export_pdf_report():
    try:
        export_report(last_similarity, last_jd_keywords, last_res_keywords, last_missing)
    except Exception:
        messagebox.showerror("Error", "Please analyze documents first before exporting report.")


# ------------ GUI Design ------------
root = tk.Tk()
root.title("Automated Resume/Document Analyzer")
root.geometry("750x650")
root.config(bg="#E0F2F1")

title_label = tk.Label(root, text="📄 Automated Resume/Document Analyzer", 
                       bg="#008080", fg="white", font=("Segoe UI", 16, "bold"), pady=10)
title_label.pack(fill="x")

frame = tk.Frame(root, bg="#E0F2F1")
frame.pack(pady=20)

job_btn = tk.Button(frame, text="Upload Job Description", command=upload_job_desc, 
                    bg="#008080", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=10, pady=5)
job_btn.grid(row=0, column=0, padx=15)

job_desc_label = tk.Label(frame, text="No file uploaded", bg="#E0F2F1", fg="gray", font=("Segoe UI", 10))
job_desc_label.grid(row=0, column=1)

resume_btn = tk.Button(frame, text="Upload Resume", command=upload_resume, 
                       bg="#008080", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=10, pady=5)
resume_btn.grid(row=1, column=0, padx=15, pady=10)

resume_label = tk.Label(frame, text="No file uploaded", bg="#E0F2F1", fg="gray", font=("Segoe UI", 10))
resume_label.grid(row=1, column=1)

analyze_btn = tk.Button(root, text="Analyze", command=analyze_documents, 
                        bg="#004D40", fg="white", font=("Segoe UI", 12, "bold"), relief="flat", padx=20, pady=8)
analyze_btn.pack(pady=10)

export_btn = tk.Button(root, text="Export Report to PDF", command=export_pdf_report,
                       bg="#66CCCC", fg="#004D40", font=("Segoe UI", 11, "bold"), relief="flat", padx=20, pady=6)
export_btn.pack(pady=5)

result_box = scrolledtext.ScrolledText(root, width=85, height=15, wrap=tk.WORD, font=("Consolas", 10))
result_box.pack(padx=20, pady=10)
result_box.config(state='disabled', bg="#FFFFFF", fg="#004D40")

footer = tk.Label(root, text="Created by Midhun | Powered by Python 🐍", 
                  bg="#E0F2F1", fg="#004D40", font=("Segoe UI", 9))
footer.pack(side="bottom", pady=10)

root.mainloop()
