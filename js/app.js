document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard SIC3PRO cargado');
    
    // Configurar gráfico
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Área 1', 'Área 2', 'Área 3', 'Área 4', 'Área 5'],
            datasets: [{
                label: 'Completados',
                data: [25, 18, 22, 19, 10],
                backgroundColor: '#28a745'
            }, {
                label: 'Pendientes',
                data: [8, 12, 6, 10, 6],
                backgroundColor: '#ffc107'
            }, {
                label: 'Retrasados',
                data: [3, 5, 4, 6, 2],
                backgroundColor: '#dc3545'
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
                    text: 'Estado de Terminaciones por Área'
                }
            }
        }
    });
    
    // Agregar funcionalidad básica
    console.log('Gráfico inicializado correctamente');
    
    // Simular actualización de datos
    setInterval(() => {
        const date = new Date();
        console.log('Dashboard activo - Última actualización:', date.toLocaleTimeString());
    }, 60000);
});
