import json
from random_generator.generator import RandomGenerator
from individuals.generator import IndividualGenerator
from experiments.experiment_details import EXPERIMENT_RESOURCES
from config.constants import GENERATE_TRANSCRIPTOMICS_MATRIX


def main():
    rng = RandomGenerator()
    individual_generator = IndividualGenerator(rng)

    with open("./config/individuals.json") as j:
        individuals = json.load(j)

    for i in individuals:
        individual_generator.generate_data(i)

    phenopackets = individual_generator.phenopackets
    experiments = individual_generator.experiments

    if GENERATE_TRANSCRIPTOMICS_MATRIX:
        biosamples_rna_seq = [e["biosample"] for e in individual_generator.experiments if e["experiment_type"] == "RNA-Seq"]
        individual_generator.generate_and_assign_matrices(biosamples_rna_seq)

    experiments_dict = {
        "experiments": experiments,
        "resources": EXPERIMENT_RESOURCES
    }

    with open("./synthetic_phenopackets_v2.json", "w") as pxf:
        json.dump(phenopackets, pxf, indent=4)
    with open("./synthetic_experiments.json", "w") as e:
        json.dump(experiments_dict, e, indent=4)

    print(f"Created {len(phenopackets)} phenopackets and {len(experiments)} experiments")


if __name__ == "__main__":
    main()
