
# copied from phenopackets docs, although with a few corrections
# https://phenopacket-schema.readthedocs.io/en/latest/interpretation.html
# note that these are chosen at random, so may not match what's actually in a vcf
# TODO? drop any diseases appearing here into diseases field

def interpretations(id):
    return [
        {
            "id": "interpretation:001",
            "progressStatus": "SOLVED",
            "diagnosis": {
                "disease": {
                    "id": "OMIM:263750",
                    "label": "Miller syndrome"
                },
                "genomicInterpretations": [
                    {
                        "subject_or_biosample_id": id,
                        "interpretationStatus": "CONTRIBUTORY",
                        "geneDescriptor": {
                            "valueId": "HGNC:2867",
                            "symbol": "DHODH"
                        }
                    }
                ]
            }
        },
        {
            "id": "interpretation:002",
            "progressStatus": "SOLVED",
            "diagnosis": {
                "disease": {
                    "id": "OMIM:154700",
                    "label": "Marfan syndrome"
                },
                "genomicInterpretations": [
                    {
                        "subjectOrBiosampleId": id,
                        "interpretationStatus": "CONTRIBUTORY",
                        "variantInterpretation": {
                            "acmgPathogenicityClassification": "PATHOGENIC",
                            "variationDescriptor": {
                                "expressions": [
                                    {
                                        "syntax": "hgvs",
                                        "value": "NM_000138.4(FBN1):c.6751T>A"
                                    }
                                ],
                                "allelicState": {
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
            "id": "interpretation:003",
            "progressStatus": "SOLVED",
            "diagnosis": {
                "disease": {
                    "id": "OMIM: 219700",
                    "label": "Cystic fibrosis"
                },
                "genomicInterpretations": [
                    {
                        "subjectOrBiosampleId": id,
                        "interpretationStatus": "CONTRIBUTORY",
                        "variantInterpretation": {
                            "acmgPathogenicityClassification": "PATHOGENIC",
                            "variationDescriptor": {
                                "expressions": [
                                    {
                                        "syntax": "hgvs",
                                        "value": "NM_000492.3(CFTR):c.1477C>T (p.Gln493Ter)"
                                    }
                                ],
                                "allelicState": {
                                    "id": "GENO:0000135",
                                    "label": "heterozygous"
                                }
                            }
                        }
                    },
                    {
                        "subjectOrBiosampleId": id,
                        "interpretationStatus": "CONTRIBUTORY",
                        "variantInterpretation": {
                            "acmgPathogenicityClassification": "PATHOGENIC",
                            "variationDescriptor": {
                                "expressions": [
                                    {
                                        "syntax": "hgvs",
                                        "value": "NM_000492.3(CFTR):c.1521_1523delCTT (p.Phe508delPhe)"
                                    }
                                ],
                                "allelicState": {
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
            "id": "interpretation:004",
            "progressStatus": "COMPLETED",
            "diagnosis": {
                "disease": {
                    "id": "NCIT:C3224",
                    "label": "Melanoma"
                },
                "genomicInterpretations": [
                    {
                        "subjectOrBiosampleId": id,
                        "interpretationStatus": "CONTRIBUTORY",
                        "variantInterpretation": {
                            "acmgPathogenicityClassification": "PATHOGENIC",
                            "therapeuticActionability": "ACTIONABLE",
                            "variationDescriptor": {
                                "expressions": [
                                    {
                                        "syntax": "hgvs",
                                        "value": "NM_001374258.1(BRAF):c.1919T>A (p.Val640Glu)"
                                    }
                                ],
                                "allelicState": {
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
