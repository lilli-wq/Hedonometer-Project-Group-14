
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

- **word** (text) — The English word being evaluated in the labMT dataset.  
  *Missingness:* No missing values.

- **happiness_rank** (integer) — Rank order of the word based on its average happiness score (1 = highest happiness).  
  *Missingness:* No missing values.

- **happiness_average** (float) — Mean happiness rating assigned by Mechanical Turk annotators on a 1–9 scale.  
  *Missingness:* No missing values.

- **happiness_standard_deviation** (float) — Standard deviation of happiness ratings across annotators, indicating the level of agreement or disagreement.  
  *Missingness:* No missing values.

- **twitter_rank** (float) — Frequency rank of the word in the Twitter corpus (restricted to the top 5000 most frequent words).  
  *Missingness:* 5,222 values are missing. A `NaN` value indicates the word does not appear in Twitter’s top-5000 list.

- **google_rank** (float) — Frequency rank in the Google Books corpus (top 5000 words).  
  *Missingness:* 5,222 values are missing. A `NaN` value indicates the word does not appear in Google Books’ top-5000 list.

- **nyt_rank** (float) — Frequency rank in the New York Times corpus (top 5000 words).  
  *Missingness:* 5,222 values are missing. A `NaN` value indicates the word does not appear in the NYT top-5000 list.

- **lyrics_rank** (float) — Frequency rank in the song lyrics corpus (top 5000 words).  
  *Missingness:* 5,222 values are missing. A `NaN` value indicates the word does not appear in the lyrics top-5000 list.

### Sanity Checks
**1. Checking for duplicate words:**  
Each row is supposed to represent a distinct word, so duplicates would indicate
a problem in the source file or in the read‑in options. We found no repetitions.

**2. Inspecting a random sample:**  
Picking 15 random rows lets you quickly spot formatting errors, data-type problems, missing values, and encoding issues without inspecting the entire dataset.

**3. Extreme value check: Ten most positive / ten most negative words:**  
Sorting by happiness score and examining the top and bottom 10 words verifies that numeric values are in the expected range and that the scores make intuitive sense (positive words score high, negative words score low). The data makes sense - most positive words such as laughter, happiness and love and most negative words such as died, kill or killed align with the expected data.

---

## 3. Methods

-Loading and Cleaning:

We loaded the labMT 1.0 dataset into a pandas DataFrame using pd.read_csv with tab (\t) as the delimiter. Because the file begins with metadata lines, we skipped the first three lines (skiprows=3). We also treated "--" as missing values (NaN) and converted numeric columns to appropriate numeric types to enable statistical analysis.

The dataset contains 10,222 rows and 8 columns.

A missing rank ("--") indicates that the word does not appear in the top-5000 list of that particular corpus, rather than representing corrupted or unknown data.

We used Python (pandas and matplotlib) to:


All code is available in the `src/` folder.

We conducted three main quantitative analyses:

1. Distribution analysis of happiness scores
2. Identification of contested words based on rating disagreement
3. Comparison of word frequency across four corpora (Twitter, Google Books, NYT, Lyrics)

The code calculates summary statistics, generates visualizations, and outputs tables for further interpretation.

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

