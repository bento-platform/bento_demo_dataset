from datetime import date, datetime, timezone
from random_generator.generator import RandomGenerator
from typing import Literal


# ideally we would only mention resources used in a particular phenopacket
# rather than including all each time.
def metadata(rng: RandomGenerator, n_updates: Literal[0, 1, 2, 3], min_update_date: date):
    created_datetime = datetime.now(timezone.utc)
    return {
        "created": created_datetime.isoformat(timespec="seconds"),
        "created_by": "C3G_synthetic_data",
        "phenopacket_schema_version": "2.0",
        "resources": RESOURCES,
        **({"updates": updates(rng, n_updates, min_update_date, created_datetime.date())} if n_updates else {}),
    }


RESOURCES = [
    {
        "name": "NCBI Taxonomy OBO Edition",
        "version": "2023-09-19",
        "namespace_prefix": "NCBITaxon",
        "id": "NCBITaxon:2023-09-19",
        "iri_prefix": "http://purl.obolibrary.org/obo/NCBITaxon_",
        "url": "http://purl.obolibrary.org/obo/ncbitaxon/2023-09-19/ncbitaxon.owl",
    },
    {
        "id": "UBERON:2019-06-27",
        "name": "Uber-anatomy ontology",
        "namespace_prefix": "UBERON",
        "url": "http://purl.obolibrary.org/obo/uberon.owl",
        "version": "2019-06-27",
        "iri_prefix": "http://purl.obolibrary.org/obo/UBERON_",
    },
    {
        "name": "National Cancer Institute Thesaurus",
        "version": "2021-02-12",
        "namespace_prefix": "NCIT",
        "id": "NCIT:2021-02-12",
        "iri_prefix": "http://purl.obolibrary.org/obo/NCIT_",
        "url": "http://purl.obolibrary.org/obo/ncit/releases/2021-02-12/ncit.owl",
    },
    {
        "name": "GENO ontology",
        "version": "2023-10-08",
        "namespace_prefix": "GENO",
        "id": "GENO:2023-10-08",
        "iri_prefix": "http://purl.obolibrary.org/obo/GENO_",
        "url": "http://purl.obolibrary.org/obo/geno/releases/2023-10-08/geno.owl",
    },
    {
        "name": "The Human Phenotype Ontology",
        "version": "2023-09-01",
        "namespace_prefix": "HP",
        "id": "HP:2023-09-01",
        "iri_prefix": "http://purl.obolibrary.org/obo/HP_",
        "url": "http://purl.obolibrary.org/obo/hp/releases/2023-09-01/hp.owl",
    },
    {
        "name": "SNOMED Clinical Terms",
        "version": "2019-04-11",
        "namespace_prefix": "SNOMED",
        "id": "SNOMED:2019-04-11",
        "iri_prefix": "http://purl.bioontology.org/ontology/SNOMEDCT/",
        "url": "http://purl.bioontology.org/ontology/SNOMEDCT",
    },
    {
        "name": "Mondo Disease Ontology",
        "version": "2025-06-03",
        "namespace_prefix": "MONDO",
        "id": "MONDO:2025-06-03",
        "iri_prefix": "http://purl.obolibrary.org/obo/MONDO_",
        "url": "http://purl.obolibrary.org/obo/mondo/releases/2025-06-03/mondo-international.owl",
    },
]


def updates(rng: RandomGenerator, n: int, min_update_date: date, max_update_date: date):
    update_timestamps = sorted(
        rng.recent_datetime_string(min_date=min_update_date, max_date=max_update_date) for _ in range(3)
    )
    return [
        {
            "timestamp": update_timestamps[0],
            "updated_by": "C3G_synthetic_data",
            "comment": "Fake update for testing",
        },
        {
            "timestamp": update_timestamps[1],
            "comment": "A second fake update",
        },
        {
            "timestamp": update_timestamps[2],
        },
    ][:n]
