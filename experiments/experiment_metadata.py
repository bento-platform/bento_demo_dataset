from constants import DEFAULT_ASSEMBLY, P_ADD_FAKE_CRAM_TO_1K_VCF, P_ADD_EXAMPLE_FILE_TO_EXPERIMENT
from experiments.experiment_constants import SYNTHETIC_EXPERIMENT_TYPES, GENERIC_EXPERIMENT_FILES


def one_thousand_genomes_experiment(rng, biosample_id):
    vcf_filename = biosample_id + ".vcf.gz"  # our 1000 genomes vcf_filename convention
    experiment = vcf_experiment_metadata(rng, biosample_id, vcf_filename)
    if randomly_add_cram_to_1k(rng):
        cram_filename = biosample_id + ".cram"
        experiment["experiment_results"].append(cram_file_metadata(rng, cram_filename))
    return experiment


def randomly_add_cram_to_1k(rng):
    return bool(rng.biased_coin_toss(P_ADD_FAKE_CRAM_TO_1K_VCF))


def vcf_experiment_metadata(rng, biosample_id, filename=None, assembly_id=DEFAULT_ASSEMBLY):
    experiment_id = rng.uuid4()
    if filename is None:
        # "good enough" fake filename, we don't care about filename collisions between fake files
        filename = biosample_id + "-" + experiment_id[4:] + ".gz.vcf"
    return {
        "id": experiment_id,
        "biosample": biosample_id,
        "experiment_type": "WGS",
        "study_type": "Genomics",
        "molecule": "genomic DNA",
        "molecule_ontology": [
            {
                "id": "EFO:0008479",
                "label": "genomic DNA"
            }
        ],
        "experiment_ontology": [
            {
                "id": "OBI:0002117",
                "label": "whole genome sequencing assay"
            }
        ],
        "instrument": {
            "platform": "Illumina",
            "model": "Illumina Genome Analyzer II",
            "identifier": "Illumina Genome Analyzer II"
        },
        "library_source": "Genomic",
        "library_strategy": "WGS",
        "library_selection": "PCR",
        "experiment_results": [vcf_file_metadata(rng, filename, assembly_id)]
    }


def random_synthetic_experiment(rng, biosample_id):
    return rng.gaussian_choice([synthetic_experiment_wrapper(rng, biosample_id, exp)
                                for exp in SYNTHETIC_EXPERIMENT_TYPES])


def randomly_add_example_file(rng):
    return bool(rng.biased_coin_toss(P_ADD_EXAMPLE_FILE_TO_EXPERIMENT))


def synthetic_experiment_wrapper(rng, biosample_id, experiment_type):
    e = {
        "id": rng.uuid4(),
        "biosample": biosample_id,
        **experiment_type
    }
    if randomly_add_example_file(rng):
        e["experiment_results"] = random_generic_file_metadata(rng)
    return e


def random_generic_file_metadata(rng):
    filename, file_type = rng.gaussian_choice(GENERIC_EXPERIMENT_FILES).values()
    return generic_file_metadata(rng, filename, file_type)


# files ---------------------------

def vcf_file_metadata(rng, filename, assembly_id=DEFAULT_ASSEMBLY):
    return {
        "identifier": rng.uuid4(),
        "creation_date": rng.recent_date_string(),
        "data_output_type": "Derived data",
        "usage": "Downloaded",
        "created_by": "C3G_synthetic_data",
        "description": "VCF file",
        "filename": filename,
        "file_format": "VCF",
        "genome_assembly_id": assembly_id
    }


def cram_file_metadata(rng, filename, assembly_id=DEFAULT_ASSEMBLY):
    return {
        "identifier": rng.uuid4(),
        "data_output_type": "Derived data",
        "usage": "Downloaded",
        "created_by": "C3G_synthetic_data",
        "description": "Alignment File",
        "filename": filename,
        "file_format": "CRAM",
        "genome_assembly_id": assembly_id
    }


def bigwig_file_metadata(rng, filename, assembly_id=DEFAULT_ASSEMBLY):
    return {
        "identifier": rng.uuid4(),
        "creation_date": rng.recent_date_string(),
        "data_output_type": "Derived data",
        "usage": "Downloaded",
        "created_by": "C3G_synthetic_data",
        "description": "RNAseq coverage",
        "filename": filename,
        "file_format": "BigWig",
        "genome_assembly_id": assembly_id
    }


def generic_file_metadata(rng, filename, file_type):
    return {
        "identifier": rng.uuid4(),
        "usage": "Downloaded",
        "created_by": "C3G_synthetic_data",
        "filename": filename,
        "file_format": file_type,
    }
