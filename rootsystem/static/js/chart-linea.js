var ctx = document.getElementById('lineChart').getContext('2d');


var line_chart = new Chart(ctx, {
    type: 'line',
    data: { 
        labels: ['13-Sep', '14-Sep', '15-Sep', '16-Sep', '17-Sep'],
        datasets: [{
            label: 'Pedidos',
            backgroundColor: 'rgb(75, 192, 192)',
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            data: [1, 2, 3, 0, 2]
        }],
        }
}); 
