# converters.py - Convertidores específicos por tipo de datos
from typing import Dict, List, Any, Optional
from database import DatabaseManager
from config import COLUMN_MAPPING

class DataConverters:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def _get_string_value(self, row: Dict, column_path: str, default: str = '') -> str:
        """Obtiene valor como string"""
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
        """Obtiene valor como entero"""
        try:
            value = row.get(column_path, default)
            if value is None:
                return default
            if isinstance(value, str):
                return int(value.strip()) if value.strip() else default
            return int(value)
        except:
            return default
    
    def _get_bool_value(self, row: Dict, column_path: str, default: bool = False) -> bool:
        """Obtiene valor como booleano"""
        try:
            value = row.get(column_path, default)
            if value is None:
                return default
            if isinstance(value, str):
                return value.strip().lower() in ['1', 'true', 'si', 'sí', 'yes']
            return bool(value)
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
        """Convierte provincias con clasificación urbano/rural"""
        print("Procesando provincias...")
        count = 0
        
        for row in data:
            nombre = self._get_string_value(row, COLUMN_MAPPING['provincias']['nombre'])
            if not nombre:
                continue
            
            depto_nombre = self._get_string_value(row, COLUMN_MAPPING['provincias']['departamento'])
            depto_id = self.db.get_id_by_field('departamento', 'nombre', depto_nombre) if depto_nombre else None
            
            # Detectar si es urbano (Cercado) o rural
            es_urbano = self._get_bool_value(row, COLUMN_MAPPING['provincias']['es_urbano'])
            
            prov_data = {
                'departamento_id': depto_id,
                'nombre': nombre,
                'es_urbano': 1 if es_urbano else 0
            }
            
            self.db.insert_or_update('provincia', prov_data, 'nombre')
            count += 1
        
        print(f"   {count} provincias procesadas")

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
        """Convierte recintos usando clave compuesta (asiento + nombre)"""
        print("Procesando recintos...")
        inserted = 0
        updated = 0
        skipped = 0
        
        for row in data:
            nombre = self._get_string_value(row, COLUMN_MAPPING['recintos']['nombre'])
            if not nombre:
                continue
            
            asiento_nombre = self._get_string_value(row, COLUMN_MAPPING['recintos']['asiento_electoral'])
            asiento_id = self.db.get_id_by_field('asiento_electoral', 'nombre', asiento_nombre) if asiento_nombre else None
            
            if not asiento_id:
                print(f"   Asiento '{asiento_nombre}' no encontrado para recinto '{nombre}'")
                skipped += 1
                continue
            
            # Verificar si ya existe (por clave compuesta)
            existing_id = self.db.get_recinto_id_by_asiento_and_nombre(asiento_nombre, nombre)
            
            recinto_data = {
                'asiento_id': asiento_id,
                'nombre': nombre,
                'direccion': self._get_string_value(row, COLUMN_MAPPING['recintos']['direccion']),
                'distrito': self._get_int_value(row, COLUMN_MAPPING['recintos']['distrito'])
            }
            
            if existing_id:
                self.db.update_record('recinto', recinto_data, existing_id)
                updated += 1
            else:
                self.db.insert_record('recinto', recinto_data)
                inserted += 1
        
        print(f"   {inserted} nuevos, {updated} actualizados, {skipped} omitidos")
  
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
        """Convierte operadores usando asiento_electoral + recinto"""
        print("Procesando operadores...")
        count = 0
        errors = 0
        
        for row in data:
            ci = self._get_string_value(row, COLUMN_MAPPING['operadores']['ci'])
            if not ci:
                continue
            
            # Buscar grupo
            grupo_nombre = self._get_string_value(row, COLUMN_MAPPING['operadores']['grupo'])
            grupo_id = self.db.get_id_by_field('grupo', 'nombre', grupo_nombre) if grupo_nombre else None
            
            # Buscar recinto por clave compuesta
            asiento_nombre = self._get_string_value(row, COLUMN_MAPPING['operadores']['asiento_electoral'])
            recinto_nombre = self._get_string_value(row, COLUMN_MAPPING['operadores']['recinto'])
            recinto_id = self.db.get_recinto_id_by_asiento_and_nombre(asiento_nombre, recinto_nombre)
            
            if not recinto_id:
                print(f"   Recinto '{recinto_nombre}' en '{asiento_nombre}' no encontrado para operador CI {ci}")
                errors += 1
                continue
            
            operador_data = {
                'grupo_id': grupo_id,
                'recinto_id': recinto_id,
                'nombre': self._get_string_value(row, COLUMN_MAPPING['operadores']['nombre']),
                'ci': ci,
                'expedido': self._get_string_value(row, COLUMN_MAPPING['operadores']['expedido']),
                'celular': self._get_string_value(row, COLUMN_MAPPING['operadores']['celular']),
                'correo': self._get_string_value(row, COLUMN_MAPPING['operadores']['correo']),
                'cargo': self._get_string_value(row, COLUMN_MAPPING['operadores']['cargo'])
            }
            
            self.db.insert_or_update('operador', operador_data, 'ci')
            count += 1
        
        print(f"   {count} operadores procesados, {errors} errores")



    def convert_notarios(self, data: List[Dict[str, Any]]):
        """Convierte notarios usando asiento_electoral + recinto"""
        print("Procesando notarios...")
        count = 0
        errors = 0
        
        for row in data:
            ci = self._get_string_value(row, COLUMN_MAPPING['notarios']['ci'])
            if not ci:
                continue
            
            asiento_nombre = self._get_string_value(row, COLUMN_MAPPING['notarios']['asiento_electoral'])
            recinto_nombre = self._get_string_value(row, COLUMN_MAPPING['notarios']['recinto'])
            recinto_id = self.db.get_recinto_id_by_asiento_and_nombre(asiento_nombre, recinto_nombre)
            
            if not recinto_id:
                print(f"   Recinto '{recinto_nombre}' en '{asiento_nombre}' no encontrado para notario CI {ci}")
                errors += 1
                continue
            
            notario_data = {
                'recinto_id': recinto_id,
                'nombre': self._get_string_value(row, COLUMN_MAPPING['notarios']['nombre']),
                'ci': ci,
                'expedido': self._get_string_value(row, COLUMN_MAPPING['notarios']['expedido']),
                'celular': self._get_string_value(row, COLUMN_MAPPING['notarios']['celular']),
                'correo': self._get_string_value(row, COLUMN_MAPPING['notarios']['correo']),
                'cargo': self._get_string_value(row, COLUMN_MAPPING['notarios']['cargo'])
            }
            
            self.db.insert_or_update('notario', notario_data, 'ci')
            count += 1
        
        print(f"   {count} notarios procesados, {errors} errores")


    def convert_actas(self, data: List[Dict[str, Any]]):
        """Convierte actas usando asiento_electoral + recinto"""
        print("Procesando actas...")
        total_actas = 0
        recintos_procesados = 0
        skipped = 0
        
        for row in data:
            asiento_nombre = self._get_string_value(row, COLUMN_MAPPING['actas']['asiento_electoral'])
            recinto_nombre = self._get_string_value(row, COLUMN_MAPPING['actas']['recinto'])
            codigos_str = self._get_string_value(row, COLUMN_MAPPING['actas']['codigos'], '')
            
            if not codigos_str:
                skipped += 1
                continue
            
            recinto_id = self.db.get_recinto_id_by_asiento_and_nombre(asiento_nombre, recinto_nombre)
            if not recinto_id:
                print(f"   Recinto '{recinto_nombre}' en '{asiento_nombre}' no encontrado")
                skipped += 1
                continue
            
            codigos = self._separar_codigos(codigos_str)
            
            for codigo in codigos:
                if not codigo or not self._validar_codigo_acta(codigo):
                    continue
                    
                acta_data = {
                    'recinto_id': recinto_id,
                    'codigo': codigo
                }
                
                try:
                    self.db.insert_or_update('acta', acta_data, 'codigo')
                    total_actas
                    total_actas += 1
                except Exception as e:
                    print(f"   Error insertando acta '{codigo}': {e}")
            
            recintos_procesados += 1
        
        print(f"   {total_actas} actas en {recintos_procesados} recintos, {skipped} omitidos")
    
    def _separar_codigos(self, codigos_str: str) -> List[str]:
        """Separa códigos por diferentes delimitadores"""
        if not codigos_str or not codigos_str.strip():
            return []
        
        codigos_limpios = codigos_str.strip()
        separadores = [',', ';', '|', '\t', ' ']
        
        for sep in separadores:
            if sep in codigos_limpios:
                codigos = [c.strip() for c in codigos_limpios.split(sep) if c.strip()]
                if len(codigos) > 1:
                    return codigos
        
        return [codigos_limpios] if codigos_limpios else []
    
    def _validar_codigo_acta(self, codigo: str) -> bool:
        """Valida formato de código de acta"""
        if not codigo or not isinstance(codigo, str):
            return False
        
        codigo_limpio = codigo.strip()
        
        if len(codigo_limpio) < 3 or len(codigo_limpio) > 50:
            return False
        
        if not any(c.isalnum() for c in codigo_limpio):
            return False
        
        caracteres_peligrosos = ['<', '>', '"', "'", '\\', '/', '?', '*']
        if any(caracter in codigo_limpio for caracter in caracteres_peligrosos):
            return False
        
        return True
    
    def convert_cuentas(self, data: List[Dict[str, Any]]):
        """Convierte cuentas de usuario"""
        print("Procesando cuentas...")
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
        
        print(f"   {count} cuentas procesadas")
    
    # Métodos convert_jefes, convert_coordinadores, convert_grupos, 
    # convert_departamentos, convert_municipios, convert_asientos_electorales
    # permanecen igual que en tu versión original


