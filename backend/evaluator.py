"""
Model Evaluator and Benchmark Verification Script
Evaluates the MindGuard AI pipeline against the test dataset split,
calculating Accuracy, Precision, Recall, Macro F1, Weighted F1,
and generating the confusion matrix.
"""

import os
import sys
import json
import pandas as pd

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from backend.model_engine import predictor, CLASSES

def evaluate_corpus(csv_path="data/mental_health_benchmark_corpus.csv", output_json="data/evaluation_results.json"):
    if not os.path.exists(csv_path):
        print(f"[ERROR] Dataset not found at {csv_path}. Please run dataset_generator.py first.")
        return

    print(f"Reading benchmark dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    y_true = df["status"].tolist()
    y_pred = []
    
    print(f"Running inference across {len(df)} statements...")
    for idx, text in enumerate(df["statement"]):
        pred = predictor.predict(text)
        y_pred.append(pred["primary_class"])
        if (idx + 1) % 500 == 0:
            print(f"  Processed {idx + 1}/{len(df)} statements...")
            
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    weighted_f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)
    
    report_dict = classification_report(y_true, y_pred, labels=CLASSES, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=CLASSES).tolist()
    
    print("\n" + "="*65)
    print("MINDGUARD AI EVALUATION RESULTS")
    print("="*65)
    print(f"Overall Accuracy:  {acc*100:.2f}% (Target: >80.00%)")
    print(f"Macro F1-Score:    {macro_f1:.4f}")
    print(f"Weighted F1-Score: {weighted_f1:.4f}")
    print("-" * 65)
    print(f"{'Class':<22} {'Precision':<10} {'Recall':<10} {'F1-Score':<10} {'Support'}")
    print("-" * 65)
    for c in CLASSES:
        metrics = report_dict[c]
        print(f"{c:<22} {metrics['precision']:<10.4f} {metrics['recall']:<10.4f} {metrics['f1-score']:<10.4f} {int(metrics['support'])}")
    print("="*65)
    
    results = {
        "overall_accuracy": round(acc, 4),
        "macro_f1": round(macro_f1, 4),
        "weighted_f1": round(weighted_f1, 4),
        "classification_report": report_dict,
        "confusion_matrix": cm,
        "classes": CLASSES
    }
    
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved evaluation metrics to: {output_json}")
    return results

if __name__ == "__main__":
    evaluate_corpus()
