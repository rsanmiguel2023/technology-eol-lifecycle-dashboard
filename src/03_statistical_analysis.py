import pandas as pd
from scipy.stats import chi2_contingency, kruskal, spearmanr
from utils import PROCESSED, REPORTS

assets = pd.read_csv(PROCESSED / 'asset_risk_model.csv', low_memory=False)

# 1. EOL status vs criticality association
ct = pd.crosstab(assets['Lifecycle_Status'], assets['Criticality'])
chi2, p, dof, expected = chi2_contingency(ct)

# 2. Risk score differences by asset type
samples = [g['Risk_Score'].dropna() for _, g in assets.groupby('Asset_Type') if len(g) > 30]
h_stat, h_p = kruskal(*samples)

# 3. Correlation between age and incident volume
corr, corr_p = spearmanr(assets['Age_Years'].fillna(0), assets['Incident_Count'].fillna(0))

results = pd.DataFrame([
    {'test': 'Chi-square: Lifecycle status vs Criticality', 'statistic': chi2, 'p_value': p, 'interpretation': 'Tests whether EOL exposure is independent of business criticality.'},
    {'test': 'Kruskal-Wallis: Risk score by asset type', 'statistic': h_stat, 'p_value': h_p, 'interpretation': 'Tests whether risk score distributions differ across hardware categories.'},
    {'test': 'Spearman correlation: Asset age vs incident count', 'statistic': corr, 'p_value': corr_p, 'interpretation': 'Tests monotonic relationship between asset age and incident frequency.'}
])
results.to_csv(REPORTS / 'statistical_analysis_results.csv', index=False)
print(results.to_string(index=False))
