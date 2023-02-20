# Generate a set of VCF files from the 1000 genomes project
# Each file corresponds to 1 individual (here also a sample) and the
# filename is a catenation of the sample ID and file shecksum (using sha1)
# To reduce VCF file size, the variants are filtered against the AF field value:
# modify the AF_THRESHOLD value accordingly.

# The VCF from 1000 genomes for Chromosome 22 (because it is small)
ORIG_VCF=ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz
FILTERED_VCF=filtered.vcf
AF_THRESHOLD=0.97
CACHE_DIR=./cache
DATA_DIR=./data

check_prerequisites()
{
    # bcftools
    if ! command -v bcftools &> /dev/null
    then
        echo "Error: bcftools could not be found"
        exit 1
    fi

    # compgen
    if ! command -v compgen &> /dev/null
    then
        echo "Error: compgen utility could not be found"
        exit 1
    fi
}

download_orig_file()
{
    echo "Downloading Chr22 VCF from 1000 genomes project"
    if [ -f "${CACHE_DIR}/${ORIG_VCF}" ]; then 
        echo "Using Chr22 VCF file from cache."
        return 0 
    fi

    curl -v "http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/${ORIG_VCF}" -o "${CACHE_DIR}/${ORIG_VCF}"
}

filter_vcf()
{
    echo "Generating a downsized filtered version of Chr22 VCF file. This may take a few minutes."
    if [ -f "${CACHE_DIR}/${FILTERED_VCF}" ]; then 
        echo "Using filtered VCF file from cache."
        return 0; 
    fi

    bcftools view -i "AF>${AF_THRESHOLD}" "${CACHE_DIR}/${ORIG_VCF}" > "${CACHE_DIR}/${FILTERED_VCF}"
}

create_dirs()
{
    if [ ! -d $CACHE_DIR ]; then 
        mkdir $CACHE_DIR
    fi
    if [ ! -d $DATA_DIR ]; then
        mkdir $DATA_DIR
    fi
}


check_prerequisites
create_dirs 
download_orig_file
filter_vcf

echo "Generating sample VCF files in ${DATA_DIR}"
FILE="${CACHE_DIR}/${FILTERED_VCF}"
SAMPLE_LIST=$(bcftools query -l $FILE)
SAMPLE_NB=$(echo "${SAMPLE_LIST}" | wc -l | awk '{$1=$1};1')
COUNT=0

for sample in $SAMPLE_LIST; do
    ((COUNT+=1))
    printf "Generating VCF file ${COUNT} / ${SAMPLE_NB} \\r"

    SAMPLE_FILE="${DATA_DIR}/${sample}.vcf.gz"
    if compgen -G "${DATA_DIR}/${sample}-*.vcf.gz" > /dev/null; then
        echo "VCF for ${sample} already exists."
        continue
    fi
    bcftools view -c1 -Oz -s $sample -o $SAMPLE_FILE $FILE

    # # Rename file using hash from check sum
    # SHA=$(shasum $SAMPLE_FILE | head -c 40)
    # mv "${SAMPLE_FILE}" "${DATA_DIR}/${sample}-${SHA}.vcf.gz"
done
echo "${SAMPLE_NB} sample VCF files generated."
