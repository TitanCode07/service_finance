import io
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder

from fastapi import Depends
from utils import verify_jwt_token

from database import (
        retrieve_insurer,
        get_financial_exercises_by_insurer,
        upload_financial_exercise,
        get_field_value,
        get_all_field_values,
        get_monthly_exercise,
        get_field_values_by_insurer,
        delete_one_document,
        delete_many_document,
        delete_documents_by_date,
        delete_document_by_id
)

from pipeline import (
        generate_dataframes_list,
        process_data,
)

from models import (
        Insurer,
)

from preprocessing_tools import (
        extract_list
)

router = APIRouter(
    prefix="/finance",
    tags=["finance"]
)


@router.get("/insurer")
async def get_all_insurers(token: str = Depends(verify_jwt_token)):
    try:
        return await retrieve_insurer()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/exercise/{insurer_id}")
async def get_exercises_by_insurer(insurer_id: str, token: str = Depends(verify_jwt_token)):
    try:
        return await get_financial_exercises_by_insurer(insurer_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/field_value/{insurer_id}/{year}/{month}/{field}")
async def get_field_value_route(insurer_id: str, year: int, month: str, field: str, token: str = Depends(verify_jwt_token)):
    value = await get_field_value(insurer_id, year, month, field)
    if value is not None:
        return {"value": value}
    else:
        raise HTTPException(status_code=404, detail="Document not found or field does not exist")
    

@router.get("/all_field_values/{year}/{month}/{field}")
async def get_all_field_values_route(year: int, month: str, field: str, token: str = Depends(verify_jwt_token)):
    try:
        results = await get_all_field_values(year, month, field)
        if results:
            return extract_list(results)
        else:
            raise HTTPException(status_code=404, detail="No documents found for the given year and month")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/exercise/{year}/{month}")
async def get_monthly_exercise_route(year: int, month: str, token: str = Depends(verify_jwt_token)):
    try:
        return await get_monthly_exercise(year, month)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/field_values_insurer/{insurer_id}/{field}")
async def get_field_values_by_insurer_route(insurer_id: str, field: str,    token: str = Depends(verify_jwt_token)):
    try:
        results = await get_field_values_by_insurer(insurer_id, field)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete_one/{insurer_id}/{year}/{month}")
async def delete_one_document_route(insurer_id: str, year: int, month: str, token: str = Depends(verify_jwt_token)):
    try:
        return await delete_one_document(insurer_id, year, month)
    except Exception as e:
        raise HTTPException(status_code_=400, detail=str(e))
    

@router.delete("/delete_many/{insurer_id}/{year}/{month}")
async def delete_many_document_route(insurer_id: str, year: int, month: str, token: str = Depends(verify_jwt_token)):
    try:
        return await delete_many_document(insurer_id, year, month)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{year}/{month}")
async def delete_documents_by_date_route(year: int = None, month: str = None, token: str = Depends(verify_jwt_token)):
    try:
        return await delete_documents_by_date(year, month)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{document_id}")
async def delete_document_by_id_route(document_id: str, token: str = Depends(verify_jwt_token)):
    try:
        return await delete_document_by_id(document_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/exercise")
async def upload_exercise(data: dict, token: str = Depends(verify_jwt_token)):
    try:
        result = await upload_financial_exercise(data)
        return {"inserted_id": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload/{year}/{month}")
async def process_file(year: int, month: str, file: UploadFile = File(...), token: str = Depends(verify_jwt_token)):
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        try:
            df_list = generate_dataframes_list(io.BytesIO(await file.read()))
            processed_data = [process_data(df, year, month) for df in df_list]
            ids = []
            for data in processed_data:
                id = await upload_financial_exercise(data)
                ids.append(id)
            return {"inserted_ids": ids}
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid file format")
    else:
        raise HTTPException(status_code=400, detail="Invalid file format")