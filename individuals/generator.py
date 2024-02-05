import numpy as np
from config.constants import (
    AGE_MEAN, AGE_SD, AGE_MIN, AGE_MAX, DISEASE_MASS_DISTRIBUTION, PHENOTYPIC_FEATURE_MASS_DISTRIBUTION,
    LAB_MIN, LAB_MAX, LAB_MEAN, P_EXCLUDED, P_SMOKING_STATUS_PRESENT, MEDICAL_ACTION_MASS_DISTRIBUTION,
    INTERPRETATION_MASS_DISTRIBUTION, EXTRA_BIOSAMPLES_MASS_DISTRIBUTION, P_ADD_EXPERIMENT_TO_BIOSAMPLE)
from experiments.experiment_metadata import one_thousand_genomes_experiment, random_biosample_with_experiment
from experiments.experiment_details import TISSUES_WITH_EXPERIMENTS
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
# - individual id = "ind-" + biosample id
# - vcf file name is <biosample id>.vcf.gz
#
# for entries in individuals.json, copy over the value of these fields where they exist:
# - biosamples
# - experiments
# - diseases
#
# ... this allows us to have sensible values associated with any real data files we use, eg:
# - we can make sure that biosample ids match between a real file and fake metadata
# - real cancer data can have cancer mentioned in the metadata


class IndividualGenerator:
    def __init__(self, rng):
        self.rng: RandomGenerator = rng
        self.phenopackets = []
        self.experiments = []

        # fix some probability weightings over the whole dataset
        self.choice_weights = {
            "covid_severity": rng.gaussian_weights(len(COVID_SEVERITY)),
            "diseases": rng.gaussian_weights(len(DISEASES)),
            "interpretations": rng.gaussian_weights(len(interpretations(rng, ""))),
            "medical_actions_procedures": rng.gaussian_weights(len(PROCEDURES)),
            "medical_actions_treatments": rng.gaussian_weights(len(treatments(rng))),
            "mobility": rng.gaussian_weights(len(MOBILITY)),
            "phenotypic_features": rng.gaussian_weights(len(phenotypic_features())),
            "smoking_status": rng.gaussian_weights(len(SMOKING_STATUS)),
            "synthetic_experiments": rng.gaussian_weights(len(TISSUES_WITH_EXPERIMENTS))
        }

    def generate_data(self, individual):
        p = {
            "id": self.rng.uuid4(),
            # "alternate_ids": []  # ...why are alternate subject ids CURIEs?
            "subject": self.subject(individual),
            "biosamples": self.biosamples(individual),
            "phenotypic_features": self.phenotypic_features()
        }

        # --------- conditional additions ------------
        if ms := self.measurements():
            p["measurements"] = ms

        if ma := self.medical_actions():
            p["medical_actions"] = ma

        if intp := self.interpretations(individual):
            p["interpretations"] = intp
        # --------------------------------------------

        # random diseases, plus diseases mentioned elsewhere in this phenopacket
        p["diseases"] = self.diseases(individual, intp, p["subject"]["extra_properties"]["covid_severity"])

        p["meta_data"] = self.metadata()

        self.phenopackets.append(p)

    def add_experiment(self, e):
        self.experiments.append(e)

    def subject(self, individual):
        age = self.rng.int_from_gaussian_range(AGE_MIN, AGE_MAX, AGE_MEAN, AGE_SD)
        age_iso = f"P{age}Y"
        s = {
            "id": individual["id"],
            "sex": individual["sex"],
            "time_at_last_encounter": {
                "age": {
                    "iso8601duration": age_iso
                }
            },
            "taxonomy": {
                "id": "NCBITaxon:9606",
                "label": "Homo sapiens"
            },
            "karyotypic_sex": {"MALE": "XY", "FEMALE": "XX"}[individual["sex"]],
            "extra_properties": {
                "mobility": self.mobility(),
                "covid_severity": self.covid_severity(),
                "date_of_consent": self.rng.recent_date_string(),
                "lab_test_result_value": self.lab_value()
            }
        }

        # conditionally add smoking status extra property
        if self.has_smoking_status():
            s["extra_properties"]["smoking_status"] = self.smoking_status()

        return s

    # creates experiments associated with a biosample as a side effect
    def biosamples(self, individual):
        indiv_id = individual["id"]
        b = []

        # add any real stuff from config
        if bs := individual.get("biosamples"):
            b.extend(bs)
        if es := individual.get("experiments"):
            self.experiments.extend(es)

        # add an experiment with vcf for all 1000 genomes ids, whether vcf exists or not
        if self.is_1000_genomes_id(individual["id"]):
            one_k_biosample_id = indiv_id[len("ind-"):]
            b.append({
                "id": one_k_biosample_id,
                "sampled_tissue": {
                    "id": "UBERON:0000178",
                    "label": "blood"
                },
            })
            self.add_experiment(one_thousand_genomes_experiment(self.rng, one_k_biosample_id))

        # randomly add more biosamples...
        extra_biosamples = self.extra_biosamples(indiv_id)

        # ... then typically give them experiments
        for eb_id in extra_biosamples:
            synthetic_biosample, synthetic_experiment = random_biosample_with_experiment(
                self.rng, eb_id, self.choice_weights["synthetic_experiments"])

            b.append(synthetic_biosample)
            if self.should_add_experiment_to_biosample():
                self.add_experiment(synthetic_experiment)

        return b

    def diseases(self, individual, intp, covid_severity):
        # randomly choose some diseases
        ds = self.rng.zero_or_more_choices(DISEASES, DISEASE_MASS_DISTRIBUTION, self.choice_weights["diseases"])

        # very rarely, mark a disease as excluded
        ds_ex = [
            {**d, "excluded": True}
            if self.should_exclude() and "disease_stage" not in d else d for d in ds]

        # add anything in config
        if config_ds := individual.get("diseases"):
            ds_ex.extend(config_ds)

        # add any diseases mentioned in "interpretations"
        ds_ex.extend({"term": i["diagnosis"]["disease"]} for i in intp if "diagnosis" in i)

        # add covid if present
        if covid_severity != "Uninfected":
            ds_ex.append(COVID_19)

        return ds_ex

    def phenotypic_features(self):
        # randomly choose some phenotypic features
        pfs = self.rng.zero_or_more_choices(
            phenotypic_features(),
            PHENOTYPIC_FEATURE_MASS_DISTRIBUTION,
            self.choice_weights["phenotypic_features"])

        # very rarely, mark as excluded
        pfs_ex = [{**p, "excluded": True} if self.should_exclude() else p for p in pfs]
        return pfs_ex

    def measurements(self):
        ms = []
        if has_bmi(self.rng):
            ms.append(bmi(self.rng))

        if has_blood_pressure(self.rng):
            ms.append(blood_pressure(self.rng))

        return ms

    def interpretations(self, individual):
        return self.rng.zero_or_more_choices(
            interpretations(self.rng, individual["id"]),
            INTERPRETATION_MASS_DISTRIBUTION,
            self.choice_weights["interpretations"]
        )

    def medical_actions(self):
        action_procedures = self.rng.zero_or_more_choices(
            PROCEDURES, MEDICAL_ACTION_MASS_DISTRIBUTION,
            self.choice_weights["medical_actions_procedures"])

        action_treatments = self.rng.zero_or_more_choices(
            treatments(self.rng),
            MEDICAL_ACTION_MASS_DISTRIBUTION,
            self.choice_weights["medical_actions_treatments"])

        # could add top-level values here (treatment_target, etc)
        return action_procedures + action_treatments

    # possible later TODO, currently we only attach files to experiments, not to phenopackets
    # def files(self):
    #     pass

    def metadata(self):
        return metadata()

# utils ------------------------

    @staticmethod
    def is_1000_genomes_id(individual_id) -> bool:
        return individual_id.startswith(("ind-HG", "ind-NA"))

    def lab_value(self) -> int:
        return self.rng.int_from_exponential_range(LAB_MIN, LAB_MAX, LAB_MEAN)

    def mobility(self) -> str:
        return self.rng.weighted_choice(MOBILITY, self.choice_weights["mobility"])

    def covid_severity(self) -> str:
        return self.rng.weighted_choice(COVID_SEVERITY, self.choice_weights["covid_severity"])

    def has_smoking_status(self) -> bool:
        return bool(self.rng.biased_coin_toss(P_SMOKING_STATUS_PRESENT))

    def smoking_status(self):
        return self.rng.weighted_choice(SMOKING_STATUS, self.choice_weights["smoking_status"])

    def extra_biosamples(self, indiv_id):
        return self.rng.zero_or_more_choices(
            [f"{indiv_id}-{n}" for n in range(len(EXTRA_BIOSAMPLES_MASS_DISTRIBUTION))],
            EXTRA_BIOSAMPLES_MASS_DISTRIBUTION,
            self.rng.gaussian_weights(len(EXTRA_BIOSAMPLES_MASS_DISTRIBUTION))
        )

    def should_add_experiment_to_biosample(self) -> bool:
        return bool(self.rng.biased_coin_toss(P_ADD_EXPERIMENT_TO_BIOSAMPLE))

    def should_exclude(self) -> bool:
        return bool(self.rng.biased_coin_toss(P_EXCLUDED))
