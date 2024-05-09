# synthetic experiments with a few sensible sampled_tissue values
TISSUES_WITH_EXPERIMENTS = [
    {
        "sampled_tissue": None,
        "experiments": [
            {
                "study_type": "Transcriptomics",
                "experiment_type": "RNA-Seq",
                "experiment_ontology": [{"id": "OBI:0001177", "label": "RNA sequencing assay"}],
                "library_strategy": "RNA-Seq",
                "library_selection": "Random PCR",
                "molecule": "total RNA",
                "molecule_ontology": [{"id": "EFO:0004964", "label": "total RNA"}],
            },
            {
                "study_type": "Proteomics",
                "experiment_type": "Proteomic profiling",
                "experiment_ontology": [{"id": "OBI:0001318", "label": "proteomic profiling by array assay"}],
            },
        ],
    },
    {
        "sampled_tissue": {"id": "NCIT:C13356", "label": "Plasma"},
        "experiments": [
            {
                "study_type": "Metabolomics",
                "experiment_type": "Metabolite profiling",
                "experiment_ontology": [{"id": "OBI:0000366", "label": "metabolite profiling assay"}],
            },
            {
                "study_type": "Proteomics",
                "experiment_type": "Proteomic profiling",
                "experiment_ontology": [{"id": "OBI:0001318", "label": "proteomic profiling by array assay"}],
            },
            {
                "study_type": "Other",
                "experiment_type": "Other",
                "experiment_ontology": [{"id": "OBI:0003172", "label": "thyroid stimulating hormone concentration assay"}],
            },
        ],
    },
    {
        "sampled_tissue": {"id": "NCIT:C13325", "label": "Serum"},
        "experiments": [
            {
                "study_type": "Serology",
                "experiment_type": "Neutralizing antibody titers",
                "experiment_ontology": [{"id": "EFO:0004556", "label": "antibody measurement"}],
            }
        ],
    },
    {
        "sampled_tissue": None,
        "experiments": [
            {
                "study_type": "Other",
                "experiment_type": "Other",
                "experiment_ontology": [{"id": "OBI:0000537", "label": "copy number variation profiling assay"}],
            }
        ],
    },
]


# references to files in "dataset_files/example_experiments" directory
GENERIC_EXPERIMENT_FILES = [
    {"filename": "example.csv", "file_type": "CSV"},
    {"filename": "example.docx", "file_type": "DOCX"},
    {"filename": "example.jpg", "file_type": "JPEG"},
    {"filename": "example.md", "file_type": "MARKDOWN"},
    {"filename": "example.pdf", "file_type": "PDF"},
    {"filename": "example.xlsx", "file_type": "XLSX"},
    {"filename": "example.mp4", "file_type": "MP4"},
]

EXPERIMENT_RESOURCES = [
    {
        "name": "Ontology for Biomedical Investigations",
        "version": "2020-12-16",
        "namespace_prefix": "OBI",
        "id": "OBI:2020-12-16",
        "iri_prefix": "http://purl.obolibrary.org/obo/OBI_",
        "url": "http://purl.obolibrary.org/obo/obi.owl",
    },
    {
        "name": "Experimental Factor Ontology",
        "version": "2021-02-16",
        "namespace_prefix": "EFO",
        "id": "EFO:2021-02-16",
        "iri_prefix": "http://www.ebi.ac.uk/efo/EFO_",
        "url": "http://www.ebi.ac.uk/efo/releases/v3.27.0/efo.owl",
    },
]
