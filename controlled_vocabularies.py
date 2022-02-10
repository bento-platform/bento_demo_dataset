# Controlled vocabularies for Experiments

STUDY_TYPE = [
    "Epigenomics",
    "Proteomics",
    "Metagenomics",
    "Transcriptomics",
    "Metabolomics",
    "Other",
]

EXPERIMENT_TYPE = [
    "DNA Methylation",
    "RNA-Seq",
    "mRNA-Seq",
    "smRNA-Seq",
    "Histone H3K4me1",
]

EXPERIMENT_ONTOLOGY = [
    {"id": "OBI:0002118", "label": "exome sequencing assay"},
    {"id": "OBI:0002117", "label": "whole genome sequencing assay"},
]

MOLECULE = [
    "total RNA",
    "polyA RNA",
    "cytoplasmic RNA",
    "nuclear RNA",
    "small RNA",
    "genomic DNA",
    "protein",
    "other", ]

MOLECULE_ONTOLOGY = [
    {"id": "SO:0000991", "label": "genomic DNA"},
    {"id": "EFO:0004964", "label": "total RNA"},
]

LIBRARY_STRATEGY = [
    "RNA-Seq",
    "ChIP-Seq",
    "Bisulfite-Seq",
]

LIBRARY_SOURCE = [
    "Genomic",
    "Genomic Single Cell",
    "Transcriptomic",
    "Transcriptomic Single Cell",
    "Metagenomic",
    "Metatranscriptomic",
    "Synthetic",
    "Viral RNA",
    "Other",
]

LIBRARY_SELECTION = [
    "Random",
    "PCR",
    "Random PCR",
    "RT-PCR",
    "MF",
    "Other",
]

LIBRARY_LAYOUT = [
    "Single",
    "Paired",
]

EXTRACTION_PROTOCOL = [
    "NGS",
    "GBS",
]

# Controlled vocabularies for extra_properties field

SMOKING = [
    "Non-smoker",
    "Smoker",
    "Former smoker",
    "Passive smoker",
    "Not specified",
]

COVIDSTATUS = [
    "Positive",
    "Negative",
    "Indeterminate",
]

VITAL_STATUS = [
    "Alive",
    "Deceased",
]

MOBILITY = [
    "I have no problems in walking about",
    "I have slight problems in walking about",
    "I have moderate problems in walking about",
    "I have severe problems in walking about",
    "I am unable to walk about",
]
