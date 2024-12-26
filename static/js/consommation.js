document.addEventListener('DOMContentLoaded', function() {
    const internetData = JSON.parse(document.getElementById('internetData').textContent);
    const electriciteData = JSON.parse(document.getElementById('electriciteData').textContent);
    const eauData = JSON.parse(document.getElementById('eauData').textContent);
    const chartData = JSON.parse(document.getElementById('chartData').textContent);

    // Function to sort data by date
    function sortByDate(data) {
        return data.sort((a, b) => new Date(a[0]) - new Date(b[0]));
    }

    // Sort the data by date
    const sortedInternetData = sortByDate(internetData);
    const sortedElectriciteData = sortByDate(electriciteData);
    const sortedEauData = sortByDate(eauData);

    const internetLabels = sortedInternetData.map(item => item[0]); // Assuming date is the first item
    const internetValues = sortedInternetData.map(item => item[1]);
    const electriciteLabels = sortedElectriciteData.map(item => item[0]);
    const electriciteValues = sortedElectriciteData.map(item => item[1]);
    const eauLabels = sortedEauData.map(item => item[0]);
    const eauValues = sortedEauData.map(item => item[1]);

    const internetCtx = document.getElementById('internetChart').getContext('2d');
    const internetChart = new Chart(internetCtx, {
        type: 'line',
        data: {
            labels: internetLabels,
            datasets: [
                {
                    label: 'Internet Consumption',
                    data: internetValues,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Consumption'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            const unit = sortedInternetData[tooltipItem.dataIndex][2];
                            return tooltipItem.dataset.label + ': ' + tooltipItem.raw + ' ' + unit;
                        }
                    }
                }
            }
        }
    });

    const electricityCtx = document.getElementById('electricityChart').getContext('2d');
    const electricityChart = new Chart(electricityCtx, {
        type: 'line',
        data: {
            labels: electriciteLabels,
            datasets: [
                {
                    label: 'Electricity Consumption',
                    data: electriciteValues,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Consumption'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            const unit = sortedElectriciteData[tooltipItem.dataIndex][2];
                            return tooltipItem.dataset.label + ': ' + tooltipItem.raw + ' ' + unit;
                        }
                    }
                }
            }
        }
    });

    const waterCtx = document.getElementById('waterChart').getContext('2d');
    const waterChart = new Chart(waterCtx, {
        type: 'line',
        data: {
            labels: eauLabels,
            datasets: [
                {
                    label: 'Water Consumption',
                    data: eauValues,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1,
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Consumption'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            const unit = sortedEauData[tooltipItem.dataIndex][2];
                            return tooltipItem.dataset.label + ': ' + tooltipItem.raw + ' ' + unit;
                        }
                    }
                }
            }
        }
    });

    const pieCtx = document.getElementById('facturePieChart').getContext('2d');
    const facturePieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: chartData.slice(1).map(item => item[0]), // Skip the header row
            datasets: [{
                data: chartData.slice(1).map(item => item[1]), // Skip the header row
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Distribution of Factures'
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            const item = chartData[tooltipItem.dataIndex + 1]; // Skip the header row
                            return item[0] + ': ' + item[1] + '€ (' + item[2] + ')';
                        }
                    }
                }
            }
        }
    });
});