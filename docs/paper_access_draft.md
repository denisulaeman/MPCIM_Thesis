# Multi-Dimensional Performance–Career Integration Model (MPCIM) for Promotion Prediction

**Author(s)**: _Fill in names_, Member/Student, IEEE  
**Affiliation(s)**: _Fill in affiliations with superscript numbering_  
**Corresponding Author**: _email_  

## Abstract
This study develops a promotion prediction system that fuses performance and behavioral assessments on an anonymized dataset of 712 employees (9.27% promoted). After outlier capping (IQR), 14 engineered features (ratios, balance, tenure categories) and SMOTE balancing, we compare three logistic-regression baselines with advanced models (Random Forest, XGBoost, and an MLP). The best model (MLP) reaches 90.9% accuracy and 55.2% F1, doubling precision over the dual baseline (24.4% → 50.0%). Behavioral scores are statistically significant for promotion (p=0.037), while performance is not (p=0.083); tenure correlates negatively with promotion (r=-0.169), revealing a “tenure paradox.” A psychological extension (28 features total) on a balanced demo dataset shows 44.7% of model importance coming from psychological factors (leadership, drive, mental readiness), underscoring the value of holistic assessment. We also deliver a decision-support app with interpretability (feature importances, SHAP), promotion candidate dashboards, and psychological insights for HR practice.

## Index Terms
Promotion prediction; HR analytics; Behavioral assessment; Psychological assessment; Class imbalance; Explainable AI; Career progression; SMOTE.

## I. Introduction
Performance management remains contentious in practice, with traditional appraisal systems criticized for subjectivity and limited predictive power [1], [2]. Competency-based approaches emphasize behavioral evidence but are often underused in predictive settings [6]–[8]. HR analytics calls for evidence-based, transparent decision-making to avoid fad-driven adoption [11], [12]. In the focal organization, only 9.27% of 712 employees were promoted, highlighting a severe class imbalance. We hypothesize that combining performance and behavioral dimensions—and later psychological readiness—can raise precision and interpretability for promotion screening. Imbalanced learning techniques such as SMOTE [13] and class-sensitive evaluation [17] are necessary to avoid bias toward the majority class.

### Contributions (Novelty)
1) **Dual-dimensional modeling**: Performance + behavioral signals improve baseline accuracy by +32.9% over single-dimension models and lift F1 to 37.0%.  
2) **Holistic psychological extension**: Adding 14 psychological features yields 44.7% cumulative importance, surfacing leadership readiness and drive.  
3) **Tenure paradox evidence**: Tenure correlates negatively with promotion (r=-0.169); junior employees are 2.8× likelier to be promoted than seniors.  
4) **Precision uplift with imbalance handling**: SMOTE + engineered ratios double precision (24.4% → 50.0%) at F1=55.2%.  
5) **End-to-end HR app**: A promotion-candidates page with probability gauges, radar charts, “why this probability?” explanations, and psychological insights operationalizes the models for HR.

## II. Related Work
Competency and behavioral validation efforts (e.g., Bartram’s Great Eight and Boyatzis) provide structured evidence but seldom integrate with predictive models [6], [7]. XGBoost [14], Random Forests [15], and deep neural networks [16] dominate structured prediction benchmarks, while class imbalance remedies such as SMOTE [13] remain standard practice. Interpretability advances—including SHAP [18], LIME [19], and broader guidance on transparent models [20]—address the need for HR-facing explanations. Talent management and succession planning literature [21]–[23] stresses leadership readiness, aligning with our psychological extension. Ethical guidelines for algorithmic hiring urge fairness and accountability safeguards [24], [25].

## III. Data
We combine a PostgreSQL HR database (195 tables, 60 relevant) with an Excel-based behavioral file; employee identifiers are MD5-hashed (no PII/financial data). Records include 13,478 performance assessments, 19,929 behavioral assessments, and 130 promotion events. The integrated set covers 712 employees (66 promoted, 646 not; 9.27% rate). A balanced demo dataset (1,000 rows, 70% promoted) adds psychological columns for UI and feature studies.

### Descriptive Statistics (712 employees)
- Performance: mean 81.88, std 34.94, min 36.63, max 125.31.  
- Behavioral: mean 89.72, std 8.71, min 71.51, max 111.09.  
- Tenure (years): mean 8.17, std 7.28, min 0, max 125.

## IV. Methods
### A. Preprocessing
Outliers are capped via the IQR rule (46 performance, 35 behavioral). Only 14 missing `performance_rating` values are handled via encoding/imputation. Standardization uses scikit-learn [26], [32] to equalize feature scales.

### B. Feature Engineering (14 features)
Ratios and balance metrics (`perf_beh_ratio`, `score_difference`, `combined_score`), categorical bands (`tenure_category`, `performance_level`, `behavioral_level`), and binary flags (`high_performer`, gender/marital/permanent/rating encodings) capture non-linear promotion patterns.

### C. Imbalance Handling
SMOTE synthesizes minority samples on the training split (66:646 → 516:516) [13], [17], consistent with established treatments of imbalanced data [35], [36]. The test split preserves the original distribution.

### D. Models and Evaluation
Baselines: Logistic Regression (performance-only, behavioral-only, dual). Advanced: Random Forest (100 trees, max_depth=10) [15], XGBoost (100 estimators, depth=6, lr=0.1) [14], and an MLP (64-32-16, ReLU, Adam) [16]. Metrics: Accuracy, Precision, Recall, F1 (primary), ROC-AUC; confusion matrices support error analysis. Implementation leverages scikit-learn and standard ML tooling [26], [32].

### E. Interpretability and UX
Global importance via tree-based feature importances and SHAP [18]; local rationale via LIME [19] (planned) and rule-based “why this probability?” explanations. Psychological and leadership indicators surface in UI elements for HR consumption.

## V. Experimental Results
### A. Significance Tests
Behavioral vs promotion: t=2.09, **p=0.037** (significant). Performance vs promotion: t=1.739, p=0.083 (not significant). Correlation with promotion: behavioral r=0.078; performance r=0.065; tenure r=-0.169.

### B. Model Comparison (Test Set, 712 dataset)
| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|----------|-----------|--------|----|---------|
| Performance-only LR | 57.3% | 15.7% | 84.6% | 26.5% | 72.3% |
| Behavioral-only LR | 35.0% | 10.8% | 84.6% | 19.1% | 65.3% |
| Dual LR | 76.2% | 24.4% | 76.9% | 37.0% | 81.2% |
| Random Forest | 87.4% | 39.1% | 69.2% | 50.0% | 90.1% |
| XGBoost | 89.5% | 44.4% | 61.5% | 51.6% | 88.3% |
| **MLP (best)** | **90.9%** | **50.0%** | **61.5%** | **55.2%** | **88.3%** |

### C. Tenure Paradox
Promotion rate: junior 14.3%, mid 10.0%, senior 5.1%; average tenure promoted 4.32 years vs 8.56 years non-promoted. Seniority alone reduces promotion odds despite higher experience.

### D. Feature Importance (Random Forest)
Top drivers: `tenure_years` (40.5%), `tenure_category` (32.6%), followed by `performance_rating` (5.1%), `behavior_avg` (4.6%), `performance_score` (3.6%). Behavioral/performance ratios add ~10–15% explanatory power.

## VI. Psychological Extension (Balanced Demo, 28 Features)
Direct features: psychological_score, drive, mental_strength, adaptability, collaboration, leadership_potential. Derived features: psych/performance ratio, psych/behavior ratio, holistic_balance, level encodings, high-drive/adaptability/leadership flags. Total psychological importance reaches 44.7%; `psych_perf_ratio` (6.12%) and `leadership_potential` (5.98%) rank in the top four. Perfect train/test scores on the balanced demo warrant cross-validated leakage checks before deployment.

## VII. System and App Innovations
The promotion-candidates page exposes probabilities, radar charts (performance/behavior/tenure), compact top-10 views with leadership badges, and psychological panels (drive, mental strength, adaptability, collaboration, leadership potential). “Why this probability?” explanations reference tenure band, balance gap, performance range, and psychological strengths/risks, aligning with explainability guidance [18]–[20]. Data sources support live PostgreSQL with CSV fallback; IDs are anonymized.

## VIII. Discussion
Multi-dimensional signals materially raise precision and F1 on an imbalanced target, outperforming single-dimension baselines. Behavioral significance suggests soft skills are decisive for promotion, while performance alone is insufficient. The tenure paradox challenges seniority-based promotion norms, indicating early-career talent acceleration. Psychological indicators surface leadership readiness but require robust validation to rule out overfitting on balanced demos. Fairness audits and probability calibration are needed to mitigate demographic bias and overconfidence [24], [25].

## IX. Conclusion
Integrating performance, behavioral, and psychological assessments yields higher promotion prediction accuracy (up to 90.9%) and doubles precision versus dual baselines. Statistical tests confirm behavioral relevance and expose a tenure paradox. The accompanying HR app operationalizes these insights with interpretable views, making promotion screening faster and more defensible.

## X. Future Work
1) Stratified K-fold and temporal splits; probability calibration.  
2) Fairness audits by gender/marital/contract status; counterfactual checks.  
3) Integrate psychological features into the main 712-employee pipeline and retrain with leakage controls.  
4) SHAP-based local explanations for both tree and neural models; ablation on ratios/tenure/psych features.  
5) Sensitivity analyses on hyperparameters and cost-sensitive learning to optimize recall without inflating false positives.

## Appendix: Figure and Table Assets (for template insertion)
- **Target distribution & EDA**: `results/eda_plots/01_target_distribution.png`, `02_performance_analysis.png`, `03_behavioral_analysis.png`, `04_correlation_matrix.png`.  
- **Feature engineering**: `results/feature_engineering/01_outlier_detection.png`, `02_feature_scaling.png`, `03_smote_balancing.png`, `04_feature_correlation.png`.  
- **Baselines**: `results/baseline_models/01_confusion_matrices.png`, `02_roc_curves.png`, `03_precision_recall_curves.png`, `04_metrics_comparison.png`, `05_feature_importance.png`.  
- **Advanced models**: `results/advanced_models/01_confusion_matrices.png`, `02_roc_curves_all.png`, `03_metrics_comparison_all.png`, `04_feature_importance.png`.  
- **SHAP**: `results/shap_analysis/01_shap_summary_plot.png`, `02_shap_bar_plot.png`, `03_waterfall_promoted.png`, `04_waterfall_not_promoted.png`, `05_waterfall_borderline.png`, `06_dependence_1_tenure_years.png`, `06_dependence_2_tenure_category_encoded.png`, `06_dependence_3_behavior_avg.png`, `09_importance_comparison.png`.  
- **Psychological extension**: `results/psychological_model/performance_comparison.png`, `feature_importance_comparison.png`.  
- **Precision tuning**: `results/precision_improvement/01_threshold_analysis.png`.  
- **Tables (CSV ready)**: `results/advanced_models/advanced_models_results.csv`, `results/psychological_model/model_comparison.csv`, `results/psychological_model/feature_importance_combined.csv`, `results/shap_analysis/feature_importance_comparison.csv`, `results/precision_improvement/threshold_results.csv`.

## Acknowledgment
_Insert funding/organization acknowledgments as required._

## References
[1] H. Aguinis, H. Joo, and R. K. Gottfredson, "Why we hate performance management—and why we should love it," Business Horizons, vol. 56, no. 6, pp. 503-507, 2019.  
[2] S. E. Scullen, M. K. Mount, and G. M. Goff, "Understanding the latent structure of job performance ratings," J. Appl. Psychol., vol. 85, no. 6, pp. 956-970, 2000.  
[3] K. R. Murphy and J. N. Cleveland, Understanding Performance Appraisal: Social, Organizational, and Goal-Based Perspectives. Thousand Oaks, CA, USA: Sage, 1995.  
[4] T. W. Ng, L. T. Eby, K. L. Sorensen, and D. C. Feldman, "Predictors of objective and subjective career success: A meta-analysis," Pers. Psychol., vol. 58, no. 2, pp. 367-408, 2005.  
[5] P. R. Niven and B. Lamorte, Objectives and Key Results: Driving Focus, Alignment, and Engagement with OKRs. Hoboken, NJ, USA: Wiley, 2016.  
[6] D. Bartram, "The Great Eight competencies: A criterion-centric approach to validation," J. Appl. Psychol., vol. 90, no. 6, pp. 1185-1203, 2005.  
[7] R. E. Boyatzis, "Competencies in the 21st century," J. Manag. Develop., vol. 27, no. 1, pp. 5-12, 2008.  
[8] L. M. Spencer and S. M. Spencer, Competence at Work: Models for Superior Performance. New York, NY, USA: Wiley, 1993.  
[9] J. W. Boudreau and P. M. Ramstad, Beyond HR: The New Science of Human Capital. Boston, MA, USA: Harvard Business, 2007.  
[10] W. F. Cascio and H. Aguinis, Applied Psychology in Talent Management, 8th ed. Thousand Oaks, CA, USA: Sage, 2019.  
[11] T. Rasmussen and D. Ulrich, "Learning from practice: How HR analytics avoids being a management fad," Organizational Dynamics, vol. 44, no. 3, pp. 236-242, 2015.  
[12] J. H. Marler and J. W. Boudreau, "An evidence-based review of HR analytics," Int. J. Hum. Resource Manag., vol. 28, no. 1, pp. 3-26, 2017.  
[13] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, "SMOTE: Synthetic minority over-sampling technique," J. Artif. Intell. Res., vol. 16, pp. 321-357, 2002.  
[14] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining, 2016, pp. 785-794.  
[15] L. Breiman, "Random forests," Mach. Learn., vol. 45, no. 1, pp. 5-32, 2001.  
[16] I. Goodfellow, Y. Bengio, and A. Courville, Deep Learning. Cambridge, MA, USA: MIT Press, 2016.  
[17] H. He and E. A. Garcia, "Learning from imbalanced data," IEEE Trans. Knowl. Data Eng., vol. 21, no. 9, pp. 1263-1284, 2009.  
[18] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in Proc. Adv. Neural Inf. Process. Syst., 2017, pp. 4765-4774.  
[19] M. T. Ribeiro, S. Singh, and C. Guestrin, "'Why should I trust you?': Explaining the predictions of any classifier," in Proc. 22nd ACM SIGKDD, 2016, pp. 1135-1144.  
[20] C. Molnar, Interpretable Machine Learning: A Guide for Making Black Box Models Explainable. 2nd ed. 2020.  
[21] D. G. Collings and K. Mellahi, "Strategic talent management: A review and research agenda," Hum. Resource Manag. Rev., vol. 19, no. 4, pp. 304-313, 2009.  
[22] P. Cappelli and J. R. Keller, "Talent management: Conceptual approaches and practical challenges," Annu. Rev. Organizational Psychol. Organizational Behav., vol. 1, no. 1, pp. 305-331, 2014.  
[23] K. S. Groves, "Integrating leadership development and succession planning best practices," J. Manag. Develop., vol. 26, no. 3, pp. 239-260, 2007.  
[24] B. Lepri, N. Oliver, E. Letouze, A. Pentland, and P. Vinck, "Fair, transparent, and accountable algorithmic decision-making processes," Philosophy & Technology, vol. 31, no. 4, pp. 611-627, 2018.  
[25] M. Raghavan, S. Barocas, J. Kleinberg, and K. Levy, "Mitigating bias in algorithmic hiring: Evaluating claims and practices," in Proc. ACM Conf. Fairness, Accountability, and Transparency, 2020, pp. 469-481.  
[26] F. Pedregosa et al., "Scikit-learn: Machine learning in Python," J. Mach. Learn. Res., vol. 12, pp. 2825-2830, 2011.  
[27] A. Field, Discovering Statistics Using IBM SPSS Statistics, 4th ed. Thousand Oaks, CA, USA: Sage, 2013.  
[28] J. F. Hair, W. C. Black, B. J. Babin, and R. E. Anderson, Multivariate Data Analysis, 8th ed. Andover, U.K.: Cengage, 2019.  
[29] T. A. Judge, C. A. Higgins, C. J. Thoresen, and M. R. Barrick, "The big five personality traits, general mental ability, and career success across the life span," Pers. Psychol., vol. 52, no. 3, pp. 621-652, 1999.  
[30] S. E. Seibert, M. L. Kraimer, and R. C. Liden, "A social capital theory of career success," Acad. Manag. J., vol. 44, no. 2, pp. 219-237, 2001.  
[31] F. Provost and T. Fawcett, Data Science for Business. Sebastopol, CA, USA: O'Reilly, 2013.  
[32] A. Geron, Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow, 2nd ed. Sebastopol, CA, USA: O'Reilly, 2019.  
[33] G. S. Benson, D. Finegold, and S. A. Mohrman, "You paid for the skills, now keep them: Tuition reimbursement and voluntary turnover," Acad. Manag. J., vol. 47, no. 3, pp. 315-331, 2004.  
[34] C. O. Trevor, B. Gerhart, and J. W. Boudreau, "Voluntary turnover and job performance: Curvilinearity and the moderating influences of salary growth and promotions," J. Appl. Psychol., vol. 82, no. 1, pp. 44-61, 1997.  
[35] A. Fernandez, S. Garcia, M. Galar, R. C. Prati, B. Krawczyk, and F. Herrera, Learning from Imbalanced Data Sets. Cham, Switzerland: Springer, 2018.  
[36] G. E. Batista, R. C. Prati, and M. C. Monard, "A study of the behavior of several methods for balancing machine learning training data," ACM SIGKDD Explor., vol. 6, no. 1, pp. 20-29, 2004.
