from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# File paths
FILE_PATH = './MES.xlsx'

# Database URIs
MONGODB_URI = os.getenv("MONGODB_URI")

# Hardcoding rows and columns names
ROWS = ["Total de Activos", "Total de Pasivos", "Capital Social", "Resultado del Ejercicio", "Total Patrimonio Neto", "Primas Directas", "Primas Reaseguros Aceptados - Local", 
        "Siniestros Seguros Directos", "Resultado Técnico Bruto [7]=[3]-[6]", "Gastos De Producción", "Gastos De Cesión Reaseguros - Local", "Gastos De Cesión Reaseguros - Exterior", 
        "Gastos Técnicos De Explotación", "Constitución De Previsiones", "Resultado Técnico Neto [11]=[7]+[10]", "Resultado Total del Ejercicio", "Resultado del Ejercicio"]

COLUMNS_UP = ['El Comercio Paraguayo S.A. De Seguros', 'La Rural S.A. De Seguros', 'La Paraguaya S.A. De Seguros', 'Seguros Generales S. A. (Segesa)', 'Rumbos S.A. De Seguros', 
           'La Consolidada S.A. De Seguros', 'El Productor S.A. De Seguros Y Reaseguros', 'Atalaya S.A De Seguros Generales', 'La Independencia De Seguros Sociedad Anonima', 
           'Patria S.A. De Seguros Y Reaseguros', 'Alianza Garantía Seguros Y Reaseguros S.A.', 'Aseguradora Paraguaya S.A', 'Fénix S.A. De Seguros Y Reaseguros', 
           'Central S.A. De Seguros', 'Seguros Chaco S.A. De Seguros Y Reaseguros', 'El Sol Del Paraguay Compañía De Seguros Y Reaseguros', 'Intercontinental De Seguros Y Reaseguros S.A.', 
           'Seguridad S.A. Compañía De Seguros', 'Aseguradora Yacyreta S.A. De Seguros Y Reaseguros', 'La Agrícola S.A. De Seguros Y Reaseguros', 'Ueno Seguros S.A.', 'Cenit De Seguros S.A.', 
           'La Meridional Paraguaya S.A. De Seguros', 'Aseguradora Del Este S.A De Seguros Y Reaseguros', 'Regional S.A. De Seguros Y Reaseguros', 'Mapfre Paraguay Compañía De Seguros S.A.', 
           'Aseguradora Tajy Propiedad Cooperativa S.A. De Seguros', 'Panal Compañía De Seguros Generales S.A.', 'Sancor Seguros Del Paraguay S.A.', 'Royal Seguros S.A. Compañía De Seguros', 
           'Nobleza Seguros S.A. Compañia De Seguros', 'Itau Seguros Paraguay S.A.', 'Familiar Seguros S.A.', 'Atlas S.A. De Seguros', 'Universo de Seguros S.A.']

COLUMNS = ['el comercio paraguayo s.a. de seguros', 'la rural s.a. de seguros', 'la paraguaya s.a. de seguros', 'seguros generales s. a. (segesa)', 'rumbos s.a. de seguros', 
'la consolidada s.a. de seguros', 'el productor s.a. de seguros y reaseguros', 'atalaya s.a de seguros generales', 'la independencia de seguros sociedad anonima', 
'patria s.a. de seguros y reaseguros', 'alianza garantía seguros y reaseguros s.a.', 'aseguradora paraguaya s.a', 'fénix s.a. de seguros y reaseguros', 
'central s.a. de seguros', 'seguros chaco s.a. de seguros y reaseguros', 'el sol del paraguay compañía de seguros y reaseguros', 'intercontinental de seguros y reaseguros s.a.', 
'seguridad s.a. compañía de seguros', 'aseguradora yacyreta s.a. de seguros y reaseguros', 'la agrícola s.a. de seguros y reaseguros', 'ueno seguros s.a.', 'cenit de seguros s.a.', 
'la meridional paraguaya s.a. de seguros', 'aseguradora del este s.a de seguros y reaseguros', 'regional s.a. de seguros y reaseguros', 'mapfre paraguay compañía de seguros s.a.', 
'aseguradora tajy propiedad cooperativa s.a. de seguros', 'panal compañía de seguros generales s.a.', 'sancor seguros del paraguay s.a.', 'royal seguros s.a. compañía de seguros', 
'nobleza seguros s.a. compañia de seguros', 'itau seguros paraguay s.a.', 'familiar seguros s.a.', 'atlas s.a. de seguros', 'universo de seguros s.a.']