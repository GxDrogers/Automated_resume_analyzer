
# 🧠 Automated Resume/Document Analyzer  
**Created by:** *Midhun Haridas*  

## 📘 Project Overview  
The **Automated Resume/Document Analyzer** is a Python-based application that compares a **candidate’s resume** with a **job description** to determine how well the resume matches the job requirements.  

It extracts text, identifies key skills and keywords, and calculates a **similarity score**. The system also lists **missing keywords** from the resume to help job seekers improve their resumes.  

The project features a **modern Tkinter GUI** with a teal-green themed interface for an attractive user experience.  

---

## 🚀 Features  
- 📄 Upload **Job Description (PDF/Text)**  
- 📑 Upload **Resume (PDF/Text)**  
- 🧩 Automatic **Keyword Extraction**  
- 🔍 Calculates **Similarity Score (%)**  
- ⚠️ Shows **Missing Skills/Keywords**  
- 💅 Simple and Beautiful **Tkinter GUI** (Teal theme)  
- ⚡ Lightweight & Runs Fully Offline  

---

## 🧰 Tech Stack  
| Component | Technology Used |
|------------|----------------|
| Programming Language | Python |
| GUI Framework | Tkinter |
| NLP & Text Processing | NLTK, re, collections |
| PDF Text Extraction | PyPDF2 |
| Data Visualization | Built-in Tkinter labels & color cues |
| File Handling | os, filedialog |

---

## 📂 Project Structure
```
Automated_Resume_Analyzer/
│
├── main.py                    # Main GUI and logic file
├── Job_Description.pdf         # Sample Job Description
├── Resume_1.pdf                # Example Resume (Good Match)
├── Resume_2.pdf                # Example Resume (Weak Match)
├── requirements.txt            # List of dependencies
└── README.md                   # Project documentation (this file)
```

---

## 🧑‍💻 How It Works  

1. The user uploads a **job description** and a **resume** (PDF or text file).  
2. The app extracts raw text using **PyPDF2**.  
3. The text is tokenized and cleaned (lowercase, removing stopwords and punctuation).  
4. It identifies keywords (mostly skill-related terms).  
5. It compares job description keywords and resume keywords using **set similarity logic**.  
6. The system calculates a **similarity score** =  
   (Number of matching keywords / Total job description keywords) × 100  
7. The GUI displays:  
   - ✅ Similarity Percentage  
   - ⚠️ Missing Keywords  

---

## 🧪 Example Results  

**Input Files:**  
- Job_Description.pdf → *Data Analyst (Junior)*  
- Resume_1.pdf → *Alex Johnson*  
- Resume_2.pdf → *Sarah Lee*  

**Output Preview:**  
| Resume | Match % | Missing Keywords |
|---------|----------|------------------|
| Resume_1 | 84% | machine learning, statistics |
| Resume_2 | 41% | python, sql, data visualization, power bi |

---

## 🖥️ GUI Preview  
🟢 Teal green themed window with:  
- Two upload buttons (Job Description & Resume)  
- “Analyze” button  
- Results section showing match score and missing skills  

---

## ⚙️ Installation & Usage  

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/midhunharidas/Automated-Resume-Analyzer.git
cd Automated-Resume-Analyzer
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the App
```bash
python main.py
```

### 4️⃣ Upload PDFs and Click “Analyze”
The GUI will instantly show your **match percentage** and **missing skills**.

---

## 🧾 requirements.txt
```
nltk
PyPDF2
tk
```

---

## 💡 Future Improvements
- Integrate AI (e.g., spaCy or BERT) for semantic keyword matching.  
- Add resume suggestions or rewording tips.  
- Export report as a PDF summary.  
- Deploy as a web app using Streamlit or Flask.  

---

## 🏆 Author
**Midhun Haridas**  
💼 *Aspiring Data Analyst | Python Developer | Innovator*  
🔗 [LinkedIn Profile](https://linkedin.com/in/midhunharidas) *(add your actual link)*  
