# 🏆 Promotion Candidates - Quick Reference Card

## 🚀 Quick Start

### Access the Page
```
1. Run Streamlit app: streamlit run app/Home.py
2. Navigate to: 👥 Promotion Candidates
3. Choose tab: 🏆 Top 10 | 📋 All | 🔍 Detail
```

---

## 📊 Understanding Rankings

### Why Employee X Ranks Higher Than Y?

**Key Factors** (in order of importance):

1. **Tenure** (40%) - Experience matters most
   - Optimal: 3-7 years
   - Too short (<3): Insufficient experience
   - Too long (>10): May prefer current role

2. **Balance** (5%) - Harmony between scores
   - Small gap (3-5): ✅ Balanced
   - Medium gap (6-10): ⚠️ Acceptable
   - Large gap (>10): ❌ Unbalanced

3. **Optimal Range** (4%) - Sweet spot performance
   - 75-85: ✅ Proven promotion zone
   - 60-75: ⚠️ Developing
   - >90: ⚠️ Already at peak
   - <60: ❌ Needs improvement

4. **Other Factors** (51%)
   - Tenure category, rating, status, etc.

---

## 🎯 Quick Interpretation

### Probability Ranges

| Range | Badge | Meaning | Action |
|-------|-------|---------|--------|
| ≥70% | 🌟 High | Ready for promotion | Interview & assess |
| 50-70% | ⭐ Medium | Good with gaps | Consider for specific roles |
| <50% | 💡 Low | Not ready yet | Development plan |

### Example Rankings Explained

**Johan (89.8%) > Lina (88.8%)**
```
Johan: 78/75 (gap=3) ✅ Balanced, optimal range
Lina:  98/91 (gap=7) ⚠️ Excellent but slight imbalance

Why? Model prefers balanced mid-performers
```

**Lina (88.8%) > Agus (85.9%)**
```
Lina: 98/91 (gap=7) ⚠️ Slight imbalance
Agus: 58/99 (gap=-41) ❌ Very unbalanced

Why? Agus is specialist, not generalist
```

---

## 🎨 UI Features

### Top 10 Tab
- Medal system: 🥇🥈🥉 for top 3
- Compact single-row design
- Click 👁️ to see details
- Inline detail expander

### All Candidates Tab
- Filter by probability threshold
- Color-coded badges
- Progress bars
- Click 👁️ Details for more info

### Employee Detail Tab
- Full analysis
- Spider chart
- Strengths & weaknesses
- HR recommendations

---

## 🔍 View Details Button

### How It Works

**Top 10 Tab**:
```
1. Click 👁️ button
2. Expander opens below list
3. Shows full employee info
4. Click ❌ Close to hide
```

**All Candidates Tab**:
```
1. Click 👁️ Details button
2. Detail section expands below card
3. Shows performance breakdown
4. Click ❌ Close to hide
```

### What You See
- Employee ID
- Promotion probability
- Performance & Behavior scores
- Score difference & ratio
- High performer status
- Personal info (gender, marital, status)

---

## 💡 Common Questions

### Q: Why is high performer not #1?
**A**: Model considers balance, not just raw scores. A balanced 78/75 may rank higher than unbalanced 98/70.

### Q: Can I trust the predictions?
**A**: Use as decision support, not sole decision maker. Consider:
- Strategic needs
- Team dynamics
- Individual goals
- Qualitative factors

### Q: How accurate is the model?
**A**: ~87% accuracy on test data. Based on historical promotion patterns.

### Q: Why does tenure matter so much?
**A**: Historical data shows experience (3-7 years) is best predictor of promotion success.

### Q: Is the model biased?
**A**: Gender has only 0.38% importance. Model is largely fair and based on performance.

---

## 🛠️ Troubleshooting

### Issue: All predictions show 0%
**Fix**: Use non-normalized data (`sample_dataset_1000_balanced.csv`)

### Issue: Duplicate employees
**Fix**: System auto-detects and shows unique only

### Issue: View Details not working
**Fix**: Now fixed with inline detail view. Refresh page if needed.

### Issue: Unexpected rankings
**Fix**: Review "Understanding Rankings" section above

---

## 📋 Filters & Options

### Minimum Probability Threshold
```
Default: 0.15 (15%)
Range: 0.00 - 1.00
Adjust: Use slider in sidebar
```

### Show All Employees
```
Toggle: Checkbox in sidebar
Effect: Shows all employees regardless of probability
```

### Refresh Data
```
Button: 🔄 Refresh Data (sidebar)
Effect: Reloads data from Data Explorer
```

---

## 🎓 Model Insights

### Feature Importance (Top 5)
1. **tenure_years** (40.51%)
2. **tenure_category** (32.63%)
3. **performance_rating** (5.08%)
4. **behavior_avg** (4.61%)
5. **performance_score** (3.64%)

### Key Patterns
- **Balance > Excellence**: 78/75 > 98/70
- **Optimal Range**: 75-85 best for promotion
- **Experience Matters**: 3-7 years optimal
- **Generalist > Specialist**: Balanced profiles preferred

---

## 📞 Quick Help

**For detailed explanation**: See `PROMOTION_CANDIDATES_GUIDE.md`  
**For model details**: See `MODEL_EXPLANATION.md`  
**For troubleshooting**: See `FIX_*.md` files

---

## 🔑 Key Takeaways

1. **Tenure is king** (40% importance)
2. **Balance matters** more than high scores
3. **75-85 range** is optimal for promotion
4. **Use as support**, not sole decision maker
5. **View Details** shows full employee info

---

**Version**: 2.0  
**Last Updated**: November 24, 2025  
**Author**: Deni Sulaeman
