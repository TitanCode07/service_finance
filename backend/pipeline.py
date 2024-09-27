import pandas as pd
import asyncio
import numpy as np
import openpyxl
from preprocessing_tools import (
        get_value_from_df, create_new_df, generate_df_list, create_dict_from_df,
        transform_keys, add_insurer_id, add_date_info, restructure_data,
        format_for_mongodb)
from config import FILE_PATH, ROWS, COLUMNS
from database import upload_financial_exercise


def load_excel_sheets(file_path: str) -> dict:
        # Load spreadsheet
        main_df = pd.ExcelFile(file_path)
        # Load every sheet into a dataframe by its name
        dataframes_dic = {sheet_name: main_df.parse(sheet_name) for sheet_name in main_df.sheet_names}
        return dataframes_dic


def extract_dataframes(dataframes_dic: dict) -> list:
        # Separate the necessary elements of the dictionary into different dataframes
        balance_general = dataframes_dic['2']
        estado_resultados = dataframes_dic['3']
        ingresos_egresos = dataframes_dic['4']
        dataframes = [balance_general, estado_resultados, ingresos_egresos]
        for df in dataframes:
                df.columns = df.columns.str.lower()
        print(balance_general.columns)
        print(dataframes[0].columns)
        print(COLUMNS)
        
        return dataframes


def generate_dataframes_list(file_path: str=FILE_PATH, rows: list=ROWS, columns: list=COLUMNS) -> list:
        # Generate a list of dataframes, one for each column
        dataframes_dic = load_excel_sheets(file_path)
        dataframes = extract_dataframes(dataframes_dic)
        dfs_list = generate_df_list(dataframes, rows, columns)
        return dfs_list


def process_data(dataframe, year: int, month: str):   
        new_dict = transform_keys(create_dict_from_df(dataframe))
        new_dict = add_insurer_id(new_dict)
        new_dict = add_date_info(new_dict, year, month)
        new_dict = restructure_data(new_dict)
        # new_json = format_for_mongodb(new_dict)
        return new_dict


async def process_file(year: int, month: str, file_path: str):
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                try:
                        df_list = generate_dataframes_list(file_path)
                        processed_data = [process_data(df, year, month) for df in df_list]
                        ids = []
                        for data in processed_data:
                                id = await upload_financial_exercise(data)
                                ids.append(id)
                        return {"inserted_ids": ids}
                except Exception as e:
                        raise Exception("Invalid file format")
        else:
                raise Exception("Invalid file format")
    


if __name__ == "__main__":
        import asyncio
        #print(process_data(generate_dataframes_list()[0], 2024, "enero"))
        print(asyncio.run(process_file(2024, "enero", "MES.xlsx")))
    