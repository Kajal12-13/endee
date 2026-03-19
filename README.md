# AI Resume Chatbot (using Endee Vector DB)

I built this project to show how we can use AI to make hiring much faster and smarter. Instead of just searching for keywords like "Python" or "Java," this chatbot uses **Semantic Search** to understand the actual meaning of what’s written in a resume.

## What this project does
Searching for candidates manually is slow. This app lets a recruiter upload a PDF resume, and then it "reads" the whole thing. The recruiter can then ask questions like "What are their top projects?" or "Tell me about their education," and the bot finds the exact section immediately.

## How I built it (System Design)
* **The Brain (Endee DB)**: I used the **Endee Vector Database** to store all the resume information. It's great because it doesn't just store text; it stores "vectors" (mathematical meanings of words).
* **The Parser**: I used `pdfplumber` to break the resume down into categories like Skills, Experience, and Education.
* **The AI Model**: I used the `all-MiniLM-L6-v2` model. This turns human sentences into 384 numbers (vectors) that the database can understand.
* **The App**: A simple **Flask** (Python) web interface where you can upload files and see the answers in real-time.

## Challenges I faced
Building this on my Windows machine was a bit tricky. The **Endee** core engine needs a very specific Linux setup (Clang-19 and C++20). 

**How I fixed it:**
I spent time fixing the `Dockerfile` and `install.sh` scripts so they work across different systems. I used `dos2unix` to make sure the scripts didn't break when moving from Windows to Linux. Even when the local database build was tough, I made sure my Python code was perfectly connected to the Endee API so the whole system stays reliable.

## Why this is useful
Standard search tools miss good people. For example, if a recruiter searches for "Web Developer" but a candidate wrote "Full Stack Engineer," a normal search might miss them. My bot understands they are the same thing, so the best candidates always show up.

## How to run it
1.  **Docker**: Make sure Docker Desktop is open.
2.  **Start Database**: Run `docker-compose up -d`.
3.  **Install Python stuff**: `pip install flask requests pdfplumber sentence-transformers`.
4.  **Launch**: Run `python AI_resume_chatbot/app.py` and go to `http://localhost:5000`.

---
*I have starred and forked the official Endee repository as part of this project setup.*