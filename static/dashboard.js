// Dashboard JavaScript functionality
let safetyData = {};
let regionalChart = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadSafetyData();
    // Refresh data every 5 minutes
    setInterval(loadSafetyData, 300000);
});

// Load safety data from API
async function loadSafetyData() {
    try {
        const response = await fetch('/api/safety-data');
        const data = await response.json();
        safetyData = data;
        updateDashboard();
    } catch (error) {
        console.error('Error loading safety data:', error);
        showError('数据加载失败，请稍后重试');
    }
}

// Update dashboard with new data
function updateDashboard() {
    updateKeyMetrics();
    updateRegionalChart();
    updateDataSources();
    updateRecentUpdates();
    updateLastUpdated();
}

// Update key metrics cards
function updateKeyMetrics() {
    if (safetyData.global_metrics) {
        document.getElementById('totalIncidents').textContent = 
            safetyData.global_metrics.total_incidents || 0;
        
        // Calculate average safety score
        const regionalScores = Object.values(safetyData.regional_data || {})
            .map(region => region.safety_score || 0);
        const avgScore = regionalScores.length > 0 ? 
            Math.round(regionalScores.reduce((a, b) => a + b, 0) / regionalScores.length) : 95;
        
        document.getElementById('avgSafetyScore').textContent = avgScore;
    }
    
    // Update regional data
    if (safetyData.regional_data) {
        const chinaData = safetyData.regional_data.china || {};
        document.getElementById('chinaScore').textContent = chinaData.safety_score || 95;
        document.getElementById('chinaIncidents').textContent = chinaData.incidents || 0;
    }
}

// Create/update regional safety chart
function updateRegionalChart() {
    const ctx = document.getElementById('regionalChart').getContext('2d');
    
    if (regionalChart) {
        regionalChart.destroy();
    }
    
    const regionalData = safetyData.regional_data || {};
    const labels = Object.keys(regionalData).map(region => getRegionName(region));
    const scores = Object.values(regionalData).map(region => region.safety_score || 0);
    
    regionalChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '安全评分',
                data: scores,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 205, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 205, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 80,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '分';
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '安全评分: ' + context.parsed.y + '分';
                        }
                    }
                }
            }
        }
    });
}

// Update data sources status
function updateDataSources() {
    const sourcesContainer = document.getElementById('dataSources');
    const sources = safetyData.data_sources || [];
    
    if (sources.length === 0) {
        sourcesContainer.innerHTML = '<p class="text-muted">暂无数据源信息</p>';
        return;
    }
    
    sourcesContainer.innerHTML = sources.map(source => `
        <div class="source-item ${source.status === 'error' ? 'danger' : source.status === 'warning' ? 'warning' : ''}">
            <h6>${source.name}</h6>
            <small class="text-muted">${source.url}</small>
            <div class="mt-1">
                <span class="badge ${source.status === 'active' ? 'bg-success' : source.status === 'warning' ? 'bg-warning' : 'bg-danger'}">
                    ${source.status === 'active' ? '正常' : source.status === 'warning' ? '警告' : '错误'}
                </span>
            </div>
        </div>
    `).join('');
    
    // Update active sources count
    const activeCount = sources.filter(s => s.status === 'active').length;
    document.getElementById('activeSources').textContent = `${activeCount}/${sources.length}`;
}

// Update recent updates section
function updateRecentUpdates() {
    const updatesContainer = document.getElementById('recentUpdates');
    const updates = safetyData.global_metrics?.recent_updates || [];
    
    if (updates.length === 0) {
        updatesContainer.innerHTML = `
            <div class="update-item">
                <div class="update-content">暂无最新安全动态</div>
            </div>
        `;
        return;
    }
    
    updatesContainer.innerHTML = updates.map(update => `
        <div class="update-item">
            <div class="d-flex justify-content-between align-items-start">
                <div class="update-content">${update.content}</div>
                <small class="update-time">${update.time}</small>
            </div>
        </div>
    `).join('');
}

// Update last updated timestamp
function updateLastUpdated() {
    const lastUpdated = safetyData.last_updated || new Date().toLocaleString('zh-CN');
    document.getElementById('lastUpdated').textContent = lastUpdated;
}

// Utility function to get Chinese region names
function getRegionName(region) {
    const regionNames = {
        'china': '中国',
        'japan': '日本',
        'europe': '欧洲',
        'america': '美洲'
    };
    return regionNames[region] || region;
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-dismissible fade show';
    errorDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.insertBefore(errorDiv, document.body.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.parentNode.removeChild(errorDiv);
        }
    }, 5000);
}

// Manual refresh function
function refreshData() {
    const refreshBtn = document.createElement('button');
    refreshBtn.className = 'btn btn-primary position-fixed';
    refreshBtn.style.cssText = 'bottom: 20px; right: 20px; z-index: 1050;';
    refreshBtn.innerHTML = '🔄 刷新数据';
    refreshBtn.onclick = loadSafetyData;
    document.body.appendChild(refreshBtn);
}

// Add refresh button
refreshData();