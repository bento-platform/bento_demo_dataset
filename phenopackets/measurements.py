from constants import BMI_MIN, BMI_MAX, BMI_MEAN, BMI_SD, BP_MIN, BP_MAX, BP_MEAN, BP_SD, P_BMI_PRESENT, P_BP_PRESENT


def has_bmi(rng) -> bool:
    return bool(rng.biased_coin_toss(P_BMI_PRESENT))


def has_blood_pressure(rng) -> bool:
    return bool(rng.biased_coin_toss(P_BP_PRESENT))


def bmi(rng) -> dict:
    return {
        "assay": {"id": "NCIT:C16358", "label": "Body Mass Index"},
        "measurement_value": {
            "unit": {"id": "NCIT:C49671", "label": "Kilogram per Square Meter"},
            "value": round(rng.float_from_gaussian_range(BMI_MIN, BMI_MAX, BMI_MEAN, BMI_SD), 2)
        }
    }


def blood_pressure(rng) -> dict:
    random_offset_range = 10, 20
    mean_bp = rng.int_from_gaussian_range(BP_MIN, BP_MAX, BP_MEAN, BP_SD)
    offset = rng.int_from_uniform_range(random_offset_range[0], random_offset_range[1])
    diastolic, systolic = mean_bp - offset, mean_bp + offset
    return {
        "assay": {"id": "NCIT:C167233", "label": "Blood Pressure Measurement"},
        "complexValue": {
            "typedQuantities": [
                {
                    "type": {
                        "id": "NCIT:C25298", "label": "Systolic Blood Pressure"
                    },
                    "quantity": {
                        "unit": {"id": "NCIT:C49670", "label": "Millimeter of Mercury"},
                        "value": systolic
                    }
                },
                {
                    "type": {"id": "NCIT:C25299", "label": "Diastolic Blood Pressure"},
                    "quantity": {
                        "unit": {"id": "NCIT:C49670", "label": "Millimeter of Mercury"},
                        "value": diastolic
                    }
                }
            ]
        }
    }
