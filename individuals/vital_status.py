VITAL_STATUS_ENUM = ["UNKNOWN_STATUS", "ALIVE", "DECEASED"]
VITAL_STATUS_CAUSES_OF_DEATH = [
    {
        "id": "SNOMED:1428003",
        "label": "Asphyxia due to foreign body in larynx",
    },
    {
        "id": "SNOMED:230690007",
        "label": "Cerebrovascular accident",
    },
    {
        "id": "SNOMED:58908002",
        "label": "Exposure to attack by amphibian",
    },
    {
        "id": "SNOMED:768147005",
        "label": "Injury due to car accident",
    },
    {
        "id": "SNOMED:22298006",
        "label": "Myocardial infarction",
    },
    {
        "id": "NCIT:C36263",
        "label": "Metastatic Malignant Neoplasm",
    },
]
VITAL_STATUS_CAUSE_OF_DEATH_COVID_19 = {
    "id": "SNOMED:1119302008",
    # technically the wrong label, "severe acute respiratory syndrome coronavirus 2" is very long.
    "label": "Acute disease caused by SARS-CoV-2",
}
