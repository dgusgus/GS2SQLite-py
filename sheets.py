# sheets.py - Manejo de Google Sheets
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict
from config import CREDENTIALS_FILE, SPREADSHEET_ID, SHEET_NAMES

class SheetsManager:
    def __init__(self, credentials_file: str = CREDENTIALS_FILE, spreadsheet_id: str = SPREADSHEET_ID):
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.client = None
        self._connect()
    
    def _connect(self):
        """Conecta con Google Sheets"""
        try:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive.readonly'
            ]
            
            creds = Credentials.from_service_account_file(self.credentials_file, scopes=scopes)
            self.client = gspread.authorize(creds)
            print("✅ Conectado a Google Sheets")
            
        except FileNotFoundError:
            print(f"❌ Archivo de credenciales no encontrado: {self.credentials_file}")
            print("   Coloca el archivo en la carpeta del proyecto")
            raise
        except Exception as e:
            print(f"❌ Error conectando con Google Sheets: {e}")
            raise
    
    def get_sheet_data(self, sheet_name: str) -> List[Dict[str, str]]:
        """Obtiene datos de una hoja específica"""
        try:
            spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            worksheet = spreadsheet.worksheet(sheet_name)
            
            data = worksheet.get_all_records()
            print(f"📊 {sheet_name}: {len(data)} registros")
            return data
            
        except gspread.WorksheetNotFound:
            print(f"⚠️  Hoja '{sheet_name}' no encontrada - saltando")
            return []
        except Exception as e:
            print(f"❌ Error en hoja '{sheet_name}': {e}")
            return []
    
    def list_sheets(self) -> List[str]:
        """Lista todas las hojas disponibles"""
        try:
            spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            sheets = [ws.title for ws in spreadsheet.worksheets()]
            print(f"📋 Hojas disponibles: {sheets}")
            return sheets
        except Exception as e:
            print(f"❌ Error listando hojas: {e}")
            return []