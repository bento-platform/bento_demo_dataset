import json
from phenopackets.generate_phenopackets import generate_phenopackets
from experiments.generate_experiments_v2xxx import generate_experiments_v2
from random_generator.generator import RandomGenerator


def main():
    # single generator for all random calls
    # rng = np.random.default_rng(seed=RANDOM_SEED)   #bare numpy version 
    rng = RandomGenerator()

# input
# TODO: revisit this config approach
    with open("./data/samples.tsv", "r") as sf:
        # individuals = {s.split("\t")[0]: {"sex": s.split("\t")[1].strip()} for s in sf.readlines()}
        individuals = [{"id": s.split("\t")[0], "sex": s.split("\t")[1].strip()} for s in sf.readlines()]

    with open("./data/has_vcf.csv", "r") as v:
        vcf_ids = [v_id.strip() for v_id in v.readlines()]
        # print(vcf_ids)

    # add vcfs to anyone who has one
    individuals_with_vcfs = list(
        map(lambda s: {**s, "vcf_file": f"{s['id']}.vcf.gz"} if s["id"] in vcf_ids else s, individuals))
    print(individuals_with_vcfs)

# generation

    phenopackets = generate_phenopackets(rng, individuals_with_vcfs)
    experiments = generate_experiments_v2(rng, individuals_with_vcfs)

# output

    # plus a version number in the name?
    with open("./synthetic_phenopackets_v2.json", "w") as pxf:
        json.dump(phenopackets, pxf, indent=4)

    with open("./synthetic_experiments.json", "w") as e:
        json.dump(experiments, e, indent=4)


if __name__ == "__main__":
    main()


# should also have a katsu config.json somewhere
# this is the same each time, so doesn't need to be generated

# a few phenotypic_features should be excluded
