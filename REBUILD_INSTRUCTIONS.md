# Fraud Detection — Learning-First Rebuild

Use Claude as a tutor, reviewer, and debugging partner—not as a code generator. Your goal is to understand and rebuild this project yourself so you can explain every major decision in an interview.

## Rules for Claude

- Do not write complete notebooks, scripts, models, APIs, dashboards, or READMEs in one response.
- First explain the concept, approach, assumptions, and trade-offs.
- Ask clarifying questions before giving advice.
- Let me attempt the implementation first.
- Review only the code, output, charts, or interpretation I provide.
- Point out bugs, leakage, poor assumptions, and weak reasoning; ask me to fix them.
- Explain why a correction matters, not only what to change.
- If I ask for a full solution, remind me of these rules and ask me to attempt it first.

## Project goal

Rebuild this into a rigorous fraud-classification project with proper validation, imbalance handling, threshold analysis, and production awareness.

**Business question:** How can a financial institution identify potentially fraudulent transactions while balancing missed fraud against unnecessary customer friction?

## Rebuild order

1. Audit and understand the existing repository.
2. Define the fraud problem and evaluation strategy.
3. Audit and document the raw data.
4. Build a reproducible preprocessing and feature pipeline.
5. Build a baseline and logistic-regression model.
6. Add XGBoost only after understanding the simpler models.
7. Evaluate, calibrate, and interpret the models.
8. Review the API, Docker setup, and deployment limitations.
9. Rewrite the README and clean the repository.

## Stage 1: Understand the current project

Create `rebuild-plan.md` before changing analysis code.

Prompt for Claude:

> I am rebuilding my fraud-detection project to learn classification, imbalanced data, model evaluation, and deployment considerations. Please do not write the full solution. First, ask me questions to establish what I understand about the IEEE-CIS dataset, fraud definition, class imbalance, evaluation metrics, data leakage, time-based validation, and business costs. Then help me create a stage-by-stage rebuild plan with deliverables and learning objectives.

Deliverables:

- Inventory of existing notebooks, model files, API code, Docker files, and dashboard components
- List of what you understand versus what you cannot yet explain
- A prioritised rebuild plan
- A learning log template

## Stage 2: Define the problem

Ask Claude:

> Teach me how to define a fraud-detection problem properly. Explain the difference between fraud and non-fraud outcomes, false positives, false negatives, precision, recall, PR-AUC, ROC-AUC, calibration, and threshold selection. Help me choose metrics based on business costs rather than accuracy. I will write the evaluation plan myself; review it afterwards.

Deliverables:

- Fraud definition and target-variable documentation
- Business-cost framework for false positives and false negatives
- Primary and secondary evaluation metrics
- Threshold-selection strategy
- Evaluation plan

## Stage 3: Data audit and leakage

Create `data_audit.md`.

Prompt for Claude:

> Teach me how to identify data leakage in a fraud-detection dataset. Explain why random train/test splits can be misleading for transaction data, and help me design a time-based validation approach. Ask me questions about the dataset schema, transaction timestamps, identifiers, missing values, duplicates, outliers, and features calculated after the prediction time. I will implement the audit and validation split myself; review my plan and code.

Deliverables:

- Data dictionary
- Target and leakage assessment
- Time-based train/validation/test strategy
- Feature documentation
- Reproducible preprocessing pipeline

Key questions to answer:

- Which columns would be available at the moment a transaction is scored?
- Are there identifiers or aggregates that leak future information?
- Why is random splitting inappropriate for time-ordered transactions?
- How should missing values and outliers be handled?
- How extreme is the class imbalance, and why does accuracy mislead?

## Stage 4: Baseline and modelling

Prompt for Claude:

> Teach me how to build a fraud-detection baseline before using XGBoost. Explain logistic regression, class weights, resampling options, probability calibration, precision-recall trade-offs, PR-AUC, ROC-AUC, and threshold selection. Ask me to implement the baseline first, then review it. Do not write the complete model pipeline.

Deliverables:

- Dummy or simple baseline classifier
- Logistic-regression model
- XGBoost model only after the baseline is understood
- Precision-recall curve and PR-AUC
- Confusion matrix at selected thresholds
- Calibration plot
- Feature-importance analysis with caveats
- Error analysis: false positives and false negatives

## Stage 5: API and deployment

Prompt for Claude:

> Teach me what production concerns matter for a fraud-scoring API: input validation, latency, model versioning, monitoring, drift, retraining, logging, and security. Help me assess my existing FastAPI and Docker setup. I will make the changes myself; review them afterwards.

Deliverables:

- API contract documentation
- Input-validation tests
- Latency measurement
- Deployment limitations
- Monitoring and retraining plan
- Clear distinction between prototype and production system

## Stage 6: Communication

Prompt for Claude:

> Review my README and analysis narrative. Help me turn technical results into a concise business recommendation for a fraud team. Ask me questions to test whether I understand my own analysis. Do not rewrite it entirely; give structured feedback first.

Deliverables:

- Professional README
- Executive summary
- Methodology
- Key findings
- Threshold recommendation
- Limitations
- Reproduction instructions

## Completion checklist

Before calling this project complete, answer in writing:

- What business decision does this support?
- What data did I use, and what are its limitations?
- What did I clean, transform, or exclude, and why?
- What baseline did I compare against?
- Why did I choose each model?
- How did I prevent data leakage?
- How did I validate the model?
- Which metric matters most, and why?
- What are the main drivers of the result?
- What would I do differently with more time or better data?
- What recommendation would I give a fraud team?
