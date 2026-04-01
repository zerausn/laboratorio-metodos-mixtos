import re


class BudgetValidator:
    def __init__(self):
        self.checksums = {
            "admon_central_presupuesto_modificado": 1164037941631,
            "admon_central_pagos": 821926343086,
            "admon_central_ejecucion": 910349407602,
            "gastos_funcionamiento_modificado": 1133833863257,
            "gastos_funcionamiento_ejecucion": 884186899741,
        }

    def clean_currency(self, text):
        clean_text = re.sub(r"[^\d]", "", str(text))
        return int(clean_text) if clean_text else 0

    def parse_account_number(self, text):
        pattern = r"^\d+(\.\d+)+$"
        return text if re.match(pattern, str(text)) else None

    def validate_totals(self, extracted_total, key):
        expected = self.checksums.get(key)
        if expected is None:
            return False, "No hay checksum para esta clave."
        diff = abs(int(extracted_total) - expected)
        return diff == 0, diff
