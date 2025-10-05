# ============================================
# config.py - CONFIGURACIÓN ACTUALIZADA
# ============================================

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
    'asientos_electorales': 'Asientos_Electorales',
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
        'jefe': 'jefe',
        'nombre': 'nombre',
        'ci': 'ci',
        'expedido': 'expedido', 
        'celular': 'celular',
        'correo': 'correo',
        'cargo': 'cargo'
    },
    'grupos': {
        'coordinador_ci': 'coordinador_ci',
        'nombre': 'nombre'
    },
    'departamentos': {
        'nombre': 'nombre'
    },
    'provincias': {
        'departamento': 'departamento',
        'nombre': 'nombre',
        'es_urbano': 'es_urbano'  # NUEVO: 1=urbano, 0=rural
    },
    'municipios': {
        'provincia': 'provincia',
        'nombre': 'nombre'
    },
    'asientos_electorales': {
        'municipio': 'municipio',
        'nombre': 'nombre'
    },
    'recintos': {
        'departamento': 'departamento',      # NUEVO
        'provincia': 'provincia',            # NUEVO
        'municipio': 'municipio',            # NUEVO
        'asiento_electoral': 'asiento_electoral',
        'nombre': 'nombre',
        'direccion': 'direccion',
        'distrito': 'distrito'
    },
    'operadores': {
        'grupo': 'grupo',
        'asiento_electoral': 'asiento_electoral',  # NUEVO
        'recinto': 'recinto',
        'nombre': 'nombre',
        'ci': 'ci',
        'expedido': 'expedido',
        'celular': 'celular',
        'correo': 'correo',
        'cargo': 'cargo'
        # ELIMINADO: 'tipo' (se calcula automáticamente)
    },
    'notarios': {
        'asiento_electoral': 'asiento_electoral',  # NUEVO
        'recinto': 'recinto',
        'nombre': 'nombre',
        'ci': 'ci',
        'expedido': 'expedido',
        'celular': 'celular',
        'correo': 'correo',
        'cargo': 'cargo'
        # ELIMINADO: 'tipo' (se calcula automáticamente)
    },
    'actas': {
        'asiento_electoral': 'asiento_electoral',  # NUEVO
        'recinto': 'recinto',
        'codigos': 'codigos'
    },
    'cuentas': {
        'operador': 'operador',
        'user': 'user',
        'password': 'password'
    }
}