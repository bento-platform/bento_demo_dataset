import numpy as np
from constants import (
    AGE_MEAN, AGE_SD, AGE_MIN, AGE_MAX, DISEASE_MASS_DISTRIBUTION, PHENOTYPIC_FEATURE_MASS_DISTRIBUTION,
    LAB_MIN, LAB_MAX, LAB_MEAN, P_EXCLUDED, BMI_MIN, BMI_MAX, P_BP_PRESENT, BP_MIN, BP_MAX, BP_MEAN,
    BP_SD, BMI_MEAN, BMI_SD, P_BMI_PRESENT, P_SMOKING_STATUS_PRESENT)
from phenopackets.extra_properties import SMOKING_STATUS, COVID_SEVERITY, MOBILITY
from ontology_terms import DISEASE_TERMS, PHENOTYPIC_FEATURES, DISEASE_STAGES, TNM_FINDING
from random_generator.generator import RandomGenerator
from experiments.experiment_metadata import one_thousand_genomes_experiment, EXPERIMENT_RESOURCES


##############################
# conventions:
# generate one phenopacket per individual
#
# for 1000 genomes ids only:
# - create a biosample and experiment with reference to a vcf file (file may or may not exist)
# - biosample_id = individual_id
# - vcf file name is <individual_id>.vcf.gz
#
# for other individuals:
# - copy over any experiments and experiment results in "experiments" field
#




# why are our phenopackets in snake_case??
# distribute a few alternate ids (lists of ids, although pxf docs say list of CURIE ??)



class Individual:
    def __init__(self, rng, individual):
        self.rng: RandomGenerator = rng
        self.individual: dict = individual
        self.experiments = individual.get("experiments", [])
        self.phenopacket = self.generate_phenopacket()

    def generate_phenopacket(self):
        p = {
            "id": self.rng.random_uuid4(),
            "subject": self.subject(),
            "biosamples": self.biosamples(),
            "meta_data": self.phenopacket_metadata()
        }

        # conditional additions
        measurements = self.measurements()
        if measurements:
            p["measurements"] = measurements

        # TODO: medical actions
        # TODO: interpretations

        return p

    def add_experiment(self, e):
        self.experiments.append(e)

    def subject(self):
        age = self.rng.int_from_gaussian_range(AGE_MIN, AGE_MAX, AGE_MEAN, AGE_SD)
        age_iso = f"P{age}Y"
        s = {
            "id": self.individual["id"],
            "sex": self.individual["sex"],
            "timeAtLastEncounter": {
                "age": {
                    "iso8601duration": age_iso
                }
            },
            "taxonomy": {
                "id": "NCBITaxon:9606",
                "label": "Homo sapiens"
            },
            "karyotypicSex": {"MALE": "XY", "FEMALE": "XX"}[self.individual["sex"]],
            "extra_properties": {
                "mobility": self.rng.gaussian_choice(MOBILITY),
                "covid_severity": self.rng.gaussian_choice(COVID_SEVERITY),
                "date_of_consent": self.rng.random_recent_date(),
                "lab_test_result_value": self.lab_value()
            }
        }

        # conditionally add smoking status extra property
        smoking = self.smoking_status()
        if smoking:
            s["extra_properties"]["smoking_status"] = smoking

        return s

    def biosamples(self):
        # return any real stuff from config
        if bs := self.individual.get("biosamples"):
            return bs

        b = []

        # add an experiment with vcf for all 1000 genomes samples, whether vcf exists or not
        if self.has_1000_genomes_sample():
            b.append({
                "id": self.individual["id"],  # convention for 1k genomes biosample ids
                "sampled_tissue": {
                    "id": "UBERON:0000178",
                    "label": "blood"
                },
            })
            self.add_experiment(one_thousand_genomes_experiment(self.rng, self.individual["id"]))

        # chose zero or more fake biosamples
        # either with zero_or_more_choices on a list of biosamples fns
        # or die roll, then that many calls to random biosample generator
        # even if the second way, some fields will need to be set?

        # required field:
        # id
        # recommended fields:
        # individual_id
        # phenotypic_features (of sample)
        # time_of_collection
        # histological_diagnosis
        # tumor_progression
        # pathological_stage
        # pathological_tnm_finding
        # diagnostic_markers
        # procedure
        # material_sample

        # randomly choose between zero and n biosamples
        # but at least make them coherent

        return b

    def diseases(self):
        # return anything in config
        if ds := self.individual.get("diseases"):
            return ds

        # randomly choose between zero and n diseases
        ds = self.rng.zero_or_more_choices(DISEASE_TERMS, DISEASE_MASS_DISTRIBUTION)

        # very rarely, mark a disease as excluded
        ds_ex = [{**d, "excluded": True} if self.rng.biased_coin_toss(P_EXCLUDED) else d for d in ds]
        return ds_ex

    def phenotypic_features(self):
        # randomly choose between zero and n phenotypic features
        pfs = self.rng.zero_or_more_choices(PHENOTYPIC_FEATURES, PHENOTYPIC_FEATURE_MASS_DISTRIBUTION)

        # very rarely, mark as excluded
        pfs_ex = [{**p, "excluded": True} if self.rng.biased_coin_toss(P_EXCLUDED) else p for p in pfs]
        return pfs_ex

    # conditionally add a measurement
    def measurements(self):
        ms = []
        if self.has_bmi():
            ms.append(self.bmi())

        if self.has_blood_pressure():
            ms.append(self.blood_pressure())

        return ms

    # TODO
    def interpretations(self):
        ...

    # TODO
    def medical_actions(self):
        ...

    # possible later TODO, currently we only attach files to experiments, not to phenopackets
    def files(self):
        ...

    # TODO: only add metadata actually used for this individual?
    #  or simply shovel all into everyone
    def meta_data(self):
        ...

# utils ------------------------

    def has_1000_genomes_sample(self) -> bool:
        return self.individual["id"].startswith(("HG", "NA"))

    def lab_value(self) -> int:
        return self.rng.int_from_exponential_range(LAB_MIN, LAB_MAX, LAB_MEAN)

    def has_smoking_status(self) -> bool:
        return bool(self.rng.biased_coin_toss(P_SMOKING_STATUS_PRESENT))

    def smoking_status(self) -> list[str]:
        return self.rng.gaussian_choice(SMOKING_STATUS)

    def has_bmi(self) -> bool:
        return bool(self.rng.biased_coin_toss(P_BMI_PRESENT))

    def bmi(self):
        return {
            "assay": {"id": "NCIT:C16358", "label": "Body Mass Index"},
            "measurement_value": {
                "unit": {"id": "NCIT:C49671", "label": "Kilogram per Square Meter"},
                "value": round(self.rng.float_from_gaussian_range(BMI_MIN, BMI_MAX, BMI_MEAN, BMI_SD), 2)
            }
        }

    def has_blood_pressure(self) -> bool:
        return bool(self.rng.biased_coin_toss(P_BP_PRESENT))

    def blood_pressure(self):
        random_offset_range = 10, 20
        mean_bp = self.rng.int_from_gaussian_range(BP_MIN, BP_MAX, BP_MEAN, BP_SD)
        offset = self.rng.int_from_uniform_range(random_offset_range[0], random_offset_range[1])
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

    # ideally we would only mention resources used in this phenopacket
    # TODO: needs correct resources
    def phenopacket_metadata(self):
        return {
            "created": self.rng.random_recent_date(),
            "created_by": "C3G_synthetic_data",
            "phenopacket_schema_version": "2.0.0",
            "resources": [
                {
                    "name": "Sequence types and features ontology",
                    "version": "2021-02-16",
                    "namespace_prefix": "SO",
                    "id": "SO:2021-02-16",
                    "iri_prefix": "http://purl.obolibrary.org/obo/so.owl#",
                    "url": "http://purl.obolibrary.org/obo/so.owl"
                }
            ]
        }
