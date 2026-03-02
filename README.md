<<<<<<< HEAD
# Seminars 3 & 4 — Hedonometer (Project Folder)

This folder provides an **example project structure** (and an instructor/demo script) for the Seminars 3 & 4 group project using the **labMT 1.0** dataset (Data Set S1 from the Hedonometer paper).

It includes:
- the labMT 1.0 dataset file (`data/raw/Data_Set_S1.txt`)
- a runnable demo analysis script (`src/hedonometer_labmt_demo.py`) that produces a *typical* set of outputs aligned to the assignment
- course documents in `docs/` (original paper + paper companion + assignment + project quickstart), provided as **.pdf**

## Folder layout (course convention)

- `src/` — Python scripts you run
- `data/raw/` — input data (treat as read-only)
- `figures/` — PNG plots (embed these in your GitHub README)
- `tables/` — CSV tables/summaries (optional to embed, but useful for analysis)
- `docs/` — assignment + paper companion + quickstart handout

## Setup + run (from the project root)

### 1) Create a virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
```

**Windows (PowerShell)**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
```

### 2) Install dependencies
```bash
python3 -m pip install -r requirements.txt
```

### 3) Run the demo analysis
```bash
python3 src/run_analysis.py
```

### What gets generated?
After running, look in:
- `figures/` — PNG plots
- `tables/` — CSV summary tables
=======
# Hedonometer Project – Group 14

## 1. Overview

This project explores the labMT 1.0 dataset (“Language Assessment by Mechanical Turk”), 
which was used to construct a large-scale “hedonometer” for measuring happiness in text. 
We analyze the statistical properties of the dataset, examine patterns of disagreement, 
compare corpus rankings, and reflect critically on how the dataset was generated and what it can (and cannot) measure.

---

## 2. Dataset

### Source



### Data Dictionary

- *(add or adjust column names based on your actual dataset)*

---

## 3. Methods

We used Python (pandas and matplotlib) to:


All code is available in the `src/` folder.

---

## 4. Results

### 4.1 Distribution of Happiness Scores

*(Insert histogram here later)*

![Histogram of Happiness Scores](figures/histogram.png)

**Interpretation:**  
(Write explanation here.)

---

### 4.2 Disagreement and Contested Words

*(Insert scatterplot here later)*

![Happiness vs Standard Deviation](figures/scatter.png)

**Interpretation:**  
(Write explanation here.)

---

### 4.3 Corpus Comparison

*(Insert bar chart or overlap table here later)*

**Interpretation:**  
(Write explanation here.)

---

## 5. Qualitative Exhibit of Words

We selected 20 words across four categories:

- 5 highly positive
- 5 highly negative
- 5 highly contested
- 5 culturally loaded or surprising

(Insert table here later.)

**Interpretive Discussion:**  
(Write analysis here.)

---

## 6. Critical Reflection

### 6.1 Data Generation Pipeline

(Describe the steps used to construct the dataset.)

### 6.2 Consequences and Limitations

(Discuss at least five design choices and their implications.)

### 6.3 Instrument Note

(200–400 word reflection.)

---

## 7. How to Run This Project

1. Clone the repository:

2. Install required packages:

3. Run the main scripts:


---

## 8. Credits

- Person 1 – Workflow lead & data cleaning
- Person 2 – Quantitative analysis ()
- Person 3 – Quantitative analysis ()
- Person 4 – Qualitative exhibit
- Person 5 – Critical reflection

### Citation
>>>>>>> 7444a025159fb95e427af3786e5af780b34c48a1
