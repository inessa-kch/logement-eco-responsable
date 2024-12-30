document.addEventListener('DOMContentLoaded', function() {
    const logementButtons = document.querySelectorAll('.custom-button');
    const chartContainerElectricite = document.getElementById('chart_div_electricite');
    const chartContainerEau = document.getElementById('chart_div_eau');
    const chartCtxElectricite = document.getElementById('economiesChartElectricite').getContext('2d');
    const chartCtxEau = document.getElementById('economiesChartEau').getContext('2d');
    let selectedLogementId = null;  // Track the currently selected logement

    // Initialize charts
    const economiesChartElectricite = createBarChart(chartCtxElectricite, "Économies Réalisées - Electricité", 'kWh');
    const economiesChartEau = createBarChart(chartCtxEau, "Économies Réalisées - Eau", 'L');

    // Chart Creation Function
    function createBarChart(ctx, label, defaultUnit) {
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Valeur Consommation',
                        data: [],
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        unit: defaultUnit
                    },
                    {
                        label: 'Valeur Hypothétique',
                        data: [],
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                        unit: defaultUnit
                    }
                ]
            },
            options: {
                scales: {
                    x: { title: { display: true, text: 'Date' }},
                    y: { title: { display: true, text: 'Valeur' }}
                },
                plugins: {
                    legend: {
                        display: true  // Show the legend
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                const unit = tooltipItem.dataset.unit;
                                const value = tooltipItem.raw;
                                return `${value} ${unit}`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Fetch and Update Charts on Logement Selection
    logementButtons.forEach(button => {
        button.addEventListener('click', async function() {
            selectedLogementId = button.getAttribute('data-logement-id');
            fetchAndUpdateCharts(selectedLogementId);
        });
    });

    // Fetch Data for the selected Logement
    async function fetchAndUpdateCharts(logementId) {
        const response = await fetch(`/economies?logement_id=${logementId}&json=true`);
        if (response.ok) {
            const data = await response.json();
            updateChart(economiesChartElectricite, data.economies_data_electricite);
            updateChart(economiesChartEau, data.economies_data_eau);
            chartContainerElectricite.style.display = 'block';
            chartContainerEau.style.display = 'block';
        } else {
            const errorText = await response.text();
            console.error('Error fetching data:', errorText);
            alert('Error fetching data for logement.');
        }
    }

    // Update Chart After Fetching Data
    function updateChart(chart, chartData) {
        chart.data.labels = [];
        chart.data.datasets[0].data = [];
        chart.data.datasets[1].data = [];

        if (chartData.length === 0) {
            console.log('No data available for this chart.');
        } else {
            chartData.sort((a, b) => new Date(a[0]) - new Date(b[0]));

            const labels = chartData.map(item => item[0]);  // Date
            const values = chartData.map(item => item[1]);  // Actual Value
            const hypotheticalValues = chartData.map(item => item[2]);  // Hypothetical Value

            chart.data.labels = labels;
            chart.data.datasets[0].data = values;
            chart.data.datasets[1].data = hypotheticalValues;
        }
        chart.update();
    }

    // Initial draw with empty data
    updateChart(economiesChartElectricite, []);
    updateChart(economiesChartEau, []);
});