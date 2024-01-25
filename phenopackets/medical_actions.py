PROCEDURES = [
    {
        "code": {
            "id": "NCIT:C28743",
            "label": "Punch Biopsy"
        }
    },
    {
        "code": {
            "id": "NCIT:C16809",
            "label": "Magnetic Resonance Imaging"
        }
    },
    {
        "code": {
            "id": "NCIT:C38101",
            "label": "X-Ray Imaging"
        }
    },
    {
        "code": {
            "id": "NCIT:C17007",
            "label": "Positron Emission Tomography"
        }
    },
    {
        "code": {
            "id": "NCIT:C51677",
            "label": "Liver Biopsy"
        },
        "body_site": {
            "id": "UBERON:0001115",
            "label": "left lobe of liver"
        }
    }
]


# TODO? treatment dates are "recent" but may be before birth :(
def treatments(rng):
    interval = rng.recent_interval_start_and_end_datetime_strings(max_days=14)
    return [
        {
            "agent": {
                "id": "Ondansetron",
                "label": "NCIT:C1119"
            }
        },
        {
            "agent": {
                "id": "NCIT:C198",
                "label": "Acetaminophen"
            },
            "routeOfAdministration": {
                "id": "NCIT:C38288",
                "label": "Oral Route of Administration"
            },
            "doseIntervals": [
                {
                    "quantity": {
                        "unit": {
                            "id": "UO:0000022",
                            "label": "milligram"
                        },
                        "value": 500
                    },
                    "scheduleFrequency": {
                        "id": "NCIT:C64496",
                        "label": "Twice Daily"
                    },
                    "interval": {
                        "start": interval["start"],
                        "end": interval["end"]
                    }
                }
            ],
            "drugType": "PRESCRIPTION"
        },
        {
            "agent": {
                "id": "NCIT:C561",
                "label": "Ibuprofen"
            },
            "routeOfAdministration": {
                "id": "NCIT:C38288",
                "label": "Oral Route of Administration"
            },
            "doseIntervals": [
                {
                    "quantity": {
                        "unit": {
                            "id": "UO:0000022",
                            "label": "milligram"
                        },
                        "value": 500
                    },
                    "scheduleFrequency": {
                        "id": "NCIT:C64496",
                        "label": "Twice Daily"
                    },
                    "interval": {
                        "start": interval["start"],
                        "end": interval["end"]
                    }
                }
            ],
            "drugType": "PRESCRIPTION"
        }
    ]
