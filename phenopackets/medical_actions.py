PROCEDURES = [
    {
        "procedure": {
            "code": {
                "id": "NCIT:C28743",
                "label": "Punch Biopsy"
            }
        },
        "treatment_intent": {
            "id": "NCIT:C15220",
            "label": "Diagnosis"
        }
    },
    {
        "procedure": {
            "code": {
                "id": "NCIT:C16809",
                "label": "Magnetic Resonance Imaging"
            }
        }
    },
    {
        "procedure": {
            "code": {
                "id": "NCIT:C38101",
                "label": "X-Ray Imaging"
            }
        }
    },
    {
        "procedure": {
            "code": {
                "id": "NCIT:C17007",
                "label": "Positron Emission Tomography"
            }
        },
        "treatment_intent": {
            "id": "NCIT:C15220",
            "label": "Diagnosis"
        },
        "adverse_events": [
            {
                "id": "NCIT:C3258",
                "label": "Nausea"
            },
            {
                "id": "NCIT:C39594",
                "label": "Skin Rash"
            },
        ],
        "treatment_target": {
            "id": "NCIT:C34660",
            "label": "Head Injury"
        }
    },
    {
        "procedure": {
            "code": {
                "id": "NCIT:C51677",
                "label": "Liver Biopsy"
            },
            "body_site": {
                "id": "UBERON:0001115",
                "label": "left lobe of liver"
            }
        }
    }
]


# TODO? treatment dates are "recent" but may be before birth :(
def treatments(rng):
    interval = rng.recent_interval_start_and_end_datetime_strings(max_days=14)
    return [
        {
            "treatment": {
                "agent": {
                    "id": "Ondansetron",
                    "label": "NCIT:C1119"
                }
            },
            "treatment_target": {
                "id": "NCIT:C3258",
                "label": "Nausea"
            },
            "adverse_events": [
                {
                    "id": "NCIT:C3038",
                    "label": "Fever"
                }
            ],
        },
        {
            "treatment": {
                "agent": {
                    "id": "NCIT:C198",
                    "label": "Acetaminophen"
                },
                "route_of_administration": {
                    "id": "NCIT:C38288",
                    "label": "Oral Route of Administration"
                },
                "dose_intervals": [
                    {
                        "quantity": {
                            "unit": {
                                "id": "UO:0000022",
                                "label": "milligram"
                            },
                            "value": 500
                        },
                        "schedule_frequency": {
                            "id": "NCIT:C64496",
                            "label": "Twice Daily"
                        },
                        "interval": {
                            "start": interval["start"],
                            "end": interval["end"]
                        }
                    }
                ],
                "drug_type": "PRESCRIPTION"
            },
            "treatment_target": {
                "id": "NCIT:C34661",
                "label": "Headache"
            }
        },
        {"treatment": {
            "agent": {
                "id": "NCIT:C561",
                "label": "Ibuprofen"
            },
            "route_of_administration": {
                "id": "NCIT:C38288",
                "label": "Oral Route of Administration"
            },
            "dose_intervals": [
                {
                    "quantity": {
                        "unit": {
                            "id": "UO:0000022",
                            "label": "milligram"
                        },
                        "value": 500
                    },
                    "schedule_frequency": {
                        "id": "NCIT:C64496",
                        "label": "Twice Daily"
                    },
                    "interval": {
                        "start": interval["start"],
                        "end": interval["end"]
                    }
                }
            ],
            "drug_type": "PRESCRIPTION"
        }}
    ]
