#!/usr/bin/env python3

import json
import random
from datetime import date
from faker import Faker

from divide_samples import datasets
from ontology_terms import PHENOTYPIC_FEATURES
from controlled_vocabularies import SMOKING, COVIDSTATUS, VITAL_STATUS, MOBILITY
from utils import generic_random_choices


fake = Faker()

Faker.seed(108643)
random.seed(19618)


SECONDS_IN_YEAR = 60 * 60 * 24 * 365


def main():
    # Each phenopacket corresponds to one patient encounter.

    dataset_phenopackets = ([], [], [])

    with open("./samples.tsv", "r") as sf:
        sample_sexes = {s.split("\t")[0]: s.split("\t")[1].strip() for s in sf.readlines()}

    for dataset_samples, phenopackets in zip(datasets, dataset_phenopackets):
        for s in dataset_samples:
            individual_id = f"ind:{s}"
            individual_dob = fake.date_of_birth(minimum_age=20, maximum_age=100)
            individual_age = date.today() - individual_dob

            age_years = individual_age.total_seconds() // SECONDS_IN_YEAR  # Missing leap years; oh well
            age_string = f"P{int(age_years)}Y"

            ind_phenopacket = {
                "subject": {
                    "id": individual_id,
                    "date_of_birth": individual_dob.isoformat(),
                    "age": {
                        "age": age_string
                    },
                    "sex": sample_sexes[s],
                    "karyotypic_sex": "XX" if sample_sexes[s] == "FEMALE" else "XY",  # TODO: Spice it up a bit
                    "taxonomy": {
                        "id": "NCBITaxon:9606",
                        "label": "Homo sapiens",
                    },
                    "extra_properties": {
                        "smoking": generic_random_choices(SMOKING),
                        "covidstatus": generic_random_choices(COVIDSTATUS),
                        "death_dc": generic_random_choices(VITAL_STATUS),
                        "mobility": generic_random_choices(MOBILITY)
                    }
                },
                "phenotypic_features": [{"type": generic_random_choices(PHENOTYPIC_FEATURES)}],
                "diseases": [],
                "meta_data": {
                    "created_by": "David Lougheed",
                    "submitted_by": "Ksenia Zaytseva",
                    "resources": [
                        {
                            "id": "NCBITaxon:2018-07-27",
                            "name": "NCBI Taxonomy OBO Edition",
                            "namespace_prefix": "NCBITaxon",
                            "url": "http://purl.obolibrary.org/obo/ncbitaxon.owl",
                            "version": "2018-07-27",
                            "iri_prefix": "http://purl.obolibrary.org/obo/NCBITaxon_"
                        },
                        {
                            "id": "UBERON:2019-06-27",
                            "name": "Uber-anatomy ontology",
                            "namespace_prefix": "UBERON",
                            "url": "http://purl.obolibrary.org/obo/uberon.owl",
                            "version": "2019-06-27",
                            "iri_prefix": "http://purl.obolibrary.org/obo/UBERON"
                        },
                        {
                            "id": "NCIT:2015-09-01",
                            "name": "NCI Thesaurus",
                            "namespace_prefix": "NCIT",
                            "url": "https://ncit.nci.nih.gov",
                            "version": "2015-09-01",
                            "iri_prefix": "https://ncit.nci.nih.gov"
                        }
                    ],
                    "updates": [],
                    "external_references": []
                },
                "biosamples": [
                    {
                        "id": s,  # TODO: Different biosample ID vs subject ID
                        "individual_id": individual_id,  # TODO: Do we need to provide this?
                        "description": f"Biosample for patient {s}",
                        "sampled_tissue": {
                            "id": "UBERON:0000178",
                            "label": "blood"
                        },
                        "phenotypic_features": [],  # TODO
                        "individual_age_at_collection": {
                            "age": age_string
                        },  # TODO: Calculate from DOB
                        "diagnostic_markers": [],  # TODO
                        "procedure": {
                            "code": {
                                "id": "NCIT:C15189",
                                "label": "Biopsy"
                            }
                        },
                        "is_control_sample": False
                    }
                ]
            }

            for i in range(random.choices([0, 1, 2], [0.8, 0.1, 0.1], k=1)[0]):
                next_biosample = {
                        "id": f"{s}_{i}",
                        "individual_id": individual_id,
                        "description": f"Biosample for patient {s}",
                        "sampled_tissue": {
                            "id": "UBERON:0000178",
                            "label": "blood"
                        },
                        "individual_age_at_collection": {
                            "age": age_string
                        },
                        "procedure": {
                            "code": {
                                "id": "NCIT:C15189",
                                "label": "Biopsy"
                            }
                        },
                        "is_control_sample": False
                    }
                ind_phenopacket["biosamples"].append(next_biosample)

            if s == "NA19648":
                ind_phenopacket["diseases"] = [
                    {
                        "term": {
                            "id": "NCIT:C4872",
                            "label": "Breast Carcinoma"
                        },
                        "onset": {
                            "age": f"P{int(age_years - random.randrange(0, 5))}Y"
                        }
                    }
                ]

            phenopackets.append(ind_phenopacket)

    for di, p in enumerate(dataset_phenopackets):
        with open(f"dataset_{di}.json", "w") as output:
            json.dump(p, output, indent=4)


if __name__ == "__main__":
    main()
