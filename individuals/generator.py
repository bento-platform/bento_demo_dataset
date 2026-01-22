from datetime import date, datetime
from typing import Literal
from urllib.parse import urlparse
import os
from config.constants import (
    AGE_MEAN,
    AGE_SD,
    AGE_MIN,
    AGE_MAX,
    DISEASE_MASS_DISTRIBUTION,
    PHENOTYPIC_FEATURE_MASS_DISTRIBUTION,
    LAB_MIN,
    LAB_MAX,
    LAB_MEAN,
    P_EXCLUDED,
    P_SMOKING_STATUS_PRESENT,
    # -- Vital status constants ---------------------------
    P_VITAL_STATUS_PRESENT,
    P_VITAL_STATUS_DISTRIBUTION,
    P_VITAL_STATUS_DISTRIBUTION_SEVERE_COVID,
    P_VITAL_STATUS_CAUSES_OF_DEATH_DISTRIBUTION,
    P_COVID_CAUSE_OF_DEATH_GIVEN_SEVERE_COVID_AND_DEATH,
    P_VITAL_STATUS_DECEASED_HAS_SURVIVAL_TIME,
    VITAL_STATUS_SURVIVAL_TIME_DIST,
    # -----------------------------------------------------
    MEDICAL_ACTION_MASS_DISTRIBUTION,
    INTERPRETATION_MASS_DISTRIBUTION,
    EXTRA_BIOSAMPLES_MASS_DISTRIBUTION,
    P_ADD_EXPERIMENT_TO_BIOSAMPLE,
    GENERATE_EXPERIMENT_INFO_MATRIX,
    GENERATE_DIFFERENTIAL_EXPERIMENT_INFO_MATRIX,
    NUMBER_OF_GROUPS,
    NUMBER_OF_SAMPLES,
    GFF3_URL,
    P_ADD_LOCATION_COLLECTED_TO_BIOSAMPLE,
)
from experiments.experiment_metadata import one_thousand_genomes_experiment, synthetic_experiment_wrapper
from experiments.experiment_details import TISSUES_WITH_EXPERIMENTS
from individuals.vital_status import (
    VITAL_STATUS_ENUM,
    VITAL_STATUS_CAUSES_OF_DEATH,
    VITAL_STATUS_CAUSE_OF_DEATH_COVID_19,
)
from phenopackets.biosample_collection_locations import BIOSAMPLE_LOCATIONS
from phenopackets.extra_properties import SMOKING_STATUS, COVID_SEVERITY, MOBILITY
from phenopackets.diseases import DISEASES, COVID_19
from phenopackets.interpretations import interpretations
from phenopackets.measurements import has_bmi, has_blood_pressure, bmi, blood_pressure
from phenopackets.medical_actions import PROCEDURES, treatments
from phenopackets.metadata import metadata
from phenopackets.phenotypic_features import phenotypic_features
from random_generator.generator import RandomGenerator
from transcriptomics.transcriptomics_matrix_generator import TranscriptomicMatrixGenerator


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
        self.transcriptomic_matrix_generator = TranscriptomicMatrixGenerator()
        self.file_path = self.get_gff_filename(GFF3_URL)

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
            "synthetic_experiments": rng.gaussian_weights(len(TISSUES_WITH_EXPERIMENTS)),
            "biosample_locations": rng.gaussian_weights(len(BIOSAMPLE_LOCATIONS)),
        }

    def get_gff_filename(self, url):
        """
        Extracts and returns the filename from a URL.
        """
        parsed_url = urlparse(url)
        return os.path.basename(parsed_url.path)

    def generate_and_assign_matrices(self, biosamples_rna_seq):
        # Download and process the GFF file
        self.transcriptomic_matrix_generator.download_and_process_gff(GFF3_URL, self.file_path)

        # Split the biosamples into groups and generate matrices
        groups = self.transcriptomic_matrix_generator.split_into_groups(
            biosamples_rna_seq, NUMBER_OF_GROUPS, NUMBER_OF_SAMPLES
        )
        for idx, group in enumerate(groups):
            matrix_filename = f"counts_matrix_group_{idx + 1}.csv"
            self.transcriptomic_matrix_generator.set_samples(group, NUMBER_OF_SAMPLES)
            counts_matrix = self.transcriptomic_matrix_generator.generate_counts_matrix()
            self.transcriptomic_matrix_generator.write_to_csv(counts_matrix, matrix_filename)
            print(f"Counts matrix generated for group {idx + 1}")

            if GENERATE_EXPERIMENT_INFO_MATRIX:
                experiment_info_matrix = self.transcriptomic_matrix_generator.generate_experiment_info_matrix()
                self.transcriptomic_matrix_generator.write_to_csv(
                    experiment_info_matrix, f"experiment_info_matrix_group_{idx + 1}.csv"
                )
            if GENERATE_DIFFERENTIAL_EXPERIMENT_INFO_MATRIX:
                self.transcriptomic_matrix_generator.write_differentially_expressed_genes_to_csv(
                    f"differentially_expressed_genes_group_{idx + 1}.csv"
                )

            for biosample_id in group:
                self.add_experiment_to_biosample(biosample_id, matrix_filename)

    def add_experiment_to_biosample(self, biosample_id, matrix_filename):
        # Create experiment metadata for RNA-Seq count matrix
        experiment_id = self.rng.uuid4()
        creation_date = str(datetime.now().date())
        experiment_data = {
            "id": experiment_id,
            "biosample": biosample_id,
            "experiment_type": "RNA-Seq",
            "study_type": "Transcriptomics",
            "molecule": "total RNA",
            "molecule_ontology": [{"id": "EFO:0001457", "label": "total RNA"}],
            "experiment_ontology": [{"id": "OBI:0001271", "label": "RNA sequencing"}],
            "library_source": "Transcriptomic",
            "library_strategy": "RNA-Seq",
            "library_selection": "PCR",
            "experiment_results": [
                {
                    "identifier": self.rng.uuid4(),
                    "creation_date": creation_date,
                    "data_output_type": "Derived data",
                    "usage": "Downloaded",
                    "created_by": "C3G_synthetic_data",
                    "description": "Gene expression count matrix",
                    "filename": matrix_filename,
                    "file_format": "CSV",
                    "genome_assembly_id": "GRCh38",
                }
            ],
        }

        self.experiments.append(experiment_data)

    def generate_data(self, individual):
        date_of_consent = self.rng.recent_date()  # for subject extra properties + constraining various other dates

        # ---------- phenopacket structure -----------
        p = {
            "id": self.rng.uuid4(),
            # "alternate_ids": []  # ...why are alternate subject ids CURIEs?
            "subject": self.subject(individual, date_of_consent),
            "phenotypic_features": self.phenotypic_features(),
        }

        # --------- conditional additions ------------
        if bs := self.biosamples(individual):
            p["biosamples"] = bs

        if ms := self.measurements():
            p["measurements"] = ms

        if ma := self.medical_actions():
            p["medical_actions"] = ma

        if intp := self.interpretations(individual):
            p["interpretations"] = intp
        # --------------------------------------------

        # random diseases, plus diseases mentioned elsewhere in this phenopacket
        p["diseases"] = self.diseases(individual, intp, p["subject"]["extra_properties"]["covid_severity"])

        p["meta_data"] = self.metadata(date_of_consent)

        self.phenopackets.append(p)

    def add_experiment(self, e):
        self.experiments.append(e)

    def subject(self, individual, date_of_consent: date):
        age = self.rng.int_from_gaussian_range(AGE_MIN, AGE_MAX, AGE_MEAN, AGE_SD)
        age_iso = f"P{age}Y"

        date_of_consent = self.rng.recent_datetime().date()

        s = {
            "id": individual["id"],
            "sex": individual["sex"],
            "time_at_last_encounter": {
                "age": {
                    "iso8601duration": age_iso,
                },
            },
            "taxonomy": {
                "id": "NCBITaxon:9606",
                "label": "Homo sapiens",
            },
            "karyotypic_sex": {"MALE": "XY", "FEMALE": "XX"}[individual["sex"]],
            "extra_properties": {
                "mobility": self.mobility(),
                "covid_severity": self.covid_severity(),
                "date_of_consent": date_of_consent.isoformat(),
                "lab_test_result_value": self.lab_value(),
            },
        }

        # conditionally add vital status
        if vital_status := self.vital_status(
            min_date_of_death=date_of_consent, severe_covid=s["extra_properties"]["covid_severity"] == "Severe"
        ):
            s["vital_status"] = vital_status

        # conditionally add smoking status extra property
        if self.has_smoking_status():
            s["extra_properties"]["smoking_status"] = self.smoking_status()

        return s

    def vital_status(self, min_date_of_death, severe_covid: bool) -> dict | None:
        if not self.rng.biased_coin_toss(P_VITAL_STATUS_PRESENT):
            return None

        status = self.rng.weighted_choice(
            VITAL_STATUS_ENUM, P_VITAL_STATUS_DISTRIBUTION_SEVERE_COVID if severe_covid else P_VITAL_STATUS_DISTRIBUTION
        )

        vital_status = {
            "status": status,
        }

        if status == "DECEASED":
            vital_status["time_of_death"] = {
                "timestamp": self.rng.recent_datetime_string(min_date=min_date_of_death),
            }

            if severe_covid and self.rng.biased_coin_toss(P_COVID_CAUSE_OF_DEATH_GIVEN_SEVERE_COVID_AND_DEATH) == 1:
                vital_status["cause_of_death"] = VITAL_STATUS_CAUSE_OF_DEATH_COVID_19
            else:
                vital_status["cause_of_death"] = self.rng.weighted_choice(
                    VITAL_STATUS_CAUSES_OF_DEATH, P_VITAL_STATUS_CAUSES_OF_DEATH_DISTRIBUTION
                )

            if self.rng.biased_coin_toss(P_VITAL_STATUS_DECEASED_HAS_SURVIVAL_TIME):
                vital_status["survival_time_in_days"] = (
                    self.rng.int_from_gaussian_range(*VITAL_STATUS_SURVIVAL_TIME_DIST)
                    if "infarction" not in vital_status["cause_of_death"]["label"]
                    else 0
                )  # make heart attacks instant

        return vital_status

    # creates experiments associated with a biosample as a side effect
    def biosamples(self, individual):
        indiv_id = individual["id"]
        base_biosample_id = indiv_id[len("ind-") :] if indiv_id.startswith("ind-") else indiv_id
        b = []

        # add any real stuff from config
        if bs := individual.get("biosamples"):
            b.extend(bs)
        if es := individual.get("experiments"):
            self.experiments.extend(es)

        # add an experiment with vcf for all 1000 genomes ids, whether vcf exists or not
        if self.is_1000_genomes_id(individual["id"]):
            b.append(
                {
                    "id": base_biosample_id,
                    "sampled_tissue": {"id": "UBERON:0000178", "label": "blood"},
                }
            )
            self.add_experiment(one_thousand_genomes_experiment(self.rng, base_biosample_id))

        # randomly add more biosamples, with zero or more experiments
        synth_biosamples = self.synthetic_biosamples_with_experiments()

        for index, sb in enumerate(synth_biosamples):
            b_id = f"{base_biosample_id}-{index}"
            extra_biosample = self.synthetic_biosample_wrapper(sb, b_id)
            b.append(extra_biosample)
            for e in sb["experiments"]:
                if self.should_add_experiment_to_biosample():
                    self.add_experiment(synthetic_experiment_wrapper(self.rng, e, b_id))

        return b

    def diseases(self, individual, intp, covid_severity):
        # randomly choose some diseases
        ds = self.rng.zero_or_more_choices(DISEASES, DISEASE_MASS_DISTRIBUTION, self.choice_weights["diseases"])

        # very rarely, mark a disease as excluded
        ds_ex = [{**d, "excluded": True} if self.should_exclude() and "disease_stage" not in d else d for d in ds]

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
            self.choice_weights["phenotypic_features"],
        )

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
            self.choice_weights["interpretations"],
        )

    def medical_actions(self):
        action_procedures = self.rng.zero_or_more_choices(
            PROCEDURES,
            MEDICAL_ACTION_MASS_DISTRIBUTION,
            self.choice_weights["medical_actions_procedures"],
        )

        action_treatments = self.rng.zero_or_more_choices(
            treatments(self.rng),
            MEDICAL_ACTION_MASS_DISTRIBUTION,
            self.choice_weights["medical_actions_treatments"],
        )

        # could add top-level values here (treatment_target, etc.)
        return action_procedures + action_treatments

    # possible later TODO, currently we only attach files to experiments, not to phenopackets
    # def files(self):
    #     pass

    def metadata(self, date_of_consent: date):
        elements: list[Literal[0, 1, 2, 3]] = [0, 1, 2, 3]  # up to 3 updates per metadata object
        n_updates = self.rng.weighted_choice(elements, [0.6, 0.2, 0.1, 0.1])
        return metadata(self.rng, n_updates, date_of_consent)

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

    def smoking_status(self) -> str:
        return self.rng.weighted_choice(SMOKING_STATUS, self.choice_weights["smoking_status"])

    def synthetic_biosamples_with_experiments(self) -> list:
        return self.rng.zero_or_more_choices(
            TISSUES_WITH_EXPERIMENTS,
            EXTRA_BIOSAMPLES_MASS_DISTRIBUTION,
            self.choice_weights["synthetic_experiments"],
        )

    def biosample_location_collected(self):
        return self.rng.weighted_choice(BIOSAMPLE_LOCATIONS, self.choice_weights["biosample_locations"])

    def synthetic_biosample_wrapper(self, experiment, sb_id) -> dict:
        sb = {
            "id": sb_id,
        }
        if tissue := experiment["sampled_tissue"]:
            sb["sampled_tissue"] = tissue

        if self.should_add_location_collected_to_biosample():
            sb["location_collected"] = self.biosample_location_collected()

        return sb

    def should_add_experiment_to_biosample(self) -> bool:
        return bool(self.rng.biased_coin_toss(P_ADD_EXPERIMENT_TO_BIOSAMPLE))

    def should_add_location_collected_to_biosample(self):
        return bool(self.rng.biased_coin_toss(P_ADD_LOCATION_COLLECTED_TO_BIOSAMPLE))

    def should_exclude(self) -> bool:
        return bool(self.rng.biased_coin_toss(P_EXCLUDED))
