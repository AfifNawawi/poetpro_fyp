# PoetPro – Malay Pantun & Syair Checker

PoetPro is a mobile-based Final Year Project (FYP) application designed to analyse and improve traditional Malay poetry, specifically **Pantun** and **Syair**. The system evaluates poems based on structural rules, linguistic correctness, and semantic coherence, and provides guided suggestions when errors are detected.

---

## 🎯 Objectives

- Analyse Pantun and Syair according to traditional poetic rules  
- Validate line count, rhyme patterns, and syllable consistency  
- Detect grammatical and semantic issues in Malay text  
- Provide AI-assisted suggestions while preserving traditional style  

---

## 🧠 System Approach

PoetPro uses a **hybrid architecture**:
- **Rule-based analysis** (line count, rhyme scheme, syllables) using NLTK and custom rules
- **Semantic and grammar analysis** using mBERT and Sentence-BERT
- **Retrieval-Augmented Generation (RAG)** with FAISS to ensure traditional style consistency
- **Controlled AI generation** using Gemini LLM

AI suggestions are only triggered when rule-based validation fails.

---

## 🏗️ Technology Stack

- **Frontend:** Flutter (Mobile App)
- **Backend:** Flask REST API (Python)
- **NLP & AI:** NLTK, spaCy, Sentence-Transformers, mBERT, Gemini LLM
- **Vector Database:** FAISS (Pantun & Syair corpus)

---

---

## 🧪 Testing & Evaluation

- Unit and integration testing for rule-based analysis, AI engine, and retriever modules
- User Acceptance Testing (UAT) conducted with  
  **Dr. Nur Syazwani Binti Ahmad**,  
  Pusat Asasi Sains, Universiti Malaya

---

## 📦 Notes

- Large datasets and trained models are excluded due to size limitations  
- Project developed for academic and research purposes  
- Supports standard Bahasa Melayu (BM)

---

## 👤 Author

**Afif Nawawi**  
Final Year Project (FYP) – Artificial Intelligence

## 📁 Project Structure

