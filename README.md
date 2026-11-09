# Detecting Covert Collusion Between AI Agents Through Behavioural Anomaly Analysis

**Research prototype | Multi-agent security · Behavioural anomaly detection · AI assurance**

## Overview

This exploratory project investigates whether behavioural anomaly detection can flag suspicious interaction patterns in simulated multi-agent environments. It also evaluates the same general anomaly-detection approach on a separate, publicly published CERT-derived organisational activity dataset.

**Important distinction:** An anomaly is not proof of collusion or malicious intent. Experiments 1–3 use hand-generated synthetic collusion labels. Experiment 4 concerns synthetic *human* organisational activity and has no verified malicious labels in the feature matrix used here.

## Research questions

1. Can Isolation Forest identify anomalous behavioural patterns associated with simulated collusive interactions?
2. How does detection change when simulated legitimate and collusive feature distributions overlap?
3. What can an external behavioural dataset reveal about persistent anomalies and the limitations of global anomaly detection?

## Methods and experimental design

The prototype uses Python, pandas and scikit-learn's Isolation Forest. Its simulated features include communication counts, action delays and objective-deviation scores. The CERT-derived analysis instead uses login, after-hours, HTTP, email, file and USB activity counts.

| Experiment | Data and evaluation | Observed result |
| --- | --- | --- |
| 1 — Initial baseline | 200 synthetic individual observations; model fitted and evaluated on the same data | Accuracy **89.5%**; precision **80.0%**; recall **48.5%**; F1 **60.4%**; confusion matrix `[[163, 4], [17, 16]]` |
| 2 — Legitimate-only training | Model fitted on a subset of legitimate synthetic observations; evaluated on held-out legitimate observations and collusion-labelled observations | Accuracy **95.2%**; precision **89.2%**; recall **100%**; F1 **94.3%**; confusion matrix `[[47, 4], [0, 33]]` |
| 3 — Overlapping interaction patterns | 500 synthetic directed interaction records; first 300 chronological records used for training; last 200 for testing | Accuracy **86.5%**; precision **70.2%**; recall **71.7%**; F1 **71.0%**; confusion matrix `[[140, 14], [13, 33]]` |
| 4 — External behavioural dataset | 330,452 CERT r4.2-derived user-day observations; 231,671 earlier records for training and 98,781 later records for testing | **4,731** test observations flagged (**4.79%**). No labelled attack-detection metrics calculated. |

Precision, recall and F1 in Experiments 1–3 treat the synthetic `collusion_label` as ground truth and refer to the simulated collusion class. The experiments have different populations and evaluation procedures; their metrics should **not** be interpreted as a controlled, causal comparison.

### Experiment 3: More challenging simulated interactions

Experiment 3 models directed sender–receiver records among three agents. Collusion labels are assigned by a predefined agent-pair/time rule, while legitimate intensive activity overlaps with collusion-like feature values. On the 200-record test set, the model flagged 33 of 46 collusion-labelled records and missed 13; it also flagged 14 of 154 legitimate records. This is a simulation of behavioural signatures, **not** evidence of autonomous agents forming covert agreements.

### Experiment 4: External behavioural anomaly detection

A published feature matrix derived from the **CERT r4.2 Insider Threat Dataset** contains 330,452 user-day records representing 1,000 simulated organisational users. The analysis selected six observable activity counts: `total_logon_activity`, `after_hours_activity`, `http_activity_count`, `total_emails`, `file_activity_count`, and `usb_activity_count`.

Records were sorted by date and user. A date-based cutoff near the 70th percentile separated 231,671 training observations from 98,781 later test observations. StandardScaler was fitted on training records only, followed by Isolation Forest (`n_estimators=100`, `contamination=0.05`, `random_state=42`). The model flagged 4,731 test observations (4.79%). This is an **anomaly rate**, not an accuracy or malicious-detection rate.

A descriptive review found that **all 120 test-period records** for pseudonymous user `AJF0370` were flagged. Across those records, average daily file, USB and after-hours activity counts were **30.45**, **22.97**, and **4.64**, respectively. This illustrates persistent deviation from the organisation-wide baseline; it does **not** establish that the user was malicious. A global model may repeatedly flag a user with unusual but legitimate job responsibilities.

**Data provenance:** CERT is a synthetic organisational insider-threat research dataset, not a dataset of AI agents. The externally published derived feature matrix must be attributed to its original publisher. See the dataset landing page: https://zenodo.org/records/19435851 and the original CERT dataset information: https://sei.cmu.edu/library/insider-threat-test-dataset/ . Consult the dataset pages for licensing and attribution terms before redistribution. The raw/derived third-party dataset is **not included** in this repository.

## Reproduce the experiments

### Prerequisites

- Python 3.10+ (the prototype was developed using Python 3.14)
- Dependencies in `requirements.txt`

On Windows PowerShell, from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell prevents activation, run `.\.venv\Scripts\python.exe` in place of `python` for the commands below.

### Simulated experiments

```powershell
python simulation.py
python explore_data.py
python anomaly_detection.py
python evaluation_v2.py
python simulation_v3.py
python evaluation_v3.py
```

Run the scripts from the project root. Simulated datasets and model outputs are written under `data/` and `results/` as implemented by each script.

### CERT-derived external experiment

Download `feature_matrix_v1.parquet` from https://zenodo.org/records/19435851 and save it at:

```text
data/cert/feature_matrix_v1.parquet
```

Then run:

```powershell
python inspect_cert.py
python explore_cert.py
python cert_anomaly_detection.py
python cert_results_analysis.py
python investigate_cert_user.py
```

The anomaly-detection script writes `results/cert_anomaly_results.csv`. The user investigation script currently examines the pseudonymous user `AJF0370` in the test period.

## Limitations and responsible interpretation

- **No real AI-agent collusion ground truth:** Simulated collusion labels are generated from rules rather than independent autonomous-agent decisions.
- **Simplified features:** Communication frequency, delays and objective-deviation values are simulated proxies; they do not establish intent or covert coordination.
- **Evaluation differences:** Experiment 1 evaluates on training data; Experiments 2 and 3 use different held-out designs. Their performance metrics are not directly comparable.
- **External dataset is a different domain:** CERT-derived user-day activity concerns synthetic human organisational behaviour, not agent-to-agent communication.
- **No verified labels in Experiment 4's feature matrix:** Its 4.79% flag rate cannot establish malicious-detection precision, recall, accuracy or false-positive rate.
- **Possible feature-construction leakage:** The external matrix's preprocessing and any user-relative statistics require provenance checks. A chronological model split alone cannot undo leakage embedded in source features.
- **Global-baseline bias:** Persistent flags for an individual may reflect a different legitimate work pattern rather than wrongdoing.
- **No independent replication yet:** Broader datasets, multiple random seeds, baselines, ablation studies and uncertainty estimates are future work.

## Future work

Investigate user-specific and peer-group baselines; test graph and temporal interaction features; simulate explicit agent objectives and covert coordination strategies; compare against simple baselines; and evaluate with independent ground-truth labels where available. Assess alert explainability and human-review workflows before making operational claims.

## Research and ethical use

This repository is an exploratory research demonstration, **not** a production insider-threat or AI-agent surveillance system. Anomaly scores should support investigation with appropriate safeguards and human oversight, not automated accusations or adverse decisions.

## Author

Research prototype by **Aderonke Thompson**. GitHub: https://github.com/aderonkethompsonphd

## Citation and licence

Please attribute the original CERT dataset and the published derived feature matrix according to their respective terms. A licence for this repository has not yet been selected; do not assume that third-party dataset redistribution is permitted.
