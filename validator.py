# ============================================
# validator.py  — NUEVO en v2
# Valida los datos de Google Sheets ANTES de
# tocar la base de datos. Muestra un reporte
# claro de errores y advertencias.
# ============================================

from typing import Dict, List, Any, Tuple


class DataValidator:
    def __init__(self):
        self.errors:   List[str] = []
        self.warnings: List[str] = []

    def _err(self, msg: str):
        self.errors.append(msg)

    def _warn(self, msg: str):
        self.warnings.append(msg)

    def _str(self, row: Dict, key: str) -> str:
        v = row.get(key, '')
        return str(v).strip() if v is not None else ''

    # ── VALIDACIONES POR HOJA ────────────────────────────────────────

    def validate_jefes(self, data: List[Dict]) -> bool:
        nombres = set()
        for i, row in enumerate(data, 1):
            nombre = self._str(row, 'nombre')
            if not nombre:
                self._err(f"Jefes fila {i}: 'nombre' vacío")
                continue
            if nombre in nombres:
                self._warn(f"Jefes: nombre duplicado '{nombre}' (fila {i})")
            nombres.add(nombre)
        return True

    def validate_coordinadores(self, data: List[Dict]) -> bool:
        cis = set()
        for i, row in enumerate(data, 1):
            ci     = self._str(row, 'ci')
            nombre = self._str(row, 'nombre')
            if not ci:
                self._err(f"Coordinadores fila {i}: 'ci' vacío (nombre: '{nombre}')")
                continue
            if ci in cis:
                self._err(f"Coordinadores: CI duplicado '{ci}' (fila {i})")
            cis.add(ci)
            if not nombre:
                self._warn(f"Coordinadores CI {ci}: 'nombre' vacío")
            if not self._str(row, 'nombre_grupo'):
                self._warn(f"Coordinadores CI {ci}: 'nombre_grupo' vacío (sin grupo asignado)")
        return True

    def validate_operadores(self, data: List[Dict]) -> bool:
        cis  = set()
        for i, row in enumerate(data, 1):
            ci     = self._str(row, 'ci')
            nombre = self._str(row, 'nombre')
            if not ci:
                self._err(f"Operadores fila {i}: 'ci' vacío (nombre: '{nombre}')")
                continue
            if ci in cis:
                self._err(f"Operadores: CI duplicado '{ci}' (fila {i})")
            cis.add(ci)
            if not self._str(row, 'recinto'):
                self._err(f"Operadores CI {ci}: 'recinto' vacío")
            if not self._str(row, 'asiento_electoral'):
                self._err(f"Operadores CI {ci}: 'asiento_electoral' vacío")
            if not self._str(row, 'coordinador_ci'):
                self._warn(f"Operadores CI {ci}: 'coordinador_ci' vacío (sin grupo asignado)")

            # Si tiene user pero no password (o viceversa) es sospechoso
            user     = self._str(row, 'user')
            password = self._str(row, 'password')
            if bool(user) != bool(password):
                self._warn(f"Operadores CI {ci}: tiene user sin password (o viceversa)")
        return True

    def validate_notarios(self, data: List[Dict]) -> bool:
        cis = set()
        for i, row in enumerate(data, 1):
            ci = self._str(row, 'ci')
            if not ci:
                self._err(f"Notarios fila {i}: 'ci' vacío")
                continue
            if ci in cis:
                self._err(f"Notarios: CI duplicado '{ci}' (fila {i})")
            cis.add(ci)
            if not self._str(row, 'recinto'):
                self._err(f"Notarios CI {ci}: 'recinto' vacío")

    def validate_actas(self, data: List[Dict]) -> bool:
        for i, row in enumerate(data, 1):
            if not self._str(row, 'operador_ci'):
                self._err(f"Actas fila {i}: 'operador_ci' vacío")
            if not self._str(row, 'codigos'):
                self._warn(f"Actas fila {i}: 'codigos' vacío")
        return True

    def validate_cross(
        self,
        operadores: List[Dict],
        notarios:   List[Dict],
        coordinadores: List[Dict],
        actas:      List[Dict],
    ):
        """Validaciones cruzadas entre hojas."""
        coord_cis  = {self._str(r, 'ci') for r in coordinadores if self._str(r, 'ci')}
        op_cis     = {self._str(r, 'ci') for r in operadores    if self._str(r, 'ci')}
        notario_cis = {self._str(r, 'ci') for r in notarios     if self._str(r, 'ci')}

        # CI en operadores Y notarios al mismo tiempo
        duplicados = op_cis & notario_cis
        for ci in duplicados:
            self._err(f"CI '{ci}' aparece como operador Y notario")

        # Actas que referencian CIs inexistentes
        for row in actas:
            ci = self._str(row, 'operador_ci')
            if ci and ci not in op_cis:
                self._err(f"Actas: operador_ci '{ci}' no existe en hoja Operadores")

        # Operadores que referencian coordinadores inexistentes
        for row in operadores:
            coord_ci = self._str(row, 'coordinador_ci')
            if coord_ci and coord_ci not in coord_cis:
                self._warn(
                    f"Operadores CI {self._str(row, 'ci')}: "
                    f"coordinador_ci '{coord_ci}' no existe en hoja Coordinadores"
                )

    # ── REPORTE FINAL ────────────────────────────────────────────────

    def report(self) -> Tuple[bool, int, int]:
        """Imprime el reporte y devuelve (puede_continuar, n_errores, n_warnings)."""
        n_err  = len(self.errors)
        n_warn = len(self.warnings)

        print("\n" + "=" * 60)
        print("🔍 REPORTE DE VALIDACIÓN PREVIA")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ ERRORES ({n_err}) — importación bloqueada:")
            for e in self.errors:
                print(f"   • {e}")

        if self.warnings:
            print(f"\n⚠️  ADVERTENCIAS ({n_warn}) — revisión recomendada:")
            for w in self.warnings:
                print(f"   • {w}")

        if not self.errors and not self.warnings:
            print("\n✅ Sin problemas detectados")

        print("=" * 60)

        if n_err > 0:
            print(f"🚫 Importación detenida: corrige los {n_err} errores primero")
        else:
            print(f"✅ Validación OK — continuando importación")

        return (n_err == 0), n_err, n_warn


def run_validation(
    jefes_data:        List[Dict],
    coordinadores_data: List[Dict],
    operadores_data:   List[Dict],
    notarios_data:     List[Dict],
    actas_data:        List[Dict],
) -> bool:
    """
    Ejecuta todas las validaciones.
    Retorna True si se puede continuar (0 errores).
    """
    print("🔍 Validando datos antes de importar...")
    v = DataValidator()

    v.validate_jefes(jefes_data)
    v.validate_coordinadores(coordinadores_data)
    v.validate_operadores(operadores_data)
    v.validate_notarios(notarios_data)
    v.validate_actas(actas_data)
    v.validate_cross(operadores_data, notarios_data, coordinadores_data, actas_data)

    can_proceed, n_err, n_warn = v.report()
    return can_proceed