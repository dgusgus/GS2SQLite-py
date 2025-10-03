# config.py - Configuraciones centralizadas
import os

# === CONFIGURACIÓN GOOGLE SHEETS ===
SPREADSHEET_ID = "1ehySw2tVI1l8INo4fgE7kEGFd0Kb2miPs7vCqsFZC8I"
CREDENTIALS_FILE = "generador-docs-31f4b831a196.json"

# === CONFIGURACIÓN BASE DE DATOS ===
DATABASE_PATH = "../database/operadores.db"

# === MAPEO DE HOJAS GOOGLE SHEETS ===
SHEET_NAMES = {
    'jefes': 'Jefes',
    'coordinadores': 'Coordinadores', 
    'grupos': 'Grupos',
    'departamentos': 'Departamentos',
    'provincias': 'Provincias',
    'municipios': 'Municipios',
    'asientos_electorales': 'Asientos_Electorales',  # Cambiado a plural
    'recintos': 'Recintos',
    'operadores': 'Operadores',
    'notarios': 'Notarios',
    'actas': 'Actas',
    'cuentas': 'Cuentas'
}

# === MAPEO DE COLUMNAS ACTUALIZADO ===
COLUMN_MAPPING = {
    'jefes': {
        'nombre': 'nombre',
        'cargo': 'cargo',
        'celular': 'celular'
    },
    'coordinadores': {
        'jefe': 'jefe',  # Cambiado de 'jefe_nombre'
        'nombre': 'nombre',
        'ci': 'ci',
        'expedido': 'expedido', 
        'celular': 'celular',
        'correo': 'correo',
        'cargo': 'cargo'
    },
    'grupos': {
        'coordinador_ci': 'coordinador_ci',  # Cambiado de 'coordinador_nombre'
        'nombre': 'nombre'
    },
    'departamentos': {
        'nombre': 'nombre'
    },
    'provincias': {
        'departamento': 'departamento',  # Cambiado de 'departamento_nombre'
        'nombre': 'nombre'
    },
    'municipios': {
        'provincia': 'provincia',  # Cambiado de 'provincia_nombre'
        'nombre': 'nombre'
    },
    'asientos_electorales': {  # Cambiado de 'asientos'
        'municipio': 'municipio',  # Cambiado de 'municipio_nombre'
        'nombre': 'nombre'
    },
    'recintos': {
        'asiento_electoral': 'asiento_electoral',  # Cambiado de 'asiento'
        'nombre': 'nombre',
        'direccion': 'direccion',
        'distrito': 'distrito'
    },
    'operadores': {
        'grupo': 'grupo',  # Cambiado de 'grupo_nombre'
        'recinto': 'recinto',  # Cambiado de 'recinto_nombre'
        'nombre': 'nombre',
        'ci': 'ci',
        'expedido': 'expedido',
        'celular': 'celular',
        'correo': 'correo',
        'cargo': 'cargo',
        'tipo': 'tipo'  # Cambiado de 'tipo_operador'
    },
    'notarios': {
        'recinto': 'recinto',  # Cambiado de 'recinto_nombre'
        'nombre': 'nombre',
        'ci': 'ci',
        'expedido': 'expedido',
        'celular': 'celular',
        'correo': 'correo',
        'cargo': 'cargo',
        'tipo': 'tipo'  # Cambiado de 'tipo_notario'
    },
    'actas': {
        'recinto': 'recinto',  # Cambiado de 'mesa_numero'
        'codigo': 'codigo'
    },
    'cuentas': {
        'operador': 'operador',  # Cambiado de 'operador_nombre' (ahora usa CI)
        'user': 'user',  # Cambiado de 'usuario'
        'password': 'password'
    }
}