from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

class AttritionPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoders = {}
        
    def prepare_features(self, data):
        """Prepare features for ML model"""
        features = data.copy()
        
        # Encode categorical variables
        categorical_cols = ['department', 'designation']
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                features[col] = self.label_encoders[col].fit_transform(features[col])
            else:
                features[col] = self.label_encoders[col].transform(features[col])
        
        # Select feature columns
        feature_cols = [
            'base_salary', 'experience_years', 'performance_rating',
            'tasks_completed', 'tasks_assigned', 'quality_score',
            'days_present', 'days_absent', 'overtime_hours',
            'avg_login_hours', 'collaboration_score', 'department', 'designation'
        ]
        
        return features[feature_cols]
    
    def train(self, data):
        """Train the attrition prediction model"""
        X = self.prepare_features(data)
        y = data['attrition_risk']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        accuracy = self.model.score(X_test, y_test)
        return accuracy
    
    def predict_attrition(self, data):
        """Predict attrition risk for employees"""
        X = self.prepare_features(data)
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)[:, 1]
        
        data['predicted_attrition'] = predictions
        data['attrition_probability'] = probabilities
        data['risk_level'] = pd.cut(probabilities, 
                                     bins=[0, 0.3, 0.7, 1.0], 
                                     labels=['Low', 'Medium', 'High'])
        return data
    
    def get_feature_importance(self):
        """Get feature importance from the model"""
        feature_names = [
            'base_salary', 'experience_years', 'performance_rating',
            'tasks_completed', 'tasks_assigned', 'quality_score',
            'days_present', 'days_absent', 'overtime_hours',
            'avg_login_hours', 'collaboration_score', 'department', 'designation'
        ]
        importance = pd.DataFrame({
            'feature': feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        return importance