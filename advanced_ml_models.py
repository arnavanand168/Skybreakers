

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import xgboost as xgb
import lightgbm as lgb
import joblib
import warnings
warnings.filterwarnings('ignore')

class AdvancedMLModels:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        self.best_model = None

    def prepare_advanced_features(self, data):

        df = data.copy()

        df['departure_hour'] = pd.to_datetime(df['scheduled_departure_datetime_local']).dt.hour
        df['departure_dayofweek'] = pd.to_datetime(df['scheduled_departure_date_local']).dt.dayofweek
        df['departure_month'] = pd.to_datetime(df['scheduled_departure_date_local']).dt.month

        df['is_peak_morning'] = df['departure_hour'].between(6, 9).astype(int)
        df['is_peak_evening'] = df['departure_hour'].between(16, 19).astype(int)
        df['is_weekend'] = df['departure_dayofweek'].isin([5, 6]).astype(int)

        df['seats_per_bag'] = df['total_seats'] / (df['total_bags'] + 1)
        df['passengers_per_bag'] = df['total_passengers'] / (df['total_bags'] + 1)

        df['has_special_needs'] = (df['unique_special_requests'] > 0).astype(int)
        df['high_load_factor'] = (df['load_factor'] > 1.0).astype(int)
        df['tight_schedule'] = (df['ground_time_pressure'] > 2.0).astype(int)

        df['load_x_ground_pressure'] = df['load_factor'] * df['ground_time_pressure']
        df['bags_x_transfer_ratio'] = df['total_bags'] * df['transfer_bag_ratio']
        df['passengers_x_ssr'] = df['total_passengers'] * df['ssr_intensity']

        fleet_mapping = {
            'B787-8': 4, 'B787-9': 4, 'B787-10': 4,
            'B777-300': 4, 'B777-2HD': 4,
            'B767-300': 3, 'B767-400': 3,
            'B757-200': 3, 'B757-300': 3,
            'B737-800': 2, 'B737-900': 2, 'B737-MAX8': 2, 'B737-MAX9': 2,
            'A319-100': 2, 'A320-200': 2, 'A321-2NX': 2,
            'ERJ-175': 1, 'ERJ-170': 1, 'CRJ-200': 1, 'CRJ-550': 1
        }
        df['fleet_complexity_score'] = df['fleet_type'].map(fleet_mapping).fillna(1)

        return df

    def train_xgboost_model(self, X_train, y_train, X_test, y_test):

        print("Training XGBoost model...")

        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 6, 9],
            'learning_rate': [0.01, 0.1, 0.2],
            'subsample': [0.8, 0.9, 1.0]
        }

        xgb_model = xgb.XGBClassifier(random_state=42, eval_metric='mlogloss')
        grid_search = GridSearchCV(
            xgb_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1
        )
        grid_search.fit(X_train, y_train)

        best_xgb = grid_search.best_estimator_
        y_pred = best_xgb.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        self.models['XGBoost'] = {
            'model': best_xgb,
            'accuracy': accuracy,
            'predictions': y_pred,
            'y_test': y_test,
            'best_params': grid_search.best_params_
        }

        self.feature_importance['XGBoost'] = dict(zip(
            X_train.columns, best_xgb.feature_importances_
        ))

        return best_xgb, accuracy

    def train_lightgbm_model(self, X_train, y_train, X_test, y_test):

        print("Training LightGBM model...")

        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 6, 9],
            'learning_rate': [0.01, 0.1, 0.2],
            'num_leaves': [31, 62, 93]
        }

        lgb_model = lgb.LGBMClassifier(random_state=42, verbose=-1)
        grid_search = GridSearchCV(
            lgb_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1
        )
        grid_search.fit(X_train, y_train)

        best_lgb = grid_search.best_estimator_
        y_pred = best_lgb.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        self.models['LightGBM'] = {
            'model': best_lgb,
            'accuracy': accuracy,
            'predictions': y_pred,
            'y_test': y_test,
            'best_params': grid_search.best_params_
        }

        self.feature_importance['LightGBM'] = dict(zip(
            X_train.columns, best_lgb.feature_importances_
        ))

        return best_lgb, accuracy

    def train_ensemble_model(self, X_train, y_train, X_test, y_test):

        print("Training Ensemble model...")

        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        xgb_model = xgb.XGBClassifier(random_state=42, eval_metric='mlogloss')
        lgb_model = lgb.LGBMClassifier(random_state=42, verbose=-1)

        voting_clf = VotingClassifier(
            estimators=[
                ('rf', rf),
                ('xgb', xgb_model),
                ('lgb', lgb_model)
            ],
            voting='soft'
        )

        voting_clf.fit(X_train, y_train)
        y_pred = voting_clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        self.models['Ensemble'] = {
            'model': voting_clf,
            'accuracy': accuracy,
            'predictions': y_pred,
            'y_test': y_test
        }

        return voting_clf, accuracy

    def train_stacking_model(self, X_train, y_train, X_test, y_test):

        print("Training Stacking model...")

        base_models = [
            ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
            ('xgb', xgb.XGBClassifier(random_state=42, eval_metric='mlogloss')),
            ('lgb', lgb.LGBMClassifier(random_state=42, verbose=-1))
        ]

        meta_learner = LogisticRegression(random_state=42)

        stacking_clf = StackingClassifier(
            estimators=base_models,
            final_estimator=meta_learner,
            cv=5
        )

        stacking_clf.fit(X_train, y_train)
        y_pred = stacking_clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        self.models['Stacking'] = {
            'model': stacking_clf,
            'accuracy': accuracy,
            'predictions': y_pred,
            'y_test': y_test
        }

        return stacking_clf, accuracy

    def train_all_models(self, data):

        print("Preparing advanced features...")
        df_advanced = self.prepare_advanced_features(data)

        feature_columns = [
            'load_factor', 'ground_time_pressure', 'transfer_bag_ratio',
            'ssr_intensity', 'is_international', 'has_children', 'has_strollers',
            'fleet_complexity', 'time_complexity', 'total_passengers',
            'total_bags', 'children_count', 'lap_children_count',
            'departure_hour', 'departure_dayofweek', 'departure_month',
            'is_peak_morning', 'is_peak_evening', 'is_weekend',
            'seats_per_bag', 'passengers_per_bag', 'has_special_needs',
            'high_load_factor', 'tight_schedule', 'load_x_ground_pressure',
            'bags_x_transfer_ratio', 'passengers_x_ssr', 'fleet_complexity_score'
        ]

        X = df_advanced[feature_columns].fillna(0)
        y = df_advanced['difficulty_classification'].map({
            'Easy': 0, 'Medium': 1, 'Difficult': 2
        })

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers['standard'] = scaler

        results = {}

        xgb_model, xgb_acc = self.train_xgboost_model(X_train, y_train, X_test, y_test)
        results['XGBoost'] = xgb_acc

        lgb_model, lgb_acc = self.train_lightgbm_model(X_train, y_train, X_test, y_test)
        results['LightGBM'] = lgb_acc

        ensemble_model, ensemble_acc = self.train_ensemble_model(X_train, y_train, X_test, y_test)
        results['Ensemble'] = ensemble_acc

        stacking_model, stacking_acc = self.train_stacking_model(X_train, y_train, X_test, y_test)
        results['Stacking'] = stacking_acc

        best_model_name = max(results, key=results.get)
        self.best_model = self.models[best_model_name]['model']

        print(f"\nModel Performance Summary:")
        for model_name, accuracy in results.items():
            print(f"{model_name}: {accuracy:.4f}")
        print(f"\nBest Model: {best_model_name} with accuracy {results[best_model_name]:.4f}")

        return results, X_test, y_test

    def get_feature_importance_analysis(self):

        importance_df = pd.DataFrame(self.feature_importance).fillna(0)

        importance_df['Average'] = importance_df.mean(axis=1)
        importance_df = importance_df.sort_values('Average', ascending=False)

        return importance_df

    def save_models(self, filepath_prefix="models/"):

        import os
        os.makedirs(filepath_prefix, exist_ok=True)

        for model_name, model_data in self.models.items():
            joblib.dump(model_data['model'], f"{filepath_prefix}{model_name.lower()}_model.pkl")

        joblib.dump(self.scalers['standard'], f"{filepath_prefix}scaler.pkl")

        print(f"Models saved to {filepath_prefix}")

    def load_models(self, filepath_prefix="models/"):

        import os

        if not os.path.exists(filepath_prefix):
            print(f"Models directory {filepath_prefix} not found!")
            return False

        try:
            for model_name in ['XGBoost', 'LightGBM', 'Ensemble', 'Stacking']:
                model_path = f"{filepath_prefix}{model_name.lower()}_model.pkl"
                if os.path.exists(model_path):
                    self.models[model_name] = {
                        'model': joblib.load(model_path)
                    }

            scaler_path = f"{filepath_prefix}scaler.pkl"
            if os.path.exists(scaler_path):
                self.scalers['standard'] = joblib.load(scaler_path)

            print("Models loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
