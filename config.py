# config.py - Configuraciones centralizadas
import os

# === CONFIGURACIÓN GOOGLE SHEETS ===
SPREADSHEET_ID = "1ehySw2tVI1l8INo4fgE7kEGFd0Kb2miPs7vCqsFZC8I"
CREDENTIALS_FILE = "generador-docs-31f4b831a196.json"

# === CONFIGURACIÓN BASE DE DATOS ===
DATABASE_PATH = "../database/operadores.db"

# === MAPEO DE HOJAS GOOGLE SHEETS ===
# Cambia estos nombres si tus hojas se llaman diferente
SHEET_NAMES = {
    'jefes': 'Jefes',
    'coordinadores': 'Coordinadores',
    'grupos': 'Grupos', 
    'departamentos': 'Departamentos',
    'provincias': 'Provincias',
    'municipios': 'Municipios',
    'asientos': 'Asientos',
    'recintos': 'Recintos',
    'vehiculos': 'Vehiculos',
    'choferes': 'Choferes',
    'operadores': 'Operadores'
}

# === MAPEO DE COLUMNAS ===
# Si cambias nombres de columnas en Google Sheets, cámbialos aquí
COLUMN_MAPPING = {
    'jefes': {
        'nombre': 'nombre',
        'telefono': 'telefono', 
        'email': 'email'
    },
    'coordinadores': {
        'nombre': 'nombre',
        'codigo': 'codigo_coordinador',
        'jefe': 'jefe_nombre',
        'telefono': 'telefono',
        'email': 'email'
    },
    'grupos': {
        'nombre': 'nombre_grupo',
        'coordinador': 'coordinador_codigo',
        'descripcion': 'descripcion'
    },
    'departamentos': {
        'nombre': 'nombre',
        'codigo': 'codigo'
    },
    'provincias': {
        'nombre': 'nombre',
        'codigo': 'codigo',
        'departamento': 'departamento_codigo'
    },
    'municipios': {
        'nombre': 'nombre',
        'codigo': 'codigo',
        'provincia': 'provincia_codigo'
    },
    'asientos': {
        'nombre': 'nombre',
        'codigo': 'codigo',
        'municipio': 'municipio_codigo'
    },
    'recintos': {
        'nombre': 'nombre',
        'direccion': 'direccion',
        'tipo': 'tipo',
        'asiento': 'asiento_codigo',
        'latitud': 'latitud',
        'longitud': 'longitud'
    },
    'vehiculos': {
        'placa': 'placa',
        'marca': 'marca',
        'modelo': 'modelo',
        'anio': 'anio'
    },
    'choferes': {
        'nombre': 'nombre',
        'cedula': 'cedula',
        'licencia': 'licencia',
        'telefono': 'telefono',
        'vehiculo': 'vehiculo_placa'
    },
    'operadores': {
        'nombre': 'nombre',
        'cedula': 'cedula',
        'telefono': 'telefono',
        'tipo': 'tipo_operador',
        'grupo': 'grupo_nombre',
        'recinto': 'recinto_nombre',
        'vehiculo': 'vehiculo_placa',
        'fecha_inicio': 'fecha_inicio',
        'fecha_fin': 'fecha_fin'
    }
}
