RANDOM_SEED = 1234

# expected assembly for 1000 genomes vcfs
DEFAULT_ASSEMBLY = "GRCh38"

AGE_MEAN = 45
AGE_SD = 25
AGE_MIN = 0
AGE_MAX = 105

# fmt: off
# must sum to one
DISEASE_MASS_DISTRIBUTION = [
    0.4,    # probability of having no disease
    0.35,   # probability of having one disease
    0.24,   # probability of having two diseases
    0.01,   # probability of having three diseases
]
# fmt: on

# all as above: P(0 items), P(1 item), etc and must sum to one
PHENOTYPIC_FEATURE_MASS_DISTRIBUTION = [0.1, 0.5, 0.3, 0.1]
MEDICAL_ACTION_MASS_DISTRIBUTION = [0.5, 0.3, 0.15, 0.05]
INTERPRETATION_MASS_DISTRIBUTION = [0.8, 0.15, 0.05]
EXTRA_BIOSAMPLES_MASS_DISTRIBUTION = [0.4, 0.4, 0.1, 0.1]

# very rarely, make a disease or phenotypic feature have the "excluded" property
P_EXCLUDED = 0.002

# have an extra property that doesn't appear for every user
P_SMOKING_STATUS_PRESENT = 0.9

# extra properties "Lab Result" values
LAB_MIN = 0
LAB_MAX = 1000
LAB_MEAN = 100

# only some individuals have BMI measurements
P_BMI_PRESENT = 0.9
BMI_MIN = 14
BMI_MAX = 100
BMI_MEAN = 21
BMI_SD = 8

# only some individuals have blood pressure measurements
P_BP_PRESENT = 0.4
BP_MIN = 80
BP_MAX = 180
BP_MEAN = 110
BP_SD = 20

# most (but not all) individuals have vital statuses
P_VITAL_STATUS_PRESENT = 0.8
P_VITAL_STATUS_DISTRIBUTION = [0.1, 0.7, 0.2]  # (UNKNOWN_STATUS, ALIVE, DECEASED)
P_VITAL_STATUS_CAUSES_OF_DEATH_DISTRIBUTION = [0.1, 0.1, 0.05, 0.1, 0.1, 0.05, 0.5]

P_ADD_FAKE_CRAM_TO_1K_VCF = 0.5
P_ADD_EXPERIMENT_TO_BIOSAMPLE = 0.4
P_ADD_EXAMPLE_FILE_TO_EXPERIMENT = 0.3
P_ADD_LOCATION_COLLECTED_TO_BIOSAMPLE = 0.7

# generate transcriptomics count matrix
GENERATE_TRANSCRIPTOMICS_MATRIX = False
GENERATE_EXPERIMENT_INFO_MATRIX = False
GENERATE_DIFFERENTIAL_EXPERIMENT_INFO_MATRIX = False
NUMBER_OF_GROUPS = 3
NUMBER_OF_SAMPLES = 9
GFF3_URL = "ftp://ftp.ensembl.org/pub/release-113/gff3/homo_sapiens/Homo_sapiens.GRCh38.113.gff3.gz"
