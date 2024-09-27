from typing import Optional
from pydantic import BaseModel, Field


class BalanceGeneral(BaseModel):
    total_activos: int
    total_pasivos: int
    capital_social: int
    resultado_ejercicio: int
    total_patrimonio_neto: int

class EstadoResultado(BaseModel):
    primas_directas: int
    primas_reaseguros_aceptados_local: int
    siniestros_seguros_directos: int
    resultado_tecnico_bruto: int
    gastos_produccion: int
    gastos_cesion_reaseguros_local: int
    gastos_cesion_reaseguros_exterior: int
    gastos_tecnicos_explotacion: int
    constitucion_previsiones: int
    resultado_tecnico_neto: int
    resultado_total_ejercicio: int

class IngresosEgresos(BaseModel):
    resultado_ejercicio: int

class FinancialExercise(BaseModel):
    id: str = Field(alias="_id", default=None)
    year: str
    month: str
    insurer_id: str
    balance_general: BalanceGeneral
    estado_resultado: EstadoResultado
    ingresos_egresos: IngresosEgresos

class Insurer(BaseModel):
    id: str = Field(alias="_id", default=None)
    name: str = Field(min_length=1, max_length=50)
    ruc: str = Field(min_length=1, max_length=16)
