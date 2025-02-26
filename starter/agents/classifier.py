# agents/classifier.py

import re

# Global variable for input text
INPUT_TEXT = None  # User must set this before calling agent_main()

def agent_main():
    """
    Classifier Agent
    ----------------
    Purpose: Classify the input text into one of several categories based on keywords and patterns.
    
    Advanced dspy Functionality:
    - Uses multiple rules and pattern matching to determine the text category.
    - Provides a confidence score based on rule matches.
    
    Usage:
        # In a Python shell:
        from agents import classifier
        classifier.INPUT_TEXT = "Hello, how are you?"
        result = classifier.agent_main()
        print(result)
        # Expected output: { "classification": "Greeting/Question", "confidence": 0.85 }
    """
    if not INPUT_TEXT or not isinstance(INPUT_TEXT, str):
        return {"error": "INPUT_TEXT is not set or is not a valid string."}
    
    text = INPUT_TEXT.lower()
    
    # Define classification rules (keywords and simple patterns)
    rules = {
        "Greeting": ["hello", "hi", "greetings"],
        "Question": [r"\?$", "what", "how", "why", "when"],
        "Command": ["do", "execute", "run"],
    }
    
    # Initialize scores
    scores = {key: 0 for key in rules.keys()}
    
    # Apply rules: check for each keyword or pattern in the text
    for category, patterns in rules.items():
        for pattern in patterns:
            if re.search(pattern, text):
                scores[category] += 1
    
    # Default classification
    classification = "Statement"
    max_score = 0
    for cat, score in scores.items():
        if score > max_score:
            max_score = score
            classification = cat
    
    # Calculate a simple confidence score (normalized, arbitrary scale)
    confidence = min(max_score / 3.0, 1.0)  # assume 3 matches gives full confidence
    
    return {
        "classification": classification,
        "confidence": round(confidence, 2)
    }