# experiments without real data files
SYNTHETIC_EXPERIMENT_TYPES = [
    {
        "study_type": "Transcriptomics",
        "experiment_type": "RNA-Seq",
        "experiment_ontology": [
            {
                "id": "OBI:0001177",
                "label": "RNA sequencing assay"
            }
        ]
    },
    {
        "study_type": "Metabolomics",
        "experiment_type": "Metabolite profiling",
        "experiment_ontology": [
            {
                "id": "OBI:0000366",
                "label": "metabolite profiling assay"
            }
        ]
    },
    {
        "study_type": "Proteomics",
        "experiment_type": "Proteomic profiling",
        "experiment_ontology": [
            {
                "id": "OBI:0001318",
                "label": "proteomic profiling by array assay"
            }
        ],
    },
    {
        "study_type": "Serology",
        "experiment_type": "Neutralizing antibody titers",
        "experiment_ontology": [
            {
                "id": "EFO:0004556",
                "label": "antibody measurement"
            }
        ],
    },
    {
        "study_type": "Other",
        "experiment_type": "Other",
        "experiment_ontology": [
            {
                "id": "OBI:0000537",
                "label": "copy number variation profiling assay"
            }
        ]
    }
]

# references to files in "dataset_files/example_experiments" directory
GENERIC_EXPERIMENT_FILES = [
    {
        "filename": "example.csv",
        "file_type": "CSV"
    },
    {
        "filename": "example.jpg",
        "file_type": "JPEG"
    },
    {
        "filename": "example.md",
        "file_type": "MARKDOWN"
    },
    {
        "filename": "example.pdf",
        "file_type": "PDF"
    },
    {
        "filename": "example.xlsx",
        "file_type": "XLSX"
    },
]

EXPERIMENT_RESOURCES = [
    {
        "name": "Ontology for Biomedical Investigations",
        "version": "2020-12-16",
        "namespace_prefix": "OBI",
        "id": "OBI:2020-12-16",
        "iri_prefix": "http://purl.obolibrary.org/obo/OBI_",
        "url": "http://purl.obolibrary.org/obo/obi.owl"
    },
    {
        "name": "Experimental Factor Ontology",
        "version": "2021-02-16",
        "namespace_prefix": "EFO",
        "id": "EFO:2021-02-16",
        "iri_prefix": "http://www.ebi.ac.uk/efo/EFO_",
        "url": "http://www.ebi.ac.uk/efo/releases/v3.27.0/efo.owl"
    }
]
