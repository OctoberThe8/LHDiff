# Evaluation Metrics and Experimental Setup

## 1. Evaluation Overview

The performance of **LHDiff** was evaluated by comparing the final predicted line mappings against **ground-truth (GT) mappings** for each file pair.
Each predicted mapping was classified as:

* **Correct**: the predicted mapping exactly matches the ground truth
* **Incorrect**: the predicted mapping points to the wrong target line
* **Missed**: a ground-truth mapping was not produced by the system
* **Spurious**: a mapping was predicted where no ground-truth mapping exists

Using these outcomes, we compute **precision**, **recall**, and **F1-score** to quantify accuracy.

Evaluation was conducted on:

1. **Real-world file pairs** with manually curated ground truth
2. A **mutation-based dataset** designed to test specific edit patterns under controlled conditions



## 2. Ground Truth and Preprocessing

### 2.1 Real-World Ground Truth

* Ground truth mappings are provided as XML files.
* Each XML file defines mappings from **old file line numbers** to **new file line numbers**.
* Ground truth files are **normalized** using the same preprocessing pipeline as the input source files to ensure consistency.

Evaluation is performed **only on lines explicitly defined in the ground truth**, preventing penalization for unmapped or ambiguous lines.



### 2.2 Mutation-Based Ground Truth

To evaluate LHDiff under controlled transformations, we use a **mutation-based dataset** consisting of:

* One original source file
* Multiple mutated versions, each applying a **single edit type**

Supported mutation types include:

* `insert`
* `delete`
* `modify`
* `rename`
* `split`
* `merge`
* `move`
* `whitespace`

Ground truth for the mutation dataset specifies how original line numbers should map to mutated line numbers after each transformation.



## 3. Evaluation Metrics

We report the following standard information retrieval metrics:

* **Precision**
  Proportion of predicted mappings that are correct.

* **Recall**
  Proportion of ground-truth mappings that were successfully recovered.

* **F1-Score**
  Harmonic mean of precision and recall.

All metrics are computed using a custom `evaluate()` function applied consistently across datasets.



## 4. Datasets Evaluated

LHDiff was evaluated on approximately **25 real file pairs** spanning multiple programming languages:

* **Java** (e.g., `GamePanel`, `Date`, `Server`)
* **Python** (e.g., `random_data_library`, `guessGame`)
* **C** (e.g., `game`, `proc`)
* **JavaScript** (e.g., `js-array`, `localStorage`)
* **PHP** (e.g., `cart`, `login`)

The datasets vary significantly in:

* file size (small scripts to large source files),
* degree of change (minor edits to major restructuring),
* coding style and language syntax.



## 5. Quantitative Results on Real-World Files

Representative evaluation results are shown below.

| Dataset             | Language   | Precision | Recall | F1   |
| ------------------- | ---------- | --------- | ------ | ---- |
| GamePanel           | Java       | 1.00      | 0.40   | 0.57 |
| Date                | Java       | 1.00      | 0.67   | 0.80 |
| Server              | Java       | 0.67      | 0.50   | 0.57 |
| Array_Data          | Java       | 1.00      | 0.40   | 0.57 |
| game                | C          | 0.86      | 0.63   | 0.73 |
| random_data_library | Python     | 1.00      | 0.77   | 0.87 |
| js-array            | JavaScript | 1.00      | 1.00   | 1.00 |
| urldecoder          | Java       | 1.00      | 1.00   | 1.00 |



## 6. Mutation-Based Evaluation Results

Mutation-based testing evaluates LHDiff’s robustness under controlled edit patterns.

### 6.1 Observed Behavior

* **Insert / Delete**
  LHDiff maintains high precision, correctly aligning unchanged lines while shifting indices appropriately.

* **Modify / Rename**
  Performance remains strong when textual similarity is preserved.

* **Split / Merge**
  These transformations are more challenging.
  Split detection improves correctness in some cases, but recall decreases under aggressive restructuring.

* **Move**
  Line relocation is partially handled through similarity and context, though recall varies depending on surrounding changes.

* **Whitespace**
  Whitespace-only changes are largely ignored due to normalization, which is a deliberate design choice.

### 6.2 Interpretation

Mutation testing demonstrates that LHDiff behaves **consistently and predictably** across different edit types, with performance degrading gracefully as transformations become more complex.



## 7. Precision–Recall Tradeoff

Across both real-world and mutation-based datasets, **precision is consistently higher than recall**.

This reflects a **conservative design philosophy**:

* LHDiff prioritizes correctness of reported mappings
* Ambiguous matches are avoided rather than guessed

As a result:

* False positives are rare
* Some true mappings may be missed under heavy restructuring

This tradeoff is appropriate for applications where **incorrect mappings are more harmful than missing mappings**.



## 8. Qualitative Evaluation (GUI)

For datasets without ground truth, qualitative evaluation was performed using the LHDiff GUI.

The GUI provides:

* side-by-side visualization of old and new files,
* highlighted line mappings,
* interactive inspection of detected matches.

Manual inspection confirms that many unchanged or lightly modified lines are correctly tracked even when quantitative evaluation is unavailable.



## 9. Limitations

While LHDiff performs well overall, several limitations remain:

* Recall decreases under extreme restructuring
* Similarity is primarily textual rather than semantic
* Split and merge cases remain challenging in complex edits

These limitations motivate future improvements.



## 10. Summary

Overall, LHDiff demonstrates:

* high precision across diverse datasets,
* robust performance on moderately changing code,
* effective handling of multiple programming languages,
* reliable behavior under controlled mutation testing.

These results validate LHDiff as a practical and extensible line-tracking system for code evolution analysis.



## 11. Future Work

Potential directions include:

* semantic similarity using embeddings or ASTs,
* improved handling of large-scale refactoring,
* expanded mutation datasets,
* finer-grained split and merge detection.

