# Text-Processor

A modern Python desktop application built with CustomTkinter, combining three powerful text utilities into one sleek, dark-mode compatible interface. Simple, beginner-friendly, and highly performant.

### 📝 About the Project
This project upgrades standard text-processing utilities with a clean, responsive GUI. It features smart regex-based text parsing and handles large files gracefully without freezing.

### ✨ Features
* **Word Frequency Analyzer**
  Select any text file using the built-in file browser. The app reads the file, smartly extracts words (preserving contractions like "don't" using regex), and displays a clean tabular list of the top 1,000 most frequent words.
* **Palindrome Checker**
  Enter any sentence or phrase to check if it reads the same forwards and backwards—automatically ignoring spaces, punctuation, and case sensitivity.
* **Caesar Cipher Tool**
  Encrypt or decrypt text using a customizable shift value. Letters are safely rotated mathematically while punctuation and spaces are perfectly preserved.
* **Modern UI**
  Built with CustomTkinter for a native look, rounded corners, and system-synced dark/light mode.

### 🛠 Tech Stack
* **Python 3.x**
* **CustomTkinter** (Modern GUI framework)
* **re** (Regex for advanced word boundary parsing)
* **collections.Counter** (High-performance counting)
