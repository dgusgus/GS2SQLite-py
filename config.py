# ============================================
# config.py
# Cambios v2:
#   - 'grupos' eliminado como hoja separada → fusionado en coordinador
#   - 'cuentas' eliminado como hoja separada → columnas en hoja Operadores
# ============================================

# === GOOGLE SHEETS ===
SPREADSHEET_ID   = "1ehySw2tVI1l8INo4fgE7kEGFd0Kb2miPs7vCqsFZC8I"
CREDENTIALS_FILE = "generador-docs-31f4b831a196.json"

# === BASE DE DATOS ===
DATABASE_PATH = "../database/operadores.db"

# === HOJAS DEL GOOGLE SHEET ===
# 'grupos' ya no existe: cada coordinador tiene una columna 'nombre_grupo'
# 'cuentas' ya no existe: user/password van directo en la hoja Operadores
SHEET_NAMES = {
    'jefes':                'Jefes',
    'coordinadores':        'Coordinadores',   # ahora incluye columna nombre_grupo
    'departamentos':        'Departamentos',
    'provincias':           'Provincias',
    'municipios':           'Municipios',
    'asientos_electorales': 'Asientos_Electorales',
    'recintos':             'Recintos',
    'operadores':           'Operadores',      # ahora incluye columnas user y password
    'notarios':             'Notarios',
    'actas':                'Actas',
}

# === MAPEO DE COLUMNAS ===
COLUMN_MAPPING = {
    'jefes': {
        'nombre':  'nombre',
        'cargo':   'cargo',
        'celular': 'celular',
    },

    # Coordinadores ahora lleva nombre_grupo (antes era hoja aparte)
    'coordinadores': {
        'jefe':         'jefe',
        'nombre':       'nombre',
        'ci':           'ci',
        'expedido':     'expedido',
        'celular':      'celular',
        'correo':       'correo',
        'cargo':        'cargo',
        'nombre_grupo': 'nombre_grupo',   # ← nuevo: reemplaza hoja Grupos
    },

    'departamentos': {
        'nombre': 'nombre',
    },
    'provincias': {
        'departamento': 'departamento',
        'nombre':       'nombre',
        'es_urbano':    'es_urbano',
    },
    'municipios': {
        'provincia': 'provincia',
        'nombre':    'nombre',
    },
    'asientos_electorales': {
        'municipio': 'municipio',
        'nombre':    'nombre',
    },
    'recintos': {
        'departamento':      'departamento',
        'provincia':         'provincia',
        'municipio':         'municipio',
        'asiento_electoral': 'asiento_electoral',
        'nombre':            'nombre',
        'direccion':         'direccion',
        'distrito':          'distrito',
    },

    # Operadores ahora incluye user/password (antes era hoja Cuentas)
    'operadores': {
        'coordinador_ci':    'coordinador_ci',    # ← nuevo: asignación directa al coordinador
        'asiento_electoral': 'asiento_electoral',
        'recinto':           'recinto',
        'nombre':            'nombre',
        'ci':                'ci',
        'expedido':          'expedido',
        'celular':           'celular',
        'correo':            'correo',
        'cargo':             'cargo',
        'user':              'user',              # ← fusionado desde hoja Cuentas
        'password':          'password',          # ← fusionado desde hoja Cuentas
    },

    'notarios': {
        'asiento_electoral': 'asiento_electoral',
        'recinto':           'recinto',
        'nombre':            'nombre',
        'ci':                'ci',
        'expedido':          'expedido',
        'celular':           'celular',
        'correo':            'correo',
        'cargo':             'cargo',
    },

    # Actas: solo lo esencial
    'actas': {
        'operador_ci': 'operador_ci',
        'codigos':     'codigos',
    },
}