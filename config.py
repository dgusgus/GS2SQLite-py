# config.py - Configuraciones centralizadas
import os
from pathlib import Path

# Configuración de Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

# IDs y rutas
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', "1ehySw2tVI1l8INo4fgE7kEGFd0Kb2miPs7vCqsFZC8I")
CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH', "generador-docs-31f4b831a196.json")
DATABASE_PATH = os.getenv('DATABASE_PATH', "../database/operadores.db")

# Configuración de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# Mapeo de hojas esperadas en Google Sheets
EXPECTED_SHEETS = {
    'jefes': 'Jefes',
    'coordinadores': 'Coordinadores', 
    'grupos': 'Grupos',
    'departamentos': 'Departamentos',
    'provincias': 'Provincias',
    'municipios': 'Municipios',
    'asientos_electorales': 'Asientos Electorales',
    'recintos': 'Recintos',
    'vehiculos': 'Vehículos',
    'choferes': 'Choferes',
    'operadores': 'Operadores'
}