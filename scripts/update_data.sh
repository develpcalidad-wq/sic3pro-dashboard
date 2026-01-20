#!/bin/bash

# Script para actualizar automáticamente datos de SIC3PRO
# Uso: ./scripts/update_data.sh [opcion]

set -e  # Detener en caso de error

echo "🔄 Actualizando datos de SIC3PRO..."
echo "Fecha: $(date)"

# Crear carpetas necesarias
mkdir -p data/datasets

# Opciones
case "${1:-auto}" in
    "manual")
        echo "📝 Modo manual seleccionado"
        python scripts/convert_sic3pro.py
        ;;
        
    "example")
        echo "📊 Generando datos de ejemplo..."
        python scripts/convert_sic3pro.py <<< "3"
        ;;
        
    "auto")
        echo "🤖 Modo automático seleccionado"
        
        # URLs de SIC3PRO (reemplazar con las reales)
        TERMINATION_URL="https://sic3pro.codelco.cl/spro//pages/dt/punch_reporte_listado_excel.php?proyecto=1253&wbs=0&area=0&top=0&sistema=0&subsistema=0&disciplina_tipo=0&disciplina=0&actividad=0&hallazgo=0&empresa_tipo=0&empresa=0&contrato=&resp_cierre=&ing_sistema=&resp_construccion=&tarjetas=&fecha_desde_emision=&fecha_hasta_emision=&fecha_desde_compromiso=&fecha_hasta_compromiso=&fecha_desde_real=&fecha_hasta_real=&caminata=&columnas=2,3,4,5,6,8,9,11,12,13,101,102,103,105,14,15,16,17,25,18,19,20,21,22,41,23,38,40,37,39,24,26,27,36,35,99,45,46,47&busqueda=&descripcion="
        
        # Descargar datos (comentar si no hay acceso directo)
        # echo "📥 Descargando datos de terminación..."
        # wget -q -O data/raw/termination.html "$TERMINATION_URL" || true
        
        # Si no se puede descargar, generar datos de ejemplo
        echo "📊 Generando datasets actualizados..."
        python scripts/convert_sic3pro.py <<< "4"
        
        # Actualizar marca de tiempo
        echo "{\"lastUpdated\": \"$(date -Iseconds)\"}" > data/datasets/last_update.json
        ;;
        
    *)
        echo "Uso: $0 [manual|example|auto]"
        echo "  manual   - Modo interactivo"
        echo "  example  - Generar datos de ejemplo"
        echo "  auto     - Actualización automática (por defecto)"
        exit 1
        ;;
esac

echo "✅ Proceso completado exitosamente"
echo "📁 Datos disponibles en: data/datasets/"
