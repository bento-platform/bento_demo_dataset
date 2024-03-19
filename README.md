# Bento Demo Dataset

Partially synthetic demo dataset for the Bento platform. Requires Python 3.10+

Based partly on data from:

- [The 1000 Genomes project](https://www.internationalgenome.org/), &copy; EMBL-EBI
- [The International Human Epigenome Consortium](https://ihec-epigenomes.org/)

#### Requirements:

Optionally create a virtual environment, e.g.:

```
virtualenv -p python3 ./env
source env/bin/activate
```

To install dependencies run:

```
pip install -r requirements.txt
```
<!-- The generation of VCF files is optional and conditional to having the `bcftools` executable in the PATH. **This does not work on Windows systems**.
Please refer to the [Samtools web page](http://www.htslib.org/download/) for installation instructions. Note that on MacOS, bcftools can also be installed
using the `brew` package manager. -->


#### Usage:

To run:

```
python generate_dataset.py
```

This will write phenopackets to `synthetic_phenopackets.json` and experiments to `synthetic_experiments.json`.

Other useful files are available in the `/dataset_files` directory:
- `config.json`: a [Katsu](https://github.com/bento-platform/katsu) config file matching the dataset
- `dats.json`: an example [DATS](https://github.com/datatagsuite) file
- `extra_properties_typing.json`: to configure typed extra properties
- mock experiment files in `.csv`, `.jpg`, `.md`, `.mp4`, `.pdf`, and `.xlsx` format



#### Optional Configuration:

The dataset is a mix of fixed and randomly generated values, random values will be the same across different runs of generate_dataset.py. To change the output, modify any of the values in [config/constants.py](config/constants.py).

The dataset is generated based on the input file [config/individuals.json](config/individuals.json). You can add (or remove) individuals for different output. Individuals with "id" and "sex" fields only will get fully synthetic metadata, while any values in the "biosamples", "experiments" or "diseases" fields will be copied over unmodified. This allows, for example, to generate appropriate metadata for real data files (which may involve, e.g., a particular disease).


#### Optional Data Files:

The dataset is meant for use with genomic data from the 1000 Genomes Project, and transcriptomics data from the International Human Epigenome Consortium. See [here](./dataset_files/README.md) for more details on data files. 