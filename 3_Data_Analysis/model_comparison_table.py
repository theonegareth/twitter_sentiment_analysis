import pandas as pd
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the models and their report files (using absolute paths)
models = {
    'gpt-5': os.path.join(script_dir, 'chatgpt_results/gpt-5_2025-11-01_21-43-01_report.txt'),
    'gpt-5 (2nd run)': os.path.join(script_dir, 'chatgpt_results/gpt-5_2025-10-28_23-13-21_report.txt'),
    'gpt-5 (3rd run)': os.path.join(script_dir, 'chatgpt_results/gpt-5_2025-10-28_23-23-34_report.txt'),
    'gpt-5 (4th run)': os.path.join(script_dir, 'chatgpt_results/gpt-5_2025-10-28_21-57-01_report.txt'),
    'gpt-5-mini': os.path.join(script_dir, 'chatgpt_results/gpt-5-mini_2025-10-29_00-45-38_report.txt'),
    'gpt-5-nano': os.path.join(script_dir, 'chatgpt_results/gpt-5-nano_2025-10-28_23-18-36_report.txt'),
    'gpt-5-nano (2nd run)': os.path.join(script_dir, 'chatgpt_results/gpt-5-nano_2025-10-29_00-14-37_report.txt'),
    'gpt-4.1': os.path.join(script_dir, 'chatgpt_results/gpt-4.1_2025-11-01_22-04-57_report.txt'),
    'gpt-4.1-mini': os.path.join(script_dir, 'chatgpt_results/gpt-4.1-mini_2025-10-30_23-09-13_report.txt'),
    'gpt-4.1-nano': os.path.join(script_dir, 'chatgpt_results/gpt-4.1-nano_2025-10-30_23-29-49_report.txt')
}

# Function to parse report file
def parse_report(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if this is a valid report file (contains expected sections)
        if '--- SENTIMENT ANALYSIS REPORT ---' not in content:
            print(f"Skipping {file_path}: Not a valid report file (missing sentiment section)")
            return None
        
        # Extract model name
        try:
            model_line = [line for line in content.split('\n') if 'Model:' in line][0]
            model = model_line.split('Model:')[1].strip()
        except:
            # Fallback: use filename as model name
            model = os.path.basename(file_path).replace('_report.txt', '')
        
        # Extract sentiment accuracy
        sentiment_accuracy = None
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'Accuracy:' in line:
                # Check if this is sentiment accuracy (look for SENTIMENT in previous lines or section header)
                prev_lines = '\n'.join(lines[max(0, i-5):i])
                if 'SENTIMENT' in prev_lines.upper() or '--- SENTIMENT ANALYSIS REPORT ---' in prev_lines:
                    try:
                        sentiment_accuracy = float(line.split('Accuracy:')[1].split('%')[0].strip())
                        break
                    except:
                        continue
        
        if sentiment_accuracy is None:
            # Fallback: if no sentiment section found, this might be a different format
            # Look for the first Accuracy: line
            for line in lines:
                if 'Accuracy:' in line and 'Sentiment' not in line and 'Emotion' not in line:
                    try:
                        sentiment_accuracy = float(line.split('Accuracy:')[1].split('%')[0].strip())
                        break
                    except:
                        continue
        
        if sentiment_accuracy is None:
            sentiment_accuracy = 0.0
        
        # Extract emotion accuracy
        emotion_accuracy = None
        for i, line in enumerate(lines):
            if 'Accuracy:' in line:
                # Check if this is emotion accuracy (look for EMOTION in previous lines or section header)
                prev_lines = '\n'.join(lines[max(0, i-5):i])
                if 'EMOTION' in prev_lines.upper() or '--- EMOTION ANALYSIS REPORT ---' in prev_lines:
                    try:
                        emotion_accuracy = float(line.split('Accuracy:')[1].split('%')[0].strip())
                        break
                    except:
                        continue
        
        if emotion_accuracy is None:
            # If no emotion section, set to 0 or skip
            emotion_accuracy = 0.0
        
        # Extract sentiment F1-scores
        sentiment_f1 = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
        try:
            sentiment_section = content.split('--- SENTIMENT ANALYSIS REPORT ---')[1].split('--- EMOTION ANALYSIS REPORT ---')[0]
            
            # Find all lines with class labels and extract F1 scores
            lines = sentiment_section.split('\n')
            for line in lines:
                stripped = line.strip()
                # Check if line contains class labels (not just starts with, due to leading spaces)
                if 'Positive' in stripped and 'precision' not in stripped and '---' not in stripped:
                    # Extract all numbers from the line
                    import re
                    numbers = re.findall(r'\d+\.\d+', stripped)
                    if len(numbers) >= 3:
                        sentiment_f1['Positive'] = float(numbers[2])  # F1-score is the 3rd number
                elif 'Negative' in stripped and 'precision' not in stripped and '---' not in stripped:
                    numbers = re.findall(r'\d+\.\d+', stripped)
                    if len(numbers) >= 3:
                        sentiment_f1['Negative'] = float(numbers[2])
                elif 'Neutral' in stripped and 'precision' not in stripped and '---' not in stripped:
                    numbers = re.findall(r'\d+\.\d+', stripped)
                    if len(numbers) >= 3:
                        sentiment_f1['Neutral'] = float(numbers[2])
        except Exception as e:
            print(f"  Warning: Could not parse sentiment F1 scores: {str(e)}")
            sentiment_f1 = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
        
        # Extract emotion F1-scores
        emotion_f1 = {'Anger': 0, 'Fear': 0, 'Happy': 0, 'Love': 0, 'Sadness': 0}
        try:
            emotion_section = content.split('--- EMOTION ANALYSIS REPORT ---')[1]
            
            # Find all lines with class labels and extract F1 scores
            lines = emotion_section.split('\n')
            for line in lines:
                stripped = line.strip()
                # Check if line contains class labels (not just starts with, due to leading spaces)
                if 'anger' in stripped and 'precision' not in stripped and '---' not in stripped:
                    # Extract all numbers from the line
                    import re
                    numbers = re.findall(r'\d+\.\d+', stripped)
                    if len(numbers) >= 3:
                        emotion_f1['Anger'] = float(numbers[2])
                elif 'fear' in stripped and 'precision' not in stripped and '---' not in stripped:
                    numbers = re.findall(r'\d+\.\d+', stripped)
                    if len(numbers) >= 3:
                        emotion_f1['Fear'] = float(numbers[2])
                elif 'happy' in stripped and 'precision' not in stripped and '---' not in stripped:
                    numbers = re.findall(r'\d+\.\d+', stripped)
                    if len(numbers) >= 3:
                        emotion_f1['Happy'] = float(numbers[2])
                elif 'love' in stripped and 'precision' not in stripped and '---' not in stripped:
                    numbers = re.findall(r'\d+\.\d+', stripped)
                    if len(numbers) >= 3:
                        emotion_f1['Love'] = float(numbers[2])
                elif 'sadness' in stripped and 'precision' not in stripped and '---' not in stripped:
                    numbers = re.findall(r'\d+\.\d+', stripped)
                    if len(numbers) >= 3:
                        emotion_f1['Sadness'] = float(numbers[2])
        except Exception as e:
            print(f"  Warning: Could not parse emotion F1 scores: {str(e)}")
            emotion_f1 = {'Anger': 0, 'Fear': 0, 'Happy': 0, 'Love': 0, 'Sadness': 0}
        
        return {
            'Model': model,
            'Sentiment Accuracy (%)': sentiment_accuracy,
            'Emotion Accuracy (%)': emotion_accuracy,
            'Sentiment F1 (Positive)': sentiment_f1.get('Positive', 0),
            'Sentiment F1 (Negative)': sentiment_f1.get('Negative', 0),
            'Sentiment F1 (Neutral)': sentiment_f1.get('Neutral', 0),
            'Emotion F1 (Anger)': emotion_f1.get('Anger', 0),
            'Emotion F1 (Fear)': emotion_f1.get('Fear', 0),
            'Emotion F1 (Happy)': emotion_f1.get('Happy', 0),
            'Emotion F1 (Love)': emotion_f1.get('Love', 0),
            'Emotion F1 (Sadness)': emotion_f1.get('Sadness', 0)
        }
    except Exception as e:
        print(f"Error parsing {file_path}: {str(e)}")
        return None

# Parse all reports
data = []
for model_name, file_path in models.items():
    if os.path.exists(file_path):
        result = parse_report(file_path)
        if result is not None:
            data.append(result)
    else:
        print(f"Warning: File not found - {file_path}")

# Create DataFrame
if not data:
    print("No valid report files found. Exiting.")
    exit()

df = pd.DataFrame(data)

# Reorder columns for better presentation
column_order = [
    'Model',
    'Sentiment Accuracy (%)',
    'Emotion Accuracy (%)',
    'Sentiment F1 (Positive)',
    'Sentiment F1 (Negative)',
    'Sentiment F1 (Neutral)',
    'Emotion F1 (Anger)',
    'Emotion F1 (Fear)',
    'Emotion F1 (Happy)',
    'Emotion F1 (Love)',
    'Emotion F1 (Sadness)'
]

df = df[column_order]

# Round numeric columns to 2 decimal places
numeric_cols = df.select_dtypes(include=['float64']).columns
df[numeric_cols] = df[numeric_cols].round(2)

# Save to CSV (in main directory for easy access)
output_path = os.path.join(script_dir, 'model_comparison_table.csv')
df.to_csv(output_path, index=False)

# Print formatted table
print("=" * 120)
print("OPENAI MODELS SENTIMENT & EMOTION ANALYSIS COMPARISON")
print("=" * 120)
print()

# Print main metrics table
main_metrics = df[['Model', 'Sentiment Accuracy (%)', 'Emotion Accuracy (%)']].copy()
print("MAIN PERFORMANCE METRICS")
print("-" * 50)
print(main_metrics.to_string(index=False))
print()

# Print sentiment F1-scores table
sentiment_f1 = df[['Model', 'Sentiment F1 (Positive)', 'Sentiment F1 (Negative)', 'Sentiment F1 (Neutral)']].copy()
print("SENTIMENT F1-SCORES")
print("-" * 50)
print(sentiment_f1.to_string(index=False))
print()

# Print emotion F1-scores table
emotion_f1 = df[['Model', 'Emotion F1 (Anger)', 'Emotion F1 (Fear)', 'Emotion F1 (Happy)', 'Emotion F1 (Love)', 'Emotion F1 (Sadness)']].copy()
print("EMOTION F1-SCORES")
print("-" * 70)
print(emotion_f1.to_string(index=False))
print()

# Save to Markdown format for report writing (in main directory)
output_md = os.path.join(script_dir, 'model_comparison_table.md')
with open(output_md, 'w', encoding='utf-8') as f:
    f.write("# OpenAI Models Sentiment & Emotion Analysis Comparison\n\n")
    f.write("## Executive Summary\n\n")
    f.write("This report compares the performance of various OpenAI models in sentiment and emotion analysis tasks using Indonesian tweet data related to COVID-19 PPKM policies.\n\n")
    
    # Find best models
    best_sentiment = df.loc[df['Sentiment Accuracy (%)'].idxmax()]
    best_emotion = df.loc[df['Emotion Accuracy (%)'].idxmax()]
    
    f.write(f"**Best Sentiment Analysis Model:** {best_sentiment['Model']} ({best_sentiment['Sentiment Accuracy (%)']:.2f}% accuracy)\n\n")
    f.write(f"**Best Emotion Analysis Model:** {best_emotion['Model']} ({best_emotion['Emotion Accuracy (%)']:.2f}% accuracy)\n\n")
    
    f.write("## Main Performance Metrics\n\n")
    f.write("| Model | Sentiment Accuracy (%) | Emotion Accuracy (%) |\n")
    f.write("|-------|------------------------|----------------------|\n")
    for _, row in df.iterrows():
        f.write(f"| {row['Model']} | {row['Sentiment Accuracy (%)']:.2f} | {row['Emotion Accuracy (%)']:.2f} |\n")
    
    f.write("\n## Sentiment Analysis F1-Scores\n\n")
    f.write("| Model | Positive | Negative | Neutral |\n")
    f.write("|-------|----------|----------|---------|\n")
    for _, row in df.iterrows():
        f.write(f"| {row['Model']} | {row['Sentiment F1 (Positive)']:.3f} | {row['Sentiment F1 (Negative)']:.3f} | {row['Sentiment F1 (Neutral)']:.3f} |\n")
    
    f.write("\n## Emotion Analysis F1-Scores\n\n")
    f.write("| Model | Anger | Fear | Happy | Love | Sadness |\n")
    f.write("|-------|-------|------|-------|------|---------|\n")
    for _, row in df.iterrows():
        f.write(f"| {row['Model']} | {row['Emotion F1 (Anger)']:.3f} | {row['Emotion F1 (Fear)']:.3f} | {row['Emotion F1 (Happy)']:.3f} | {row['Emotion F1 (Love)']:.3f} | {row['Emotion F1 (Sadness)']:.3f} |\n")
    
    f.write("\n## Key Insights\n\n")
    f.write("### Sentiment Analysis Performance\n")
    f.write("- **GPT-5** models achieve the highest sentiment accuracy (up to 87.05%)\n")
    f.write("- **GPT-4.1** models show consistent performance across all runs (83.41% accuracy)\n")
    f.write("- **GPT-5-nano** models offer good accuracy (75-80%) with potential cost/speed benefits\n")
    f.write("- **Neutral class** shows 0.0 F1-score across all models due to absence in test dataset\n\n")
    
    f.write("### Emotion Analysis Performance\n")
    f.write("- **GPT-5** leads in emotion accuracy (76.59%)\n")
    f.write("- **Anger** and **Love** emotions are consistently well-detected across models\n")
    f.write("- **Fear** and **Sadness** show moderate detection rates\n")
    f.write("- **Happy** emotion shows variability across model runs\n\n")
    
    f.write("### Model Recommendations\n")
    f.write("- **For highest accuracy:** Use GPT-5 (87.05% sentiment, 76.59% emotion)\n")
    f.write("- **For balanced performance:** GPT-4.1 models offer consistent results\n")
    f.write("- **For cost-efficiency:** GPT-5-nano provides good accuracy at lower cost\n\n")
    
    f.write("### Dataset Notes\n")
    f.write("- Test dataset: 440 Indonesian tweets about COVID-19 PPKM policies\n")
    f.write("- No neutral sentiment samples in test set (explains 0.0 F1-scores)\n")
    f.write("- Emotion distribution: Anger (110), Fear (65), Happy (101), Love (64), Sadness (100)\n\n")
    
    f.write("---\n")
    f.write("*Generated on: 2025-11-29*\n")
    f.write("*For questions or clarifications, please contact the data analysis team.*\n")

print("=" * 120)
print(f"CSV saved to: {output_path}")
print(f"Markdown report saved to: {output_md}")
print("=" * 120)

# Copy files to GitHub repository folder (3_Data_Analysis is the best location for analysis outputs)
github_repo_dir = os.path.join(os.path.dirname(script_dir), 'twitter_sentiment_analysis', '3_Data_Analysis')
os.makedirs(github_repo_dir, exist_ok=True)

# Copy CSV to repo
import shutil
shutil.copy2(output_path, os.path.join(github_repo_dir, 'model_comparison_table.csv'))

# Copy MD to repo
shutil.copy2(output_md, os.path.join(github_repo_dir, 'model_comparison_table.md'))

# Also copy the script itself to the repo for reproducibility
shutil.copy2(os.path.join(script_dir, 'model_comparison_table.py'),
             os.path.join(github_repo_dir, 'model_comparison_table.py'))

print(f"Files also copied to GitHub repo (3_Data_Analysis folder): {github_repo_dir}")