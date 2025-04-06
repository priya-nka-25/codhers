import random

def classify_text(description):
    keywords = {
        'pothole': ['pothole', 'road', 'hole'],
        'water leakage': ['leak', 'water', 'pipe'],
        'electric': ['light', 'electric', 'wire'],
    }
    for category, words in keywords.items():
        if any(word in description.lower() for word in words):
            return category
    return 'general'

def classify_image(filename):
    # Simulate image classification with dummy result
    return random.choice(['pothole', 'water leakage', 'electric'])

def get_priority(issue_type):
    priorities = {
        'pothole': 'High',
        'water leakage': 'Urgent',
        'electric': 'High',
        'general': 'Medium'
    }
    return priorities.get(issue_type, 'Low')

