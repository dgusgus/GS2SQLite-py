# 🚀 Sistema 1: Guía Completa para Windows

## 📋 Lo que Necesitas (Pre-requisitos)

### ✅ **Antes de empezar, asegúrate de tener:**
1. **Windows 10/11** con permisos de administrador
2. **Python 3.8+** instalado → [Descargar aquí](https://python.org/downloads/)
3. **Archivo de credenciales**: `generador-docs-31f4b831a196.json`
4. **Google Sheets** configurado con los datos
5. **Conexión a Internet** estable

---

## 🛠️ Instalación Súper Fácil

### **Paso 1: Descargar los Archivos**
```
📁 1-data-converter-python/
├── 📄 main.py
├── 📄 requirements.txt
├── 🔑 generador-docs-31f4b831a196.json  ← ¡IMPORTANTE!
├── 🎯 setup.bat
├── 🚀 ejecutar.bat
├── 📊 stats.bat
├── 📥 importar.bat
├── 🏗️ crear.bat
├── 🧪 test.bat
└── 🧹 limpiar.bat
```

### **Paso 2: Configuración Automática**
1. **Abrir carpeta** `1-data-converter-python`
2. **Doble clic** en `setup.bat`
3. **Esperar** que termine la instalación
4. **Listo** ✅

---

## 🎯 Cómo Usar el Sistema (Súper Simple)

### **🚀 Conversión Completa (Más Común)**
```batch
# Doble clic en:
ejecutar.bat
```
**¿Qué hace?**
- ✅ Crea la base de datos
- ✅ Importa todos los datos desde Google Sheets  
- ✅ Muestra estadísticas finales
- ✅ ¡Todo en uno!

---

### **📊 Ver Solo Estadísticas**
```batch
# Doble clic en:
stats.bat
```
**¿Cuándo usar?**
- Para ver cuántos registros tienes
- Después de hacer cambios
- Para verificar que todo esté bien

---

### **📥 Actualizar Solo los Datos**
```batch
# Doble clic en:
importar.bat
```
**¿Cuándo usar?**
- Cuando cambies datos en Google Sheets
- Para actualizar sin recrear todo
- **Seguro**: no duplica datos

---

### **🧪 Probar Conexiones**
```batch
# Doble clic en:
test.bat
```
**¿Para qué?**
- Verificar que Google Sheets funciona
- Probar la base de datos
- Diagnosticar problemas

---

## 📊 Formato del Google Sheets

### **Tu Google Sheets DEBE tener estas hojas:**

#### 📄 **Hoja "Jefes"**
| nombre | telefono | email |
|--------|----------|-------|
| Juan Pérez | 70123456 | juan@email.com |
| María López | 70234567 | maria@email.com |

#### 📄 **Hoja "Coordinadores"**  
| nombre | codigo_coordinador | jefe_nombre | telefono | email |
|--------|-------------------|-------------|----------|-------|
| Carlos Mamani | COORD001 | Juan Pérez | 70345678 | carlos@email.com |
| Ana García | COORD002 | María López | 70456789 | ana@email.com |

#### 📄 **Hoja "Grupos"**
| nombre_grupo | coordinador_codigo | descripcion |
|-------------|-------------------|-------------|
| Grupo Norte | COORD001 | Zona norte de La Paz |
| Grupo Sur | COORD002 | Zona sur de La Paz |

#### 📄 **Hoja "Departamentos"**
| nombre | codigo |
|--------|--------|
| La Paz | LP |
| Cochabamba | CB |
| Santa Cruz | SC |

#### 📄 **Hoja "Provincias"**
| nombre | codigo | departamento_codigo |
|--------|--------|-------------------|
| Murillo | MUR | LP |
| Cercado | CER | CB |

#### 📄 **Hoja "Municipios"**
| nombre | codigo | provincia_codigo |
|--------|--------|-----------------|
| La Paz | LP001 | MUR |
| El Alto | LP002 | MUR |

#### 📄 **Hoja "Asientos"**
| nombre | codigo | municipio_codigo |
|--------|--------|-----------------|
| La Paz Centro | AE001 | LP001 |
| El Alto Norte | AE002 | LP002 |

#### 📄 **Hoja "Recintos"**
| nombre | direccion | tipo | asiento_codigo | latitud | longitud |
|--------|-----------|------|---------------|---------|----------|
| Escuela Central | Av. 6 de Agosto 123 | urbano | AE001 | -16.5000 | -68.1193 |
| Colegio Rural | Comunidad Achocalla | rural | AE002 | -16.5500 | -68.1500 |

#### 📄 **Hoja "Vehiculos"**
| placa | marca | modelo | anio |
|-------|-------|--------|------|
| ABC-123 | Toyota | Hilux | 2020 |
| DEF-456 | Nissan | Navara | 2019 |

#### 📄 **Hoja "Choferes"**
| nombre | cedula | licencia | telefono | vehiculo_placa |
|--------|--------|----------|----------|---------------|
| Pedro Quispe | 12345678 | B-123456 | 70567890 | ABC-123 |
| Luis Condori | 87654321 | B-654321 | 70678901 | DEF-456 |

#### 📄 **Hoja "Operadores"**
| nombre | cedula | telefono | tipo_operador | grupo_nombre | recinto_nombre | vehiculo_placa | fecha_inicio | fecha_fin |
|--------|--------|----------|---------------|-------------|---------------|---------------|-------------|-----------|
| Ana Mamani | 11111111 | 70111111 | rural | Grupo Norte | Escuela Central | ABC-123 | 2024-02-01 | 2024-02-28 |
| José López | 22222222 | 70222222 | urbano | Grupo Sur | Colegio Rural | DEF-456 | 2024-02-01 | 2024-02-28 |

---

## 🔧 Personalización Fácil

### **🎨 Cambiar Nombres de Hojas**
Si tus hojas se llaman diferente, edita `config.py`:

```python
# En config.py, línea ~15
SHEET_NAMES = {
    'jefes': 'MisJefes',           # Cambiar 'Jefes' por 'MisJefes'
    'coordinadores': 'Coordinadores',
    'grupos': 'MisGrupos',         # Cambiar 'Grupos' por 'MisGrupos'
    # ... etc
}
```

### **📊 Cambiar Nombres de Columnas**
Si tus columnas se llaman diferente, edita `config.py`:

```python
# En config.py, línea ~35
COLUMN_MAPPING = {
    'operadores': {
        'nombre': 'nombre_completo',    # Tu columna se llama 'nombre_completo'
        'cedula': 'ci',                 # Tu columna se llama 'ci'
        'telefono': 'celular',          # Tu columna se llama 'celular'
        # ... etc
    }
}
```

### **💾 Cambiar Ubicación de Base de Datos**
```python
# En config.py, línea ~5
DATABASE_PATH = "C:/MisDocumentos/operadores.db"  # Tu ruta personalizada
```

---

## 🔍 Ejemplo de Uso Paso a Paso

### **📝 Escenario: Primera vez usando el sistema**

1. **Preparar Google Sheets**
   - Crear spreadsheet con las 11 hojas
   - Llenar datos siguiendo el formato de arriba
   - Compartir con el service account

2. **Instalar Sistema**
   ```batch
   # Doble clic:
   setup.bat
   ```

3. **Ejecutar Conversión**
   ```batch
   # Doble clic:
   ejecutar.bat
   ```

4. **Ver Resultados**
   ```
   ✅ Base de datos creada en: ../database/operadores.db
   📊 Total: 850 registros importados
   ```

### **🔄 Escenario: Actualizar datos existentes**

1. **Modificar Google Sheets**
   - Agregar nuevos operadores
   - Cambiar teléfonos
   - Actualizar fechas

2. **Reimportar Datos**
   ```batch
   # Doble clic:
   importar.bat
   ```

3. **Verificar Cambios**
   ```batch
   # Doble clic:
   stats.bat
   ```

---

## 🐛 Solución de Problemas

### **❌ Error: "Python no encontrado"**
**💡 Solución:**
1. Instalar Python desde https://python.org/downloads/
2. ✅ **IMPORTANTE**: Marcar "Add Python to PATH"
3. Reiniciar CMD
4. Ejecutar `setup.bat` otra vez

### **❌ Error: "Archivo de credenciales no encontrado"**
**💡 Solución:**
1. Verificar que `generador-docs-31f4b831a196.json` esté en la carpeta
2. Verificar que el nombre sea exacto (sin espacios extra)
3. Si tienes otro nombre, cambiar en `config.py`:
   ```python
   CREDENTIALS_FILE = "mi-archivo-credenciales.json"
   ```

### **❌ Error: "Permission denied Google Sheets"**
**💡 Solución:**
1. Abrir el archivo de credenciales
2. Buscar el campo `"client_email"`
3. Copiar el email (ej: `mi-servicio@proyecto.iam.gserviceaccount.com`)
4. En Google Sheets → Compartir → Pegar el email → Dar permisos de "Editor"

### **❌ Error: "Hoja 'XXX' no encontrada"**
**💡 Solución:**
- El sistema saltará hojas faltantes automáticamente
- Para usar nombres diferentes, modificar `SHEET_NAMES` en `config.py`
- Verificar mayúsculas/minúsculas exactas

### **❌ Error: "Database is locked"**
**💡 Solución:**
1. Cerrar cualquier programa que use la base de datos
2. Reiniciar el proceso
3. Si persiste, ejecutar `limpiar.bat` y empezar de nuevo

---

## 📈 Salidas del Sistema

### **✅ Salida Exitosa:**
```
🚀 SISTEMA 1: CONVERSIÓN DE DATOS
==================================================
⏰ Ejecutado: 2024-02-15 14:30:25

🏗️  Creando estructura...
✅ Tabla 'jefe' creada/verificada
✅ Tabla 'coordinador' creada/verificada
... (todas las tablas)
✅ Esquema de base de datos listo

📥 Importando datos...
✅ Conectado a Google Sheets
📊 Jefes: 5 registros
👔 Procesando jefes...
   ✅ 5 jefes procesados

📊 Coordinadores: 15 registros  
👥 Procesando coordinadores...
   ✅ 15 coordinadores procesados

... (todos los tipos de datos)

📊 ESTADÍSTICAS DE LA BASE DE DATOS
============================================================
👔 Jefe                    :      5 registros
👥 Coordinador             :     15 registros
🏢 Grupo                   :     25 registros
🏛️ Departamento           :      9 registros
🌄 Provincia              :     48 registros
🏘️ Municipio              :    339 registros
🗳️ Asiento Electoral      :    120 registros
🏫 Recinto                 :    245 registros
🚗 Vehiculo                :     45 registros
🚛 Chofer                  :     45 registros
👷 Operador                :    150 registros
============================================================
🎯 TOTAL:   1046 registros
============================================================

🎉 Proceso completado exitosamente!
💾 Base de datos guardada en: ..\database\operadores.db
```

---

## 🔄 Reimportación Segura

### **✅ Garantías del Sistema:**
- **No duplica datos**: Usa campos únicos (cédula, código, etc.)
- **Actualiza inteligentemente**: Solo cambia datos modificados  
- **Preserva relaciones**: Los IDs se mantienen estables
- **Rollback automático**: Si hay error, revierte cambios

### **🔄 Proceso de Actualización:**
1. Modificas datos en Google Sheets
2. Ejecutas `importar.bat`
3. El sistema:
   - Encuentra registros existentes por campo único
   - Actualiza solo los campos que cambiaron
   - Inserta solo los registros nuevos
   - Mantiene todas las relaciones intactas

---

## 📁 Archivos Generados

### **Después de usar el sistema:**
```
proyecto/
├── 1-data-converter-python/
│   ├── venv/                          ← Entorno virtual
│   ├── __pycache__/                   ← Cache de Python
│   ├── main.py                        ← Código principal
│   ├── generador-docs-31f4b831a196.json ← Credenciales
│   └── *.bat                          ← Scripts de ejecución
│
├── database/
│   └── operadores.db                  ← ¡BASE DE DATOS CREADA! 🎯
│
├── 2-web-consultas/                   ← (Sistema siguiente)
└── 3-doc-generator/                   ← (Sistema siguiente)
```

---

## 🚀 Siguiente Paso

Una vez que tengas `operadores.db` creado:

### **✅ Sistema 1 COMPLETADO**
- Base de datos SQLite funcional
- Todos los datos importados y organizados
- Relaciones entre tablas establecidas

### **🚧 Próximo: Sistema 2 (Web de Consultas)**
- Interfaz web para buscar datos
- Consultas como "¿qué operador usa qué vehículo?"
- Dashboard con estadísticas

### **🚧 Después: Sistema 3 (Generador de Documentos)**  
- Generar documentos masivos para operadores
- Plantillas Word y Excel personalizables
- Exportación a PDF

---

## 💡 Tips y Trucos

### **⚡ Automatización**
```batch
# Crear un archivo "actualizar_diario.bat":
@echo off
cd "C:\ruta\al\sistema\1-data-converter-python"
call importar.bat
```

### **📅 Programar Ejecución**
1. **Abrir** Programador de tareas de Windows
2. **Crear tarea básica**
3. **Programa**: Tu archivo `actualizar_diario.bat`
4. **Programar**: Diariamente a las 6:00 AM

### **💾 Backup Automático**
```batch
# En backup.bat:
@echo off
copy "..\database\operadores.db" "..\backup\operadores_%date%.db"
echo Backup creado: operadores_%date%.db
```

### **🔍 Consultas SQL Directas**
Si sabes SQL, puedes consultar directamente:
```sql
-- Ver operadores con sus vehículos
SELECT o.nombre, o.