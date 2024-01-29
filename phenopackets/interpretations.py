
# copied from phenopackets docs, although with a few corrections
# https://phenopacket-schema.readthedocs.io/en/latest/interpretation.html
# note that these are chosen at random, so may not match what's actually in a vcf

def interpretations(rng, id):
    return [
        {
            "id": f"{id}-interpretation-000",
            "progress_status": "UNKNOWN_PROGRESS",
            "summary": "diagnosis in progress"
        },
        {
            "id": f"{id}-interpretation:001",
            "progress_status": "SOLVED",
            "diagnosis": {
                "disease": {
                    "id": "OMIM:263750",
                    "label": "Miller syndrome"
                },
                "genomic_interpretations": [
                    {
                        "subject_or_biosample_id": id,
                        "interpretation_status": "CONTRIBUTORY",
                        "gene_descriptor": {
                            "value_id": "HGNC:2867",
                            "symbol": "DHODH"
                        }
                    }
                ]
            }
        },
        {
            "id": f"{id}-interpretation-002",
            "progress_status": "SOLVED",
            "diagnosis": {
                "disease": {
                    "id": "OMIM:154700",
                    "label": "Marfan syndrome"
                },
                "genomic_interpretations": [
                    {
                        "subject_or_biosample_id": id,
                        "interpretation_status": "CONTRIBUTORY",
                        "variant_interpretation": {
                            "acmg_pathogenicity_classification": "PATHOGENIC",
                            "therapeutic_actionability": "UNKNOWN_ACTIONABILITY",
                            "variation_descriptor": {
                                "id": rng.uuid4(),
                                "molecule_context": "genomic",
                                "expressions": [
                                    {
                                        "syntax": "hgvs",
                                        "value": "NM_000138.4(FBN1):c.6751T>A"
                                    }
                                ],
                                "allelic_state": {
                                    "id": "GENO:0000135",
                                    "label": "heterozygous"
                                }
                            }
                        }
                    }
                ]
            }
        },
        {
            "id": f"{id}-interpretation-003",
            "progress_status": "SOLVED",
            "diagnosis": {
                "disease": {
                    "id": "OMIM:219700",
                    "label": "Cystic fibrosis"
                },
                "genomic_interpretations": [
                    {
                        "subject_or_biosample_id": id,
                        "interpretation_status": "CONTRIBUTORY",
                        "variant_interpretation": {
                            "acmg_pathogenicity_classification": "PATHOGENIC",
                            "therapeutic_actionability": "UNKNOWN_ACTIONABILITY",
                            "variation_descriptor": {
                                "id": rng.uuid4(),
                                "molecule_context": "genomic",
                                "expressions": [
                                    {
                                        "syntax": "hgvs",
                                        "value": "NM_000492.3(CFTR):c.1477C>T (p.Gln493Ter)"
                                    }
                                ],
                                "allelic_state": {
                                    "id": "GENO:0000135",
                                    "label": "heterozygous"
                                }
                            }
                        }
                    },
                    {
                        "subject_or_biosample_id": id,
                        "interpretation_status": "CONTRIBUTORY",
                        "variant_interpretation": {
                            "acmg_pathogenicity_classification": "PATHOGENIC",
                            "therapeutic_actionability": "UNKNOWN_ACTIONABILITY",
                            "variation_descriptor": {
                                "id": rng.uuid4(),
                                "molecule_context": "genomic",
                                "expressions": [
                                    {
                                        "syntax": "hgvs",
                                        "value": "NM_000492.3(CFTR):c.1521_1523delCTT (p.Phe508delPhe)"
                                    }
                                ],
                                "allelic_state": {
                                    "id": "GENO:0000135",
                                    "label": "heterozygous"
                                }
                            }
                        }
                    }
                ]
            }
        },
        {
            "id": f"{id}-interpretation-004",
            "progress_status": "COMPLETED",
            "diagnosis": {
                "disease": {
                    "id": "NCIT:C3224",
                    "label": "Melanoma"
                },
                "genomic_interpretations": [
                    {
                        "subject_or_biosample_id": id,
                        "interpretation_status": "CONTRIBUTORY",
                        "variant_interpretation": {
                            "acmg_pathogenicity_classification": "PATHOGENIC",
                            "therapeutic_actionability": "ACTIONABLE",
                            "variation_descriptor": {
                                "id": rng.uuid4(),
                                "molecule_context": "genomic",
                                "expressions": [
                                    {
                                        "syntax": "hgvs",
                                        "value": "NM_001374258.1(BRAF):c.1919T>A (p.Val640Glu)"
                                    }
                                ],
                                "allelic_state": {
                                    "id": "GENO:0000135",
                                    "label": "heterozygous"
                                }
                            }
                        }
                    }
                ]
            }
        }
    ]
