# 🏆 Promotion Candidates - User Guide

## 📋 Overview

The **Promotion Candidates** page is the core feature of the MPCIM HR Decision Support System. It uses Machine Learning (Random Forest model) to predict promotion probabilities for employees based on their performance, behavior, and other factors.

---

## 🎯 Key Features

### 1. **Top 10 Candidates Tab** 🥇
- Displays the 10 employees with highest promotion probability
- Medal system for top 3 (🥇🥈🥉)
- Compact, single-row design
- Quick metrics: Probability, Performance/Behavior, Tenure
- **View Details** button (👁️) for inline detail view

### 2. **All Candidates Tab** 📋
- Browse all employees or filter by minimum probability
- Color-coded badges:
  - 🌟 **High Potential** (≥70%)
  - ⭐ **Medium Potential** (50-70%)
  - 💡 **Low Potential** (<50%)
- Progress bars for visual probability
- Expandable detail view

### 3. **Employee Detail Tab** 🔍
- Full employee analysis
- Spider chart visualization
- Strengths and development areas
- HR recommendations
- Comprehensive metrics

---

## 🤖 How the ML Model Works

### Model: Random Forest Classifier

**Training Data**: Historical promotion data from company records

**Features Used** (14 total):
1. `tenure_years` (40.51% importance) ⭐ MOST IMPORTANT
2. `tenure_category_encoded` (32.63%)
3. `performance_rating_encoded` (5.08%)
4. `behavior_avg` (4.61%)
5. `performance_score` (3.64%)
6. `combined_score` (3.32%)
7. `marital_status_encoded` (2.72%)
8. `perf_beh_ratio` (2.66%)
9. `score_difference` (2.46%)
10. `behavioral_level_encoded` (1.00%)
11. `high_performer` (0.41%)
12. `gender_encoded` (0.38%)
13. `is_permanent_encoded` (0.13%)
14. `performance_level_encoded` (0.05%)

### Key Insights from Model

**1. Balance is More Important Than Excellence**
- Model prefers employees with balanced performance and behavior scores
- Example: 78/75 (gap=3) scores higher than 98/91 (gap=7)
- Reason: Historical data shows balanced employees adapt better to new roles

**2. Optimal Performance Range: 75-85**
- This range has highest historical promotion success rate
- Scores >90 may indicate "already at peak" or "overqualified"
- Scores <60 indicate need for development

**3. Tenure is Critical**
- 40% of prediction weight comes from tenure
- Optimal range: 3-7 years (Mid-level)
- Too short (<3): Insufficient experience
- Too long (>10): May prefer current role

**4. Other Factors**
- Permanent status slightly favored
- Marital status has minor influence
- Gender has minimal impact (model is fair)

---

## 📊 Understanding Predictions

### Example Analysis: Why Johan > Lina?

**Johan Budiman** 🥇 89.8%
- Performance: 78
- Behavior: 75
- Gap: 3 ✅ (Balanced)
- Range: 75-85 ✅ (Optimal)
- Tenure: 4 years ✅ (Mid-level)

**Lina Nasution** 🥈 88.8%
- Performance: 98
- Behavior: 91
- Gap: 7 ⚠️ (Larger gap)
- Range: >90 ⚠️ (Very high)
- Tenure: 4 years ✅ (Mid-level)

**Why Johan scores higher despite lower raw scores?**
1. **Better balance** (3 vs 7 gap)
2. **Optimal range** (75-85 vs >90)
3. **Historical pattern**: Balanced mid-performers get promoted more often
4. **Adaptability**: Model predicts Johan will adapt better to new role

**Important Note**: Both are excellent candidates! Model provides data-driven insights, but final HR decision should consider:
- Strategic needs
- Team dynamics
- Career development plans
- Individual aspirations

---

## 🎨 UI Features

### Compact Design
- **Space efficient**: 65% less vertical space than previous version
- **All info visible**: No scrolling needed for Top 10
- **Clean layout**: Professional appearance
- **Quick scanning**: Easy to compare candidates

### Interactive Elements
- **👁️ View Details**: Click to see full employee information
- **❌ Close**: Hide detail view
- **Progress bars**: Visual probability indicators
- **Color coding**: Quick identification of potential levels
- **Filters**: Adjust minimum probability threshold

### Responsive Layout
- Works on different screen sizes
- Columns adjust automatically
- Metrics scale properly
- Cards remain readable

---

## 📈 Usage Scenarios

### Scenario 1: Annual Promotion Review
1. Go to **Top 10 Candidates** tab
2. Review top performers
3. Click 👁️ to see detailed metrics
4. Compare balance, tenure, and scores
5. Shortlist candidates for interviews

### Scenario 2: Department-Specific Search
1. Go to **All Candidates** tab
2. Adjust probability threshold (e.g., 60%)
3. Filter by department (if available)
4. Review candidates meeting criteria
5. Export list for further analysis

### Scenario 3: Individual Assessment
1. Go to **Employee Detail** tab
2. Select specific employee
3. Review spider chart
4. Check strengths and development areas
5. Read HR recommendations
6. Make informed decision

---

## 🔍 Interpreting Results

### Probability Ranges

**High Potential (≥70%)** 🌟
- Strong promotion candidates
- Ready for advancement
- Recommend: Interview and assess fit

**Medium Potential (50-70%)** ⭐
- Good candidates with some gaps
- May need additional development
- Recommend: Consider for specific roles

**Low Potential (<50%)** 💡
- Not ready for promotion yet
- Focus on skill development
- Recommend: Create development plan

### Key Metrics to Consider

**Performance Score**
- Current job performance
- Consistency over time
- Achievement of KPIs

**Behavior Average**
- Soft skills and competencies
- Team collaboration
- Leadership potential

**Combined Score**
- Overall employee quality
- Holistic view of capabilities

**Score Difference**
- Balance between hard and soft skills
- Smaller gap = more balanced
- Model prefers balanced profiles

**Tenure**
- Experience in company
- Stability and commitment
- Optimal: 3-7 years

---

## ⚠️ Important Considerations

### Model Limitations

1. **Historical Bias**: Model learns from past decisions
   - May reflect historical biases
   - Should be used as one input, not sole decision maker

2. **Context Missing**: Model doesn't know:
   - Strategic business needs
   - Team dynamics
   - Individual career goals
   - Market conditions

3. **Data Quality**: Predictions are only as good as input data
   - Ensure accurate performance reviews
   - Keep behavioral assessments updated
   - Verify tenure and status information

### Best Practices

1. **Use as Decision Support, Not Decision Maker**
   - Model provides insights
   - HR expertise is essential
   - Consider qualitative factors

2. **Regular Model Updates**
   - Retrain with new promotion data
   - Adjust for changing business needs
   - Monitor prediction accuracy

3. **Transparent Communication**
   - Explain model to stakeholders
   - Share how predictions are made
   - Emphasize it's one of many factors

4. **Fair and Ethical Use**
   - Monitor for bias
   - Ensure equal opportunity
   - Respect privacy and confidentiality

---

## 🛠️ Troubleshooting

### Issue: All predictions show 0%
**Cause**: Using normalized data with model trained on original scale
**Solution**: Use non-normalized datasets (e.g., `sample_dataset_1000_balanced.csv`)

### Issue: Duplicate employees in Top 10
**Cause**: Data contains duplicate records
**Solution**: System automatically detects and shows unique employees only

### Issue: View Details button not working
**Cause**: Session state issue
**Solution**: Refresh page (Ctrl+R) - now fixed with inline detail view

### Issue: Unexpected rankings
**Cause**: Model considers multiple factors, not just raw scores
**Solution**: Review "Understanding Predictions" section above

---

## 📞 Support

For questions or issues:
1. Check this guide first
2. Review `FIX_*.md` files in project root
3. Contact: Deni Sulaeman (Master Program in Information Systems)

---

## 📝 Version History

**v2.0** (Current)
- ✅ Compact Top 10 design
- ✅ Inline detail view
- ✅ Duplicate detection
- ✅ Random Forest model
- ✅ 65% space reduction

**v1.0**
- Initial release
- Neural Network model (deprecated)
- Large card design

---

**Last Updated**: November 24, 2025
**Author**: Deni Sulaeman
**Project**: MPCIM Thesis - HR Decision Support System
