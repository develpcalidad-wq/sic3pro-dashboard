// Cargador de datos para el dashboard
class DashboardLoader {
    constructor() {
        this.dataSources = {
            dashboard: 'data/datasets/dashboard.json',
            termination: 'data/datasets/termination.json',
            nonconformities: 'data/datasets/nonconformities.json',
            nonconforming: 'data/datasets/nonconforming.json'
        };
        
        this.data = {};
    }
    
    async loadAll() {
        try {
            const promises = Object.entries(this.dataSources).map(async ([key, url]) => {
                const response = await fetch(url);
                this.data[key] = await response.json();
                console.log(`✅ ${key} cargado`);
            });
            
            await Promise.all(promises);
            this.updateDashboard();
            return true;
        } catch (error) {
            console.error('Error cargando datos:', error);
            this.showError();
            return false;
        }
    }
    
    updateDashboard() {
        if (!this.data.dashboard) return;
        
        const kpis = this.data.dashboard.kpis;
        
        // Actualizar KPIs
        document.getElementById('criticalAlerts').textContent = 
            Math.floor(kpis.terminaciones_retrasadas * 0.3);
        document.getElementById('pendingItems').textContent = 
            kpis.terminaciones_pendientes;
        document.getElementById('completedItems').textContent = 
            kpis.terminaciones_completadas;
        document.getElementById('efficiencyRate').textContent = 
            kpis.eficiencia_general;
        
        // Actualizar última actualización
        const lastUpdate = document.getElementById('lastUpdate');
        if (lastUpdate) {
            lastUpdate.textContent = new Date().toLocaleTimeString('es-CL');
        }
        
        // Mostrar notificación
        this.showNotification('Datos actualizados correctamente', 'success');
    }
    
    showNotification(message, type = 'info') {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alert.style.cssText = 'top: 20px; right: 20px; z-index: 1050;';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        setTimeout(() => {
            if (alert.parentNode) alert.remove();
        }, 3000);
    }
    
    showError() {
        this.showNotification('Error cargando datos. Usando datos de ejemplo.', 'warning');
        // Cargar datos de ejemplo
        this.loadSampleData();
    }
    
    loadSampleData() {
        // Datos de ejemplo si falla la carga
        this.data.dashboard = {
            kpis: {
                terminaciones_completadas: 94,
                terminaciones_pendientes: 42,
                terminaciones_retrasadas: 20,
                eficiencia_general: '78%'
            }
        };
        this.updateDashboard();
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    const loader = new DashboardLoader();
    loader.loadAll();
    
    // Botón de actualización manual
    document.getElementById('refreshData').addEventListener('click', () => {
        loader.loadAll();
    });
});
