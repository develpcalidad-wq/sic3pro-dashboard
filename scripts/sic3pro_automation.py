#!/usr/bin/env python3
"""
Sistema automatizado de extracción y procesamiento de datos SIC3PRO
"""

import os
import json
import datetime
import pandas as pd
from datetime import timedelta
import sys

def create_realistic_data():
    """Crea datos realistas para el dashboard SIC3PRO"""
    now = datetime.datetime.now()
    
    # Datos de terminación
    areas = ['Área 1 - Eléctrica', 'Área 2 - Mecánica', 'Área 3 - Instrumentación', 
             'Área 4 - Civil', 'Área 5 - Montaje']
    sistemas = ['Eléctrico', 'Mecánico', 'Instrumentación', 'Civil', 'Montaje']
    
    termination_items = []
    for i in range(1, 51):
        area_idx = i % len(areas)
        sistema_idx = i % len(sistemas)
        
        item = {
            'id': f'TERM-{2024000 + i}',
            'descripcion': f'Terminación {i}: {sistemas[sistema_idx].lower()} en {areas[area_idx].split(" - ")[0]}',
            'area': areas[area_idx],
            'sistema': sistemas[sistema_idx],
            'estado': ['Completado', 'En progreso', 'Pendiente', 'Retrasado'][i % 4],
            'prioridad': ['Alta', 'Media', 'Baja'][i % 3],
            'fecha_compromiso': (now - timedelta(days=50-i)).strftime('%Y-%m-%d'),
            'fecha_real': (now - timedelta(days=50-i - (i % 7))).strftime('%Y-%m-%d') if i % 4 == 0 else None,
            'responsable': f'RESP_{(i % 5) + 1}',
            'dias_retraso': i % 10 if i % 4 == 3 else 0,
            'progreso': i % 100
        }
        termination_items.append(item)
    
    # Calcular resumen
    completed = len([i for i in termination_items if i['estado'] == 'Completado'])
    pending = len([i for i in termination_items if i['estado'] == 'Pendiente'])
    in_progress = len([i for i in termination_items if i['estado'] == 'En progreso'])
    delayed = len([i for i in termination_items if i['estado'] == 'Retrasado'])
    
    termination_data = {
        'metadata': {
            'tipo': 'detalles_terminacion',
            'generado_en': now.isoformat(),
            'proyecto': '1253',
            'total_items': len(termination_items)
        },
        'resumen': {
            'total': len(termination_items),
            'completados': completed,
            'en_progreso': in_progress,
            'pendientes': pending,
            'retrasados': delayed,
            'eficiencia': f'{completed / len(termination_items) * 100:.1f}%',
            'tasa_completacion': f'{(completed + in_progress * 0.5) / len(termination_items) * 100:.1f}%'
        },
        'por_area': [
            {
                'area': area.split(' - ')[0],
                'sistema': area.split(' - ')[1],
                'completados': len([i for i in termination_items if i['area'] == area and i['estado'] == 'Completado']),
                'en_progreso': len([i for i in termination_items if i['area'] == area and i['estado'] == 'En progreso']),
                'pendientes': len([i for i in termination_items if i['area'] == area and i['estado'] == 'Pendiente']),
                'retrasados': len([i for i in termination_items if i['area'] == area and i['estado'] == 'Retrasado'])
            }
            for area in areas
        ],
        'items': termination_items,
        'alertas': [
            {
                'id': 'ALT-001',
                'tipo': 'critica',
                'titulo': 'Retraso crítico en área eléctrica',
                'descripcion': f'{len([i for i in termination_items if "Eléctrica" in i["area"] and i["estado"] == "Retrasado"])} items con retraso > 5 días',
                'fecha': now.strftime('%Y-%m-%d'),
                'accion_requerida': True
            },
            {
                'id': 'ALT-002',
                'tipo': 'advertencia',
                'titulo': 'Items pendientes de documentación',
                'descripcion': f'{len([i for i in termination_items if i["estado"] == "Completado" and i["progreso"] < 100])} items completados sin documentación final',
                'fecha': (now - timedelta(days=1)).strftime('%Y-%m-%d'),
                'accion_requerida': True
            }
        ]
    }
    
    # Datos de no conformidades
    nc_types = ['Calidad', 'Seguridad', 'Ambiental', 'Proceso', 'Documentación']
    
    nonconformities_data = {
        'metadata': {
            'tipo': 'no_conformidades',
            'generado_en': now.isoformat(),
            'proyecto': '1253'
        },
        'resumen': {
            'total': 48,
            'abiertas': 15,
            'cerradas': 28,
            'en_progreso': 5,
            'tasa_resolucion': '85.4%',
            'tiempo_promedio_resolucion': '7.2 días'
        },
        'por_tipo': [
            {
                'tipo': tipo,
                'cantidad': (idx + 1) * 5,
                'porcentaje': f'{((idx + 1) * 5 / 48 * 100):.1f}%'
            }
            for idx, tipo in enumerate(nc_types)
        ],
        'por_mes': [
            {'mes': (now - timedelta(days=90)).strftime('%b'), 'cantidad': 8},
            {'mes': (now - timedelta(days=60)).strftime('%b'), 'cantidad': 12},
            {'mes': (now - timedelta(days=30)).strftime('%b'), 'cantidad': 15},
            {'mes': now.strftime('%b'), 'cantidad': 13}
        ],
        'ncs_criticas': [
            {
                'id': 'NC-2024-001',
                'descripcion': 'Soldadura no conforme en tubería principal',
                'tipo': 'Calidad',
                'prioridad': 'Crítica',
                'fecha_deteccion': (now - timedelta(days=15)).strftime('%Y-%m-%d'),
                'estado': 'Abierta',
                'responsable': 'Área Mecánica',
                'dias_abierta': 15
            }
        ]
    }
    
    # Datos de productos no conformes
    materiales = ['Tuberías A106', 'Válvulas Globo', 'Estructuras A36', 
                 'Equipos Rotativos', 'Instrumentos', 'Material Eléctrico']
    
    nonconforming_data = {
        'metadata': {
            'tipo': 'productos_no_conformes',
            'generado_en': now.isoformat(),
            'proyecto': '1253'
        },
        'resumen': {
            'total': 32,
            'rechazados': 15,
            'reprocesados': 12,
            'en_revision': 5,
            'tasa_rechazo': '46.9%'
        },
        'por_material': [
            {
                'material': material,
                'cantidad': (idx + 2) * 2,
                'estado': ['Rechazado', 'Reprocesado', 'En revisión'][idx % 3]
            }
            for idx, material in enumerate(materiales)
        ]
    }
    
    # Datos consolidados para dashboard
    dashboard_data = {
        'metadata': {
            'proyecto': 'Proyecto 1253',
            'ultima_actualizacion': now.isoformat(),
            'version_datos': '1.0'
        },
        'kpis': {
            'total_terminaciones': len(termination_items),
            'terminaciones_completadas': completed,
            'terminaciones_pendientes': pending + in_progress,
            'terminaciones_retrasadas': delayed,
            'no_conformidades_abiertas': 15,
            'productos_no_conformes': 32,
            'eficiencia_general': f'{completed / len(termination_items) * 100:.1f}%',
            'tasa_resolucion_nc': '85.4%'
        },
        'alertas_consolidadas': termination_data['alertas'] + [
            {
                'id': 'ALT-003',
                'tipo': 'informativa',
                'titulo': 'Revisión mensual programada',
                'descripcion': 'Revisión mensual de calidad programada para mañana',
                'fecha': now.strftime('%Y-%m-%d'),
                'accion_requerida': False
            }
        ],
        'ultima_actualizacion_ui': now.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return {
        'termination': termination_data,
        'nonconformities': nonconformities_data,
        'nonconforming': nonconforming_data,
        'dashboard': dashboard_data
    }

def save_data(data, output_dir='data/datasets'):
    """Guarda los datos en archivos JSON"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Guardar datos individuales
    for key in ['termination', 'nonconformities', 'nonconforming', 'dashboard']:
        if key in data:
            filename = os.path.join(output_dir, f'{key}.json')
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data[key], f, indent=2, ensure_ascii=False)
            print(f'💾 Guardado: {filename}')
    
    # Guardar resumen
    summary = {
        'ultima_actualizacion': datetime.datetime.now().isoformat(),
        'archivos_generados': ['termination.json', 'nonconformities.json', 'nonconforming.json', 'dashboard.json'],
        'estado': 'exito',
        'total_datos': sum(len(str(data.get(key, {}))) for key in ['termination', 'nonconformities', 'nonconforming'])
    }
    
    summary_file = os.path.join(output_dir, 'summary.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f'💾 Guardado: {summary_file}')

def main():
    print('=' * 60)
    print('SISTEMA AUTOMATIZADO SIC3PRO - GENERADOR DE DATOS')
    print('=' * 60)
    print(f'📅 Fecha: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'📁 Directorio: {os.getcwd()}')
    print('=' * 60)
    
    try:
        # Generar datos
        print('📊 Generando datos realistas...')
        data = create_realistic_data()
        
        # Guardar datos
        print('💾 Guardando archivos...')
        save_data(data)
        
        # Mostrar resumen
        print('\n' + '=' * 60)
        print('✅ PROCESO COMPLETADO EXITOSAMENTE')
        print('=' * 60)
        
        termination = data['termination']
        print(f'📈 Terminaciones: {termination["resumen"]["total"]} items')
        print(f'   ✅ Completados: {termination["resumen"]["completados"]}')
        print(f'   ⏳ En progreso: {termination["resumen"]["en_progreso"]}')
        print(f'   ⏱️  Pendientes: {termination["resumen"]["pendientes"]}')
        print(f'   ⚠️  Retrasados: {termination["resumen"]["retrasados"]}')
        print(f'   📊 Eficiencia: {termination["resumen"]["eficiencia"]}')
        
        print(f'\n🚨 Alertas activas: {len(termination["alertas"])}')
        for alerta in termination['alertas']:
            print(f'   • {alerta["titulo"]}')
        
        print(f'\n📁 Datos guardados en: data/datasets/')
        print(f'🕐 Última actualización: {data["dashboard"]["metadata"]["ultima_actualizacion"]}')
        print('=' * 60)
        
        return True
        
    except Exception as e:
        print(f'\n❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
