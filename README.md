# Bento Demo Dataset

Partially synthetic demo dataset for the Bento platform.

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
The generation of VCF files is optional and conditional to having the `bcftools` executable in the PATH. **This does not work on Windows systems**.
Please refer to the [Samtools web page](http://www.htslib.org/download/) for installation instructions. Note that on MacOS, bcftools can also be installed
using the `brew` package manager.


#### Usage:

Generate phenopackets metadata:

```
python samples_to_phenopackets.py
```

Generate VCF files from 1000 genomes chromosome 22 (requires `bcftools`)
```
sh sample.vcf.sh
```

Generate experiments metadata linked to the sample ids and the VCF files
if they are present in the `data` directory. When no VCF file matching the
sample ID is present, a random hash is generated and appended to the filename.

```
python generate_experiments.py
```
