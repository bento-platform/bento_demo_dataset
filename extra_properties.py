# Extra-properties on individuals

import random
from datetime import datetime

SMOKING_STATUS = [
    "Non-smoker",
    "Smoker",
    "Former smoker",
    "Passive smoker",
    "Not specified"
]

MOBILITY = [
    "I have no problems in walking about",
    "I have slight problems in walking about",
    "I have moderate problems in walking about",
    "I have severe problems in walking about",
    "I am unable to walk about"
]

COVID_SEVERITY = [
    "Uninfected",
    "Mild",
    "Moderate",
    "Severe",
    "Dead"
]

def date_of_consent():
    year = f"202{random.choice([0, 1, 2])}"
    d = random.choice(range(1, 365))
    month_day = datetime.strptime(f"{d}", "%j").strftime("%m-%d")
    return year + "-" + month_day
