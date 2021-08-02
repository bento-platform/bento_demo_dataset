#!/usr/bin/env python3

import json
import random
import uuid


STUDY_TYPE = ["Epigenomics", "Proteomics", "Metagenomics", "Transcriptomics", "Metabolomics", "Other"]
EXPERIMENT_TYPE = ["DNA Methylation", "RNA-Seq", "mRNA-Seq", "smRNA-Seq", "Histone H3K4me1"]
MOLECULE = ["total RNA", "polyA RNA", "cytoplasmic RNA", "nuclear RNA", "small RNA", "genomic DNA", "protein", "other"]
MOLECULE_ONTOLOGY = [{"id": "SO:0000991", "label": "genomic DNA"}, {"id": "EFO:0004964", "label": "total RNA"}]
LIBRARY_STRATEGY = ["RNA-Seq", "ChIP-Seq", "Bisulfite-Seq"]
LIBRARY_SOURCE = ["Genomic", "Genomic Single Cell", "Transcriptomic", "Transcriptomic Single Cell", "Metagenomic",
                  "Metatranscriptomic", "Synthetic", "Viral RNA", "Other"]
LIBRARY_SELECTION = ["Random", "PCR", "Random PCR", "RT-PCR", "MF", "Other"]
LIBRARY_LAYOUT = ["Single", "Paired"]
EXTRACTION_PROTOCOL = ["NGS", "GBS"]


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
            experiment = {
                "id": str(uuid.uuid4()),
                "study_type": random.choice(STUDY_TYPE),
                "experiment_type": random.choice(EXPERIMENT_TYPE),
                "molecule": random.choice(MOLECULE),
                "molecule_ontology": [random.choice(MOLECULE_ONTOLOGY)],
                "library_strategy": random.choice(LIBRARY_STRATEGY),
                "library_source": random.choice(LIBRARY_SOURCE),
                "library_selection": random.choice(LIBRARY_SELECTION),
                "library_layout": random.choice(LIBRARY_LAYOUT),
                "extraction_protocol": random.choice(EXTRACTION_PROTOCOL),
                "biosample": f"{sample}",
                "experiment_results": [
                    {
                        "identifier": f"{sample}_01",
                        "description": "VCF file",
                        "filename": f"{sample}_01.vcf.gz",
                        "file_format": "VCF",
                        "data_output_type": "Derived data",
                        "usage": "download",
                        "creation_date": "01-09-2021",
                        "created_by": "Admin",
                        "extra_properties": {
                            "target": "Unknown"
                        }
                    },
                    {
                        "identifier": f"{sample}_02",
                        "description": "CRAM file",
                        "filename": f"{sample}_02.sorted.dup.recal.cram",
                        "file_format": "CRAM",
                        "data_output_type": "Raw data",
                        "usage": "visualized",
                        "creation_date": "01-09-2021",
                        "created_by": "Admin",
                        "extra_properties": {
                            "target": "Unknown"
                        }
                    }
                ],
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
