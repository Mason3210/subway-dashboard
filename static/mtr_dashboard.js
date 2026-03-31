// MTR Dashboard JavaScript
// Vue.js based interactive dashboard

const { createApp } = Vue;

createApp({
    data() {
        return {
            lang: 'zh',
            activeTab: 'overview',
            isRefreshing: false,
            lastUpdated: new Date().toLocaleString('zh-CN'),
            
            // Metrics
            metrics: {
                totalIncidents: 0,
                avgSafetyScore: 95,
                complianceRate: 98,
            },
            
            // Data Sources
            dataSources: {
                total: 200,
                active: 0,
            },
            
            // Updates
            updates: [],
            
            // China Metro
            chinaMetro: [
                { name: '北京地铁', city: '北京', score: 95, status: 'active' },
                { name: '上海地铁', city: '上海', score: 96, status: 'active' },
                { name: '广州地铁', city: '广州', score: 94, status: 'active' },
                { name: '深圳地铁', city: '深圳', score: 95, status: 'active' },
                { name: '成都地铁', city: '成都', score: 93, status: 'active' },
                { name: '杭州地铁', city: '杭州', score: 94, status: 'active' },
                { name: '武汉地铁', city: '武汉', score: 92, status: 'active' },
                { name: '西安地铁', city: '西安', score: 91, status: 'active' },
                { name: '重庆轨道', city: '重庆', score: 90, status: 'active' },
                { name: '天津地铁', city: '天津', score: 89, status: 'active' },
            ],
            
            // International Systems
            internationalSystems: [
                { name: '港铁 MTR', country: '香港', url: 'https://www.mtr.com.hk', score: 98 },
                { name: '东京地铁 Tokyo Metro', country: '日本', url: 'https://www.tokyometro.jp', score: 98 },
                { name: '新加坡地铁 SMRT', country: '新加坡', url: 'https://www.smrtransit.sg', score: 96 },
                { name: '伦敦地铁 TfL', country: '英国', url: 'https://tfl.gov.uk', score: 94 },
                { name: '纽约地铁 MTA', country: '美国', url: 'https://new.mta.info', score: 85 },
            ],
            
            // Government Sources
            government: {
                national: [
                    { name: '交通运输部', url: 'https://www.mot.gov.cn' },
                    { name: '应急管理部', url: 'https://www.mem.gov.cn' },
                    { name: '中国城市轨道交通协会', url: 'http://www.camet.org.cn' },
                ],
                provincial: [
                    { name: '广东省交通运输厅', url: 'https://td.gd.gov.cn' },
                    { name: '江苏省交通运输厅', url: 'https://jtyst.jiangsu.gov.cn' },
                    { name: '浙江省交通运输厅', url: 'https://jtyst.zj.gov.cn' },
                    { name: '山东省交通运输厅', url: 'https://sdygj.gov.cn' },
                    { name: '四川省交通运输厅', url: 'https://jtt.sc.gov.cn' },
                    { name: '湖北省交通运输厅', url: 'https://jtt.hubei.gov.cn' },
                    { name: '湖南省交通运输厅', url: 'https://jtt.hunan.gov.cn' },
                    { name: '河南省交通运输厅', url: 'https://www.hncd.gov.cn' },
                    { name: '安徽省交通运输厅', url: 'https://jtt.ah.gov.cn' },
                ],
                city: [
                    { name: '北京市交通委员会', url: 'https://jw.beijing.gov.cn' },
                    { name: '上海市交通委员会', url: 'https://jw.shanghai.gov.cn' },
                    { name: '广州市交通运输局', url: 'https://www.gz.gov.cn' },
                    { name: '深圳市交通运输局', url: 'https://jtys.sz.gov.cn' },
                    { name: '成都市交通运输局', url: 'https://www.cdjt.gov.cn' },
                    { name: '杭州市交通运输局', url: 'https://hzcb.hangzhou.gov.cn' },
                    { name: '武汉市交通运输局', url: 'https://www.wht.gov.cn' },
                    { name: '西安市交通运输局', url: 'http://jtys.xa.gov.cn' },
                    { name: '重庆市交通局', url: 'https://www.cq.gov.cn' },
                    { name: '天津市交通运输委员会', url: 'https://www.tj.gov.cn' },
                ]
            },
            
            // Social Media
            socialMedia: {
                wechat: 53,
                weibo: 14,
            },
            
            socialMediaAccounts: {
                wechat: [
                    { name: '北京地铁', city: '北京' },
                    { name: '上海地铁', city: '上海' },
                    { name: '广州地铁', city: '广州' },
                    { name: '深圳地铁', city: '深圳' },
                    { name: '成都地铁', city: '成都' },
                    { name: '杭州地铁', city: '杭州' },
                    { name: '武汉地铁', city: '武汉' },
                    { name: '交通运输部', city: '全国' },
                    { name: '应急管理部', city: '全国' },
                ],
                weibo: [
                    { name: '北京地铁', city: '北京' },
                    { name: '上海地铁', city: '上海' },
                    { name: '广州地铁', city: '广州' },
                    { name: '深圳地铁', city: '深圳' },
                    { name: '交通运输部', city: '全国' },
                    { name: '应急管理部', city: '全国' },
                ]
            },
            
            // Charts
            charts: {
                regional: null,
                source: null,
                intl: null
            }
        }
    },
    
    mounted() {
        this.loadData();
        this.initCharts();
        
        // Auto refresh every 5 minutes
        setInterval(() => this.loadData(), 300000);
    },
    
    methods: {
        toggleLang() {
            this.lang = this.lang === 'zh' ? 'en' : 'zh';
            this.updateLanguage();
        },
        
        updateLanguage() {
            // Re-render charts with new language
            this.$nextTick(() => {
                this.initCharts();
            });
        },
        
        async loadData() {
            this.isRefreshing = true;
            
            try {
                const response = await fetch('/api/safety-data');
                const data = await response.json();
                
                // Update metrics
                if (data.global_metrics) {
                    this.metrics.totalIncidents = data.global_metrics.total_incidents || 0;
                    
                    // Calculate average score from regional data
                    const scores = Object.values(data.regional_data || {}).map(r => r.safety_score || 0);
                    if (scores.length > 0) {
                        this.metrics.avgSafetyScore = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
                    }
                }
                
                // Update data sources
                if (data.data_sources) {
                    const active = data.data_sources.filter(s => s.status === 'active').length;
                    this.dataSources.active = active || Math.floor(this.dataSources.total * 0.8);
                }
                
                // Update recent updates
                if (data.global_metrics && data.global_metrics.recent_updates) {
                    this.updates = data.global_metrics.recent_updates;
                }
                
                // Update regional data for charts
                if (data.regional_data) {
                    this.updateRegionalData(data.regional_data);
                }
                
                this.lastUpdated = new Date().toLocaleString(this.lang === 'zh' ? 'zh-CN' : 'en-US');
                
            } catch (error) {
                console.error('Error loading data:', error);
                // Use demo data
                this.useDemoData();
            }
            
            this.isRefreshing = false;
        },
        
        useDemoData() {
            // Demo data when API is not available
            this.metrics = {
                totalIncidents: 12,
                avgSafetyScore: 94,
                complianceRate: 97,
            };
            this.dataSources.active = 165;
            
            this.updates = [
                { time: '2024-01-15', title: '北京地铁启动冬季安全检查', source: '北京地铁', type: '安全' },
                { time: '2024-01-14', title: '交通运输部发布最新安全预警', source: '交通运输部', type: '政策' },
                { time: '2024-01-14', title: '上海地铁1号线运营调整通知', source: '上海地铁', type: '运营' },
                { time: '2024-01-13', title: '广州地铁开展应急演练', source: '广州地铁', type: '演练' },
                { time: '2024-01-12', title: '港铁获得年度安全卓越奖', source: '港铁', type: '荣誉' },
            ];
        },
        
        updateRegionalData(regionalData) {
            // Update China metro scores
            if (regionalData.china) {
                const china = regionalData.china;
                this.chinaMetro.forEach((metro, i) => {
                    if (i < 3) metro.score = china.safety_score || 95;
                });
            }
        },
        
        refreshData() {
            this.loadData();
        },
        
        initCharts() {
            this.initRegionalChart();
            this.initSourceChart();
            this.initIntlChart();
        },
        
        initRegionalChart() {
            const ctx = document.getElementById('regionalChart');
            if (!ctx) return;
            
            if (this.charts.regional) {
                this.charts.regional.destroy();
            }
            
            const labels = this.lang === 'zh' 
                ? ['中国', '日本', '欧洲', '美洲', '香港']
                : ['China', 'Japan', 'Europe', 'America', 'HK'];
            
            const scores = [95, 98, 96, 92, 98];
            const colors = ['#E31837', '#0069C0', '#00875A', '#FF8C00', '#FFD100'];
            
            this.charts.regional = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: this.lang === 'zh' ? '安全评分' : 'Safety Score',
                        data: scores,
                        backgroundColor: colors,
                        borderRadius: 6,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            min: 80,
                            max: 100,
                            ticks: {
                                callback: value => value + (this.lang === 'zh' ? '分' : '')
                            }
                        }
                    }
                }
            });
        },
        
        initSourceChart() {
            const ctx = document.getElementById('sourceChart');
            if (!ctx) return;
            
            if (this.charts.source) {
                this.charts.source.destroy();
            }
            
            const data = {
                labels: this.lang === 'zh'
                    ? ['地铁公司', '政府部门', '社交媒体', '国际']
                    : ['Metro', 'Government', 'Social Media', 'International'],
                datasets: [{
                    data: [52, 116, 67, 5],
                    backgroundColor: ['#E31837', '#0069C0', '#FFD100', '#00875A'],
                }]
            };
            
            this.charts.source = new Chart(ctx, {
                type: 'doughnut',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        },
        
        initIntlChart() {
            const ctx = document.getElementById('intlChart');
            if (!ctx) return;
            
            if (this.charts.intl) {
                this.charts.intl.destroy();
            }
            
            const systems = this.internationalSystems;
            
            this.charts.intl = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: systems.map(s => s.name.split(' ')[0]),
                    datasets: [{
                        label: this.lang === 'zh' ? '安全评分' : 'Safety Score',
                        data: systems.map(s => s.score),
                        backgroundColor: 'rgba(227, 24, 55, 0.2)',
                        borderColor: '#E31837',
                        pointBackgroundColor: '#E31837',
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            min: 80,
                            max: 100,
                            ticks: {
                                stepSize: 5
                            }
                        }
                    }
                }
            });
        },
        
        getTypeBadgeClass(type) {
            const types = {
                '安全': 'bg-success',
                '运营': 'bg-primary',
                '政策': 'bg-info',
                '演练': 'bg-warning',
                '荣誉': 'bg-danger',
                'Safety': 'bg-success',
                'Operation': 'bg-primary',
                'Policy': 'bg-info',
                'Drill': 'bg-warning',
                'Award': 'bg-danger',
            };
            return types[type] || 'bg-secondary';
        },
        
        getScoreClass(score) {
            if (score >= 95) return 'bg-success';
            if (score >= 90) return 'bg-warning';
            return 'bg-danger';
        }
    }
}).mount('#app');