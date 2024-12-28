document.addEventListener('DOMContentLoaded', function() {
    const logementButtons = document.querySelectorAll('.custom-button');
    const chartsContainer = document.querySelector('.charts-container');
    const factureForm = document.getElementById('factureForm');
    let selectedLogementId = null;  // Track the currently selected logement

    // Initialize charts
    const internetCtx = document.getElementById('internetChart').getContext('2d');
    const internetChart = createLineChart(internetCtx, "Consommation d'Internet", 'Go');

    const electricityCtx = document.getElementById('electricityChart').getContext('2d');
    const electricityChart = createLineChart(electricityCtx, "Consommation d'Electricité", 'kWh');

    const waterCtx = document.getElementById('waterChart').getContext('2d');
    const waterChart = createLineChart(waterCtx, "Consommation d'Eau", 'L');

    const pieCtx = document.getElementById('facturePieChart').getContext('2d');
    const facturePieChart = createPieChart(pieCtx);

    // Chart Creation Functions
    function createLineChart(ctx, label, defaultUnit) {
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: label,  // Dataset label (will not appear if legend is hidden)
                    data: [],
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: false,
                    unit: defaultUnit
                }]
            },
            options: {
                scales: {
                    x: { title: { display: true, text: 'Date' }},
                    y: { title: { display: true, text: 'Consommation' }}
                },
                plugins: {
                    legend: {
                        display: false  // Hide the legend to avoid duplication
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
    

    function createPieChart(ctx) {
        return new Chart(ctx, {
            type: 'pie',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)', 
                        'rgba(255, 99, 132, 0.2)', 
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)', 
                        'rgba(255, 99, 132, 1)', 
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' },
                    title: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                const value = tooltipItem.raw;
                                return `${tooltipItem.label}: €${value.toFixed(2)}`;
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

    async function fetchAndUpdateCharts(logementId) {
        console.log(`Fetching data for logement ID: ${logementId}`);
        const response = await fetch(`/consommation?logement_id=${logementId}&json=true`);
        console.log(`/consommation?logement_id=${logementId}&json=true`);

        if (response.ok) {
            const data = await response.json();
            console.log('Fetched Data:', data);
            updateCharts(data);
            chartsContainer.style.display = 'block';
        } else {
            const errorText = await response.text();
            console.error('Error fetching data:', errorText);
            alert('Error fetching data for logement.');
        }
    }

    // Update Charts After Fetching Data
    function updateCharts(data) {
        const { internet_data, electricite_data, eau_data, pie_chart_data } = data;

        updateChart(internetChart, internet_data);
        updateChart(electricityChart, electricite_data);
        updateChart(waterChart, eau_data);
        updatePieChart(facturePieChart, pie_chart_data);
    }

    // Handle Chart Updates (Line Charts)
    function updateChart(chart, chartData) {
        chart.data.labels = [];
        chart.data.datasets[0].data = [];

        if (chartData.length === 0) {
            console.log('No data available for this chart.');
        } else {
            chartData.sort((a, b) => new Date(a[0]) - new Date(b[0]));

            const labels = chartData.map(item => item[0]);  // Date
            const values = chartData.map(item => item[1]);  // Consumption
            const unit = chartData[0][2];  // Unit of consumption

            chart.data.labels = labels;
            chart.data.datasets[0].data = values;
            chart.data.datasets[0].unit = unit;  // Update the dataset with unit
        }
        chart.update();
    }

    // Update Pie Chart (Fix for Empty Data)
    function updatePieChart(chart, chartData) {
        chart.data.labels = [];
        chart.data.datasets[0].data = [];

        if (chartData.length === 0) {
            chart.data.labels = ['Pas de Factures'];
            chart.data.datasets[0].data = [0];
            chart.data.datasets[0].backgroundColor = ['rgba(200, 200, 200, 0.2)'];
            chart.data.datasets[0].borderColor = ['rgba(200, 200, 200, 1)'];
        } else {
            const labels = chartData.map(item => item[0]);
            const values = chartData.map(item => item[1]);
            
            chart.data.labels = labels;
            chart.data.datasets[0].data = values;
        }
        chart.update();
    }

    // Handle Facture Form Submission
    factureForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        if (!factureForm.checkValidity()) {
            alert('Veuillez remplir tous les champs.');
            return;
        }

        const formData = new FormData(factureForm);
        const response = await fetch('/facture', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const newFacture = await response.json();
            if (selectedLogementId && parseInt(selectedLogementId) === newFacture.id_logement) {
                fetchAndUpdateCharts(selectedLogementId);
            }
            factureForm.reset();
        } else {
             alert('Erreur lors de l\'ajout de la facture.');
        }
    });
});
