import json
from random_generator.generator import RandomGenerator
from individuals.generator import Individual

def main():
    # single generator for all random calls
    rng = RandomGenerator()

    with open("./config/individuals.json") as j:
        individuals = json.load(j)

    data = [Individual(rng, i) for i in individuals]
    phenopackets = [d.phenopacket for d in data]
    experiments = [d.experiments for d in data]

    with open("./synthetic_phenopackets_v2.json", "w") as pxf:
        json.dump(phenopackets, pxf, indent=4)
    with open("./synthetic_experiments.json", "w") as e:
        json.dump(experiments, e, indent=4)


if __name__ == "__main__":
    main()


# TODO: katsu config
# TODO: DATS
# these just need to be available, they don't need random generation
