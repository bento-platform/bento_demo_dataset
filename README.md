# CHORD Demo Dataset

Partially synthetic demo dataset for CHORD.

Portions are courtesy of the 1000 Genomes project, &copy; EMBL-EBI.

#### Requirements:

Create virtual environment, e.g.:

```
virtualenv -p python3 ./env
source env/bin/activate
```

To install dependencies run:

```
pip install -r requirements.txt
```

#### Usage:

Generate phenopackets metadata:

```
python samples_to_phenopackets.py
```

Generate experiments metadata linked to the sample ids:

```
python generate_experiments.py
```