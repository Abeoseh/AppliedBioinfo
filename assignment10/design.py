
#!/usr/bin/env python3

import csv
import re
import sys
from collections import OrderedDict


def read_design(filename):
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)

        required = {"Run", "TranscriptionFactor", "treatment"}

        if not required.issubset(reader.fieldnames or []):
            raise ValueError(
                f"Design file must contain columns: {required}"
            )

        rows = list(reader)

    return rows


def get_runs(rows):
    runs = []

    for row in rows:
        run = row["Run"].strip()

        if run and run not in runs:
            runs.append(run)

    return runs


def get_pairs(rows):
    groups = OrderedDict()

    for row in rows:
        tf = row["TranscriptionFactor"].strip()
        treatment = row["treatment"].strip()
        run = row["Run"].strip()

        match = re.fullmatch(
            r"(case|control)(\d+)",
            treatment.removeprefix(tf + "_")
        )

        if not match:
            raise ValueError(
                f"Invalid treatment format: {treatment}"
            )

        condition, replicate = match.groups()

        key = (tf, replicate)

        if key not in groups:
            groups[key] = {}

        if condition in groups[key]:
            raise ValueError(
                f"Duplicate {condition} for {tf} replicate {replicate}"
            )

        groups[key][condition] = run

    pairs = []

    for (tf, replicate), samples in groups.items():
        if "case" not in samples or "control" not in samples:
            raise ValueError(
                f"Unmatched samples: {tf} replicate {replicate}"
            )

        pairs.append(
            (tf, samples["case"], samples["control"])
        )

    return pairs


if __name__ == "__main__":
    mode = sys.argv[1]
    design = sys.argv[2]

    rows = read_design(design)

    if mode == "runs":
        print(" ".join(get_runs(rows)))

    elif mode == "pairs":
        for tf, case, control in get_pairs(rows):
            print(f"{case}:{control}")

    elif mode == "tf-pairs":
        for tf, case, control in get_pairs(rows):
            print(f"{tf}:{case}:{control}")

    else:
        raise ValueError(f"Unknown mode: {mode}")
