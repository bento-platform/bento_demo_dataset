import numpy as np
from constants import (
    AGE_MEAN, AGE_SD, AGE_MIN, AGE_MAX, DISEASE_MASS_DISTRIBUTION, PHENOTYPIC_FEATURE_MASS_DISTRIBUTION,
    LAB_MIN, LAB_MAX, LAB_MEAN, P_EXCLUDED, P_SMOKING_STATUS_PRESENT, MEDICAL_ACTION_MASS_DISTRIBUTION,
    INTERPRETATION_MASS_DISTRIBUTION, EXTRA_BIOSAMPLES_MASS_DISTRIBUTION, P_ADD_EXPERIMENT_TO_BIOSAMPLE,
    P_ADD_EXAMPLE_FILE_TO_EXPERIMENT)
from experiments.experiment_metadata import one_thousand_genomes_experiment, random_synthetic_experiment
from phenopackets.extra_properties import SMOKING_STATUS, COVID_SEVERITY, MOBILITY
from phenopackets.diseases import DISEASES, COVID_19
from phenopackets.interpretations import interpretations
from phenopackets.measurements import has_bmi, has_blood_pressure, bmi, blood_pressure
from phenopackets.medical_actions import PROCEDURES, treatments
from phenopackets.metadata import metadata
from phenopackets.phenotypic_features import phenotypic_features
from random_generator.generator import RandomGenerator


##############################
# conventions:
# generate one phenopacket per individual in individuals.json
#
# for 1000 genomes ids only:
# - create a biosample and experiment with reference to a vcf file (file may or may not exist)
# - biosample_id = individual_id
# - vcf file name is <individual_id>.vcf.gz
#
# for any ids, copy over the value of these fields where they exist:
# - biosamples
# - experiments
# - diseases
#
# ... this allows us to have sensible values associated with any real data files we use,
# eg: we can make sure that biosample ids match between a real file and imaginary metadata
# or cancer data can have cancer mentioned in the metadata


class Individual:
    def __init__(self, rng, individual):
        self.rng: RandomGenerator = rng
        self.individual = individual
        self.experiments = individual.get("experiments", [])
        self.phenopacket = self.generate_phenopacket()

    def generate_phenopacket(self):
        p = {
            "id": self.rng.uuid4(),
            # "alternate_ids": []  # why are alternate ids CURIEs?
            "subject": self.subject(),
            "biosamples": self.biosamples(),
            "phenotypic_features": self.phenotypic_features()
        }

        # --------- conditional additions ------------
        if ms := self.measurements():
            p["measurements"] = ms

        if ma := self.medical_actions():
            p["medical_actions"] = ma

        if intp := self.interpretations():
            p["interpretations"] = intp
        # --------------------------------------------
            
        # random diseases, plus diseases mentioned elsewhere in this phenopacket
        p["diseases"] = self.diseases(intp, p["subject"]["extra_properties"]["covid_severity"])

        p["meta_data"] = self.metadata()

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
                "date_of_consent": self.rng.recent_date_string(),
                "lab_test_result_value": self.lab_value()
            }
        }

        # conditionally add smoking status extra property
        if self.has_smoking_status():
            s["extra_properties"]["smoking_status"] = self.smoking_status()

        return s

    # creates experiments associated with a biosample as a side effect
    def biosamples(self):
        # return any real stuff from config
        if bs := self.individual.get("biosamples"):
            return bs

        b = []

        # add an experiment with vcf for all 1000 genomes ids, whether vcf exists or not
        if self.has_1000_genomes_sample():
            b.append({
                "id": self.individual["id"],  # convention for 1k genomes biosample ids
                "sampled_tissue": {
                    "id": "UBERON:0000178",
                    "label": "blood"
                },
            })
            self.add_experiment(one_thousand_genomes_experiment(self.rng, self.individual["id"]))

        # randomly add more biosamples...
        extra_biosamples = self.rng.zero_or_more_choices(
            [f"{self.individual['id']}-{n}" for n in range(len(EXTRA_BIOSAMPLES_MASS_DISTRIBUTION))],
            EXTRA_BIOSAMPLES_MASS_DISTRIBUTION)

        # ... then typically give them experiments
        for eb_id in extra_biosamples:
            if self.should_add_experiment_to_biosample():
                self.add_experiment(random_synthetic_experiment(self.rng, eb_id))

        
        # TODO?
        # could have more top-level biosample properties (procedure, etc)
        # but some properties only make sense with particular experiments
        
        return b

    def diseases(self, intp, covid_severity):
        # randomly choose between zero and n diseases
        ds = self.rng.zero_or_more_choices(DISEASES, DISEASE_MASS_DISTRIBUTION)

        # very rarely, mark a disease as excluded
        ds_ex = [
            {**d, "excluded": True}
            if self.rng.biased_coin_toss(P_EXCLUDED) and "disease_stage" not in d else d for d in ds]

        # add anything in config
        if config_ds := self.individual.get("diseases"):
            ds_ex.extend(config_ds)

        # add any diseases mentioned in "interpretations"
        ds_ex.extend({"term": i["diagnosis"]["disease"]} for i in intp if "diagnosis" in i)

        # add covid if present
        if covid_severity != "Uninfected":
            ds_ex.append(COVID_19)

        return ds_ex

    def phenotypic_features(self):
        # randomly choose between zero and n phenotypic features
        pfs = self.rng.zero_or_more_choices(phenotypic_features(), PHENOTYPIC_FEATURE_MASS_DISTRIBUTION)

        # very rarely, mark as excluded
        pfs_ex = [{**p, "excluded": True} if self.rng.biased_coin_toss(P_EXCLUDED) else p for p in pfs]
        return pfs_ex

    def measurements(self):
        ms = []
        if has_bmi(self.rng):
            ms.append(bmi(self.rng))

        if has_blood_pressure(self.rng):
            ms.append(blood_pressure(self.rng))

        return ms

    def interpretations(self):
        return self.rng.zero_or_more_choices(interpretations(self.individual["id"]), INTERPRETATION_MASS_DISTRIBUTION)

    def medical_actions(self):
        action_procedures = self.rng.zero_or_more_choices(PROCEDURES, MEDICAL_ACTION_MASS_DISTRIBUTION)
        action_treatments = self.rng.zero_or_more_choices(treatments(self.rng), MEDICAL_ACTION_MASS_DISTRIBUTION)
        # could add top-level values here (treatment_target, etc)
        return action_procedures + action_treatments

    # possible later TODO, currently we only attach files to experiments, not to phenopackets
    def files(self):
        pass

    def metadata(self):
        return metadata()

# utils ------------------------

    def has_1000_genomes_sample(self) -> bool:
        return self.individual["id"].startswith(("HG", "NA"))

    def lab_value(self) -> int:
        return self.rng.int_from_exponential_range(LAB_MIN, LAB_MAX, LAB_MEAN)

    def has_smoking_status(self) -> bool:
        return bool(self.rng.biased_coin_toss(P_SMOKING_STATUS_PRESENT))

    def smoking_status(self) -> list[str]:
        return self.rng.gaussian_choice(SMOKING_STATUS)
    
    def should_add_experiment_to_biosample(self):
        return bool(self.rng.biased_coin_toss(P_ADD_EXPERIMENT_TO_BIOSAMPLE))
