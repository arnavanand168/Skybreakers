from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json
import os
from datetime import datetime, timedelta
import numpy as np

app = Flask(__name__)
app.secret_key = 'demo-secret-key-for-united-airlines-dashboard'

class DemoFlightAnalyzer:

    def __init__(self):

        self.flight_data = self.generate_sample_data()

    def generate_sample_data(self):

        np.random.seed(42)

        n_flights = 8155
        destinations = ['LAX', 'SFO', 'YUL', 'YYZ', 'LHR', 'STL', 'YOW', 'DEN', 'SEA', 'ATL', 'ORD', 'JFK']
        fleet_types = ['B738', 'B737', 'B757', 'B767', 'B787', 'A319']
        classifications = ['Easy', 'Medium', 'Difficult'] * (n_flights // 3 + 1)

        data = []
        for i in range(n_flights):

            hour = np.random.randint(6, 23)
            month_day = np.random.randint(1, 31)

            is_difficult = np.random.choice([0, 1], p=[0.3, 0.7])
            if np.random.random() < 0.1:
                is_difficult = 1

            if is_difficult:
                difficulty_score = np.random.uniform(0.7, 1.0)
                classification = 'Difficult'
            else:
                difficulty_score = np.random.uniform(0.0, 0.6)
                classification = np.random.choice(['Easy', 'Medium'], p=[0.6, 0.4])

            dest = np.random.choice(destinations)
            if dest in ['YUL', 'YYZ', 'LHR']:
                difficulty_score += 0.2
                classification = 'Difficult' if difficulty_score > 0.7 else 'Medium'
            elif dest in ['YOW']:
                difficulty_score += 0.3

            flight_data = {
                'company_id': 'UA',
                'flight_number': f'UA{np.random.randint(100, 9999)}',
                'scheduled_departure_date_local': f'2024-10-{month_day:02d}',
                'scheduled_departure_datetime_local': f'2024-10-{month_day:02d} {hour:02d}:{np.random.randint(0, 59):02d}:00',
                'scheduled_departure_station_code': 'ORD',
                'scheduled_arrival_station_code': dest,
                'difficulty_score': min(1.0, difficulty_score),
                'difficulty_classification': classification,
                'load_factor': np.random.uniform(0.4, 1.0),
                'ground_time_pressure': np.random.uniform(0.1, 0.9),
                'transfer_bag_ratio': np.random.uniform(0.0, 0.6),
                'ssr_intensity': np.random.uniform(0.0, 0.4),
                'is_international': 1 if dest in ['YUL', 'YYZ', 'LHR', 'YOW'] else 0,
                'is_delayed': np.random.choice([0, 1], p=[0.65, 0.35]),
                'departure_delay_minutes': max(0, np.random.normal(15, 25)) if np.random.random() < 0.35 else 0,
                'total_passengers': np.random.randint(50, 300),
                'total_bags': np.random.randint(10, 200),
                'fleet_type': np.random.choice(fleet_types),
                'departure_hour': hour
            }
            data.append(flight_data)

        return pd.DataFrame(data)

    def load_flight_data(self):

        return self.flight_data

    def get_dashboard_stats(self):

        df = self.load_flight_data()

        stats = {
            'total_flights': len(df),
            'avg_delay': round(df['departure_delay_minutes'].mean(), 1),
            'delayed_pct': round((df['is_delayed'] == 1).mean() * 100, 1),
            'avg_difficulty': round(df['difficulty_score'].mean(), 3),
            'difficulty_distribution': df['difficulty_classification'].value_counts().to_dict()
        }
        return stats

    def get_destination_analysis(self):

        df = self.load_flight_data()

        dest_analysis = df.groupby('scheduled_arrival_station_code').agg({
            'difficulty_classification': lambda x: (x == 'Difficult').sum(),
            'difficulty_score': 'mean',
            'departure_delay_minutes': 'mean'
        }).sort_values('difficulty_classification', ascending=False).head(15)

        return dest_analysis.reset_index()

    def get_fleet_analysis(self):

        df = self.load_flight_data()

        fleet_analysis = df.groupby('fleet_type').agg({
            'difficulty_classification': lambda x: (x == 'Difficult').sum(),
            'difficulty_score': 'mean',
            'total_passengers': 'mean'
        }).sort_values('difficulty_classification', ascending=False).head(15)

        return fleet_analysis.reset_index()

    def get_time_analysis(self):

        df = self.load_flight_data()

        time_analysis = df.groupby('departure_hour').agg({
            'difficulty_classification': lambda x: (x == 'Difficult').sum(),
            'departure_delay_minutes': 'mean'
        }).reset_index()

        return time_analysis

    def create_classification_chart(self):

        df = self.load_flight_data()
        classification_counts = df['difficulty_classification'].value_counts()

        colors = {'Easy': '
        pie_colors = [colors.get(label, '

        fig = go.Figure(data=[go.Pie(
            labels=classification_counts.index,
            values=classification_counts.values,
            marker_colors=pie_colors,
            textinfo='label+percent',
            textposition='auto'
        )])

        fig.update_layout(
            title="Flight Difficulty Distribution",
            showlegend=True,
            margin=dict(t=50)
        )

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    def create_destination_chart(self):

        dest_data = self.get_destination_analysis()

        fig = go.Figure(data=[go.Bar(
            x=dest_data['scheduled_arrival_station_code'][:10],
            y=dest_data['difficulty_classification'][:10],
            marker_color='lightblue',
            text=dest_data['difficulty_classification'][:10],
            textposition='auto'
        )])

        fig.update_layout(
            title="Top 10 Most Difficult Destinations",
            xaxis_title="Destination",
            yaxis_title="Number of Difficult Flights",
            margin=dict(t=50)
        )

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    def create_time_chart(self):

        time_data = self.get_time_analysis()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_data['departure_hour'],
            y=time_data['difficulty_classification'],
            mode='lines+markers',
            name='Difficult Flights',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))

        fig.add_trace(go.Scatter(
            x=time_data['departure_hour'],
            y=time_data['departure_delay_minutes'],
            mode='lines+markers',
            name='Avg Delay (min)',
            line=dict(color='blue', width=2),
            marker=dict(size=6),
            yaxis='y2'
        ))

        fig.update_layout(
            title="Difficult Flights & Avg Delay by Hour of Day",
            xaxis_title="Hour of Day",
            yaxis_title="Number of Difficult Flights",
            yaxis2=dict(
                title="Average Delay (minutes)",
                overlaying='y',
                side='right'
            ),
            margin=dict(t=50)
        )

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

analyzer = DemoFlightAnalyzer()

@app.route('/')
def dashboard():

    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():

    stats = analyzer.get_dashboard_stats()
    return jsonify(stats)

@app.route('/api/classification-chart')
def get_classification_chart():

    chart_json = analyzer.create_classification_chart()
    return chart_json

@app.route('/api/destination-chart')
def get_destination_chart():

    chart_json = analyzer.create_destination_chart()
    return chart_json

@app.route('/api/time-chart')
def get_time_chart():

    chart_json = analyzer.create_time_chart()
    return chart_json

@app.route('/api/destinations')
def get_destinations():

    dest_data = analyzer.get_destination_analysis()
    return jsonify(dest_data.to_dict('records'))

@app.route('/api/fleet')
def get_fleet():

    fleet_data = analyzer.get_fleet_analysis()
    return jsonify(fleet_data.to_dict('records'))

@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/api/health')
def health_check():

    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database_exists': True,
        'sample_data': True,
        'deployment': 'demo'
    })

@app.route('/demo')
def demo():

    return jsonify({
        'message': 'United Airlines Flight Difficulty Dashboard - Demo Mode',
        'total_flights': 8155,
        'capabilities': [
            'Real-time flight difficulty analysis',
            'Interactive data visualizations',
            'Destination and fleet analysis',
            'Machine learning powered scoring',
            'Mobile responsive design',
            'Ready for cloud deployment'
        ],
        'deployment_status': 'Ready for Vercel, Heroku, Railway, or PythonAnywhere'
    })

if __name__ == '__main__':
    print("🚀 Starting United Airlines Flight Difficulty Dashboard (Demo Mode)")
    print("📊 Serving sample data for demonstration")
    print("🌐 Open http://localhost:5000 to view the dashboard")
    app.run(debug=True, host='0.0.0.0', port=5000)
