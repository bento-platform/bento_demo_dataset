RANDOM_SEED = 123456

AGE_MEAN = 45
AGE_SD = 25
AGE_MIN = 0
AGE_MAX = 105

# must sum to one
DISEASE_MASS_DISTRIBUTION = [
    0.4,    # probability of having no disease
    0.35,   # probability of having one disease
    0.25,   # probability of having two diseases
    0       # probability of having three diseases
]

# must sum to one
PHENOTYPIC_FEATURE_MASS_DISTRIBUTION = [
    0.1,    # probability of zero phenotypic features
    0.5,    # probability of one phenotypic feature
    0.3,    # probability of two phenotypic features
    0.1     # probability of three phenotypic features
]

# very rarely, make a disease or phenotypic feature have the "excluded" property
P_EXCLUDED = 0.001

# have an extra property that doesn't appear for every user
P_SMOKING_STATUS_PRESENT = 0.9

# extra properties "Lab Result"
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
P_BP_PRESENT = 0.5
BP_MIN = 80
BP_MAX = 180
BP_MEAN = 110
BP_SD = 20


# use default that matches our current 1000 genomes data
DEFAULT_ASSEMBLY = "GRCh38"
