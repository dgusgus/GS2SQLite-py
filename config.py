# ============================================
# config.py - ACTUALIZADO PARA ESQUEMA SIMPLIFICADO
# ============================================

# === GOOGLE SHEETS ===
SPREADSHEET_ID  = "1ehySw2tVI1l8INo4fgE7kEGFd0Kb2miPs7vCqsFZC8I"
CREDENTIALS_FILE = "generador-docs-31f4b831a196.json"

# === BASE DE DATOS ===
DATABASE_PATH = "../database/operadores.db"

# === HOJAS DEL GOOGLE SHEET ===
SHEET_NAMES = {
    'jefes':                'Jefes',
    'coordinadores':        'Coordinadores',
    'grupos':               'Grupos',
    'departamentos':        'Departamentos',
    'provincias':           'Provincias',
    'municipios':           'Municipios',
    'asientos_electorales': 'Asientos_Electorales',
    'recintos':             'Recintos',
    'operadores':           'Operadores',
    'notarios':             'Notarios',
    'actas':                'Actas',
    'cuentas':              'Cuentas',   # se fusiona en persona, hoja sigue existiendo
}

# === MAPEO DE COLUMNAS ===
COLUMN_MAPPING = {
    'jefes': {
        'nombre':  'nombre',
        'cargo':   'cargo',
        'celular': 'celular',
    },
    'coordinadores': {
        'jefe':     'jefe',
        'nombre':   'nombre',
        'ci':       'ci',
        'expedido': 'expedido',
        'celular':  'celular',
        'correo':   'correo',
        'cargo':    'cargo',
    },
    'grupos': {
        'coordinador_ci': 'coordinador_ci',
        'nombre':         'nombre',
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
    # operadores y notarios comparten estructura similar
    'operadores': {
        'grupo':             'grupo',
        'asiento_electoral': 'asiento_electoral',
        'recinto':           'recinto',
        'nombre':            'nombre',
        'ci':                'ci',
        'expedido':          'expedido',
        'celular':           'celular',
        'correo':            'correo',
        'cargo':             'cargo',
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
    'actas': {
        'asiento_electoral': 'asiento_electoral',
        'recinto':           'recinto',
        'operador_ci':       'operador_ci',
        'codigos':           'codigos',
    },
    # cuentas: aún se lee desde su hoja y se fusiona en persona
    'cuentas': {
        'operador': 'operador',   # CI del operador
        'user':     'user',
        'password': 'password',
    },
}