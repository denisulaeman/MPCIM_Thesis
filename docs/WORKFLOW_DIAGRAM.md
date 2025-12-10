# Workflow Diagram - Job Level Approach

## 📊 Complete Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA PREPARATION                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Raw Data Sources:                                                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ Employee Master  │  │  Performance     │  │  Job Levels      │     │
│  │ (2000 records)   │  │  Behavioral      │  │  (12 levels)     │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
│           │                      │                      │                │
│           └──────────────────────┴──────────────────────┘                │
│                                  │                                        │
│                                  ▼                                        │
│                    ┌──────────────────────────┐                         │
│                    │  Integrated Dataset      │                         │
│                    │  with Job Level Info     │                         │
│                    └──────────────────────────┘                         │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    STEP 1: JOB LEVEL ANALYSIS                           │
│                    (01_job_level_analysis.py)                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Tasks:                                                                   │
│  ✓ Analyze distribution per job level                                   │
│  ✓ Identify promotion patterns                                          │
│  ✓ Create career progression paths                                      │
│  ✓ Feature engineering                                                   │
│                                                                           │
│  Features Created:                                                        │
│  • group_job_level (0, 1, 2)                                            │
│  • level_name_encoded                                                    │
│  • promotion_readiness_score                                             │
│  • is_management/is_staff/is_support                                    │
│  • tenure_level_ratio                                                    │
│                                                                           │
│  Output:                                                                  │
│  └─► Enhanced Dataset + Visualizations                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 STEP 2: PROMOTION PREDICTION MODEL                       │
│                 (02_promotion_prediction_model.py)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Model Training:                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │    Logistic      │  │  Random Forest   │  │   Gradient       │     │
│  │   Regression     │  │                  │  │   Boosting       │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
│           │                      │                      │                │
│           └──────────────────────┴──────────────────────┘                │
│                                  │                                        │
│                                  ▼                                        │
│                    ┌──────────────────────────┐                         │
│                    │   Model Comparison       │                         │
│                    │   (AUC-ROC, F1-Score)    │                         │
│                    └──────────────────────────┘                         │
│                                  │                                        │
│                                  ▼                                        │
│                    ┌──────────────────────────┐                         │
│                    │   Best Model Selection   │                         │
│                    │   + Feature Importance   │                         │
│                    └──────────────────────────┘                         │
│                                                                           │
│  Output:                                                                  │
│  └─► Trained Model (.pkl) + Evaluation Reports                         │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   STEP 3: SUCCESSION PLANNING                            │
│                   (03_succession_planning.py)                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Analysis:                                                                │
│  ┌──────────────────────────────────────────────────────────┐           │
│  │  1. Calculate Succession Readiness Score                 │           │
│  │     (Performance + Leadership + Behavior + Holistic)     │           │
│  └──────────────────────────────────────────────────────────┘           │
│                           │                                               │
│                           ▼                                               │
│  ┌──────────────────────────────────────────────────────────┐           │
│  │  2. Categorize Readiness                                 │           │
│  │     • Ready Now                                          │           │
│  │     • Ready 1-2 Years                                    │           │
│  │     • Ready 3+ Years                                     │           │
│  │     • Not Ready                                          │           │
│  └──────────────────────────────────────────────────────────┘           │
│                           │                                               │
│                           ▼                                               │
│  ┌──────────────────────────────────────────────────────────┐           │
│  │  3. Identify Successor Candidates                        │           │
│  │     (Top 3 per job level)                                │           │
│  └──────────────────────────────────────────────────────────┘           │
│                           │                                               │
│                           ▼                                               │
│  ┌──────────────────────────────────────────────────────────┐           │
│  │  4. Talent Pool Analysis                                 │           │
│  │     (Strength per job level)                             │           │
│  └──────────────────────────────────────────────────────────┘           │
│                           │                                               │
│                           ▼                                               │
│  ┌──────────────────────────────────────────────────────────┐           │
│  │  5. Succession Gap Analysis                              │           │
│  │     (Identify critical gaps)                             │           │
│  └──────────────────────────────────────────────────────────┘           │
│                                                                           │
│  Output:                                                                  │
│  └─► Successor List + Talent Pool Report + Dashboard                   │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          FINAL OUTPUTS                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  For HR/Management:                                                       │
│  • Successor candidates list                                             │
│  • Talent pool strength report                                           │
│  • Succession gap analysis                                               │
│  • Visual dashboards                                                      │
│                                                                           │
│  For Thesis:                                                              │
│  • Model performance metrics                                             │
│  • Feature importance analysis                                           │
│  • Visualizations & charts                                               │
│  • Methodology documentation                                             │
│                                                                           │
│  For Production (Optional):                                               │
│  • Trained model (.pkl)                                                  │
│  • Prediction API                                                        │
│  • Automated reports                                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

```
┌─────────────┐
│   Raw Data  │
│  (CSV files)│
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  Data Integration           │
│  • Merge employee data      │
│  • Add job level info       │
│  • Handle missing values    │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Feature Engineering        │
│  • Job level encoding       │
│  • Readiness score          │
│  • Interaction features     │
└──────┬──────────────────────┘
       │
       ├─────────────────────────────┐
       │                             │
       ▼                             ▼
┌──────────────┐            ┌──────────────────┐
│  ML Model    │            │  Succession      │
│  Training    │            │  Planning        │
│              │            │                  │
│  Input:      │            │  Input:          │
│  • Features  │            │  • Features      │
│  • Target    │            │  • Trained model │
│              │            │  • Career paths  │
│  Output:     │            │                  │
│  • Model     │────────────►  Output:         │
│  • Metrics   │            │  • Successors    │
└──────────────┘            │  • Gaps          │
                            │  • Reports       │
                            └──────────────────┘
```

---

## 🎯 Job Level Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    JOB LEVEL STRUCTURE                       │
└─────────────────────────────────────────────────────────────┘

GROUP 2: MANAGEMENT LEVEL
┌─────────────────────────────────────────────────────────────┐
│  Komisaris                                                   │
│     ▲                                                        │
│     │                                                        │
│  Direktur Utama                                             │
│     ▲                                                        │
│     │                                                        │
│  Direktur                                                    │
│     ▲                                                        │
│     │                                                        │
│  General Manager                                             │
│     ▲                                                        │
│     │                                                        │
│  Senior Manager                                              │
│     ▲                                                        │
│     │                                                        │
│  Manager                                                     │
│     ▲                                                        │
│     │                                                        │
│  Assistent Manager                                           │
└─────┬───────────────────────────────────────────────────────┘
      │
      │ PROMOTION PATH
      │
GROUP 1: STAFF/OFFICER LEVEL
┌─────┴───────────────────────────────────────────────────────┐
│  Officer / Staff                                             │
│     ▲                                                        │
│     │                                                        │
│  Junior Officer                                              │
└─────┬───────────────────────────────────────────────────────┘
      │
      │ PROMOTION PATH
      │
GROUP 0: SUPPORT LEVEL
┌─────┴───────────────────────────────────────────────────────┐
│  Non Staff / Non Pangkat                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 Succession Readiness Framework

```
┌─────────────────────────────────────────────────────────────┐
│              SUCCESSION READINESS CATEGORIES                 │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│  READY NOW   │  Performance ≥85, Leadership ≥80
│   (15-20%)   │  Tenure ≥2 years, Behavior ≥85
└──────┬───────┘
       │
       │ Action: Promote immediately or assign stretch roles
       │
┌──────▼────────────┐
│  READY 1-2 YEARS  │  Performance ≥75, Leadership ≥70
│     (25-30%)      │  Tenure ≥1 year, Behavior ≥75
└──────┬────────────┘
       │
       │ Action: Development programs, mentoring
       │
┌──────▼────────────┐
│  READY 3+ YEARS   │  Performance ≥65, Leadership ≥60
│     (30-35%)      │  Tenure ≥0 years, Behavior ≥65
└──────┬────────────┘
       │
       │ Action: Basic training, skill building
       │
┌──────▼────────────┐
│    NOT READY      │  Below all criteria
│     (15-20%)      │
└───────────────────┘
       │
       │ Action: Performance improvement plan
       │
```

---

## 🔍 Feature Importance Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  FEATURE IMPORTANCE                          │
│                  (Expected Ranking)                          │
└─────────────────────────────────────────────────────────────┘

1. Performance Score          ████████████████████████ 25-30%
   └─► Primary indicator of capability

2. Leadership Potential       ████████████████████ 20-25%
   └─► Critical for management roles

3. Job Level                  ████████████████ 15-20%
   └─► Career stage & readiness

4. Behavior Average           ████████████ 10-15%
   └─► Cultural fit & soft skills

5. Tenure Years               ██████████ 8-12%
   └─► Experience & stability

6. Holistic Score             ████████ 6-10%
   └─► Overall assessment

7. Interaction Features       ██████ 5-8%
   └─► Performance × Leadership

8. Other Features             ████ 3-5%
   └─► Gender, marital status, etc.
```

---

## 🎨 Output Visualizations

### 1. Job Level Analysis
```
┌─────────────────────────────────────────┐
│  Employee Distribution by Job Level     │
│                                         │
│  Manager        ████████████ 300       │
│  Officer        ███████████ 280        │
│  Staff          ██████████ 250         │
│  Senior Mgr     ████████ 200           │
│  ...                                    │
└─────────────────────────────────────────┘
```

### 2. Promotion Rate Analysis
```
┌─────────────────────────────────────────┐
│  Promotion Rate by Job Level            │
│                                         │
│  Manager        ████████████ 35%       │
│  Officer        ██████████ 28%         │
│  Staff          ████████ 22%           │
│  ...                                    │
└─────────────────────────────────────────┘
```

### 3. Model Performance
```
┌─────────────────────────────────────────┐
│  ROC Curve                              │
│                                         │
│  1.0 ┌─────────────────────────┐       │
│      │         ╱               │       │
│  0.8 │       ╱                 │       │
│      │     ╱                   │       │
│  0.6 │   ╱                     │       │
│      │ ╱                       │       │
│  0.4 │╱                        │       │
│      └─────────────────────────┘       │
│      0.0  0.2  0.4  0.6  0.8  1.0     │
│                                         │
│  AUC = 0.78                            │
└─────────────────────────────────────────┘
```

### 4. Succession Dashboard
```
┌─────────────────────────────────────────┐
│  Succession Readiness Distribution      │
│                                         │
│  Ready Now       ████ 18%              │
│  Ready 1-2Y      ████████ 28%          │
│  Ready 3+Y       ██████████ 32%        │
│  Not Ready       ██████ 22%            │
└─────────────────────────────────────────┘
```

---

## 🚦 Decision Tree for Usage

```
START
  │
  ▼
Do you have job level data?
  │
  ├─ YES ──► Run 01_job_level_analysis.py
  │          │
  │          ▼
  │       Is distribution balanced?
  │          │
  │          ├─ YES ──► Run 02_promotion_prediction_model.py
  │          │          │
  │          │          ▼
  │          │       Is model performance good (AUC ≥0.75)?
  │          │          │
  │          │          ├─ YES ──► Run 03_succession_planning.py
  │          │          │          │
  │          │          │          ▼
  │          │          │       SUCCESS! Use outputs for thesis
  │          │          │
  │          │          └─ NO ──► Tune hyperparameters
  │          │                    Add more features
  │          │                    Check data quality
  │          │
  │          └─ NO ──► Merge small levels
  │                    Use group_job_level instead
  │
  └─ NO ──► Create job level mapping
            from job positions
            Consult with HR
```

---

## 📋 Checklist for Thesis

```
Data Preparation
  ☐ Data cleaned and validated
  ☐ Job level mapping verified
  ☐ Missing values handled
  ☐ Outliers checked

Analysis
  ☐ Distribution analysis complete
  ☐ Feature engineering done
  ☐ Model trained and evaluated
  ☐ Cross-validation performed

Succession Planning
  ☐ Successor candidates identified
  ☐ Talent pools analyzed
  ☐ Gaps identified
  ☐ Recommendations made

Documentation
  ☐ Methodology written
  ☐ Results documented
  ☐ Visualizations created
  ☐ Limitations discussed

Validation
  ☐ Results validated with HR
  ☐ Business logic checked
  ☐ Peer review completed
  ☐ Ready for thesis submission
```

---

*This workflow ensures a systematic approach to promotion prediction and succession planning using job level as the primary organizational construct.*
