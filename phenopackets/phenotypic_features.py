import hashlib

from random_generator.generator import RandomGenerator
from config.constants import (
    P_EXCLUDED,
    P_PF_HAS_SEVERITY,
    PF_SEVERITY_DISTRIBUTION,
    P_PF_RECURRENT,
    P_PF_HAS_EXTRA_PROPERTIES,
)


def phenotypic_features(rng: RandomGenerator):
    pfs = []

    for p in PHENOTYPIC_FEATURE_TYPES:
        pf = {"type": p}

        # if adding a severity to this phenotypic feature makes sense (+ we flip a weighted coin), add it:
        if p["id"] not in PHENOTYPIC_FEATURE_SEVERITY_TYPE_ID_EXCLUSIONS and rng.biased_coin_toss(P_PF_HAS_SEVERITY):
            pf["severity"] = rng.weighted_choice(PHENOTYPIC_FEATURE_SEVERITY, PF_SEVERITY_DISTRIBUTION)

        # if making this phenotypic feature recurrent even makes sense (+ we flip a coin), add the modifier:
        if p["id"] in PHENOTYPIC_FEATURE_RECURRENT_TYPE_IDS and rng.biased_coin_toss(P_PF_RECURRENT):
            pf["modifiers"] = [{"id": "HP:0031796", "label": "Recurrent"}]

        # very rarely, mark as excluded
        if rng.biased_coin_toss(P_EXCLUDED):
            pf["excluded"] = True

        if rng.biased_coin_toss(P_PF_HAS_EXTRA_PROPERTIES):
            pf["extra_properties"] = {
                "internal_code": hashlib.md5(p["id"].encode("ascii"), usedforsecurity=False).hexdigest()[:12],
            }

        pfs.append(pf)

    return pfs


PHENOTYPIC_FEATURE_TYPES = [
    {
        "id": "HP:0000822",
        "label": "Hypertension",
    },
    {
        "id": "SNOMED:29857009",
        "label": "Chest pain",
    },
    {
        "id": "SNOMED:386661006",
        "label": "Fever",
    },
    {
        "id": "SNOMED:49727002",
        "label": "Cough",
    },
    {
        "id": "SNOMED:52448006",
        "label": "Dementia",
    },
    {
        "id": "SNOMED:79890006",
        "label": "Loss of appetite",
    },
    {
        "id": "SNOMED:195967001",
        "label": "Asthma",
    },
    {
        "id": "SNOMED:75570004",
        "label": "Viral pneumonia/pneumonitis",
    },
    {
        "id": "SNOMED:25064002",
        "label": "Headache",
    },
    {
        "id": "SNOMED:44169009",
        "label": "Loss of sense of smell",
    },
    {
        "id": "SNOMED:370391006",
        "label": "Patient immunosuppressed",
    },
    {
        "id": "SNOMED:414916001",
        "label": "Obesity",
    },
    {
        "id": "SNOMED:422587007",
        "label": "Nausea",
    },
    {
        "id": "SNOMED:21522001",
        "label": "Abdominal pain",
    },
    {
        "id": "SNOMED:80394007",
        "label": "Hyperglycemia",
    },
    {
        "id": "SNOMED:70995007",
        "label": "Pulmonary hypertension",
    },
    {
        "id": "SNOMED:410429000",
        "label": "Cardiac arrest",
    },
    {
        "id": "SNOMED:36118008",
        "label": "Pneumothorax",
    },
    {
        "id": "NCIT:C3108",
        "label": "HIV Infection",
    },
]

# phenotypic features where "recurrent" makes sense
PHENOTYPIC_FEATURE_RECURRENT_TYPE_IDS = frozenset(
    (
        "SNOMED:79890006",  # loss of appetite
        "SNOMED:25064002",  # headache
        "SNOMED:21522001",  # abdominal pain
    )
)

# phenotypic features where severity does not make sense
PHENOTYPIC_FEATURE_SEVERITY_TYPE_ID_EXCLUSIONS = frozenset(
    (
        "SNOMED:370391006",  # patient immunosuppressed
        "SNOMED:414916001",  # obesity
        "SNOMED:410429000",  # cardiac arrest
        "SNOMED:36118008",  # pneumothorax
        "NCIT:C3108",  # HIV infection
    )
)

# In order of severity least --> greatest; see https://hpo.jax.org/browse/term/HP:0012824
PHENOTYPIC_FEATURE_SEVERITY = [
    {"id": "HP:0012827", "label": "Borderline"},
    {"id": "HP:0012825", "label": "Mild"},
    {"id": "HP:0012826", "label": "Moderate"},
    {"id": "HP:0012828", "label": "Severe"},
    {"id": "HP:0012829", "label": "Profound"},
]
