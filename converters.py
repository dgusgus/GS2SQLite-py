# ============================================
# converters.py
# Cambios v2:
#   - convert_grupos() eliminado
#   - convert_coordinadores() ahora guarda nombre_grupo
#   - convert_personas(): recibe coordinadores_data para resolver coordinador_ci
#                         user/password vienen directo en operadores_data
#   - convert_actas(): solo codigo + persona_id
# ============================================

from typing import Dict, List, Any, Optional
from database import DatabaseManager
from config import COLUMN_MAPPING


class DataConverters:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    # ── UTILIDADES ────────────────────────────────────────────────────

    def _str(self, row: Dict, key: str, default: str = '') -> str:
        value = row.get(key, default)
        if value is None:
            return default
        if isinstance(value, (int, float)):
            return str(value)
        return str(value).strip()

    def _int(self, row: Dict, key: str, default: int = 0) -> int:
        try:
            value = row.get(key, default)
            if value is None:
                return default
            return int(str(value).strip()) if str(value).strip() else default
        except (ValueError, TypeError):
            return default

    def _bool(self, row: Dict, key: str, default: bool = False) -> bool:
        try:
            value = row.get(key, default)
            if value is None:
                return default
            return str(value).strip().lower() in ['1', 'true', 'si', 'sí', 'yes']
        except Exception:
            return default

    # ── ORGANIZACIÓN ──────────────────────────────────────────────────

    def convert_jefes(self, data: List[Dict[str, Any]]):
        print("👔 Procesando jefes...")
        count = 0
        for row in data:
            nombre = self._str(row, COLUMN_MAPPING['jefes']['nombre'])
            if not nombre:
                continue
            self.db.insert_or_update('jefe', {
                'nombre':  nombre,
                'cargo':   self._str(row, COLUMN_MAPPING['jefes']['cargo']),
                'celular': self._str(row, COLUMN_MAPPING['jefes']['celular']),
            }, 'nombre')
            count += 1
        print(f"   ✅ {count} jefes procesados")

    def convert_coordinadores(self, data: List[Dict[str, Any]]):
        """
        Guarda coordinador con nombre_grupo incluido.
        Ya no existe tabla separada 'grupo'.
        """
        print("👥 Procesando coordinadores (con grupo)...")
        count = 0
        for row in data:
            ci = self._str(row, COLUMN_MAPPING['coordinadores']['ci'])
            if not ci:
                continue
            jefe_nombre = self._str(row, COLUMN_MAPPING['coordinadores']['jefe'])
            jefe_id = (
                self.db.get_id_by_field('jefe', 'nombre', jefe_nombre)
                if jefe_nombre else None
            )
            self.db.insert_or_update('coordinador', {
                'ci':           ci,
                'nombre':       self._str(row, COLUMN_MAPPING['coordinadores']['nombre']),
                'expedido':     self._str(row, COLUMN_MAPPING['coordinadores']['expedido']),
                'celular':      self._str(row, COLUMN_MAPPING['coordinadores']['celular']),
                'correo':       self._str(row, COLUMN_MAPPING['coordinadores']['correo']),
                'cargo':        self._str(row, COLUMN_MAPPING['coordinadores']['cargo']),
                'nombre_grupo': self._str(row, COLUMN_MAPPING['coordinadores']['nombre_grupo']),
                'jefe_id':      jefe_id,
            }, 'ci')
            count += 1
        print(f"   ✅ {count} coordinadores procesados")

    # ── GEOGRAFÍA ─────────────────────────────────────────────────────

    def convert_departamentos(self, data: List[Dict[str, Any]]):
        print("🏛️  Procesando departamentos...")
        count = 0
        for row in data:
            nombre = self._str(row, COLUMN_MAPPING['departamentos']['nombre'])
            if not nombre:
                continue
            self.db.insert_or_update('departamento', {'nombre': nombre}, 'nombre')
            count += 1
        print(f"   ✅ {count} departamentos procesados")

    def convert_provincias(self, data: List[Dict[str, Any]]):
        print("🌄 Procesando provincias...")
        count = 0
        for row in data:
            nombre = self._str(row, COLUMN_MAPPING['provincias']['nombre'])
            if not nombre:
                continue
            depto_nombre = self._str(row, COLUMN_MAPPING['provincias']['departamento'])
            depto_id = (
                self.db.get_id_by_field('departamento', 'nombre', depto_nombre)
                if depto_nombre else None
            )
            es_urbano = self._bool(row, COLUMN_MAPPING['provincias']['es_urbano'])
            self.db.insert_or_update('provincia', {
                'departamento_id': depto_id,
                'nombre':          nombre,
                'es_urbano':       1 if es_urbano else 0,
            }, 'nombre')
            count += 1
        print(f"   ✅ {count} provincias procesadas")

    def convert_municipios(self, data: List[Dict[str, Any]]):
        print("🏘️  Procesando municipios...")
        count = 0
        for row in data:
            nombre = self._str(row, COLUMN_MAPPING['municipios']['nombre'])
            if not nombre:
                continue
            prov_nombre = self._str(row, COLUMN_MAPPING['municipios']['provincia'])
            prov_id = (
                self.db.get_id_by_field('provincia', 'nombre', prov_nombre)
                if prov_nombre else None
            )
            self.db.insert_or_update('municipio', {
                'provincia_id': prov_id,
                'nombre':       nombre,
            }, 'nombre')
            count += 1
        print(f"   ✅ {count} municipios procesados")

    def convert_asientos_electorales(self, data: List[Dict[str, Any]]):
        print("🗳️  Procesando asientos electorales...")
        count = 0
        for row in data:
            nombre = self._str(row, COLUMN_MAPPING['asientos_electorales']['nombre'])
            if not nombre:
                continue
            mun_nombre = self._str(row, COLUMN_MAPPING['asientos_electorales']['municipio'])
            mun_id = (
                self.db.get_id_by_field('municipio', 'nombre', mun_nombre)
                if mun_nombre else None
            )
            self.db.insert_or_update('asiento_electoral', {
                'municipio_id': mun_id,
                'nombre':       nombre,
            }, 'nombre')
            count += 1
        print(f"   ✅ {count} asientos procesados")

    def convert_recintos(self, data: List[Dict[str, Any]]):
        print("🏫 Procesando recintos...")
        inserted = updated = skipped = 0
        for row in data:
            nombre = self._str(row, COLUMN_MAPPING['recintos']['nombre'])
            if not nombre:
                continue
            asiento_nombre = self._str(row, COLUMN_MAPPING['recintos']['asiento_electoral'])
            asiento_id = (
                self.db.get_id_by_field('asiento_electoral', 'nombre', asiento_nombre)
                if asiento_nombre else None
            )
            if not asiento_id:
                print(f"   ⚠️  Asiento '{asiento_nombre}' no encontrado → recinto '{nombre}' omitido")
                skipped += 1
                continue

            existing_id = self.db.get_recinto_id_by_asiento_and_nombre(asiento_nombre, nombre)
            recinto_data = {
                'asiento_id': asiento_id,
                'nombre':     nombre,
                'direccion':  self._str(row, COLUMN_MAPPING['recintos']['direccion']),
                'distrito':   self._int(row, COLUMN_MAPPING['recintos']['distrito']),
            }
            if existing_id:
                self.db.update_record('recinto', recinto_data, existing_id)
                updated += 1
            else:
                self.db.insert_record('recinto', recinto_data)
                inserted += 1
        print(f"   ✅ {inserted} nuevos, {updated} actualizados, {skipped} omitidos")

    # ── PERSONAS ──────────────────────────────────────────────────────

    def convert_personas(
        self,
        operadores_data: List[Dict[str, Any]],
        notarios_data:   List[Dict[str, Any]],
    ):
        """
        Procesa operadores y notarios en la tabla 'persona'.

        Cambios v2:
        - user/password vienen directo en operadores_data (ya no hay hoja Cuentas)
        - coordinador_id resuelve directamente por ci del coordinador
          (ya no existe grupo_id)
        """
        print("👷 Procesando personas (operadores + notarios)...")
        op_count = notario_count = errors = 0

        # ── Operadores ────────────────────────────────────────────────
        for row in operadores_data:
            ci = self._str(row, COLUMN_MAPPING['operadores']['ci'])
            if not ci:
                continue

            asiento_nombre = self._str(row, COLUMN_MAPPING['operadores']['asiento_electoral'])
            recinto_nombre = self._str(row, COLUMN_MAPPING['operadores']['recinto'])
            recinto_id = self.db.get_recinto_id_by_asiento_and_nombre(
                asiento_nombre, recinto_nombre
            )
            if not recinto_id:
                print(
                    f"   ⚠️  Recinto '{recinto_nombre}' / '{asiento_nombre}' "
                    f"no encontrado (operador CI {ci})"
                )
                errors += 1
                continue

            coord_ci = self._str(row, COLUMN_MAPPING['operadores']['coordinador_ci'])
            coordinador_id = (
                self.db.get_id_by_field('coordinador', 'ci', coord_ci)
                if coord_ci else None
            )

            user     = self._str(row, COLUMN_MAPPING['operadores']['user'])     or None
            password = self._str(row, COLUMN_MAPPING['operadores']['password']) or None

            self.db.insert_or_update('persona', {
                'tipo':           'operador',
                'nombre':         self._str(row, COLUMN_MAPPING['operadores']['nombre']),
                'ci':             ci,
                'expedido':       self._str(row, COLUMN_MAPPING['operadores']['expedido']),
                'celular':        self._str(row, COLUMN_MAPPING['operadores']['celular']),
                'correo':         self._str(row, COLUMN_MAPPING['operadores']['correo']),
                'cargo':          self._str(row, COLUMN_MAPPING['operadores']['cargo']),
                'recinto_id':     recinto_id,
                'coordinador_id': coordinador_id,
                'user':           user,
                'password':       password,
            }, 'ci')
            op_count += 1

        # ── Notarios ──────────────────────────────────────────────────
        for row in notarios_data:
            ci = self._str(row, COLUMN_MAPPING['notarios']['ci'])
            if not ci:
                continue

            asiento_nombre = self._str(row, COLUMN_MAPPING['notarios']['asiento_electoral'])
            recinto_nombre = self._str(row, COLUMN_MAPPING['notarios']['recinto'])
            recinto_id = self.db.get_recinto_id_by_asiento_and_nombre(
                asiento_nombre, recinto_nombre
            )
            if not recinto_id:
                print(
                    f"   ⚠️  Recinto '{recinto_nombre}' / '{asiento_nombre}' "
                    f"no encontrado (notario CI {ci})"
                )
                errors += 1
                continue

            self.db.insert_or_update('persona', {
                'tipo':           'notario',
                'nombre':         self._str(row, COLUMN_MAPPING['notarios']['nombre']),
                'ci':             ci,
                'expedido':       self._str(row, COLUMN_MAPPING['notarios']['expedido']),
                'celular':        self._str(row, COLUMN_MAPPING['notarios']['celular']),
                'correo':         self._str(row, COLUMN_MAPPING['notarios']['correo']),
                'cargo':          self._str(row, COLUMN_MAPPING['notarios']['cargo']),
                'recinto_id':     recinto_id,
                'coordinador_id': None,
                'user':           None,
                'password':       None,
            }, 'ci')
            notario_count += 1

        print(
            f"   ✅ {op_count} operadores, {notario_count} notarios procesados, "
            f"{errors} errores"
        )

    # ── ACTAS ─────────────────────────────────────────────────────────

    def convert_actas(self, data: List[Dict[str, Any]]):
        """
        Actas simplificadas: solo codigo + persona_id.
        El recinto se obtiene siempre via persona.recinto_id.
        """
        print("📄 Procesando actas...")
        total = asignaciones_ok = errors = 0

        for row in data:
            operador_ci = self._str(row, COLUMN_MAPPING['actas']['operador_ci'])
            codigos_str = self._str(row, COLUMN_MAPPING['actas']['codigos'])

            if not operador_ci:
                errors += 1
                continue
            if not codigos_str:
                self._warn_fila(operador_ci, "sin códigos")
                errors += 1
                continue

            persona_id = self.db.get_id_by_field('persona', 'ci', operador_ci)
            if not persona_id:
                print(f"   ⚠️  Operador CI '{operador_ci}' no encontrado")
                errors += 1
                continue

            codigos = self._separar_codigos(codigos_str)
            actas_ok = 0
            for codigo in codigos:
                if not codigo or not self._validar_codigo(codigo):
                    continue
                try:
                    self.db.insert_or_update('acta', {
                        'codigo':     codigo,
                        'persona_id': persona_id,
                    }, 'codigo')
                    actas_ok += 1
                    total += 1
                except Exception as e:
                    print(f"   ❌ Error insertando acta '{codigo}': {e}")
                    errors += 1

            if actas_ok:
                asignaciones_ok += 1

        print(f"   📊 {total} actas en {asignaciones_ok} asignaciones, {errors} errores")

    def _warn_fila(self, ci: str, msg: str):
        print(f"   ⚠️  Operador CI {ci}: {msg}")

    # ── HELPERS PRIVADOS ──────────────────────────────────────────────

    def _separar_codigos(self, codigos_str: str) -> List[str]:
        if not codigos_str or not codigos_str.strip():
            return []

        # Convertir a string por si Google Sheets lo entregó como número
        s = str(codigos_str).strip()

        # Caso 1: hay separador explícito → dividir y limpiar vacíos (comas finales)
        for sep in [",", ";", "|", "\t"]:
            if sep in s:
                parts = [c.strip() for c in s.split(sep) if c.strip()]
                return parts

        # Caso 2: string largo de solo dígitos sin separador
        # (Google Sheets a veces borra las comas de celdas numéricas)
        # Intentar dividir en chunks del mismo tamaño probando de 6 a 10 dígitos
        s_clean = s.replace(" ", "")
        if len(s_clean) > 10 and s_clean.isdigit():
            for chunk_size in range(6, 11):
                if len(s_clean) % chunk_size == 0:
                    parts = [s_clean[i:i + chunk_size]
                             for i in range(0, len(s_clean), chunk_size)]
                    print(f"   ℹ️  Códigos pegados detectados → separados en "
                          f"{len(parts)} grupos de {chunk_size} dígitos")
                    return parts

        # Caso 3: código único
        return [s_clean if s_clean else s]

    def _validar_codigo(self, codigo: str) -> bool:
        if not codigo or not isinstance(codigo, str):
            return False
        c = codigo.strip()
        if len(c) < 3 or len(c) > 50:
            return False
        if not any(ch.isalnum() for ch in c):
            return False
        if any(ch in c for ch in ['<', '>', '"', "'", '\\', '/', '?', '*']):
            return False
        return True