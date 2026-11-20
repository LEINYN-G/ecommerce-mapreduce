# Large-Scale E-Commerce Sales and Customer Behaviour Analysis Using Hadoop MapReduce

A Python-based Hadoop MapReduce project that analyses 100,000 e-commerce transactions to generate customer-level sales metrics and classify customers using purchase behaviour.

The project implements and compares two execution modes:

1. MapReduce without a Combiner
2. MapReduce with a Combiner

Both modes produce identical final customer-level results, while the Combiner reduces the number of intermediate records processed by the Reducer.

---

## 1. Project Objectives

- Calculate customer-wise transaction statistics.
- Calculate total purchase amount and successful purchase amount.
- Count successful, failed, and high-value transactions.
- Classify customers using business rules.
- Implement a safe, reusable Combiner.
- Execute jobs using Hadoop Streaming and Python.
- Compare execution results with and without a Combiner.
- Validate output correctness using independent comparisons.

## 2. Dataset

**Dataset:** `ecommerce_transactions_100k_synthetic.csv`

- Transactions: 100,000
- Unique customers: 11,997
- File size: approximately 5.9 MB
- Successful transactions: 88,197
- Failed transactions: 11,803
- High-value transactions: 20,068

**Dataset disclosure:** The dataset used in this project is synthetically generated for experimentation and validation. It is not represented as an official faculty-provided dataset or real customer data.

The dataset generator and inspection scripts are available in the `scripts/` directory.

## 3. Customer-Level Analysis

For every customer, the Mapper generates six additive metrics:

| Metric | Description |
|---|---|
| Total Transactions | Total transaction count |
| Total Amount | Total purchase amount, including all statuses |
| Successful Count | Number of successful transactions |
| Failed Count | Number of failed transactions |
| High-Value Count | Transactions with amount >= ₹50,000 |
| Successful Amount | Total amount from successful transactions only |

### Customer Classification Rules

| Condition | Classification |
|---|---|
| Successful spend >= ₹1,00,000 AND successful count >= 4 | PREMIUM_FREQUENT |
| Successful spend >= ₹1,00,000 only | PREMIUM |
| Successful count >= 4 only | FREQUENT |
| Neither condition | NORMAL |

## 4. MapReduce Architecture

```text
             Input CSV Dataset
                     |
                     v
                   Mapper
                     |
           Customer-wise key/value
                     |
          +----------+----------+
          |                     |
          v                     v
     No Combiner             Combiner
          |                     |
          |              Local Aggregation
          |                     |
          +----------+----------+
                     |
                     v
                   Reducer
                     |
          Customer Classification
                     |
                     v
             Final Customer Output
Components
- src/mapper.py — Reads and validates transaction records, then emits customer-level metrics.
- src/combiner.py — Performs safe local aggregation of additive metrics.
- src/reducer.py — Aggregates metrics and applies customer classification rules.
The Combiner is safe for repeated aggregation because all six metrics are additive and can be combined using associative and commutative addition.
## 5. Technology Stack
- Apache Hadoop 3.3.6
- Hadoop Streaming
- Python 3
- HDFS
- Linux / Ubuntu on WSL
- Git and GitHub
## 6. Project Structure
ecommerce-mapreduce/
├── data/
│   └── raw/
│       └── ecommerce_transactions_100k_synthetic.csv
├── results/
│   ├── college/
│   │   ├── combiner_comparison.txt
│   │   ├── final_validation.txt
│   │   ├── hdfs_evidence.txt
│   │   ├── hdfs_evidence_clean.txt
│   │   └── test_verification.txt
│   └── local/
│       ├── combiner_counters.txt
│       ├── mapper_output.tsv
│       ├── with_combiner/
│       └── without_combiner/
├── scripts/
│   ├── generate_ecommerce_dataset.py
│   └── inspect_dataset.py
├── src/
│   ├── mapper.py
│   ├── combiner.py
│   └── reducer.py
├── .gitignore
└── README.md
## 7. Execution Using Hadoop Streaming
Ensure Hadoop services are running and HDFS is accessible.

Set the Hadoop Streaming JAR path:
export HADOOP_HOME=/path/to/hadoop
STREAMING_JAR="$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar"
Upload the dataset to HDFS:
hdfs dfs -mkdir -p /ecommerce/input

hdfs dfs -put -f \
data/raw/ecommerce_transactions_100k_synthetic.csv \
/ecommerce/input/
A. Run Without Combiner
hadoop jar "$STREAMING_JAR" \
-D mapreduce.job.reduces=1 \
-files src/mapper.py,src/reducer.py \
-input /ecommerce/input/ecommerce_transactions_100k_synthetic.csv \
-output /ecommerce/output_without_combiner \
-mapper "python3 mapper.py" \
-reducer "python3 reducer.py"
B. Run With Combiner
hadoop jar "$STREAMING_JAR" \
-D mapreduce.job.reduces=1 \
-files src/mapper.py,src/combiner.py,src/reducer.py \
-input /ecommerce/input/ecommerce_transactions_100k_synthetic.csv \
-output /ecommerce/output_with_combiner \
-mapper "python3 mapper.py" \
-combiner "python3 combiner.py" \
-reducer "python3 reducer.py"
Note: Hadoop output directories must not already exist when a job is submitted. Remove only the relevant previous experiment output directory before rerunning that experiment.

Retrieve results:
hdfs dfs -get \
/ecommerce/output_with_combiner/part-00000 \
results/local/with_combiner/hadoop_output.tsv
For the no-Combiner run, use /ecommerce/output_without_combiner/part-00000 and results/local/without_combiner/hadoop_output.tsv.
## 8. Experimental Results
Both Hadoop Streaming jobs completed successfully on the 100,000-transaction dataset.
Measurement	Without Combiner	With Combiner
Mapper input records	100,000	100,000
Combiner input records	Not applicable	100,000
Combiner output records	Not applicable	23,624
Reducer input records	100,000	23,624
Final customer records	11,997	11,997

Intermediate Record Reduction
\[
\text{Reduction} =
\frac{100000-23624}{100000}\times100
=76.376\%
\]

The Combiner reduced the intermediate record count processed by the Reducer by 76.376%.

This is a reduction in intermediate record count, not a direct measurement of network bytes saved or execution-time improvement.
## 9. Final Customer Classification
Both execution modes produced identical final output.
Customer Category	Number of Customers
NORMAL	536
FREQUENT	1,830
PREMIUM_FREQUENT	9,353
PREMIUM	278
Total	11,997

## 10. Validation and Correctness
The following checks were performed:
- Dataset quality inspection.
- Python syntax compilation.
- Mapper and Combiner testing.
- Repeated Combiner aggregation testing.
- All four customer classification cases tested.
- Both Hadoop Streaming jobs completed successfully.
- Final Hadoop outputs compared between both execution modes.
- Both outputs contained 11,997 customer records.
- Final output files were identical.
Supporting evidence is stored in results/college/.
## 11. Important Observations
1. The Combiner reduces intermediate data volume by aggregating repeated customer keys before Reducer processing.
2. The Combiner does not replace the Reducer; it performs optional local aggregation.
3. Hadoop may invoke the Combiner multiple times or not at all, so the aggregation logic must remain safe under repeated execution.
4. Final results must remain identical regardless of whether a Combiner is used.
5. Intermediate record reduction should not be confused with measured network-byte or runtime reduction.
## 12. Repository Contents
This repository includes:
- Python Mapper, Combiner, and Reducer implementations.
- Synthetic transaction dataset.
- Dataset generation and inspection scripts.
- Local experimental outputs.
- Hadoop execution evidence.
- Customer validation results.
- Combiner comparison evidence.

Project: Large-Scale E-Commerce Sales and Customer Behaviour Analysis Using Hadoop MapReduce

Focus: Distributed data processing, customer analytics, safe aggregation, Hadoop Streaming, and experimental validation.
