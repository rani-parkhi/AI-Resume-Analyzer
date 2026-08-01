import re

# Strong action verbs
ACTION_VERBS = [
    "developed", "designed", "implemented", "created",
    "built", "optimized", "improved", "managed",
    "led", "engineered", "deployed", "automated",
    "analyzed", "trained", "tested", "integrated"
]

# Weak phrases
WEAK_PHRASES = [
    "responsible for",
    "worked on",
    "helped",
    "participated",
    "involved in"
]


def analyze_resume_quality(text):

    text = text.lower()

    score = 100

    feedback = []

    # ---------- Action Verbs ----------
    action_count = sum(
        text.count(word)
        for word in ACTION_VERBS
    )

    if action_count < 5:
        score -= 15
        feedback.append(
            "Use more action verbs like Developed, Built, Designed, Implemented."
        )

    # ---------- Quantified Achievements ----------
    numbers = re.findall(r"\d+%?|\d+\+", text)

    if len(numbers) < 3:
        score -= 15
        feedback.append(
            "Include measurable achievements using numbers or percentages."
        )

    # ---------- Weak Phrases ----------
    weak_count = sum(
        text.count(word)
        for word in WEAK_PHRASES
    )

    if weak_count > 2:
        score -= 10
        feedback.append(
            "Reduce weak phrases like 'Worked on' or 'Responsible for'."
        )

    # ---------- Resume Length ----------
    words = len(text.split())

    if words < 250:
        score -= 10
        feedback.append(
            "Resume is slightly short. Aim for 250–700 words."
        )

    score = max(score, 0)

    return {
        "score": score,
        "action_verbs": action_count,
        "numbers": len(numbers),
        "weak_phrases": weak_count,
        "feedback": feedback
    }