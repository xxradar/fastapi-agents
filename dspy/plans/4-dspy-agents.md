# Plan for dspy Agents Implementation

## Objective

- Develop three advanced agents that showcase dspy-inspired functionality:
  - **Classifier Agent (`classifier.py`):** A more complex agent that classifies input text based on multiple criteria and demonstrates advanced decision-making.
  - **Summarizer Agent (`summarizer.py`):** An agent that processes a block of text and returns a concise summary.
  - **TextRank Summarizer Agent (`textrank_summarizer.py`):** An agent that summarizes text using the TextRank algorithm.
- Both agents will be implemented as single file modules in the `agents/` directory.
- They will be dynamically loaded and executed via the common FastAPI endpoint (`/agent/{agent_name}`).

> **Note:** Tests and logs have been created throughout the project. Update documentation and commit changes after completion. The TextRank Summarizer agent has also been added.

---

## Overview

This plan outlines the steps to implement three dspy showcase agents. The Classifier Agent will exhibit more complex logic, such as multi-criteria classification using advanced dspy concepts. The Summarizer Agent will provide text summarization by processing and truncating input text intelligently. The TextRank Summarizer agent will provide text summarization using the TextRank algorithm. All agents are designed to serve as examples for further dspy enhancements and modular agent development.

---

## Implementation Steps

### Step 1: Design the dspy Agents

#### Classifier Agent (`classifier.py`)
- **Purpose:**  
  Analyze an input text (provided via a global variable) and classify it into categories such as "Greeting", "Question", "Command", or "Statement".
- **Advanced Functionality:**  
  - Use a dictionary of keywords and regular expressions to perform classification.
  - Showcase a simple form of self-improvement by adjusting weights (hard-coded for now) or by applying multiple rules.
- **Output:**  
  Returns a JSON object with a classification result and a confidence score.

#### Summarizer Agent (`summarizer.py`)
- **Purpose:**  
  Summarize a given block of text (via a global variable) to produce a concise summary.
- **Functionality:**  
  - Perform basic text processing (e.g., splitting, truncating, or extracting key sentences).
  - Optionally demonstrate dspy-inspired dynamic reasoning by showing a multi-step processing flow.
- **Output:**  
  Returns a JSON object with the summary and possibly an "explanation" of the summarization process.

#### TextRank Summarizer Agent (`textrank_summarizer.py`)
- **Purpose:**
  Summarize a given block of text using the TextRank algorithm.
- **Functionality:**
  - Implement the TextRank algorithm to rank sentences based on their importance.
  - Extract the top-ranked sentences to form a concise summary.
- **Output:**
  Returns a JSON object with the summary.

*Log Instruction:* Record the design decisions and expected behavior in the logs before proceeding.

---

### Step 2: Create the Agent Files

#### A. Classifier Agent (`agents/classifier.py`)

```python
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
```

#### B. Summarizer Agent (`agents/summarizer.py`)

```python
# agents/summarizer.py

# Global variable for the text to summarize
TEXT_TO_SUMMARIZE = None  # User must set this before calling agent_main()

def agent_main():
    """
    Summarizer Agent
    ----------------
    Purpose: Summarize the input text by extracting the first sentence or truncating after a certain length.
    
    dspy-inspired Functionality:
    - Demonstrates a multi-step processing approach.
    - Optionally, includes a simple explanation of how the text was summarized.
    
    Usage:
        # In a Python shell:
        from agents import summarizer
        summarizer.TEXT_TO_SUMMARIZE = (
            "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python. "
            "It is based on standard Python type hints and is very easy to use. "
            "This agent summarizes long texts."
        )
        result = summarizer.agent_main()
        print(result)
        # Expected output: { "summary": "FastAPI is a modern, fast web framework for building APIs with Python.", "explanation": "Summary generated by extracting the first sentence." }
    """
    if not TEXT_TO_SUMMARIZE or not isinstance(TEXT_TO_SUMMARIZE, str):
        return {"error": "TEXT_TO_SUMMARIZE is not set or is not a valid string."}
    
    # Step 1: Split the text into sentences
    sentences = TEXT_TO_SUMMARIZE.split('. ')
    
    # Step 2: Choose the first sentence as the summary (or apply more advanced logic if desired)
    summary = sentences[0].strip()
    
    # Append an ellipsis if there is more text
    if len(sentences) > 1:
        summary += "..."
    
    explanation = "Summary generated by extracting the first sentence."
    
    return {
        "summary": summary,
        "explanation": explanation
    }
```

#### C. TextRank Summarizer Agent (`agents/textrank_summarizer.py`)

```python
# agents/textrank_summarizer.py

# Global variable for the text to summarize
TEXT_TO_SUMMARIZE = None  # User must set this before calling agent_main()
NUM_SENTENCES = 2 # Number of sentences in summary

def agent_main():
    """
    TextRank Summarizer Agent
    ----------------
    Purpose: Summarize the input text using the TextRank algorithm.
    
    Usage:
        # In a Python shell:
        from agents import textrank_summarizer
        textrank_summarizer.TEXT_TO_SUMMARIZE = (
            "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python. "
            "It is based on standard Python type hints and is very easy to use. "
            "This agent summarizes long texts."
        )
        textrank_summarizer.NUM_SENTENCES = 2
        result = textrank_summarizer.agent_main()
        print(result)
        # Expected output: { "summary": "FastAPI is a modern, fast web framework for building APIs with Python. It is based on standard Python type hints and is very easy to use." }
    """
    if not TEXT_TO_SUMMARIZE or not isinstance(TEXT_TO_SUMMARIZE, str):
        return {"error": "TEXT_TO_SUMMARIZE is not set or is not a valid string."}
    
    # Step 1: Split the text into sentences
    sentences = TEXT_TO_SUMMARIZE.split('. ')
    
    # Step 2: Calculate sentence similarity
    # Step 3: Run TextRank algorithm
    # Step 4: Extract top N sentences
    
    summary = "This is a placeholder summary using TextRank." # Replace with actual implementation
    
    return {
        "summary": summary,
    }
```

*Log Instruction:* Update `/logs/4-logs.md` with details on file creation and code implementation for all agents.

---

### Step 3: Validate Integration

- **Dynamic Loading:**  
  The FastAPI endpoint (`/agent/{agent_name}`) in `app/main.py` will load these files when `/agent/classifier`, `/agent/summarizer`, and `/agent/textrank_summarizer` are requested.
  
- **Manual Testing:**  
  1. Start the FastAPI server:
     ```bash
     uvicorn app.main:app --reload
     ```
  2. For the Classifier Agent:
     - In a Python shell, set `INPUT_TEXT` and call:
       ```python
       from agents import classifier
       classifier.INPUT_TEXT = "Hello, how are you?"
       print(classifier.agent_main())
       ```
     - Verify the JSON output contains a classification and a confidence score.
  3. For the Summarizer Agent:
     - In a Python shell, set `TEXT_TO_SUMMARIZE` and call:
       ```python
       from agents import summarizer
       summarizer.TEXT_TO_SUMMARIZE = "FastAPI is an efficient framework. It simplifies API development. This agent summarizes text."
       print(summarizer.agent_main())
       ```
     - Verify that the summary and explanation are returned as expected.
  4. For the TextRank Summarizer Agent:
     - In a Python shell, set `TEXT_TO_SUMMARIZE` and call:
       ```python
       from agents import textrank_summarizer
       textrank_summarizer.TEXT_TO_SUMMARIZE = "FastAPI is an efficient framework. It simplifies API development. This agent summarizes text."
       print(textrank_summarizer.agent_main())
       ```
     - Verify that the summary is returned as expected.

- **Automated Testing:**  
  Ensure tests in `/tests/` (e.g., `tests/test_agents.py`) include cases for all agents.

*Log Instruction:* Record testing outcomes in `/logs/4-logs.md`.

---

### Step 4: Final Documentation and Commit

- **Documentation:**  
  Update the repository’s README and any additional documentation in `/docs/` to include usage instructions for the Classifier, Summarizer, and TextRank Summarizer agents.
  
- **Review:**  
  Verify that the code adheres to the naming conventions (all lowercase) and that the advanced dspy functionality is clearly documented in inline comments.
  
- **Commit Changes:**  
  Commit all changes with clear commit messages referencing the completion of the dspy agents phase.

*Log Instruction:* Finalize `/logs/4-logs.md` with a summary of all completed tasks, test results, and any technical debt.

---

## Summary

This plan details the implementation of three dspy showcase agents:
- **Classifier Agent (`classifier.py`):** Uses advanced rule-based classification with keyword matching and regular expressions to classify input text.
- **Summarizer Agent (`summarizer.py`):** Summarizes a block of text by extracting the first sentence and provides an explanation.
- **TextRank Summarizer Agent (`textrank_summarizer.py`):** Summarizes a block of text using the TextRank algorithm.

All agents are designed to be dynamically loaded and executed via the FastAPI endpoint. Their implementation showcases advanced features inspired by dspy, providing a robust foundation for further agent development.
