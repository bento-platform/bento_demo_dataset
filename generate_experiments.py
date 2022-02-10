#!/usr/bin/env python3

import json
import random
import uuid

from utils import generic_random_choices
from controlled_vocabularies import *


def single_experiment_result(sample_id, file_format):
    # generate a single experiment result: VCF or CRAM
    experiment_result = {
        "identifier": f"{sample_id}_{uuid.uuid4()}",
        "creation_date": "01-09-2021",
        "created_by": "Admin",
        "extra_properties": {
            "target": "Unknown"
        }
    }
    if file_format == "VCF":
        experiment_result_vcf = {
            "description": "VCF file",
            "filename": f"{sample_id}_{uuid.uuid4()}.vcf.gz",
            "file_format": "VCF",
            "data_output_type": "Derived data",
            "usage": "download",
        }
        experiment_result.update(experiment_result_vcf)
    elif file_format == "CRAM":
        experiment_result_cram = {
            "description": "CRAM file",
            "filename": f"{sample_id}_{uuid.uuid4()}.sorted.dup.recal.cram",
            "file_format": "CRAM",
            "data_output_type": "Raw data",
            "usage": "visualized",
        }
        experiment_result.update(experiment_result_cram)
    else:
        raise Exception("Specify file format.")

    return experiment_result


def attach_experiment_results(sample_id):
    # generate a random list of random experiment results
    range_numbers = [0, 1, 2, 3, 4]
    experiments_results = []
    for i in range(random.choices(range_numbers, [0.1, 0.3, 0.4, 0.1, 0.1], k=1)[0]):
        exp_result = single_experiment_result(sample_id, random.choices(["VCF", "CRAM"], [0.6, 0.4], k=1)[0])
        experiments_results.append(exp_result)
    return experiments_results


def main():
    experiments = {
        "experiments": [],
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
    with open("./samples.tsv", "r") as sf:
        for s in sf.readlines():
            sample = s.split("\t")[0]
            # attach biosamples with many experiments
            for i in range(random.choices([0, 1, 2, 3], [0.3, 0.5, 0.1, 0.1], k=1)[0]):
                experiment = {
                    "id": str(uuid.uuid4()),
                    "study_type": generic_random_choices(STUDY_TYPE),
                    "experiment_type": generic_random_choices(EXPERIMENT_TYPE),
                    "experiment_ontology": [generic_random_choices(EXPERIMENT_ONTOLOGY)],
                    "molecule": generic_random_choices(MOLECULE),
                    "molecule_ontology": [generic_random_choices(MOLECULE_ONTOLOGY)],
                    "library_strategy": generic_random_choices(LIBRARY_STRATEGY),
                    "library_source": generic_random_choices(LIBRARY_SOURCE),
                    "library_selection": generic_random_choices(LIBRARY_SELECTION),
                    "library_layout": generic_random_choices(LIBRARY_LAYOUT),
                    "extraction_protocol": generic_random_choices(EXTRACTION_PROTOCOL),
                    "biosample": f"{sample}",
                    "experiment_results": attach_experiment_results(str(sample)),
                    "instrument": {
                        "identifier": "instrument:01",
                        "platform": "Illumina",
                        "description": "Illumina",
                        "model": "Illumina HiSeq 4000",
                        "extra_properties": {
                            "date": "2021-06-21"
                        }
                    },
                    "extra_properties": {
                        "comment": "This is randomly generated data for the test purposes only."
                    }
                }
                experiments["experiments"].append(experiment)

    # save experiments to the file
    with open(f"experiments.json", "w") as output:
        json.dump(experiments, output, indent=4)

    print(f"Created {len(experiments['experiments'])} experiments")


if __name__ == "__main__":
    main()
