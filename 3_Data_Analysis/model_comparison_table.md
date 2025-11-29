# OpenAI Models Sentiment & Emotion Analysis Comparison

## Executive Summary

This report compares the performance of various OpenAI models in sentiment and emotion analysis tasks using Indonesian tweet data related to COVID-19 PPKM policies.

**Best Sentiment Analysis Model:** gpt-5 (87.05% accuracy)

**Best Emotion Analysis Model:** gpt-5 (76.59% accuracy)

## Main Performance Metrics

| Model | Sentiment Accuracy (%) | Emotion Accuracy (%) |
|-------|------------------------|----------------------|
| gpt-5 | 87.05 | 76.59 |
| gpt-5 | 82.00 | 54.00 |
| gpt-5 | 82.00 | 76.00 |
| gpt-5-mini | 81.59 | 72.50 |
| gpt-5-nano | 80.00 | 42.00 |
| gpt-5-nano | 75.68 | 60.45 |
| gpt-4.1 | 83.41 | 72.27 |
| gpt-4.1-mini | 83.41 | 70.91 |
| gpt-4.1-nano | 77.05 | 62.73 |

## Sentiment Analysis F1-Scores

| Model | Positive | Negative | Neutral |
|-------|----------|----------|---------|
| gpt-5 | 0.920 | 0.900 | 0.000 |
| gpt-5 | 0.870 | 0.840 | 0.000 |
| gpt-5 | 0.840 | 0.860 | 0.000 |
| gpt-5-mini | 0.900 | 0.850 | 0.000 |
| gpt-5-nano | 0.820 | 0.900 | 0.000 |
| gpt-5-nano | 0.850 | 0.830 | 0.000 |
| gpt-4.1 | 0.910 | 0.880 | 0.000 |
| gpt-4.1-mini | 0.920 | 0.870 | 0.000 |
| gpt-4.1-nano | 0.890 | 0.820 | 0.000 |

## Emotion Analysis F1-Scores

| Model | Anger | Fear | Happy | Love | Sadness |
|-------|-------|------|-------|------|---------|
| gpt-5 | 0.830 | 0.750 | 0.810 | 0.820 | 0.730 |
| gpt-5 | 0.850 | 0.600 | 0.450 | 0.670 | 0.570 |
| gpt-5 | 0.890 | 0.600 | 0.810 | 0.860 | 0.670 |
| gpt-5-mini | 0.810 | 0.750 | 0.750 | 0.770 | 0.680 |
| gpt-5-nano | 0.750 | 0.600 | 0.000 | 0.400 | 0.730 |
| gpt-5-nano | 0.680 | 0.710 | 0.690 | 0.740 | 0.640 |
| gpt-4.1 | 0.790 | 0.760 | 0.800 | 0.830 | 0.710 |
| gpt-4.1-mini | 0.790 | 0.760 | 0.770 | 0.780 | 0.680 |
| gpt-4.1-nano | 0.720 | 0.720 | 0.760 | 0.790 | 0.590 |

## Key Insights

### Sentiment Analysis Performance
- **GPT-5** models achieve the highest sentiment accuracy (up to 87.05%)
- **GPT-4.1** models show consistent performance across all runs (83.41% accuracy)
- **GPT-5-nano** models offer good accuracy (75-80%) with potential cost/speed benefits
- **Neutral class** shows 0.0 F1-score across all models due to absence in test dataset

### Emotion Analysis Performance
- **GPT-5** leads in emotion accuracy (76.59%)
- **Anger** and **Love** emotions are consistently well-detected across models
- **Fear** and **Sadness** show moderate detection rates
- **Happy** emotion shows variability across model runs

### Model Recommendations
- **For highest accuracy:** Use GPT-5 (87.05% sentiment, 76.59% emotion)
- **For balanced performance:** GPT-4.1 models offer consistent results
- **For cost-efficiency:** GPT-5-nano provides good accuracy at lower cost

### Dataset Notes
- Test dataset: 440 Indonesian tweets about COVID-19 PPKM policies
- No neutral sentiment samples in test set (explains 0.0 F1-scores)
- Emotion distribution: Anger (110), Fear (65), Happy (101), Love (64), Sadness (100)

---
*Generated on: 2025-11-29*
*For questions or clarifications, please contact the data analysis team.*
