import spacy

nlp = spacy.load("en_core_web_sm")

keyword_weights = {
    'pothole': ('High', 3),
    'road': ('High', 2),
    'hole': ('High', 2),
    'water': ('Urgent', 3),
    'leak': ('Urgent', 3),
    'pipe': ('Urgent', 2),
    'electric': ('High', 3),
    'light': ('High', 2),
    'wire': ('High', 2),
    'trash': ('Medium', 2),
    'garbage': ('Medium', 2),
    'noise': ('Low', 1),
    'animal': ('Low', 1)
}

def prioritize_issue(description):
    doc = nlp(description.lower())
    scores = {'Urgent': 0, 'High': 0, 'Medium': 0, 'Low': 0}

    for token in doc:
        if token.lemma_ in keyword_weights:
            priority, weight = keyword_weights[token.lemma_]
            scores[priority] += weight

    if all(score == 0 for score in scores.values()):
        return 'Medium'

    return max(scores, key=scores.get)
