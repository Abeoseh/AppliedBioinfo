
#!/usr/bin/env python3

import os
import csv
import xml.etree.ElementTree as ET
from pathlib import Path

genome = Path(os.environ["REF_GENOME"]).resolve()
manifest = Path(os.environ["IGV_MANIFEST"]).resolve()
session = Path(os.environ["IGV_SESSION"]).resolve()

root = ET.Element(
    "Session",
    {
        "genome": str(genome),
        "version": "8"
    }
)

resources = ET.SubElement(root, "Resources")

loaded = set()

with open(manifest) as f:
    reader = csv.DictReader(f, delimiter="\t")

    for row in reader:
        case = row["Case"]
        control = row["Control"]

        peak = Path(row["Peak"]).resolve()
        case_bam = Path(row["Case_BAM"]).resolve()
        control_bam = Path(row["Control_BAM"]).resolve()

        for bam in (case_bam, control_bam):
            if bam not in loaded:
                if not bam.is_file():
                    raise FileNotFoundError(bam)

                ET.SubElement(
                    resources,
                    "Resource",
                    {"path": str(bam)}
                )
                loaded.add(bam)

        if not peak.is_file():
            raise FileNotFoundError(peak)

        if peak not in loaded:
            ET.SubElement(
                resources,
                "Resource",
                {"path": str(peak)}
            )
            loaded.add(peak)

        print(f"Registered: {case} vs {control}")

ET.indent(root, space="    ")

ET.ElementTree(root).write(
    session,
    encoding="UTF-8",
    xml_declaration=True
)

print(f"\nIGV session created: {session}")
print(f"Total tracks: {len(loaded)}")
