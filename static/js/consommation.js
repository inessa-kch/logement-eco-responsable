document.addEventListener('DOMContentLoaded', function() {
    const logementButtons = document.querySelectorAll('.logement-btn');
    const chartsContainer = document.querySelector('.charts-container');
    const factureForm = document.getElementById('factureForm');
    let selectedLogementId = null;  // Track the currently selected logement

    // Initialize charts
    const internetCtx = document.getElementById('internetChart').getContext('2d');
    const internetChart = createLineChart(internetCtx, 'Internet Consumption');

    const electricityCtx = document.getElementById('electricityChart').getContext('2d');
    const electricityChart = createLineChart(electricityCtx, 'Electricity Consumption');

    const waterCtx = document.getElementById('waterChart').getContext('2d');
    const waterChart = createLineChart(waterCtx, 'Water Consumption');

    const pieCtx = document.getElementById('facturePieChart').getContext('2d');
    const facturePieChart = createPieChart(pieCtx);

    // Chart Creation Functions
    function createLineChart(ctx, label) {
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: label,
                    data: [],
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: false
                }]
            },
            options: {
                scales: {
                    x: { 
                        title: { display: true, text: 'Date' }
                    },
                    y: { 
                        title: { display: true, text: 'Consumption' }
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
                    backgroundColor: ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)'],
                    borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' },
                    title: { display: true, text: 'Distribution of Factures' },
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
        const response = await fetch(`/consommation?logement_id=${logementId}&json=true`);
        if (response.ok) {
            const data = await response.json();
            console.log('Fetched Data:', data);
            updateCharts(data);
            chartsContainer.style.display = 'block';
        } else {
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

            const labels = chartData.map(item => item[0]);
            const values = chartData.map(item => item[1]);
            
            chart.data.labels = labels;
            chart.data.datasets[0].data = values;
        }
        chart.update();
    }

    // Update Pie Chart
// Update Pie Chart (Fix for Empty Data)
    function updatePieChart(chart, chartData) {
        // Clear existing data
        chart.data.labels = [];
        chart.data.datasets[0].data = [];

        if (chartData.length === 0) {
            console.log('No data available for the pie chart.');
            // If no data, add a placeholder to show empty chart
            chart.data.labels = ['No Factures'];
            chart.data.datasets[0].data = [0];  // Placeholder value to keep the chart visible
            chart.data.datasets[0].backgroundColor = ['rgba(200, 200, 200, 0.2)'];  // Grey out the pie chart
            chart.data.datasets[0].borderColor = ['rgba(200, 200, 200, 1)'];
        } else {
            // Populate pie chart with actual data
            const labels = chartData.map(item => item[0]);
            const values = chartData.map(item => item[1]);
            
            chart.data.labels = labels;
            chart.data.datasets[0].data = values;
            chart.data.datasets[0].backgroundColor = [
                'rgba(75, 192, 192, 0.2)', 
                'rgba(255, 99, 132, 0.2)', 
                'rgba(54, 162, 235, 0.2)'
            ];
            chart.data.datasets[0].borderColor = [
                'rgba(75, 192, 192, 1)', 
                'rgba(255, 99, 132, 1)', 
                'rgba(54, 162, 235, 1)'
            ];
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
            alert('Facture ajoutée avec succès!');
            if (selectedLogementId && parseInt(selectedLogementId) === newFacture.id_logement) {
                fetchAndUpdateCharts(selectedLogementId);
            }
            factureForm.reset();
        } else {
            alert('Erreur lors de l\'ajout de la facture.');
        }
    });
});
