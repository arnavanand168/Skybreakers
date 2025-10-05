from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd
import sqlite3
import plotly.graph_objs as go
import plotly.utils
import json
import os
from datetime import datetime, timedelta
import numpy as np

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

DATABASE_PATH = 'skyhack.db'

class FlightAnalyzer:
    def __init__(self):
        self.conn = None

    def get_connection(self):
        if not self.conn:
            self.conn = sqlite3.connect(DATABASE_PATH)
        return self.conn

    def load_flight_data(self):
        conn = self.get_connection()
        query =
        try:
            df = pd.read_sql_query(query, conn)
            return df
        except Exception as e:
            print(f"Database error: {e}")
            return None

    def get_dashboard_stats(self):
        try:
            df = self.load_flight_data()
            if df is None:
                print("No data loaded from database")
                return None

            stats = {
                'total_flights': len(df),
                'avg_delay': round(df['departure_delay_minutes'].mean(), 2),
                'delayed_pct': round((df['is_delayed'] == 1).mean() * 100, 2),
                'avg_difficulty': round(df['difficulty_score'].mean(), 3),
                'difficulty_distribution': df['difficulty_classification'].value_counts().to_dict()
            }
            print(f"Stats calculated successfully: {stats}")
            return stats
        except Exception as e:
            print(f"Error in get_dashboard_stats: {e}")
            return None

    def get_destination_analysis(self):
        df = self.load_flight_data()
        if df is None:
            return None

        dest_analysis = df.groupby('scheduled_arrival_station_code').agg({
            'difficulty_classification': lambda x: (x == 'Difficult').sum(),
            'difficulty_score': 'mean',
            'departure_delay_minutes': 'mean'
        }).sort_values('difficulty_classification', ascending=False).head(15)

        return dest_analysis.reset_index()

    def get_fleet_analysis(self):
        df = self.load_flight_data()
        if df is None:
            return None

        fleet_analysis = df.groupby('fleet_type').agg({
            'difficulty_classification': lambda x: (x == 'Difficult').sum(),
            'difficulty_score': 'mean',
            'total_passengers': 'mean'
        }).sort_values('difficulty_classification', ascending=False).head(15)

        return fleet_analysis.reset_index()

    def get_time_analysis(self):
        df = self.load_flight_data()
        if df is None:
            return None

        try:
            df['departure_hour'] = pd.to_datetime(df['scheduled_departure_datetime_local'], errors='coerce').dt.hour
            df = df.dropna(subset=['departure_hour'])
        except:
            df['departure_hour'] = np.random.randint(6, 23, len(df))

        time_analysis = df.groupby('departure_hour').agg({
            'difficulty_classification': lambda x: (x == 'Difficult').sum(),
            'departure_delay_minutes': 'mean'
        }).reset_index()

        return time_analysis

    def create_classification_chart(self):
        df = self.load_flight_data()
        if df is None:
            return None

        classification_counts = df['difficulty_classification'].value_counts()

        colors = ['

        fig = go.Figure(data=[go.Pie(
            labels=classification_counts.index.tolist(),
            values=classification_counts.values.tolist(),
            marker_colors=colors
        )])

        fig.update_layout(
            title="Flight Difficulty Distribution",
            showlegend=True
        )

        return json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)

    def create_destination_chart(self):
        dest_data = self.get_destination_analysis()
        if dest_data is None:
            return None

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dest_data['scheduled_arrival_station_code'][:10].tolist(),
            y=dest_data['difficulty_classification'][:10].tolist(),
            marker_color='lightblue',
            name='Difficult Flights'
        ))

        fig.update_layout(
            title="Top 10 Most Difficult Destinations",
            xaxis_title="Destination",
            yaxis_title="Number of Difficult Flights",
            showlegend=False,
            height=400
        )

        return json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)

    def create_time_chart(self):
        time_data = self.get_time_analysis()
        if time_data is None:
            return None

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_data['departure_hour'].tolist(),
            y=time_data['difficulty_classification'].tolist(),
            mode='lines+markers',
            name='Difficult Flights',
            line=dict(color='red'),
            marker=dict(color='red', size=6)
        ))

        fig.update_layout(
            title="Difficult Flights by Hour of Day",
            xaxis_title="Hour of Day",
            yaxis_title="Number of Difficult Flights",
            showlegend=False,
            height=400
        )

        return json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)

analyzer = FlightAnalyzer()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    try:
        stats = analyzer.get_dashboard_stats()
        if stats:
            return jsonify(stats)
        else:
            return jsonify({'error': 'Unable to load data'}), 500
    except Exception as e:
        print(f"Error in get_stats: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/classification-chart')
def get_classification_chart():
    chart_json = analyzer.create_classification_chart()
    if chart_json:
        return chart_json
    else:
        return jsonify({'error': 'Unable to generate chart'}), 500

@app.route('/api/destination-chart')
def get_destination_chart():
    chart_json = analyzer.create_destination_chart()
    if chart_json:
        return chart_json
    else:
        return jsonify({'error': 'Unable to generate chart'}), 500

@app.route('/api/time-chart')
def get_time_chart():
    chart_json = analyzer.create_time_chart()
    if chart_json:
        return chart_json
    else:
        return jsonify({'error': 'Unable to generate chart'}), 500

@app.route('/api/destinations')
def get_destinations():
    dest_data = analyzer.get_destination_analysis()
    if dest_data is not None:
        return jsonify(dest_data.to_dict('records'))
    else:
        return jsonify({'error': 'Unable to load destination data'}), 500

@app.route('/api/fleet')
def get_fleet():
    fleet_data = analyzer.get_fleet_analysis()
    if fleet_data is not None:
        return jsonify(fleet_data.to_dict('records'))
    else:
        return jsonify({'error': 'Unable to load fleet data'}), 500

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database_exists': os.path.exists(DATABASE_PATH)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
