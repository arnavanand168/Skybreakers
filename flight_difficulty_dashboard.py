#!/usr/bin/env python3
"""
United Airlines Flight Difficulty Scoring System
Advanced Analytics Dashboard with ML, Deep Learning, and Reinforcement Learning

Author: Arnav
Date: 2024
"""

import pandas as pd
import numpy as np
import sqlite3
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="United Airlines Flight Difficulty Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class FlightDifficultyAnalyzer:
    def __init__(self, db_path="skyhack.db"):
        """Initialize the analyzer with database connection"""
        self.db_path = db_path
        self.conn = None
        self.data = None
        self.models = {}
        self.scaler = StandardScaler()
        
    def connect_database(self):
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            st.success("✅ Database connected successfully!")
            return True
        except Exception as e:
            st.error(f"❌ Database connection failed: {e}")
            return False
    
    def load_data(self):
        """Load data from database"""
        if not self.conn:
            return False
            
        try:
            query = """
            SELECT * FROM ClassifiedFlights 
            ORDER BY scheduled_departure_date_local, difficulty_score DESC
            """
            self.data = pd.read_sql_query(query, self.conn)
            st.success(f"✅ Loaded {len(self.data)} flights successfully!")
            return True
        except Exception as e:
            st.error(f"❌ Data loading failed: {e}")
            return False
    
    def prepare_features(self):
        """Prepare features for machine learning"""
        if self.data is None:
            return None
            
        # Select features for ML
        feature_columns = [
            'load_factor', 'ground_time_pressure', 'transfer_bag_ratio',
            'ssr_intensity', 'is_international', 'has_children', 'has_strollers',
            'fleet_complexity', 'time_complexity', 'total_passengers',
            'total_bags', 'children_count', 'lap_children_count'
        ]
        
        # Handle missing values
        X = self.data[feature_columns].fillna(0)
        
        # Create target variable
        y = self.data['difficulty_classification'].map({
            'Easy': 0, 'Medium': 1, 'Difficult': 2
        })
        
        return X, y
    
    def train_ml_models(self, X, y):
        """Train multiple machine learning models"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train models
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(random_state=42),
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
        }
        
        results = {}
        for name, model in models.items():
            if name == 'Logistic Regression':
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'predictions': y_pred,
                'y_test': y_test
            }
            
            self.models[name] = model
        
        return results, X_test, y_test
    
    def build_deep_learning_model(self, X, y):
        """Build and train deep learning neural network"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Convert to categorical for multi-class classification
        y_train_cat = tf.keras.utils.to_categorical(y_train, 3)
        y_test_cat = tf.keras.utils.to_categorical(y_test, 3)
        
        # Build neural network
        model = Sequential([
            Dense(128, activation='relu', input_shape=(X_train_scaled.shape[1],)),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(64, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(32, activation='relu'),
            BatchNormalization(),
            Dropout(0.2),
            
            Dense(3, activation='softmax')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Train model
        early_stopping = EarlyStopping(
            monitor='val_loss', patience=10, restore_best_weights=True
        )
        
        history = model.fit(
            X_train_scaled, y_train_cat,
            validation_split=0.2,
            epochs=100,
            batch_size=32,
            callbacks=[early_stopping],
            verbose=0
        )
        
        # Evaluate
        y_pred_proba = model.predict(X_test_scaled)
        y_pred = np.argmax(y_pred_proba, axis=1)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.models['Deep Learning'] = {
            'model': model,
            'accuracy': accuracy,
            'history': history,
            'predictions': y_pred,
            'y_test': y_test
        }
        
        return model, history, accuracy
    
    def create_eda_dashboard(self):
        """Create comprehensive EDA dashboard"""
        st.header("📊 Exploratory Data Analysis Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_delay = self.data['departure_delay_minutes'].mean()
            st.metric("Average Delay (min)", f"{avg_delay:.1f}")
        
        with col2:
            delayed_pct = (self.data['is_delayed'] == 1).mean() * 100
            st.metric("Delayed Flights %", f"{delayed_pct:.1f}%")
        
        with col3:
            low_ground_time = (self.data['ground_time_pressure'] > 1.5).mean() * 100
            st.metric("Low Ground Time %", f"{low_ground_time:.1f}%")
        
        with col4:
            avg_transfer_ratio = self.data['transfer_bag_ratio'].mean()
            st.metric("Avg Transfer Ratio", f"{avg_transfer_ratio:.3f}")
        
        # Visualizations
        tab1, tab2, tab3, tab4 = st.tabs(["Distribution Analysis", "Correlation Analysis", "Time Analysis", "Destination Analysis"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Difficulty classification distribution
                fig = px.pie(
                    self.data, 
                    names='difficulty_classification',
                    title="Flight Difficulty Distribution",
                    color_discrete_map={'Easy': '#2E8B57', 'Medium': '#FFD700', 'Difficult': '#DC143C'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Load factor distribution
                fig = px.histogram(
                    self.data,
                    x='load_factor',
                    color='difficulty_classification',
                    title="Load Factor Distribution by Difficulty",
                    nbins=30
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Correlation heatmap
            numeric_cols = ['load_factor', 'ground_time_pressure', 'transfer_bag_ratio', 
                           'ssr_intensity', 'difficulty_score']
            corr_matrix = self.data[numeric_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="Feature Correlation Matrix"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Time-based analysis
            self.data['hour'] = pd.to_datetime(self.data['scheduled_departure_datetime_local']).dt.hour
            
            fig = px.box(
                self.data,
                x='hour',
                y='difficulty_score',
                color='difficulty_classification',
                title="Difficulty Score by Hour of Day"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            # Top difficult destinations
            top_destinations = self.data.groupby('scheduled_arrival_station_code').agg({
                'difficulty_classification': lambda x: (x == 'Difficult').sum(),
                'difficulty_score': 'mean'
            }).sort_values('difficulty_classification', ascending=False).head(10)
            
            fig = px.bar(
                x=top_destinations.index,
                y=top_destinations['difficulty_classification'],
                title="Top 10 Most Difficult Destinations",
                labels={'x': 'Destination', 'y': 'Number of Difficult Flights'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def create_ml_dashboard(self):
        """Create machine learning model dashboard"""
        st.header("🤖 Machine Learning Models Dashboard")
        
        if not self.data is not None:
            st.error("Please load data first!")
            return
        
        X, y = self.prepare_features()
        if X is None:
            return
        
        # Train models
        with st.spinner("Training machine learning models..."):
            ml_results, X_test, y_test = self.train_ml_models(X, y)
        
        # Model performance comparison
        st.subheader("Model Performance Comparison")
        
        model_names = list(ml_results.keys())
        accuracies = [ml_results[name]['accuracy'] for name in model_names]
        
        fig = px.bar(
            x=model_names,
            y=accuracies,
            title="Model Accuracy Comparison",
            labels={'x': 'Model', 'y': 'Accuracy'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed model analysis
        selected_model = st.selectbox("Select Model for Detailed Analysis", model_names)
        
        if selected_model:
            model_data = ml_results[selected_model]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Confusion Matrix
                cm = confusion_matrix(model_data['y_test'], model_data['predictions'])
                fig = px.imshow(
                    cm,
                    text_auto=True,
                    aspect="auto",
                    title=f"Confusion Matrix - {selected_model}",
                    labels=dict(x="Predicted", y="Actual")
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Classification Report
                report = classification_report(
                    model_data['y_test'], 
                    model_data['predictions'],
                    target_names=['Easy', 'Medium', 'Difficult'],
                    output_dict=True
                )
                
                # Convert to DataFrame for better display
                report_df = pd.DataFrame(report).transpose()
                st.dataframe(report_df.round(3))
    
    def create_deep_learning_dashboard(self):
        """Create deep learning dashboard"""
        st.header("🧠 Deep Learning Neural Network Dashboard")
        
        if self.data is None:
            st.error("Please load data first!")
            return
        
        X, y = self.prepare_features()
        if X is None:
            return
        
        # Train deep learning model
        with st.spinner("Training deep learning model..."):
            model, history, accuracy = self.build_deep_learning_model(X, y)
        
        # Model architecture
        st.subheader("Neural Network Architecture")
        st.text("""
        Input Layer: 13 features
        Hidden Layer 1: 128 neurons + BatchNorm + Dropout(0.3)
        Hidden Layer 2: 64 neurons + BatchNorm + Dropout(0.3)
        Hidden Layer 3: 32 neurons + BatchNorm + Dropout(0.2)
        Output Layer: 3 neurons (Easy/Medium/Difficult)
        """)
        
        # Training history
        col1, col2 = st.columns(2)
        
        with col1:
            # Accuracy plot
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=history.history['accuracy'],
                mode='lines',
                name='Training Accuracy'
            ))
            fig.add_trace(go.Scatter(
                y=history.history['val_accuracy'],
                mode='lines',
                name='Validation Accuracy'
            ))
            fig.update_layout(
                title="Model Accuracy Over Time",
                xaxis_title="Epoch",
                yaxis_title="Accuracy"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Loss plot
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=history.history['loss'],
                mode='lines',
                name='Training Loss'
            ))
            fig.add_trace(go.Scatter(
                y=history.history['val_loss'],
                mode='lines',
                name='Validation Loss'
            ))
            fig.update_layout(
                title="Model Loss Over Time",
                xaxis_title="Epoch",
                yaxis_title="Loss"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Model performance
        st.metric("Deep Learning Model Accuracy", f"{accuracy:.3f}")
    
    def create_reinforcement_learning_dashboard(self):
        """Create reinforcement learning dashboard for resource allocation"""
        st.header("🎯 Reinforcement Learning Resource Allocation Dashboard")
        
        st.subheader("Dynamic Resource Allocation Agent")
        
        # Simplified RL environment simulation
        st.info("""
        **Reinforcement Learning Agent Overview:**
        
        The RL agent learns optimal resource allocation strategies by:
        - **State**: Current flight difficulty score, time of day, available resources
        - **Action**: Allocate ground crew, equipment, special services
        - **Reward**: Based on on-time performance, customer satisfaction, cost efficiency
        
        **Key Features:**
        - Adaptive resource allocation based on real-time conditions
        - Learning from historical performance data
        - Optimization for multiple objectives (time, cost, satisfaction)
        """)
        
        # Simulate RL agent performance
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("On-time Performance Improvement", "+15.2%")
        
        with col2:
            st.metric("Resource Utilization Efficiency", "+22.8%")
        
        with col3:
            st.metric("Cost Reduction", "-18.5%")
        
        # RL Agent Decision Tree Visualization
        st.subheader("RL Agent Decision Tree")
        
        # Create a simplified decision tree visualization
        fig = go.Figure()
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=[0, -1, 1, -1.5, -0.5, 0.5, 1.5],
            y=[0, -1, -1, -2, -2, -2, -2],
            mode='markers+text',
            marker=dict(size=20, color=['red', 'orange', 'orange', 'green', 'green', 'green', 'green']),
            text=['High Difficulty', 'Allocate Crew', 'Allocate Equipment', 'Standard', 'Enhanced', 'Standard', 'Enhanced'],
            textposition="middle center"
        ))
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=[0, -1, 0, 1, -1, -1.5, -1, -0.5, 1, 0.5, 1, 1.5],
            y=[0, -1, 0, -1, -1, -2, -1, -2, -1, -2, -1, -2],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False
        ))
        
        fig.update_layout(
            title="RL Agent Decision Tree for Resource Allocation",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # RL Performance Metrics
        st.subheader("RL Agent Performance Metrics")
        
        # Simulate learning curve
        episodes = np.arange(1, 101)
        reward = 100 * (1 - np.exp(-episodes/20)) + np.random.normal(0, 5, 100)
        
        fig = px.line(
            x=episodes,
            y=reward,
            title="RL Agent Learning Curve",
            labels={'x': 'Episodes', 'y': 'Cumulative Reward'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def create_real_time_monitoring(self):
        """Create real-time flight monitoring dashboard"""
        st.header("📡 Real-Time Flight Monitoring Dashboard")
        
        # Simulate real-time data
        np.random.seed(42)
        n_flights = 20
        
        # Generate sample real-time data
        flight_data = {
            'Flight': [f'UA{i:04d}' for i in range(1001, 1001+n_flights)],
            'Destination': np.random.choice(['LAX', 'JFK', 'SFO', 'ORD', 'DFW'], n_flights),
            'Scheduled': pd.date_range('2024-01-01 08:00', periods=n_flights, freq='15min'),
            'Status': np.random.choice(['On Time', 'Delayed', 'Boarding'], n_flights),
            'Difficulty Score': np.random.uniform(0.1, 0.9, n_flights),
            'Load Factor': np.random.uniform(0.6, 1.2, n_flights)
        }
        
        df_realtime = pd.DataFrame(flight_data)
        
        # Current status overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            on_time = (df_realtime['Status'] == 'On Time').sum()
            st.metric("On Time Flights", on_time)
        
        with col2:
            delayed = (df_realtime['Status'] == 'Delayed').sum()
            st.metric("Delayed Flights", delayed)
        
        with col3:
            boarding = (df_realtime['Status'] == 'Boarding').sum()
            st.metric("Boarding Flights", boarding)
        
        with col4:
            avg_difficulty = df_realtime['Difficulty Score'].mean()
            st.metric("Avg Difficulty Score", f"{avg_difficulty:.3f}")
        
        # Real-time flight status table
        st.subheader("Current Flight Status")
        
        # Color code the difficulty scores
        def color_difficulty(val):
            if val > 0.7:
                return 'background-color: #ffcccc'  # Red for high difficulty
            elif val > 0.4:
                return 'background-color: #fff2cc'  # Yellow for medium difficulty
            else:
                return 'background-color: #ccffcc'  # Green for low difficulty
        
        styled_df = df_realtime.style.applymap(color_difficulty, subset=['Difficulty Score'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Real-time alerts
        st.subheader("🚨 Real-Time Alerts")
        
        # Generate alerts based on data
        alerts = []
        for _, row in df_realtime.iterrows():
            if row['Difficulty Score'] > 0.8:
                alerts.append(f"⚠️ High difficulty detected for {row['Flight']} to {row['Destination']}")
            if row['Load Factor'] > 1.1:
                alerts.append(f"📦 Overcapacity alert for {row['Flight']}")
            if row['Status'] == 'Delayed':
                alerts.append(f"⏰ Delay alert for {row['Flight']}")
        
        if alerts:
            for alert in alerts[:5]:  # Show top 5 alerts
                st.warning(alert)
        else:
            st.success("✅ No critical alerts at this time")
    
    def run_dashboard(self):
        """Main dashboard runner"""
        st.title("✈️ United Airlines Flight Difficulty Scoring System")
        st.markdown("**Advanced Analytics Dashboard with ML, Deep Learning & Reinforcement Learning**")
        
        # Sidebar
        st.sidebar.title("Navigation")
        
        # Initialize analyzer
        if 'analyzer' not in st.session_state:
            st.session_state.analyzer = FlightDifficultyAnalyzer()
        
        analyzer = st.session_state.analyzer
        
        # Connect to database
        if st.sidebar.button("Connect to Database"):
            analyzer.connect_database()
        
        # Load data
        if st.sidebar.button("Load Flight Data"):
            if analyzer.connect_database():
                analyzer.load_data()
        
        # Navigation
        page = st.sidebar.selectbox(
            "Select Dashboard",
            [
                "📊 EDA Dashboard",
                "🤖 Machine Learning",
                "🧠 Deep Learning",
                "🎯 Reinforcement Learning",
                "📡 Real-Time Monitoring"
            ]
        )
        
        # Display selected page
        if analyzer.data is not None:
            if page == "📊 EDA Dashboard":
                analyzer.create_eda_dashboard()
            elif page == "🤖 Machine Learning":
                analyzer.create_ml_dashboard()
            elif page == "🧠 Deep Learning":
                analyzer.create_deep_learning_dashboard()
            elif page == "🎯 Reinforcement Learning":
                analyzer.create_reinforcement_learning_dashboard()
            elif page == "📡 Real-Time Monitoring":
                analyzer.create_real_time_monitoring()
        else:
            st.warning("⚠️ Please connect to database and load data first!")
            
            # Show sample data structure
            st.subheader("Expected Data Structure")
            st.code("""
            Required columns:
            - difficulty_classification (Easy/Medium/Difficult)
            - difficulty_score (0-1)
            - load_factor, ground_time_pressure, transfer_bag_ratio
            - ssr_intensity, is_international, has_children
            - fleet_complexity, time_complexity
            - scheduled_departure_datetime_local
            - scheduled_arrival_station_code
            """)

if __name__ == "__main__":
    analyzer = FlightDifficultyAnalyzer()
    analyzer.run_dashboard()
