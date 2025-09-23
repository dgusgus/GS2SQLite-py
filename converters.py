# converters.py - Convertidores específicos por tipo de datos
from typing import Dict, List, Any
from database import DatabaseManager
from config import COLUMN_MAPPING

class DataConverters:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def convert_jefes(self, data: List[Dict[str, str]]):
        """Convierte datos de jefes"""
        print("👔 Procesando jefes...")
        count = 0
        
        for row in data:
            if not row.get(COLUMN_MAPPING['jefes']['nombre'], '').strip():
                continue
                
            jefe_data = {
                'nombre': row.get(COLUMN_MAPPING['jefes']['nombre'], '').strip(),
                'telefono': row.get(COLUMN_MAPPING['jefes']['telefono'], '').strip(),
                'email': row.get(COLUMN_MAPPING['jefes']['email'], '').strip()
            }
            
            self.db.insert_or_update('jefe', jefe_data, 'nombre')
            count += 1
        
        print(f"   ✅ {count} jefes procesados")
    
    def convert_coordinadores(self, data: List[Dict[str, str]]):
        """Convierte datos de coordinadores"""
        print("👥 Procesando coordinadores...")
        count = 0
        
        for row in data:
            if not row.get(COLUMN_MAPPING['coordinadores']['codigo'], '').strip():
                continue
            
            # Buscar jefe_id
            jefe_nombre = row.get(COLUMN_MAPPING['coordinadores']['jefe'], '').strip()
            jefe_id = self.db.get_id_by_field('jefe', 'nombre', jefe_nombre) if jefe_nombre else None
            
            coord_data = {
                'jefe_id': jefe_id,
                'nombre': row.get(COLUMN_MAPPING['coordinadores']['nombre'], '').strip(),
                'codigo_coordinador': row.get(COLUMN_MAPPING['coordinadores']['codigo'], '').strip(),
                'telefono': row.get(COLUMN_MAPPING['coordinadores']['telefono'], '').strip(),
                'email': row.get(COLUMN_MAPPING['coordinadores']['email'], '').strip()
            }
            
            self.db.insert_or_update('coordinador', coord_data, 'codigo_coordinador')
            count += 1
        
        print(f"   ✅ {count} coordinadores procesados")
    
    def convert_grupos(self, data: List[Dict[str, str]]):
        """Convierte datos de grupos"""
        print("🏢 Procesando grupos...")
        count = 0
        
        for row in data:
            if not row.get(COLUMN_MAPPING['grupos']['nombre'], '').strip():
                continue
            
            # Buscar coordinador_id
            coord_codigo = row.get(COLUMN_MAPPING['grupos']['coordinador'], '').strip()
            coord_id = self.db.get_id_by_field('coordinador', 'codigo_coordinador', coord_codigo) if coord_codigo else None
            
            grupo_data = {
                'coordinador_id': coord_id,
                'nombre_grupo': row.get(COLUMN_MAPPING['grupos']['nombre'], '').strip(),
                'descripcion': row.get(COLUMN_MAPPING['grupos']['descripcion'], '').strip()
            }
            
            self.db.insert_or_update('grupo', grupo_data, 'nombre_grupo')
            count += 1
        
        print(f"   ✅ {count} grupos procesados")
    
    def convert_departamentos(self, data: List[Dict[str, str]]):
        """Convierte departamentos"""
        print("🏛️  Procesando departamentos...")
        count = 0
        
        for row in data:
            if not row.get(COLUMN_MAPPING['departamentos']['codigo'], '').strip():
                continue
                
            depto_data = {
                'nombre': row.get(COLUMN_MAPPING['departamentos']['nombre'], '').strip(),
                'codigo': row.get(COLUMN_MAPPING['departamentos']['codigo'], '').strip()
            }
            
            self.db.insert_or_update('departamento', depto_data, 'codigo')
            count += 1
        
        print(f"   ✅ {count} departamentos procesados")
    
    def convert_provincias(self, data: List[Dict[str, str]]):
        """Convierte provincias"""
        print("🌄 Procesando provincias...")
        count = 0
        
        for row in data:
            if not row.get(COLUMN_MAPPING['provincias']['codigo'], '').strip():
                continue
            
            depto_codigo = row.get(COLUMN_MAPPING['provincias']['departamento'], '').strip()
            depto_id = self.db.get_id_by_field('departamento', 'codigo', depto_codigo) if depto_codigo else None
            
            prov_data = {
                'depto_id': depto_id,
                'nombre': row.get(COLUMN_MAPPING['provincias']['nombre'], '').strip(),
                'codigo': row.get(COLUMN_MAPPING['provincias']['codigo'], '').strip()
            }
            
            self.db.insert_or_update('provincia', prov_data, 'codigo')
            count += 1
        
        print(f"   ✅ {count} provincias procesadas")
    
    def convert_municipios(self, data: List[Dict[str, str]]):
        """Convierte municipios"""
        print("🏘️  Procesando municipios...")
        count = 0
        
        for row in data:
            if not row.get(COLUMN_MAPPING['municipios']['codigo'], '').strip():
                continue
            
            prov_codigo = row.get(COLUMN_MAPPING['municipios']['provincia'], '').strip()
            prov_id = self.db.get_id_by_field('provincia', 'codigo', prov_codigo) if prov_codigo else None
            
            mun_data = {
                'provincia_id': prov_id,
                'nombre': row.get(COLUMN_MAPPING['municipios']['nombre'], '').strip(),
                'codigo': row.get(COLUMN_MAPPING['municipios']['codigo'], '').strip()
            }
            
            self.db.insert_or_update('municipio', mun_data, 'codigo')
            count += 1
        
        print(f"   ✅ {count} municipios procesados")
    
    def convert_asientos(self, data: List[Dict[str, str]]):
        """Convierte asientos electorales"""
        print("🗳️  Procesando asientos electorales...")
        count = 0
        
        for row in data:
            if not row.get(COLUMN_MAPPING['asientos']['codigo'], '').strip():
                continue
            
            mun_codigo = row.get(COLUMN_MAPPING['asientos']['municipio'], '').strip()
            mun_id = self.db.get_id_by_field('municipio', 'codigo', mun_codigo) if mun_codigo else None
            
            asiento_data = {
                'municipio_id': mun_id,
                'nombre': row.get(COLUMN_MAPPING['asientos']['nombre'], '').strip(),
                'codigo': row.get(COLUMN_MAPPING['asientos']['codigo'], '').strip()
            }
            
            self.db.insert_or_update('asiento_electoral', asiento_data, 'codigo')
            count += 1
        
        print(f"   ✅ {count} asientos procesados")
    
    def convert_recintos(self, data: List[Dict[str, str]]):
        """Convierte recintos"""
        print("🏫 Procesando recintos...")
        count = 0
        
        for row in data:
            if not row.get(COLUMN_MAPPING['recintos']['nombre'], '').strip():
                continue
            
            asiento_codigo = row.get(COLUMN_MAPPING['recintos']['asiento'], '').strip()
            asiento_id = self.db.get_id_by_field('asiento_electoral', 'codigo', asiento_codigo) if asiento_codigo else None
            
            recinto_data = {
                'asiento_id': asiento_id,
                'nombre': row.get(COLUMN_MAPPING['recintos']['nombre'], '').strip(),
                'direccion': row.get(COLUMN_MAPPING['recintos']['direccion'], '').strip(),
                'tipo': row.get(COLUMN_MAPPING['recintos']['tipo'], 'urbano').lower(),
                'latitud': float(row.get(COLUMN_MAPPING['recintos']['latitud'], 0) or 0),
                'longitud': float(row.get(COLUMN_MAPPING['recintos']['longitud'], 0) or 0)
            }
            
            self.db.insert_or_update('recinto', recinto_data, 'nombre')
            count += 1
        
        print(f"   ✅ {count} recintos procesados")
    
    def convert_vehiculos(self, data: List[Dict[str, str]]):
        """Convierte vehículos"""
        print("🚗 Procesando vehículos...")
        count = 0
        
        for row in data:
            if not row.get(COLUMN_MAPPING['vehiculos']['placa'], '').strip():
                continue
            
            vehiculo_data = {
                'placa': row.get(COLUMN_MAPPING['vehiculos']['placa'], '').strip().upper(),
                'modelo': row.get(COLUMN_MAPPING['vehiculos']['modelo'], '').strip(),
                'marca': row.get(COLUMN_MAPPING['vehiculos']['marca'], '').strip(),
                'anio': int(row.get(COLUMN_MAPPING['vehiculos']['anio'], 0) or 0),
                'estado': 'activo'
            }
            
            self.db.insert_or_update('vehiculo', vehiculo_data, 'placa')
            count += 1
        
        print(f"   ✅ {count} vehículos procesados")
    
    def convert_choferes(self, data: List[Dict[str, str]]):
        """Convierte choferes"""
        print("🚛 Procesando choferes...")
        count = 0
        
        for row in data:
            if not row.get(COLUMN_MAPPING['choferes']['cedula'], '').strip():
                continue
            
            placa = row.get(COLUMN_MAPPING['choferes']['vehiculo'], '').strip().upper()
            vehiculo_id = self.db.get_id_by_field('vehiculo', 'placa', placa) if placa else None
            
            chofer_data = {
                'vehiculo_id': vehiculo_id,
                'nombre': row.get(COLUMN_MAPPING['choferes']['nombre'], '').strip(),
                'cedula': row.get(COLUMN_MAPPING['choferes']['cedula'], '').strip(),
                'licencia': row.get(COLUMN_MAPPING['choferes']['licencia'], '').strip(),
                'telefono': row.get(COLUMN_MAPPING['choferes']['telefono'], '').strip()
            }
            
            self.db.insert_or_update('chofer', chofer_data, 'cedula')
            count += 1
        
        print(f"   ✅ {count} choferes procesados")
    
    def convert_operadores(self, data: List[Dict[str, str]]):
        """Convierte operadores"""
        print("👷 Procesando operadores...")
        count = 0
        
        for row in data:
            if not row.get(COLUMN_MAPPING['operadores']['cedula'], '').strip():
                continue
            
            # Buscar IDs relacionados
            grupo_nombre = row.get(COLUMN_MAPPING['operadores']['grupo'], '').strip()
            grupo_id = self.db.get_id_by_field('grupo', 'nombre_grupo', grupo_nombre) if grupo_nombre else None
            
            recinto_nombre = row.get(COLUMN_MAPPING['operadores']['recinto'], '').strip()
            recinto_id = self.db.get_id_by_field('recinto', 'nombre', recinto_nombre) if recinto_nombre else None
            
            placa = row.get(COLUMN_MAPPING['operadores']['vehiculo'], '').strip().upper()
            vehiculo_id = self.db.get_id_by_field('vehiculo', 'placa', placa) if placa else None
            
            operador_data = {
                'grupo_id': grupo_id,
                'recinto_id': recinto_id,
                'vehiculo_id': vehiculo_id,
                'nombre': row.get(COLUMN_MAPPING['operadores']['nombre'], '').strip(),
                'cedula': row.get(COLUMN_MAPPING['operadores']['cedula'], '').strip(),
                'telefono': row.get(COLUMN_MAPPING['operadores']['telefono'], '').strip(),
                'tipo_operador': row.get(COLUMN_MAPPING['operadores']['tipo'], 'urbano').lower(),
                'fecha_inicio': row.get(COLUMN_MAPPING['operadores']['fecha_inicio'], ''),
                'fecha_fin': row.get(COLUMN_MAPPING['operadores']['fecha_fin'], ''),
                'estado': 'activo'
            }
            
            self.db.insert_or_update('operador', operador_data, 'cedula')
            count += 1
        
        print(f"   ✅ {count} operadores procesados")