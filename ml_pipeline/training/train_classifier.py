"""
Train Problem Classifier
========================

Goal: Build ML model that predicts which data quality problems exist in a column.

Input: Column features (35+ numeric features)
Output: 5 binary predictions (has_duplicates, has_missing, etc.)

This is a MULTI-LABEL classification problem.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
import joblib
from pathlib import Path
import json
from datetime import datetime


class ProblemClassifier:
    """
    Multi-label classifier for data quality problems.
    
    Uses Random Forest (simple, interpretable, works well for tabular data).
    """
    
    def __init__(self):
        self.models = {}  # One model per problem type
        self.feature_columns = None
        self.problem_types = [
            'has_duplicates',
            'has_missing',
            'has_outliers',
            'has_format_issue',
            'has_type_issue'
        ]
        
    def prepare_data(self, feature_df):
        """
        Prepare features and labels for training.
        
        Args:
            feature_df: DataFrame with features and labels
            
        Returns:
            X: Feature matrix
            y: Label dictionary {problem_type: labels}
        """
        # Separate features and labels
        label_columns = self.problem_types
        self.feature_columns = [col for col in feature_df.columns 
                               if col not in label_columns + ['filename', 'column_name']]
        
        X = feature_df[self.feature_columns]
        y = {ptype: feature_df[ptype] for ptype in self.problem_types}
        
        return X, y
    
    def train(self, X_train, y_train):
        """
        Train one classifier per problem type.
        
        Why separate models?
        - Each problem has different patterns
        - Easier to interpret
        - Can optimize each independently
        """
        print("\n🤖 Training Problem Classifiers")
        print("=" * 60)
        
        for problem_type in self.problem_types:
            print(f"\nTraining: {problem_type}...")
            
            # Create Random Forest classifier
            # n_estimators: number of trees (more = better but slower)
            # max_depth: prevents overfitting
            # class_weight: handles imbalanced data
            clf = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                class_weight='balanced',  # Important: most columns won't have problems
                random_state=42,
                n_jobs=-1  # Use all CPU cores
            )
            
            # Train
            clf.fit(X_train, y_train[problem_type])
            
            # Save model
            self.models[problem_type] = clf
            
            # Show class distribution
            unique, counts = np.unique(y_train[problem_type], return_counts=True)
            print(f"  Class distribution: {dict(zip(unique, counts))}")
            print(f"  ✅ Trained")
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate all models on test set.
        
        Returns:
            results: Dict with metrics per problem type
        """
        print("\n📊 Evaluation Results")
        print("=" * 60)
        
        results = {}
        
        for problem_type in self.problem_types:
            print(f"\n{problem_type}:")
            print("-" * 40)
            
            # Predict
            y_pred = self.models[problem_type].predict(X_test)
            
            # Calculate metrics
            report = classification_report(y_test[problem_type], y_pred, 
                                          output_dict=True, zero_division=0)
            
            f1 = f1_score(y_test[problem_type], y_pred, average='binary', zero_division=0)
            
            # Store results
            results[problem_type] = {
                'f1_score': f1,
                'precision': report['1']['precision'] if '1' in report else 0,
                'recall': report['1']['recall'] if '1' in report else 0,
                'support': report['1']['support'] if '1' in report else 0
            }
            
            # Print
            print(f"  F1 Score: {f1:.3f}")
            print(f"  Precision: {results[problem_type]['precision']:.3f}")
            print(f"  Recall: {results[problem_type]['recall']:.3f}")
        
        # Overall F1 (average across all problem types)
        avg_f1 = np.mean([r['f1_score'] for r in results.values()])
        print(f"\n{'='*60}")
        print(f"📈 Average F1 Score: {avg_f1:.3f}")
        print(f"{'='*60}")
        
        return results
    
    def save_models(self, output_dir='../../models'):
        """
        Save trained models to disk.
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save each model
        for problem_type, model in self.models.items():
            model_path = output_path / f'{problem_type}_classifier.joblib'
            joblib.dump(model, model_path)
            print(f"✅ Saved: {model_path}")
        
        # Save feature columns (needed for prediction)
        metadata = {
            'feature_columns': self.feature_columns,
            'problem_types': self.problem_types,
            'trained_at': datetime.now().isoformat()
        }
        
        metadata_path = output_path / 'classifier_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Saved metadata: {metadata_path}")


# Training script
if __name__ == "__main__":
    print("🚀 Starting Training Pipeline")
    print("=" * 60)
    
    # 1. Load feature dataset
    print("\n1️⃣ Loading feature dataset...")
    feature_df = pd.read_csv('../../data/processed/feature_dataset.csv')
    print(f"   Shape: {feature_df.shape}")
    
    # 2. Initialize classifier
    classifier = ProblemClassifier()
    
    # 3. Prepare data
    print("\n2️⃣ Preparing data...")
    X, y = classifier.prepare_data(feature_df)
    print(f"   Features: {X.shape}")
    print(f"   Labels: {len(y)} problem types")
    
    # 4. Train/test split
    print("\n3️⃣ Creating train/test split (80/20)...")
    X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)
    
    y_train = {}
    y_test = {}
    for ptype in classifier.problem_types:
        y_train[ptype], y_test[ptype] = train_test_split(
            y[ptype], test_size=0.2, random_state=42
        )
    
    print(f"   Train: {X_train.shape}")
    print(f"   Test: {X_test.shape}")
    
    # 5. Train models
    print("\n4️⃣ Training models...")
    classifier.train(X_train, y_train)
    
    # 6. Evaluate
    print("\n5️⃣ Evaluating models...")
    results = classifier.evaluate(X_test, y_test)
    
    # 7. Save models
    print("\n6️⃣ Saving models...")
    classifier.save_models()
    
    print("\n" + "=" * 60)
    print("✅ Training Complete!")
    print("=" * 60)