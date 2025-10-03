# converters.py - Convertidores específicos por tipo de datos
from typing import Dict, List, Any, Optional
from database import DatabaseManager
from config import COLUMN_MAPPING

class DataConverters:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def _get_string_value(self, row: Dict, column_path: str, default: str = '') -> str:
        """Obtiene un valor como string, manejando diferentes tipos de datos"""
        try:
            value = row.get(column_path, default)
            if value is None:
                return default
            if isinstance(value, (int, float)):
                return str(value)
            return str(value).strip()
        except:
            return default
    
    def _get_int_value(self, row: Dict, column_path: str, default: int = 0) -> int:
        """Obtiene un valor como entero"""
        try:
            value = row.get(column_path, default)
            if value is None:
                return default
            if isinstance(value, str):
                return int(value.strip()) if value.strip() else default
            return int(value)
        except:
            return default

    def convert_jefes(self, data: List[Dict[str, Any]]):
        """Convierte datos de jefes"""
        print("👔 Procesando jefes...")
        count = 0
        
        for row in data:
            nombre = self._get_string_value(row, COLUMN_MAPPING['jefes']['nombre'])
            if not nombre:
                continue
                
            jefe_data = {
                'nombre': nombre,
                'cargo': self._get_string_value(row, COLUMN_MAPPING['jefes']['cargo']),
                'celular': self._get_string_value(row, COLUMN_MAPPING['jefes']['celular'])
            }
            
            self.db.insert_or_update('jefe', jefe_data, 'nombre')
            count += 1
        
        print(f"   ✅ {count} jefes procesados")
    
    def convert_coordinadores(self, data: List[Dict[str, Any]]):
        """Convierte datos de coordinadores"""
        print("👥 Procesando coordinadores...")
        count = 0
        
        for row in data:
            nombre = self._get_string_value(row, COLUMN_MAPPING['coordinadores']['nombre'])
            if not nombre:
                continue
            
            # Buscar jefe_id
            jefe_nombre = self._get_string_value(row, COLUMN_MAPPING['coordinadores']['jefe'])
            jefe_id = self.db.get_id_by_field('jefe', 'nombre', jefe_nombre) if jefe_nombre else None
            
            coord_data = {
                'jefe_id': jefe_id,
                'nombre': nombre,
                'ci': self._get_string_value(row, COLUMN_MAPPING['coordinadores']['ci']),
                'expedido': self._get_string_value(row, COLUMN_MAPPING['coordinadores']['expedido']),
                'celular': self._get_string_value(row, COLUMN_MAPPING['coordinadores']['celular']),
                'correo': self._get_string_value(row, COLUMN_MAPPING['coordinadores']['correo']),
                'cargo': self._get_string_value(row, COLUMN_MAPPING['coordinadores']['cargo'])
            }
            
            self.db.insert_or_update('coordinador', coord_data, 'ci')
            count += 1
        
        print(f"   ✅ {count} coordinadores procesados")
    
    def convert_grupos(self, data: List[Dict[str, Any]]):
        """Convierte datos de grupos"""
        print("🏢 Procesando grupos...")
        count = 0
        
        for row in data:
            nombre = self._get_string_value(row, COLUMN_MAPPING['grupos']['nombre'])
            if not nombre:
                continue
            
            # Buscar coordinador_id
            coord_ci = self._get_string_value(row, COLUMN_MAPPING['grupos']['coordinador_ci'])
            coord_id = self.db.get_id_by_field('coordinador', 'ci', coord_ci) if coord_ci else None
            
            grupo_data = {
                'coordinador_id': coord_id,
                'nombre': nombre
            }
            
            self.db.insert_or_update('grupo', grupo_data, 'nombre')
            count += 1
        
        print(f"   ✅ {count} grupos procesados")
    
    def convert_departamentos(self, data: List[Dict[str, Any]]):
        """Convierte departamentos"""
        print("🏛️  Procesando departamentos...")
        count = 0
        
        for row in data:
            nombre = self._get_string_value(row, COLUMN_MAPPING['departamentos']['nombre'])
            if not nombre:
                continue
                
            depto_data = {
                'nombre': nombre
            }
            
            self.db.insert_or_update('departamento', depto_data, 'nombre')
            count += 1
        
        print(f"   ✅ {count} departamentos procesados")
    
    def convert_provincias(self, data: List[Dict[str, Any]]):
        """Convierte provincias"""
        print("🌄 Procesando provincias...")
        count = 0
        
        for row in data:
            nombre = self._get_string_value(row, COLUMN_MAPPING['provincias']['nombre'])
            if not nombre:
                continue
            
            depto_nombre = self._get_string_value(row, COLUMN_MAPPING['provincias']['departamento'])
            depto_id = self.db.get_id_by_field('departamento', 'nombre', depto_nombre) if depto_nombre else None
            
            prov_data = {
                'departamento_id': depto_id,
                'nombre': nombre
            }
            
            self.db.insert_or_update('provincia', prov_data, 'nombre')
            count += 1
        
        print(f"   ✅ {count} provincias procesadas")
    
    def convert_municipios(self, data: List[Dict[str, Any]]):
        """Convierte municipios"""
        print("🏘️  Procesando municipios...")
        count = 0
        
        for row in data:
            nombre = self._get_string_value(row, COLUMN_MAPPING['municipios']['nombre'])
            if not nombre:
                continue
            
            prov_nombre = self._get_string_value(row, COLUMN_MAPPING['municipios']['provincia'])
            prov_id = self.db.get_id_by_field('provincia', 'nombre', prov_nombre) if prov_nombre else None
            
            mun_data = {
                'provincia_id': prov_id,
                'nombre': nombre
            }
            
            self.db.insert_or_update('municipio', mun_data, 'nombre')
            count += 1
        
        print(f"   ✅ {count} municipios procesados")
    
    def convert_asientos_electorales(self, data: List[Dict[str, Any]]):
        """Convierte asientos electorales"""
        print("🗳️  Procesando asientos electorales...")
        count = 0
        
        for row in data:
            nombre = self._get_string_value(row, COLUMN_MAPPING['asientos_electorales']['nombre'])
            if not nombre:
                continue
            
            mun_nombre = self._get_string_value(row, COLUMN_MAPPING['asientos_electorales']['municipio'])
            mun_id = self.db.get_id_by_field('municipio', 'nombre', mun_nombre) if mun_nombre else None
            
            asiento_data = {
                'municipio_id': mun_id,
                'nombre': nombre
            }
            
            self.db.insert_or_update('asiento_electoral', asiento_data, 'nombre')
            count += 1
        
        print(f"   ✅ {count} asientos procesados")
    
    


    def convert_recintos(self, data: List[Dict[str, Any]]):
        """Convierte recintos"""
        print("🏫 Procesando recintos...")
        count = 0
        skipped = 0
        duplicates = 0
        
        for row in data:
            nombre = self._get_string_value(row, COLUMN_MAPPING['recintos']['nombre'])
            if not nombre:
                continue
            
            asiento_nombre = self._get_string_value(row, COLUMN_MAPPING['recintos']['asiento_electoral'])
            asiento_id = self.db.get_id_by_field('asiento_electoral', 'nombre', asiento_nombre) if asiento_nombre else None
            
            if not asiento_id:
                print(f"   ⚠️  Asiento electoral no encontrado: '{asiento_nombre}' para recinto '{nombre}'")
                skipped += 1
                continue
            
            recinto_data = {
                'asiento_id': asiento_id,
                'nombre': nombre,
                'direccion': self._get_string_value(row, COLUMN_MAPPING['recintos']['direccion']),
                'distrito': self._get_int_value(row, COLUMN_MAPPING['recintos']['distrito'])
            }
            
            # Verificar si ya existe un recinto con el mismo nombre Y asiento_id Y dirección
            existing_id = self._check_existing_recinto(recinto_data)
            
            if existing_id:
                # Si existe, actualizar
                self.db.update_record('recinto', recinto_data, existing_id)
                count += 1
            else:
                # Si no existe, insertar nuevo
                self.db.insert_record('recinto', recinto_data)
                count += 1
        
        print(f"   ✅ {count} recintos procesados")
        if skipped > 0:
            print(f"   ⚠️  {skipped} recintos omitidos (asiento no encontrado)")

    def _check_existing_recinto(self, recinto_data: Dict[str, Any]) -> Optional[int]:
        """Verifica si ya existe un recinto con los mismos datos clave"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id FROM recinto 
                WHERE nombre = ? AND asiento_id = ? AND direccion = ?
            """, (recinto_data['nombre'], recinto_data['asiento_id'], recinto_data['direccion']))
            result = cursor.fetchone()
            return result[0] if result else None

    
    
    def convert_operadores(self, data: List[Dict[str, Any]]):
        """Convierte operadores"""
        print("👷 Procesando operadores...")
        count = 0
        
        for row in data:
            ci = self._get_string_value(row, COLUMN_MAPPING['operadores']['ci'])
            if not ci:
                continue
            
            # Buscar IDs relacionados
            grupo_nombre = self._get_string_value(row, COLUMN_MAPPING['operadores']['grupo'])
            grupo_id = self.db.get_id_by_field('grupo', 'nombre', grupo_nombre) if grupo_nombre else None
            
            recinto_nombre = self._get_string_value(row, COLUMN_MAPPING['operadores']['recinto'])
            recinto_id = self.db.get_id_by_field('recinto', 'nombre', recinto_nombre) if recinto_nombre else None
            
            operador_data = {
                'grupo_id': grupo_id,
                'recinto_id': recinto_id,
                'nombre': self._get_string_value(row, COLUMN_MAPPING['operadores']['nombre']),
                'ci': ci,
                'expedido': self._get_string_value(row, COLUMN_MAPPING['operadores']['expedido']),
                'celular': self._get_string_value(row, COLUMN_MAPPING['operadores']['celular']),
                'correo': self._get_string_value(row, COLUMN_MAPPING['operadores']['correo']),
                'cargo': self._get_string_value(row, COLUMN_MAPPING['operadores']['cargo']),
                'tipo': self._get_string_value(row, COLUMN_MAPPING['operadores']['tipo'], 'urbano').lower()
            }
            
            self.db.insert_or_update('operador', operador_data, 'ci')
            count += 1
        
        print(f"   ✅ {count} operadores procesados")
    
    def convert_notarios(self, data: List[Dict[str, Any]]):
        """Convierte notarios"""
        print("📝 Procesando notarios...")
        count = 0
        
        for row in data:
            ci = self._get_string_value(row, COLUMN_MAPPING['notarios']['ci'])
            if not ci:
                continue
            
            recinto_nombre = self._get_string_value(row, COLUMN_MAPPING['notarios']['recinto'])
            recinto_id = self.db.get_id_by_field('recinto', 'nombre', recinto_nombre) if recinto_nombre else None
            
            notario_data = {
                'recinto_id': recinto_id,
                'nombre': self._get_string_value(row, COLUMN_MAPPING['notarios']['nombre']),
                'ci': ci,
                'expedido': self._get_string_value(row, COLUMN_MAPPING['notarios']['expedido']),
                'celular': self._get_string_value(row, COLUMN_MAPPING['notarios']['celular']),
                'correo': self._get_string_value(row, COLUMN_MAPPING['notarios']['correo']),
                'cargo': self._get_string_value(row, COLUMN_MAPPING['notarios']['cargo']),
                'tipo': self._get_string_value(row, COLUMN_MAPPING['notarios']['tipo'], 'urbano').lower()
            }
            
            self.db.insert_or_update('notario', notario_data, 'ci')
            count += 1
        
        print(f"   ✅ {count} notarios procesados")
    
    def convert_actas(self, data: List[Dict[str, Any]]):
        """Convierte actas SOLO con recinto"""
        print("📄 Procesando actas...")
        count = 0
        skipped = 0
        
        # ✅ DEBUG: Mostrar primeros registros
        #print("   🔍 DEBUG - Primeros registros:")
        for i, row in enumerate(data[:3]):  # Mostrar solo 3
            recinto_valor = self._get_string_value(row, COLUMN_MAPPING['actas']['recinto'])
            codigo_valor = self._get_string_value(row, COLUMN_MAPPING['actas']['codigo'])
            #print(f"      Registro {i+1}: recinto='{recinto_valor}', codigo='{codigo_valor}'")
            #print(f"      Campos disponibles: {list(row.keys())}")
        
        for row in data:
            codigo = self._get_string_value(row, COLUMN_MAPPING['actas']['codigo'])
            if not codigo:
                continue
            
            # Buscar SOLO recinto_id
            recinto_nombre = self._get_string_value(row, COLUMN_MAPPING['actas']['recinto'])
            
            # ✅ DEBUG: Mostrar qué está buscando
            # print(f"   🔍 Buscando recinto: '{recinto_nombre}'")
            
            recinto_id = self.db.get_id_by_field('recinto', 'nombre', recinto_nombre)
            
            if not recinto_id:
                print(f"   ⚠️  Acta '{codigo}' omitida - recinto '{recinto_nombre}' no encontrado")
                skipped += 1
                continue
            
            acta_data = {
                'recinto_id': recinto_id,
                'codigo': codigo
            }
            
            self.db.insert_or_update('acta', acta_data, 'codigo')
            count += 1
        
        print(f"   ✅ {count} actas procesadas")
        if skipped > 0:
            print(f"   ⚠️  {skipped} actas omitidas (recinto no encontrado)")

    def convert_cuentas(self, data: List[Dict[str, Any]]):
        """Convierte cuentas de usuario"""
        print("👤 Procesando cuentas...")
        count = 0
        
        for row in data:
            user = self._get_string_value(row, COLUMN_MAPPING['cuentas']['user'])
            if not user:
                continue
            
            operador_ci = self._get_string_value(row, COLUMN_MAPPING['cuentas']['operador'])
            operador_id = self.db.get_id_by_field('operador', 'ci', operador_ci) if operador_ci else None
            
            cuenta_data = {
                'operador_id': operador_id,
                'user': user,
                'password': self._get_string_value(row, COLUMN_MAPPING['cuentas']['password'])
            }
            
            self.db.insert_or_update('cuenta', cuenta_data, 'user')
            count += 1
        
        print(f"   ✅ {count} cuentas procesadas")