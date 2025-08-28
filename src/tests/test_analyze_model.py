######
# Test for analyze_model.py
# This module contains tests for the analyze_model.py functionality.
######



from unittest import result
import os, sys
import pytest
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from proxy.PI_analyzer import PIAnalyzer

# Importing the dataset for evaluation 
splits = {'train': 'data/train-00000-of-00001-9564e8b05b4757ab.parquet', 'test': 'data/test-00000-of-00001-701d16158af87368.parquet'}
df = pd.read_parquet("hf://datasets/deepset/prompt-injections/" + splits["test"])


@pytest.fixture
def pi_analyzer():
    return PIAnalyzer()

class TestPIAnalyzer:
    """
    Test suite for the PIAnalyzer class.
    """

    def test_analyze(self, pi_analyzer):
        miss_count = 0
        results_data = []

        for index, row in df.iterrows():
            result = pi_analyzer.analyze(row['text'])
            assert result is not None

            is_correct = result == row['label']
            if not is_correct:
                miss_count += 1

            results_data.append({
                'index': index,
                'expected': row['label'],
                'predicted': result,
                'correct': is_correct,
                'text_length': len(row['text'])
            })

        # results_df = pd.DataFrame(results_data)
        
        # # Create visualizations
        # fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # # 1. Overall accuracy pie chart
        # accuracy_counts = results_df['correct'].value_counts()
        # axes[0, 0].pie(accuracy_counts.values, labels=['Incorrect', 'Correct'], autopct='%1.1f%%', 
        #                colors=['red', 'green'])
        # axes[0, 0].set_title('Overall Prediction Accuracy')
        
        # # 2. Confusion matrix
        # confusion_data = pd.crosstab(results_df['expected'], results_df['predicted'], 
        #                            rownames=['Expected'], colnames=['Predicted'])
        # sns.heatmap(confusion_data, annot=True, fmt='d', ax=axes[0, 1], cmap='Blues')
        # axes[0, 1].set_title('Confusion Matrix')
        
        # # 3. Accuracy by text length
        # results_df['length_bin'] = pd.cut(results_df['text_length'], bins=5)
        # length_accuracy = results_df.groupby('length_bin')['correct'].mean()
        # length_accuracy.plot(kind='bar', ax=axes[1, 0], color='skyblue')
        # axes[1, 0].set_title('Accuracy by Text Length')
        # axes[1, 0].set_ylabel('Accuracy')
        # axes[1, 0].tick_params(axis='x', rotation=45)
        
        # # 4. Distribution of predictions
        # pred_counts = results_df['predicted'].value_counts()
        # pred_counts.plot(kind='bar', ax=axes[1, 1], color='orange')
        # axes[1, 1].set_title('Distribution of Predictions')
        # axes[1, 1].set_ylabel('Count')
        
        # plt.tight_layout()
        # plt.savefig('pi_analyzer_results.png', dpi=300, bbox_inches='tight')
        # plt.show()
        

        print(f"Total missed: {miss_count} out of {len(df)}")
        print(f"Accuracy: {(len(df) - miss_count) / len(df) * 100:.2f}%")