# Controlled vocabularies for Experiments

STUDY_TYPE = [
    "Genomics",
    "Epigenomics",
    "Metagenomics",
    "Transcriptomics",
    "Other",
]

EXPERIMENT_TYPE = [
    "DNA Methylation",
    "RNA-Seq",
    "mRNA-Seq",
    "smRNA-Seq",
    "WES",
    "Other"
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
    "Other", ]

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
    "Exome capture",
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
