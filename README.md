# Fake News Detector

An AI-powered web application that analyzes news headlines for credibility.
Paste any headline and get an instant report with a credibility score, verdict,
flagged issues, and a suggested search query to verify the claim yourself.

## Files

**`backend/app.py`**
The main server. Receives a headline from the frontend, sends it to the AI, and returns the result. Also contains the system prompt that tells the AI how to analyze headlines.

**`backend/test.py`**
A simple script used during development to test the AI connection. Not part of the final app.

**`frontend/index.html`**
The entire frontend in one file. Contains the input form, styling, and the logic that displays the score, verdict, flags, and reasoning returned by the backend.
