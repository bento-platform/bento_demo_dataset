import pandas as pd
import numpy as np
import scipy.stats as stats
import string
from datetime import datetime, timedelta
import random
import gzip
import subprocess
import os
import json
import warnings


class TranscriptomicMatrixGenerator:
    def __init__(self):
        self.differentially_expressed_genes_info = []
        self.num_samples = 0
        self.sample_ids = []
        self.sample_names = []
        self.treatments = []
        self.gene_names = []

    def set_samples(self, biosample_ids, num_samples):
        min_samples = 4
        max_samples = min(9, len(biosample_ids))
        self.num_samples = random.randint(min_samples, max_samples)
        self.num_samples = num_samples if num_samples is not None else self.num_samples
        selected_samples = random.sample(biosample_ids, self.num_samples)

        num_control = random.randint(1, self.num_samples - 1)
        num_treatment = self.num_samples - num_control
        self.sample_ids = selected_samples
        self.sample_names = ["Sample_" + str(i) for i in selected_samples]
        self.treatments = ["Control"] * num_control + ["Treatment"] * num_treatment
        random.shuffle(self.treatments)

    def load_sample_info(self, json_file_path):
        with open(json_file_path, "r") as file:
            sample_info = json.load(file)
            self.num_samples = len(sample_info)
            self.sample_ids = [item["SampleID"] for item in sample_info]
            self.sample_names = [item["SampleName"] for item in sample_info]
            self.treatments = [item["Treatment"] for item in sample_info]
            self.experiment_id = [item["ExperimentID"] for item in sample_info]

    def download_and_process_gff(self, url, file_path):
        if not os.path.exists(file_path):
            subprocess.run(["wget", "-O", file_path, url], check=True)
        self.extract_gff_genes_info(file_path)

    def extract_gff_genes_info(self, file_path):
        with gzip.open(file_path, "rt") as file:
            gff_data = pd.read_csv(
                file,
                sep="\t",
                comment="#",
                header=None,
                names=[
                    "seqname",
                    "source",
                    "feature",
                    "start",
                    "end",
                    "score",
                    "strand",
                    "frame",
                    "attribute",
                ],
                dtype=str,
            )
        genes = gff_data[gff_data["feature"] == "gene"].copy()
        genes.loc[:, "GeneID"] = genes["attribute"].str.extract(
            "Name=([^;]+)", expand=False
        )
        genes.loc[:, "GeneLength"] = (
            genes["end"].astype(int) - genes["start"].astype(int) + 1
        )
        gene_info = (
            genes[["GeneID", "GeneLength"]].dropna().drop_duplicates(subset="GeneID")
        )
        output_file_csv = "gene_lengths.csv"
        gene_info.to_csv(output_file_csv, index=False)
        print(f"Gene lengths have been saved to {output_file_csv}.")

        self.gene_names = gene_info["GeneID"].tolist()

    def split_into_groups(self, biosamples, num_groups, max_size=None):
        if len(biosamples) < num_groups:
            return [[] for _ in range(num_groups)]

        random.shuffle(biosamples)
        groups = [[] for _ in range(num_groups)]
        if max_size is not None:
            for biosample in biosamples:
                for group in groups:
                    if len(group) < max_size:
                        group.append(biosample)
                        break
        else:
            start_index = 0
            group_size = len(biosamples) // num_groups
            remainder = len(biosamples) % num_groups

            for i in range(num_groups):
                if start_index >= len(biosamples):
                    break
                end_index = start_index + group_size + (1 if i < remainder else 0)
                groups[i] = biosamples[start_index:end_index]
                start_index = end_index

        return groups

    def generate_counts_matrix(
        self,
        differential_expr_percentage=10,
        differential_factor=2.5,
        dispersion=0.2,
        outlier_percentage=5,
        outlier_factor=10,
    ):
        if not self.gene_names:
            raise ValueError("No gene names available for count matrix generation.")

        unique_gene_names = list(filter(None, set(self.gene_names)))
        if not unique_gene_names:
            raise ValueError(
                "No valid gene names available after filtering duplicates and empty entries."
            )
        self.gene_names = unique_gene_names

        genes_count = len(unique_gene_names)
        expression_levels = np.random.choice(
            [2, 50, 100, 223, 800], size=genes_count, p=[0.1, 0.3, 0.3, 0.2, 0.1]
        )
        matrix = np.zeros((genes_count, self.num_samples), dtype=np.int32)
        for i in range(genes_count):
            mean_expression = expression_levels[i]
            size = (
                (mean_expression**2)
                / (mean_expression * dispersion - mean_expression**2)
                if mean_expression * dispersion > mean_expression
                else 10
            )
            matrix[i, :] = np.random.negative_binomial(
                n=size, p=size / (size + mean_expression), size=self.num_samples
            ).astype(int)
        self.apply_modifications(
            matrix,
            differential_expr_percentage,
            differential_factor,
            outlier_percentage,
            outlier_factor,
        )
        df = pd.DataFrame(matrix, columns=self.sample_ids, index=unique_gene_names)
        df.index.name = "GeneID"
        return df

    def apply_modifications(
        self,
        matrix,
        differential_expr_percentage,
        differential_factor,
        outlier_percentage,
        outlier_factor,
        p_value_threshold=0.05,
    ):
        genes_count = len(self.gene_names)
        num_differential_genes = int(genes_count * (differential_expr_percentage / 100))
        differential_indices = np.random.choice(
            genes_count, num_differential_genes, replace=False
        )

        for idx in differential_indices:
            matrix[idx, :] = (matrix[idx, :] * differential_factor).astype(int)

            # Splitting samples based on treatment labels
            control_samples = matrix[
                idx, [i for i, x in enumerate(self.treatments) if x == "Control"]
            ]
            treatment_samples = matrix[
                idx, [i for i, x in enumerate(self.treatments) if x == "Treatment"]
            ]

            if len(control_samples) > 0 and len(treatment_samples) > 0:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    t_stat, p_value = stats.ttest_ind(
                        treatment_samples, control_samples, equal_var=False
                    )
                    if p_value < p_value_threshold:
                        self.differentially_expressed_genes_info.append(
                            {
                                "Gene": self.gene_names[idx],
                                "Control Mean": np.mean(control_samples),
                                "Treatment Mean": np.mean(treatment_samples),
                                "Fold Change": differential_factor,
                                "T-statistic": t_stat,
                                "P-value": p_value,
                            }
                        )

        # Apply outlier modifications
        num_outlier_genes = int(genes_count * (outlier_percentage / 100))
        outlier_indices = np.random.choice(
            genes_count, num_outlier_genes, replace=False
        )
        for idx in outlier_indices:
            matrix[idx, :] = (matrix[idx, :] * outlier_factor).astype(int)

    def write_differentially_expressed_genes_to_csv(self, filename):
        df = pd.DataFrame(self.differentially_expressed_genes_info)
        df.to_csv(filename, index=False)

    def generate_experiment_info_matrix(self):
        return pd.DataFrame(
            {
                "SampleID": self.sample_ids,
                "SampleName": self.sample_names,
                "Treatment": self.treatments,
            }
        )

    def generate_metadata_matrix(self):
        fictional_info = [
            self.generate_fictional_info() for _ in range(self.num_samples)
        ]
        return pd.DataFrame(
            {
                "ExperimentID": self.experiment_id,
                "SampleID": self.sample_ids,
                "FictionalInfo": fictional_info,
            }
        )

    def generate_fictional_info(self):
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2023, 1, 1)
        time_between_dates = end_date - start_date
        random_number_of_days = random.randrange(time_between_dates.days)
        random_date = start_date + timedelta(days=random_number_of_days)
        random_text = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=5)
        )
        return f"{random_date.date()}_{random_text}"

    def write_to_csv(self, dataframe, filename):
        dataframe.to_csv(filename)
