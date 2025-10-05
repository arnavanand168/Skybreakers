class FlightDashboard {
    constructor() {
        this.dataLoaded = false;
        this.charts = {};
        this.init();
    }

    init() {
        console.log('Initializing Flight Dashboard...');
        this.loadDashboardData();
        this.setupEventListeners();
    }

    setupEventListeners() {
        setInterval(() => {
            this.loadDashboardData();
            this.updateLastRefreshTime();
        }, 30000);

        const refreshBtn = document.querySelector('#refreshBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.loadDashboardData();
                this.showSuccess('Data refreshed successfully!');
            });
        }
    }

    async loadDashboardData() {
        try {
            this.showLoading();
            
            const statsResponse = await fetch('/api/stats');
            const stats = await statsResponse.json();
            
            if (stats.error) {
                throw new Error(stats.error);
            }
            
            this.updateStats(stats);
            
            await new Promise(resolve => setTimeout(resolve, 200));
            
            console.log('Loading charts sequentially...');
            
            await this.loadClassificationChart();
            await new Promise(resolve => setTimeout(resolve, 100));
            
            await this.loadDestinationChart();
            await new Promise(resolve => setTimeout(resolve, 100));
            
            await this.loadTimeChart();
            await new Promise(resolve => setTimeout(resolve, 100));
            
            await this.loadDestinationTable();
            await this.loadFleetTable();
            
            this.dataLoaded = true;
            this.hideLoading();
            
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showError('Failed to load dashboard data: ' + error.message);
            this.hideLoading();
        }
    }

    updateStats(stats) {
        document.getElementById('totalFlights').textContent = stats.total_flights.toLocaleString();
        document.getElementById('avgDelay').textContent = stats.avg_delay + ' min';
        document.getElementById('delayedPct').textContent = stats.delayed_pct + '%';
        document.getElementById('avgDifficulty').textContent = stats.avg_difficulty;
    }

    async loadClassificationChart() {
        try {
            const response = await fetch('/api/classification-chart');
            const chartData = await response.json();
            
            if (chartData.error) {
                throw new Error(chartData.error);
            }
            
            const chartContainer = document.getElementById('classificationChart');
            Plotly.newPlot(chartContainer, chartData.data, chartData.layout, {
                responsive: true,
                displayModeBar: false
            });
            
        } catch (error) {
            console.error('Error loading classification chart:', error);
            this.showChartError('classificationChart');
        }
    }

    async loadDestinationChart() {
        try {
            console.log('Loading destination chart...');
            
            if (typeof Plotly === 'undefined') {
                throw new Error('Plotly library not loaded');
            }
            
            const response = await fetch('/api/destination-chart');
            const chartData = await response.json();
            
            console.log('Destination chart data:', chartData);
            
            if (chartData.error) {
                throw new Error(chartData.error);
            }
            
            const chartContainer = document.getElementById('destinationChart');
            console.log('Destination chart container:', chartContainer);
            
            if (!chartContainer) {
                throw new Error('Destination chart container not found');
            }
            
            try {
                const config = {
                    responsive: true,
                    displayModeBar: false,
                    staticPlot: false
                };
                
                Plotly.newPlot(chartContainer, chartData.data, chartData.layout, config);
                console.log('Destination chart loaded successfully with config');
                
            } catch (plotlyError) {
                console.warn('First attempt failed, trying simplified config:', plotlyError);
                
                const simpleConfig = {
                    responsive: true,
                    displayModeBar: false
                };
                
                Plotly.newPlot(chartContainer, chartData.data, chartData.layout, simpleConfig);
                console.log('Destination chart loaded successfully with simple config');
            }
            
        } catch (error) {
            console.error('Error loading destination chart:', error);
            this.showChartError('destinationChart');
        }
    }

    async loadTimeChart() {
        try {
            console.log('Loading time chart...');
            
            if (typeof Plotly === 'undefined') {
                throw new Error('Plotly library not loaded');
            }
            
            const response = await fetch('/api/time-chart');
            const chartData = await response.json();
            
            console.log('Time chart data:', chartData);
            
            if (chartData.error) {
                throw new Error(chartData.error);
            }
            
            const chartContainer = document.getElementById('timeChart');
            console.log('Time chart container:', chartContainer);
            
            if (!chartContainer) {
                throw new Error('Time chart container not found');
            }
            
            try {
                const config = {
                    responsive: true,
                    displayModeBar: false,
                    staticPlot: false
                };
                
                Plotly.newPlot(chartContainer, chartData.data, chartData.layout, config);
                console.log('Time chart loaded successfully with config');
                
            } catch (plotlyError) {
                console.warn('First attempt failed, trying simplified config:', plotlyError);
                
                const simpleConfig = {
                    responsive: true,
                    displayModeBar: false
                };
                
                Plotly.newPlot(chartContainer, chartData.data, chartData.layout, simpleConfig);
                console.log('Time chart loaded successfully with simple config');
            }
            
        } catch (error) {
            console.error('Error loading time chart:', error);
            this.showChartError('timeChart');
        }
    }

    async loadDestinationTable() {
        try {
            const response = await fetch('/api/destinations');
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            const tbody = document.querySelector('#destinationTable tbody');
            tbody.innerHTML = '';
            
            data.slice(0, 10).forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${row.scheduled_arrival_station_code}</strong></td>
                    <td><span class="badge bg-danger">${row.difficulty_classification}</span></td>
                    <td>${row.difficulty_score.toFixed(3)}</td>
                    <td>${row.departure_delay_minutes.toFixed(1)} min</td>
                `;
                tbody.appendChild(tr);
            });
            
        } catch (error) {
            console.error('Error loading destination table:', error);
            this.showTableError('destinationTable');
        }
    }

    async loadFleetTable() {
        try {
            const response = await fetch('/api/fleet');
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            const tbody = document.querySelector('#fleetTable tbody');
            tbody.innerHTML = '';
            
            data.slice(0, 10).forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${row.fleet_type}</strong></td>
                    <td><span class="badge bg-warning">${row.difficulty_classification}</span></td>
                    <td>${row.difficulty_score.toFixed(3)}</td>
                    <td>${row.total_passengers.toFixed(0)}</td>
                `;
                tbody.appendChild(tr);
            });
            
        } catch (error) {
            console.error('Error loading fleet table:', error);
            this.showTableError('fleetTable');
        }
    }

    showChartError(containerId) {
        const container = document.getElementById(containerId);
        container.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
                <p>Unable to load chart data</p>
                <button class="btn btn-sm btn-outline-primary" onclick="dashboard.loadDashboardData()">
                    <i class="fas fa-refresh"></i> Retry
                </button>
            </div>
        `;
    }

    showTableError(tableId) {
        const tbody = document.querySelector(`#${tableId} tbody`);
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center text-muted py-3">
                    <i class="fas fa-exclamation-triangle"></i> Unable to load data
                </td>
            </tr>
        `;
    }

    showLoading() {
        document.getElementById('loadingSpinner').style.display = 'block';
    }

    hideLoading() {
        document.getElementById('loadingSpinner').style.display = 'none';
    }

    updateLastRefreshTime() {
        const now = new Date();
        const element = document.getElementById('lastUpdate');
        if (element) {
            element.textContent = `Last updated: ${now.toLocaleTimeString()}`;
        }
    }

    showSuccess(message) {
        this.showToast(message, 'success');
    }

    showError(message) {
        this.showToast(message, 'danger');
    }

    showToast(message, type = 'info') {
        const toastContainer = document.querySelector('.toast-container') || this.createToastContainer();
        
        const toastId = 'toast-' + Date.now();
        const toast = document.createElement('div');
        toast.id = toastId;
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                        data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    createToastContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(container);
        return container;
    }
}

function showStatus() {
    const modal = new bootstrap.Modal(document.getElementById('statusModal'));
    modal.show();
    
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            const content = document.getElementById('statusContent');
            content.innerHTML = `
                <div class="row text-center">
                    <div class="col-md-4">
                        <div class="border rounded p-3">
                            <h5 class="${data.status === 'healthy' ? 'text-success' : 'text-danger'}">
                                <i class="fas fa-heartbeat"></i> System Status
                            </h5>
                            <p class="h4 ${data.status === 'healthy' ? 'text-success' : 'text-danger'}">
                                ${data.status.charAt(0).toUpperCase() + data.status.slice(1)}
                            </p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="border rounded p-3">
                            <h5 class="text-info">
                                <i class="fas fa-clock"></i> Timestamp
                            </h5>
                            <p class="small">${new Date(data.timestamp).toLocaleString()}</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="border rounded p-3">
                            <h5 class="${data.database_exists ? 'text-success' : 'text-danger'}">
                                <i class="fas fa-database"></i> Database
                            </h5>
                            <p class="h4 ${data.database_exists ? 'text-success' : 'text-danger'}">
                                ${data.database_exists ? 'Connected' : 'Missing'}
                            </p>
                        </div>
                    </div>
                </div>
            `;
        })
        .catch(error => {
            console.error('Error loading status:', error);
            document.getElementById('statusContent').innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i>
                    Unable to load status information: ${error.message}
                </div>
            `;
        });
}

let dashboard;
document.addEventListener('DOMContentLoaded', function() {
    dashboard = new FlightDashboard();
});

function toggleFullscreen(chartId) {
    const chart = document.getElementById(chartId);
    if (chart.requestFullscreen) {
        chart.requestFullscreen();
    } else if (chart.webkitRequestFullscreen) {
        chart.webkitRequestFullscreen();
    } else if (chart.msRequestFullscreen) {
        chart.msRequestFullscreen();
    }
}

function exportChart(chartId) {
    const chart = document.getElementById(chartId);
    Plotly.downloadImage(chart, {
        format: 'png',
        width: 1200,
        height: 600,
        filename: `flight-difficulty-chart-${new Date().getTime()}`
    });
}
