# agents/quote.py
import random

# Collection of inspirational quotes
QUOTES = [
    "Believe in yourself and all that you are.",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "Success is not final, failure is not fatal. - Winston Churchill",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Everything you've ever wanted is on the other side of fear. - George Addair",
    "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
    "What you do today can improve all your tomorrows. - Ralph Marston",
    "The way to get started is to quit talking and begin doing. - Walt Disney"
]

def agent_main():
    """
    Quote Agent
    -----------
    Purpose: Returns a random inspirational quote from a collection.
    
    Usage:
        # In a Python shell:
        from agents import quote
        result = quote.agent_main()
        print(result)  # Example output: {'quote': 'Believe in yourself and all that you are.'}
    """
    return {"quote": random.choice(QUOTES)}