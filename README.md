# 🎯 AI Talent Scout
### Catalyst Hackathon — Deccan AI

An AI agent that reads a Job Description, finds the best matching candidates, simulates how they'd respond to a recruiter, and gives you a ranked shortlist.

---

## 🔗 Links

| | |
|---|---|
| **Live App** | [ai-talent-scout-9ghzwwwfawdeovmagkfpbs.streamlit.app](https://ai-talent-scout-9ghzwwwfawdeovmagkfpbs.streamlit.app) |
| **Demo Video** | [Watch on Loom](https://www.loom.com/share/b96f6eb56749417b95acc65c54f77e73) |
| **GitHub** | [AbishekVelan/ai-talent-scout](https://github.com/AbishekVelan/ai-talent-scout) |

---

## 🧩 What Problem Does It Solve?

Recruiters waste hours doing this manually:
- Reading JDs and figuring out what skills are needed
- Going through every candidate profile one by one
- Sending outreach messages and hoping candidates reply
- Trying to rank candidates with no clear system

**AI Talent Scout does all of this automatically.**

---

## 🚀 How It Works

```
You paste a Job Description
        ↓
AI reads it and extracts: skills needed, experience, job title
        ↓
Every candidate is scored on 3 things:
  • Skill Match  — do their skills match the JD?
  • Experience   — do they have enough years?
  • Role Fit     — is their current role similar? (AI judges this)
        ↓
AI pretends to message each candidate and simulates their reply
        ↓
AI reads the reply and decides: High / Medium / Low interest
        ↓
Final ranked list = Match Score (70%) + Interest Score (30%)
```

---

## 📐 Scoring Explained Simply

| Score | What it measures | How |
|-------|-----------------|-----|
| Skill Match | How many JD skills the candidate has | Simple overlap count |
| Experience Fit | How close their years of experience are | Penalty if under, small bonus if over |
| Role Fit | How similar their job title is | AI judges and gives 0–1 score |
| Interest Score | How keen they seem | AI simulates their reply, then classifies it |
| **Final Score** | Overall rank | Match × 0.7 + Interest × 0.3 |

---

## 🏗️ Architecture

```
+--------------------------------------------+
|            Streamlit Web App               |
|   JD input | sliders | ranked cards | CSV  |
+--------------------------------------------+
                      |
                      v
+--------------------------------------------+
|                  app.py                    |
|          Runs the full pipeline            |
+--------------------------------------------+
          |                      |
          v                      v
+------------------+    +--------------------+
|    utils.py      |    |    prompts.py      |
|  Scoring logic   |    |  4 AI prompt       |
|  LLM API calls   |    |  templates         |
+------------------+    +--------------------+
          |
          v
+------------------+
|   Groq API       |
| Llama 3.1 (LLM)  |
+------------------+
```

### What each file does

| File | Purpose |
|------|---------|
| `app.py` | The web app — UI, buttons, results display |
| `utils.py` | Scoring math + making AI calls |
| `prompts.py` | The instructions given to the AI for each task |
| `candidates.json` | List of 20 candidate profiles |
| `requirements.txt` | Python packages to install |

---

## 🛠️ Tech Stack

| What | Tool Used |
|------|-----------|
| Web UI | Streamlit |
| AI / LLM | Groq API (Llama 3.1 8B) |
| Language | Python |
| Candidate Data | JSON file (20 candidates) |
| Export | CSV download |

---

## ⚙️ Run It Locally

**Step 1 — Clone the repo**
```bash
git clone https://github.com/AbishekVelan/ai-talent-scout.git
cd ai-talent-scout
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Add your Groq API key**

Create a file called `.env` in the folder and paste this inside:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free key at [console.groq.com](https://console.groq.com)

**Step 4 — Run the app**
```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Sample Input & Output

**Job Description pasted:**
> We are hiring an ML Engineer with expertise in Deep Learning, PyTorch, and Computer Vision. Minimum 4 years of experience.

**Top 3 Results:**

| Rank | Candidate | Match | Interest | Final |
|------|-----------|-------|----------|-------|
| 🥇 1 | Mohudoom | 99% | High | 95% |
| 🥈 2 | Vignesh Kumar | 88% | High | 88% |
| 🥉 3 | Neya Mithra | 63% | High | 69% |

**Simulated reply from Mohudoom:**
> "This sounds like a great fit — I'm currently working on object detection and would love to learn more. When can we connect?"

---

## 🤖 How This Was Built

This project was built using **vibe coding** — describing what I wanted in plain English and letting AI (Claude + ChatGPT) help write and debug the code. The logic, design decisions, and overall architecture were mine; the AI helped turn ideas into working code faster.

---

## 👤 Author

**Abishek Velan M**
Submitted for: Catalyst Hackathon — Deccan AI

---

*Built with ❤️ and too much coffee.*
*Thanks to ChatGPT and Claude.*
