# 🚀 Guía de Uso: Sistema 1 - Conversión de Datos

## 📋 Pre-requisitos

### ✅ Lo que necesitas tener:
1. **Python 3.8+** instalado
2. **Archivo de credenciales**: `generador-docs-31f4b831a196.json` 
3. **Google Sheets** con los datos formateados correctamente
4. **Acceso a internet** para conectar con Google Sheets API

## 🛠️ Instalación Rápida

### Opción 1: Windows (Automático)
```batch
# 1. Descargar archivos del sistema
# 2. Colocar generador-docs-31f4b831a196.json en la carpeta
# 3. Ejecutar instalación automática
setup.bat
```

### Opción 2: Manual (Cualquier SO)
```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

## 🧪 Verificar que Todo Funciona

### Paso 1: Probar Conexiones
```bash
# Ejecutar pruebas automáticas
python test_connection.py
```

**Salida esperada:**
```
🧪 PRUEBAS DEL SISTEMA 1: CONVERSIÓN DE DATOS
==================================================

🔍 Probando: Archivo de credenciales
✅ Archivo de credenciales válido

🔍 Probando: Conexión Google Sheets
✅ Conexión exitosa a: Operadores Electoral 2024
📊 Hojas disponibles: 11
   - Jefes
   - Coordinadores
   - Grupos
   - Departamentos
   - Provincias
   - Municipios
   - Asientos Electorales
   - Recintos
   - Vehículos
   - Choferes
   - Operadores

🔍 Probando: Base de datos SQLite
✅ Base de datos funcional en: ../database/operadores.db

==================================================
📋 RESUMEN DE PRUEBAS
==================================================
Archivo de credenciales  : ✅ PASS
Conexión Google Sheets   : ✅ PASS  
Base de datos SQLite     : ✅ PASS
==================================================
🎉 Todas las pruebas pasaron! El sistema está listo.
```

## 🚀 Ejecución del Sistema

### Conversión Completa (Recomendado)
```bash
# Crear BD + Importar datos + Mostrar estadísticas
python main.py --action all
```

### Opciones Avanzadas
```bash
# Solo crear estructura de base de datos
python main.py --action create

# Solo importar datos (BD debe existir)
python main.py --action import  

# Solo ver estadísticas
python main.py --action stats

# Usar credenciales personalizadas
python main.py --credentials mi-archivo.json

# Usar BD personalizada
python main.py --database mi-base.db
```

## 📊 Ejemplo de Salida Exitosa

```
🚀 Iniciando conversión de datos...
✅ Autenticación con Google Sheets exitosa
📊 Hojas disponibles: ['Jefes', 'Coordinadores', 'Grupos', 'Departamentos', 'Provincias', 'Municipios', 'Asientos Electorales', 'Recintos', 'Vehículos', 'Choferes', 'Operadores']
✅ Base de datos creada exitosamente

📝 Procesando jefes...
✅ Obtenidos 3 registros de 'Jefes'

📝 Procesando coordinadores...
✅ Obtenidos 8 registros de 'Coordinadores'

📝 Procesando grupos...
✅ Obtenidos 12 registros de 'Grupos'

📝 Procesando departamentos...
✅ Obtenidos 9 registros de 'Departamentos'

📝 Procesando provincias...
✅ Obtenidos 48 registros de 'Provincias'

📝 Procesando municipios...
✅ Obtenidos 339 registros de 'Municipios'

📝 Procesando asientos_electorales...
✅ Obtenidos 89 registros de 'Asientos Electorales'

📝 Procesando recintos...
✅ Obtenidos 245 registros de 'Recintos'

📝 Procesando vehiculos...
✅ Obtenidos 45 registros de 'Vehículos'

📝 Procesando choferes...
✅ Obtenidos 45 registros de 'Choferes'

📝 Procesando operadores...
✅ Obtenidos 150 registros de 'Operadores'

✅ Conversión completada!

📊 ESTADÍSTICAS DE IMPORTACIÓN
==================================================
jefe                :     3 registros
coordinador         :     8 registros
grupo              :    12 registros
departamento       :     9 registros
provincia          :    48 registros
municipio          :   339 registros
asiento_electoral  :    89 registros
recinto            :   245 registros
vehiculo           :    45 registros
chofer             :    45 registros
operador           :   150 registros

🎉 Proceso completado exitosamente!
```

## 🔄 Reimportación Segura

El sistema permite **reimportar datos** sin romper la base:

```bash
# 1. Primera importación
python main.py --action all

# 2. Cambios en Google Sheets...

# 3. Reimportar (actualiza datos existentes)
python main.py --action import

# 4. Verificar cambios
python main.py --action stats
```

### ✅ **Garantías de Seguridad:**
- **No duplica registros**: Usa campos únicos para identificar
- **Preserva IDs**: Los auto-increment se mantienen estables  
- **Actualización inteligente**: Solo cambia datos modificados
- **Rollback automático**: Si hay error, revierte cambios

## 🐛 Solución de Problemas Comunes

### Error: "Archivo no encontrado"
```bash
# Verificar ubicación del archivo
ls -la generador-docs-31f4b831a196.json

# Usar ruta absoluta si es necesario
python main.py --credentials C:\ruta\completa\generador-docs.json
```

### Error: "Permission denied Google Sheets"
1. Verificar que el email del service account tenga acceso al sheet
2. Compartir el Google Sheet con: `tu-service-account@proyecto.iam.gserviceaccount.com`
3. Dar permisos de "Viewer" o "Editor"

### Error: "Hoja 'XXX' no encontrada"
- El sistema saltará hojas faltantes automáticamente
- Verificar nombres exactos en Google Sheets
- Revisar mayúsculas/minúsculas

### Error: "SQLite database locked"
- Cerrar otras conexiones a la base de datos
- Verificar permisos de escritura en la carpeta `../database/`

## 📁 Estructura de Archivos Generados

Después de ejecutar el sistema:

```
proyecto/
├── 1-data-converter-python/
│   ├── main.py ✅
│   ├── generador-docs-31f4b831a196.json ✅
│   ├── venv/ ✅
│   └── ...
├── database/
│   └── operadores.db ✅ CREADO
├── 2-web-consultas/ (pendiente)
└── 3-doc-generator/ (pendiente)
```

## 🔗 Siguiente Paso: Sistema 2

Una vez que tengas `operadores.db` creado y poblado:

1. ✅ **Sistema 1 completado** - Datos convertidos
2. 🚧 **Sistema 2**: Crear interfaz web para consultas  
3. 🚧 **Sistema 3**: Crear generador de documentos

La base de datos `operadores.db` será el **núcleo compartido** entre todos los sistemas.

## 💡 Tips Avanzados

### Automatización con Cron (Linux/Mac)
```bash
# Ejecutar conversión cada día a las 6 AM
0 6 * * * cd /ruta/al/sistema && ./venv/bin/python main.py --action import
```

### Monitoreo de Cambios
```bash
# Script para detectar cambios en Google Sheets
python main.py --action stats > antes.txt
# ... hacer cambios en sheets ...
python main.py --action import
python main.py --action stats > despues.txt
diff antes.txt despues.txt
```

### Backup Automático
```bash
# Crear backup