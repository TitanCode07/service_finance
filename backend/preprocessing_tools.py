import pandas as pd
import json



# Retrieves the value from a dataframe based on the given row value and column name.
def get_value_from_df(df, row_value, column_name):    
    try:
        row = df[df['nombre de la cuenta'] == row_value]
        print(row[column_name].values[0])
        return row[column_name].values[0]
    except (IndexError, KeyError):
        return "Error: Invalid row or column names. Please verify and try again."


# Create a new dataframe by extracting values from multiples dataframes.
def create_new_df(dfs, rows, columns):
    new_df = pd.DataFrame(rows, columns=["Nombre de la Cuenta"])
    
    for column in columns:
        new_df[column] = None

    for df in dfs:
        for i, row in enumerate(rows):
            for column in columns:
                # Get the value at the intersection of the row and column
                value = get_value_from_df(df, row, column)
                
                # If the value is not an error mmessage, assign it to the new dataframe
                if not isinstance(value, str):
                    new_df.at[i, column] = value

    return new_df

# Create a list containing a dataframe for every column
def generate_df_list(dfs, rows, columns):
    dfs_list = []
    columns = [column.lower() for column in columns]

    for column in columns:
        new_df = pd.DataFrame(rows, columns=["nombre de la cuenta"])
        new_df[column] = None

        for df in dfs:
            for i, row in enumerate(rows):
                value = get_value_from_df(df, row, column)

                if not isinstance(value, str):
                    new_df.at[i, column] = value
       
        dfs_list.append(new_df)

    return dfs_list
    

def create_dict_from_df(df):
    new_dict = {}
    second_key = list(df.columns)[1]
    new_dict["Insurer"] = second_key

    for _, row in df.iterrows():
        new_dict[row['nombre de la cuenta']] = row[second_key]

    return new_dict


def transform_keys(input_dict: dict) -> dict:
    # Define a mapping from the old keys to the new keys
    key_mapping = {
        "Insurer": "insurer",
        "Total de Activos": "total_activos",
        "Total de Pasivos": "total_pasivos",
        "Capital Social": "capital_social",
        "Resultado del Ejercicio": "resultado_ejercicio",
        "Total Patrimonio Neto": "total_patrimonio_neto",
        "Primas Directas": "primas_directas",
        "Primas Reaseguros Aceptados - Local": "primas_reaseguros_aceptados_local",
        "Siniestros Seguros Directos": "siniestros_seguros_directos",
        "Resultado Técnico Bruto [7]=[3]-[6]": "resultado_tecnico_bruto",
        "Gastos De Producción": "gastos_produccion",
        "Gastos De Cesión Reaseguros - Local": "gastos_cesion_reaseguros_local",
        "Gastos De Cesión Reaseguros - Exterior": "gastos_cesion_reaseguros_exterior",
        "Gastos Técnicos De Explotación": "gastos_tecnicos_explotacion",
        "Constitución De Previsiones": "constitucion_previsiones",
        "Resultado Técnico Neto [11]=[7]+[10]": "resultado_tecnico_neto",
        "Resultado Total del Ejercicio": "resultado_total_ejercicio",
        "Resultado del Ejercicio": "resultado_ejercicio"
    }

    # Create a new dictionary with the transformed keys
    output_dict = {key_mapping[key]: value for key, value in input_dict.items() if key in key_mapping}

    return output_dict


def add_insurer_id(input_dict: dict) -> dict:
    # Insurer id encoder
    insurer_id = {
        'El Comercio Paraguayo S.A. De Seguros': "802",
        'La Rural S.A. De Seguros': "803",
        'La Paraguaya S.A. De Seguros': "804",
        'Seguros Generales S. A. (Segesa)': "805",
        'Rumbos S.A. De Seguros': "806", 
        'La Consolidada S.A. De Seguros': "807",
        'El Productor S.A. De Seguros Y Reaseguros': "808",
        'Atalaya S.A De Seguros Generales': "809",
        'La Independencia De Seguros Sociedad Anonima': "810", 
        'Patria S.A. De Seguros Y Reaseguros': "811",
        'Alianza Garantía Seguros Y Reaseguros S.A.': "812",
        'Aseguradora Paraguaya S.A': "813",
        'Fénix S.A. De Seguros Y Reaseguros': "814", 
        'Central S.A. De Seguros': "815",
        'Seguros Chaco S.A. De Seguros Y Reaseguros': "816",
        'El Sol Del Paraguay Compañía De Seguros Y Reaseguros': "817",
        'Intercontinental De Seguros Y Reaseguros S.A.': "818",
        'Seguridad S.A. Compañía De Seguros': "819",
        'Aseguradora Yacyreta S.A. De Seguros Y Reaseguros': "820",
        'La Agrícola S.A. De Seguros Y Reaseguros': "821",
        'Ueno Seguros S.A.': "822",
        'Cenit De Seguros S.A.': "823",
        'La Meridional Paraguaya S.A. De Seguros': "824",
        'Aseguradora Del Este S.A De Seguros Y Reaseguros': "825",
        'Regional S.A. De Seguros Y Reaseguros': "801",
        'Mapfre Paraguay Compañía De Seguros S.A.': "826",
        'Aseguradora Tajy Propiedad Cooperativa S.A. De Seguros': "827",
        'Panal Compañía De Seguros Generales S.A.': "828",
        'Sancor Seguros Del Paraguay S.A.': "829",
        'Royal Seguros S.A. Compañía De Seguros': "830",
        'Nobleza Seguros S.A. Compañia De Seguros': "831",
        'Itau Seguros Paraguay S.A.': "832",
        'Familiar Seguros S.A.': "833",
        'Atlas S.A. De Seguros': "834",
        'Universo de Seguros S.A.': "835"
    }

    insurer_id_lower = {
        'el comercio paraguayo s.a. de seguros': "802",
        'la rural s.a. de seguros': "803",
        'la paraguaya s.a. de seguros': "804",
        'seguros generales s. a. (segesa)': "805",
        'rumbos s.a. de seguros': "806", 
        'la consolidada s.a. de seguros': "807",
        'el productor s.a. de seguros y reaseguros': "808",
        'atalaya s.a de seguros generales': "809",
        'la independencia de seguros sociedad anonima': "810", 
        'patria s.a. de seguros y reaseguros': "811",
        'alianza garantía seguros y reaseguros s.a.': "812",
        'aseguradora paraguaya s.a': "813",
        'fénix s.a. de seguros y reaseguros': "814", 
        'central s.a. de seguros': "815",
        'seguros chaco s.a. de seguros y reaseguros': "816",
        'el sol del paraguay compañía de seguros y reaseguros': "817",
        'intercontinental de seguros y reaseguros s.a.': "818",
        'seguridad s.a. compañía de seguros': "819",
        'aseguradora yacyreta s.a. de seguros y reaseguros': "820",
        'la agrícola s.a. de seguros y reaseguros': "821",
        'ueno seguros s.a.': "822",
        'cenit de seguros s.a.': "823",
        'la meridional paraguaya s.a. de seguros': "824",
        'aseguradora del este s.a de seguros y reaseguros': "825",
        'regional s.a. de seguros y reaseguros': "801",
        'mapfre paraguay compañía de seguros s.a.': "826",
        'aseguradora tajy propiedad cooperativa s.a. de seguros': "827",
        'panal compañía de seguros generales s.a.': "828",
        'sancor seguros del paraguay s.a.': "829",
        'royal seguros s.a. compañía de seguros': "830",
        'nobleza seguros s.a. compañia de seguros': "831",
        'itau seguros paraguay s.a.': "832",
        'familiar seguros s.a.': "833",
        'atlas s.a. de seguros': "834",
        'universo de seguros s.a.': "835"
    }

    # insurer_id = {k.lower(): v for k, v in insurer_id.items()}

    # If the "insurer" key is in the input dictionary and its value is in the insurer_id dictionary,
    # add a new key-value pair to the input dictionary
    if "insurer" in input_dict and input_dict["insurer"] in insurer_id_lower:
        input_dict["insurer_id"] = insurer_id_lower[input_dict["insurer"]]

    return input_dict


def add_date_info(input_dict: dict, year: int, month: str) -> dict:
    # Add the year and month to the dictionary
    input_dict["year"] = year
    input_dict["month"] = month

    return input_dict


def restructure_data(input_dict):
    # Create a new dictionary with the desired structure
    output_dict = {
        "year": input_dict["year"],
        "month": input_dict["month"],
        "insurer_id": input_dict["insurer_id"],
        "balance_general": {
            "total_activos": {"$numberLong": str(input_dict["total_activos"])},
            "total_pasivos": {"$numberLong": str(input_dict["total_pasivos"])},
            "capital_social": {"$numberLong": str(input_dict["capital_social"])},
            "resultado_ejercicio": {"$numberLong": str(input_dict["resultado_ejercicio"])},
            "total_patrimonio_neto": {"$numberLong": str(input_dict["total_patrimonio_neto"])}
        },
        "estado_resultado": {
            "primas_directas": {"$numberLong": str(input_dict["primas_directas"])},
            "primas_reaseguros_aceptados_local": {"$numberInt": str(input_dict["primas_reaseguros_aceptados_local"])},
            "siniestros_seguros_directos": {"$numberLong": str(input_dict["siniestros_seguros_directos"])},
            "resultado_tecnico_bruto": {"$numberLong": str(input_dict["resultado_tecnico_bruto"])},
            "gastos_produccion": {"$numberLong": str(input_dict["gastos_produccion"])},
            "gastos_cesion_reaseguros_local": {"$numberInt": str(input_dict["gastos_cesion_reaseguros_local"])},
            "gastos_cesion_reaseguros_exterior": {"$numberInt": str(input_dict["gastos_cesion_reaseguros_exterior"])},
            "gastos_tecnicos_explotacion": {"$numberLong": str(input_dict["gastos_tecnicos_explotacion"])},
            "constitucion_previsiones": {"$numberInt": str(input_dict["constitucion_previsiones"])},
            "resultado_tecnico_neto": {"$numberLong": str(input_dict["resultado_tecnico_neto"])},
            "resultado_total_ejercicio": {"$numberLong": str(input_dict["resultado_total_ejercicio"])}
        },
        "ingresos_egresos": {
            "resultado_ejercicio": {"$numberLong": str(input_dict["resultado_ejercicio"])}
        }
    }

    return output_dict


def extract_list(data):
    # Create a list of insuere names by extracting the 'insurer_name' field from each item in the data
    insurer_names = [item['insurer_name'] for item in data]
    # Create a list of numeric values by extracting the '$numberLong' field from the 'value' field in each item in the data
    numeric_values = [item['value']['$numberLong'] for item in data]
    # Initialize an empty list to store the numeric values after conversion to integers
    output_numeric = []
    # Iterate over the numeric values
    for value in numeric_values:
        try:
            # Try to convert the value to an integer and append it to the output_numeric list
            output_numeric.append(int(value))
        except ValueError:
            # If the value cannot be converted to an integer, append 0 to the output_numeric list
            output_numeric.append(0)
    # Return the list of insurer names and the list of numeric values
    return insurer_names, output_numeric


def format_for_mongodb(data: dict) -> dict:
    # Convert the dictionary to a JSON-formatted string
    json_str = json.dumps(data)

    return json_str