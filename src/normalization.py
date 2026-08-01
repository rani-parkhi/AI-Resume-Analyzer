SKILL_MAPPING = {

    "ml": "machine learning",
    "machine-learning": "machine learning",

    "ai": "artificial intelligence",
    "artificial-intelligence": "artificial intelligence",

    "dl": "deep learning",

    "js": "javascript",

    "ts": "typescript",

    "node": "node.js",

    "nodejs": "node.js",

    "reactjs": "react",

    "py": "python",

    "postgres": "postgresql",

    "mongo": "mongodb",

    "sklearn": "scikit-learn",

    "tf": "tensorflow",

    "cv": "computer vision",

    "nlp": "natural language processing",

    "oops": "oop"
}


def normalize_resume_text(text):

    text = text.lower()

    for short_name, full_name in SKILL_MAPPING.items():

        text = text.replace(short_name, full_name)

    return text