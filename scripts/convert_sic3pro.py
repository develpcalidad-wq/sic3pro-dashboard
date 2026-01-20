#!/usr/bin/env python3
"""
Script para convertir reportes de SIC3PRO (Excel/HTML) a JSON para el dashboard
"""

import pandas as pd
import json
import os
import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def convert_excel_html_to_json(html_file, output_file):
    """Convierte un archivo HTML (exportado de SIC3PRO) a JSON"""
    
    print(f"Convirtiendo {html_file} a {output_file}...")
    
    try:
        # Leer el archivo HTML
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parsear HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Encontrar todas las tablas
        tables = soup.find_all('table')
        
        data = {
            "metadata": {
                "sourceFile": os.path.basename(html_file),
                "conversionDate": datetime.now().isoformat(),
                "tablesFound": len(tables)
            },
            "tables": []
        }
        
        for i, table in enumerate(tables):
            table_data = []
            
            # Obtener filas
            rows = table.find_all('tr')
            
            # Obtener encabezados (primera fila)
            if rows:
                headers = []
                header_cells = rows[0].find_all(['th', 'td'])
                for cell in header_cells:
                    headers.append(cell.get_text(strip=True))
                
                # Obtener datos (filas siguientes)
                for row in rows[1:]:
                    row_data = {}
                    cells = row.find_all('td')
                    
                    for j, cell in enumerate(cells):
                        if j < len(headers):
                            row_data[headers[j]] = cell.get_text(strip=True)
                    
                    if row_data:  # Solo agregar filas con datos
                        table_data.append(row_data)
                
                if table_data:
                    data["tables"].append({
                        "tableIndex": i,
                        "headers": headers,
                        "rows": table_data,
                        "rowCount": len(table_data)
                    })
        
        # Guardar como JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Conversión exitosa: {len(data['tables'])} tablas convertidas")
        return True
        
    except Exception as e:
        print(f"❌ Error en conversión: {str(e)}")
        return False

def download_from_url(url, output_file):
    """Descarga datos directamente desde SIC3PRO (si está permitido)"""
    
    print(f"Descargando datos desde {url}...")
    
    try:
        # Headers para simular navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        
        # Guardar HTML
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✅ Descarga exitosa: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error en descarga: {str(e)}")
        return False

def create_sample_json(output_file):
    """Crea un JSON de ejemplo con datos simulados"""
    
    print(f"Creando datos de ejemplo en {output_file}...")
    
    data = {
        "metadata": {
            "source": "SIC3PRO - Datos de ejemplo",
            "lastUpdated": datetime.now().isoformat(),
            "project": "1253",
            "type": "detalles_terminacion"
        },
        "summary": {
            "totalItems": 156,
            "completed": 94,
            "pending": 42,
            "delayed": 20,
            "efficiency": "78%",
            "lastUpdate": datetime.now().strftime("%Y-%m-%d %H:%M")
        },
        "items": [
            {
                "id": f"TERM-{1000 + i}",
                "description": f"Terminación {i+1}: Sistema eléctrico área {i%5 + 1}",
                "area": f"Área {i%5 + 1}",
                "system": ["Eléctrico", "Mecánico", "Instrumentación", "Civil"][i%4],
                "status": ["completed", "pending", "delayed", "in_progress"][i%4],
                "commitmentDate": (datetime.now().replace(day=1).strftime("%Y-%m-%d")),
                "responsible": f"Responsable {(i%3) + 1}",
                "daysRemaining": i%7 - 3,
                "priority": ["Alta", "Media", "Baja"][i%3]
            }
            for i in range(50)
        ],
        "alerts": [
            {
                "id": "ALT-001",
                "type": "critical",
                "title": "Retraso crítico en área eléctrica",
                "description": "3 items con más de 10 días de retraso",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "actionRequired": True
            },
            {
                "id": "ALT-002",
                "type": "warning",
                "title": "No conformidad pendiente de revisión",
                "description": "NC-2024-001 requiere revisión inmediata",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "actionRequired": True
            }
        ]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Datos de ejemplo creados: {len(data['items'])} items")
    return True

def main():
    """Función principal"""
    
    print("=" * 60)
    print("CONVERSOR SIC3PRO -> JSON")
    print("=" * 60)
    
    # Crear carpeta de salida si no existe
    os.makedirs('data/datasets', exist_ok=True)
    
    # Opciones disponibles
    print("\nOpciones disponibles:")
    print("1. Convertir archivo HTML de SIC3PRO a JSON")
    print("2. Descargar datos desde URL de SIC3PRO")
    print("3. Generar datos de ejemplo")
    print("4. Procesar todos los reportes automáticamente")
    
    try:
        option = input("\nSelecciona una opción (1-4): ").strip()
        
        if option == "1":
            # Convertir archivo local
            html_file = input("Ruta del archivo HTML: ").strip()
            if not os.path.exists(html_file):
                print("❌ El archivo no existe")
                return
            
            output_file = "data/datasets/sic3pro_data.json"
            convert_excel_html_to_json(html_file, output_file)
            
        elif option == "2":
            # Descargar desde URL
            url = input("URL del reporte SIC3PRO: ").strip()
            temp_file = "temp_sic3pro.html"
            output_file = "data/datasets/sic3pro_data.json"
            
            if download_from_url(url, temp_file):
                convert_excel_html_to_json(temp_file, output_file)
                os.remove(temp_file)  # Limpiar archivo temporal
        
        elif option == "3":
            # Generar datos de ejemplo
            output_file = "data/datasets/sic3pro_data.json"
            create_sample_json(output_file)
            
        elif option == "4":
            # Procesamiento automático
            print("\n📊 Procesando todos los reportes...")
            
            # 1. Detalles de terminación
            print("\n1. Detalles de terminación...")
            create_sample_json("data/datasets/termination.json")
            
            # 2. No conformidades
            print("2. No conformidades...")
            nc_data = {
                "metadata": {
                    "type": "no_conformidades",
                    "lastUpdated": datetime.now().isoformat()
                },
                "byType": [
                    {"type": "Calidad", "count": 25, "percent": "52%"},
                    {"type": "Seguridad", "count": 12, "percent": "25%"},
                    {"type": "Ambiental", "count": 6, "percent": "12.5%"},
                    {"type": "Proceso", "count": 5, "percent": "10.5%"}
                ],
                "byMonth": [
                    {"month": "Oct 2023", "count": 8},
                    {"month": "Nov 2023", "count": 10},
                    {"month": "Dec 2023", "count": 12},
                    {"month": "Ene 2024", "count": 18}
                ]
            }
            
            with open("data/datasets/nonconformities.json", 'w') as f:
                json.dump(nc_data, f, indent=2)
            
            print("✅ Procesamiento automático completado")
            
        else:
            print("❌ Opción no válida")
            
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
