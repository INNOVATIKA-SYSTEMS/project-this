// Конфигурация графиков
const chartColors = [
    'rgba(45, 106, 79, 0.7)',   // Глубокий зеленый
    'rgba(64, 145, 108, 0.7)',  // Средний зеленый
    'rgba(82, 183, 136, 0.7)',  // Яркий зеленый
    'rgba(27, 67, 50, 0.7)'     // Тёмно-зеленый
];

// Типы данных и их метки
const dataTypes = {
    sales: {
        label: 'Продажи',
        labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
        ranges: {
            min: 1000,
            max: 50000
        }
    },
    users: {
        label: 'Пользователи',
        labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
        ranges: {
            min: 100,
            max: 5000
        }
    },
    revenue: {
        label: 'Выручка',
        labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
        ranges: {
            min: 5000,
            max: 100000
        }
    },
    conversion: {
        label: 'Конверсия',
        labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
        ranges: {
            min: 1,
            max: 100
        }
    }
};

// Класс для управления графиками
class ChartManager {
    constructor() {
        this.charts = new Map();
        this.chartCounter = 0;
        this.currentDataType = 'sales';
        
        // Инициализация обработчиков событий
        this.initEventListeners();
        
        // Создание первого графика
        this.createDefaultChart();
    }

    initEventListeners() {
        document.getElementById('addChartBtn').addEventListener('click', () => this.addNewChart());
        document.getElementById('updateDataBtn').addEventListener('click', () => this.updateRandomData());
        document.getElementById('dataType').addEventListener('change', (e) => this.handleDataTypeChange(e));
    }

    handleDataTypeChange(e) {
        this.currentDataType = e.target.value;
        this.updateAllCharts();
    }

    createDefaultChart() {
        const ctx = document.getElementById('defaultChart').getContext('2d');
        const defaultChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dataTypes[this.currentDataType].labels,
                datasets: [{
                    label: dataTypes[this.currentDataType].label,
                    data: this.generateRandomData(),
                    backgroundColor: chartColors[0],
                    borderColor: chartColors[0],
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'График 1'
                    }
                }
            }
        });
        this.charts.set('defaultChart', defaultChart);
    }

    addNewChart() {
        this.chartCounter++;
        const chartsContainer = document.getElementById('chartsContainer');
        
        // Создаем новый wrapper для графика
        const chartWrapper = document.createElement('div');
        chartWrapper.className = 'chart-wrapper';
        
        // Создаем canvas для нового графика
        const canvas = document.createElement('canvas');
        const chartId = `chart${this.chartCounter}`;
        canvas.id = chartId;
        chartWrapper.appendChild(canvas);
        chartsContainer.appendChild(chartWrapper);

        // Инициализируем новый график
        const ctx = canvas.getContext('2d');
        const newChart = new Chart(ctx, {
            type: this.getRandomChartType(),
            data: {
                labels: dataTypes[this.currentDataType].labels,
                datasets: [{
                    label: dataTypes[this.currentDataType].label,
                    data: this.generateRandomData(),
                    backgroundColor: chartColors[this.chartCounter % chartColors.length],
                    borderColor: chartColors[this.chartCounter % chartColors.length],
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: `График ${this.chartCounter + 1}`
                    }
                }
            }
        });
        
        this.charts.set(chartId, newChart);
    }

    updateAllCharts() {
        this.charts.forEach(chart => {
            chart.data.datasets.forEach(dataset => {
                dataset.label = dataTypes[this.currentDataType].label;
                dataset.data = this.generateRandomData();
            });
            chart.data.labels = dataTypes[this.currentDataType].labels;
            chart.update();
        });
    }

    updateRandomData() {
        this.charts.forEach(chart => {
            chart.data.datasets.forEach(dataset => {
                dataset.data = this.generateRandomData();
            });
            chart.update();
        });
    }

    generateRandomData() {
        const { min, max } = dataTypes[this.currentDataType].ranges;
        return Array.from({ length: 6 }, () => {
            if (this.currentDataType === 'conversion') {
                return +(Math.random() * (max - min) + min).toFixed(2);
            }
            return Math.floor(Math.random() * (max - min) + min);
        });
    }

    getRandomChartType() {
        const types = ['line', 'bar', 'radar', 'polarArea'];
        return types[Math.floor(Math.random() * types.length)];
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.chartManager = new ChartManager();
});