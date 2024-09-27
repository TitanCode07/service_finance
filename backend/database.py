
import motor.motor_asyncio
from bson.objectid import ObjectId
from config import MONGODB_URI

# Get the URI from the .env file
uri = MONGODB_URI


def setup_database(uri):
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    database = client.get_database("insurer_market_statistics")
    insurer_collection = database.get_collection("insurance_companies")
    exercises_collection = database.get_collection("financial_exercises")

    return insurer_collection, exercises_collection


def insurer_helper(insurer) -> dict:
    return {
        "id": str(insurer["_id"]),
        "name": insurer["name"],
        "ruc": insurer["ruc"],
    }
  

# GET METHODS
async def retrieve_insurer() -> list[dict]:
    insurers = []
    async for insurer in insurer_collection.find():
        insurers.append(insurer_helper(insurer))
    return insurers


async def get_financial_exercises_by_insurer(insurer_id):
    # Find the insurer by id
    insurer = await insurer_collection.find_one({'_id': insurer_id})

    if insurer:
        # Find the financial exercises by insurer_id
        exercises = []
        async for exercise in exercises_collection.find({'insurer_id': str(insurer_id)}):
            exercise["_id"] = str(exercise["_id"])  # convert ObjectId to string
            exercises.append(exercise)  # modify this line as needed to format the exercise data
        return exercises
    else:
        return None  # or raise an exception, or return an error message, etc.
    
    
async def get_field_value(insurer_id, year, month, field):
    # Find the document that matches the given parameters
    document = await exercises_collection.find_one({
        'insurer_id': insurer_id,
        'year': year,
        'month': month
    })

    if document:
        # Split the field into its components (e.g., 'balance_general.total_activos.$numberLong' becomes ['balance_general', 'total_activos', '$numberLong'])
        field_components = field.split('.')
        # Start with the entire document
        value = document
        # Traverse the document using the field components
        for component in field_components:
            value = value.get(component)  # Get the next component
            if value is None:
                # If a component doesn't exist, return None
                return None
        # If all components exist, return the final value
        return value
    else:
        return None


async def get_all_field_values(year, month, field):
    # Find all documents that match the given year and month
    cursor = exercises_collection.find({
        'year': year,
        'month': month
    })

    # Initialize an empty list to store the results
    results = []

    # Iterate over the documents
    async for document in cursor:
        # Get the field value using the get_field_value function
        value = await get_field_value(document['insurer_id'], year, month, field)
        if value is not None:
            # If the field value exist, find the insurer an add the result
            insurer = await insurer_collection.find_one({'_id': document['insurer_id']})
            if insurer:
                results.append({
                    'insurer_name': insurer['name'],
                    'value': value
                })

    # Return the results
    return results        


async def get_monthly_exercise(year, month):
    # Find all documents that match the given year and month
    cursor = exercises_collection.find({
        'year': year,
        'month': month
    })

    # Initialize an empty list to store the results
    results = []

    # Iterate over the documents
    async for document in cursor:
        # Find the insurer by id
        document['_id'] = str(document['_id'])  # convert ObjectId to string
        insurer = await insurer_collection.find_one({'_id': document['insurer_id']})
        if insurer:
            # Add the document to the results list
            results.append({
                'insurer_name': insurer['name'],
                'exercise': document
            })

    # Return the results
    return results


async def get_field_values_by_insurer(insurer_id, field):
    # Initialize an empty list to store the results
    results = []

    # Find all documents in the exercises collection that match the insurer_id
    cursor = exercises_collection.find({'insurer_id': insurer_id})

    # Iterate over the documents
    async for document in  cursor:
        # Find the insurer by id
        insurer = await insurer_collection.find_one({'_id': insurer_id})

        if insurer:
            # Get the insurer name 
            insurer_name = insurer.get('name')

            # Get the year and month from the document
            year = document.get('year')
            month = document.get('month')

            # Get the field value from the document using the get_field_value function
            field_value = await get_field_value(insurer_id, year, month, field)

            # Add the result to the results list
            results.append({
                'insurer_name': insurer_name,
                'year': year,
                'month': month,
                field: field_value
            })

    # Return the results
    return results




# DELETE METHODS
async def delete_one_document(insurer_id, year, month):
    # Delete the document that matches the given parameters
    result = await exercises_collection.delete_one({
        'insurer_id': insurer_id,
        'year': year,
        'month': month
    })

    # result.deleted_count contains the number of deleted documents
    if result.deleted_count:
        return {"status": "success", "message": f"Deleted {result.deleted_count} documents." }
    else:
        return {"status": "failure", "message": "No documents matched the given parameters."}


async def delete_many_document(insurer_id, year, month):
    # Delete all the documents that matches the given parameters
    result = await exercises_collection.delete_many({
        'insurer_id': insurer_id,
        'year': year,
        'month': month
    })

    # result.deleted_count contains the number of deleted documents
    if result.deleted_count:
        return {"status": "success", "message": f"Deleted {result.deleted_count} document(s)."}
    else:
        return {"status": "failure", "message": "No documents matched the given parameters."}
    


async def delete_documents_by_date(year=None, month=None):
    # Create a dictionary with the parameters that are not None
    query = {}
    if year is not None:
        query['year'] = year
    if month is not None:
        query['month'] = month

    # Delete the documents that match the given parameters
    result = await exercises_collection.delete_many(query)

    # result.deleted_count contains the number of deleted documents
    if result.deleted_count:
        return {"status": "success", "message": f"Deleted {result.deleted_count} document(s)."}
    else:
        return {"status": "failure", "message": "No documents matched the given parameters."}


async def delete_document_by_id(document_id):
    # Delete the document that matches the given id
    result = await exercises_collection.delete_one({'_id': ObjectId(document_id)})

    # result.deleted_count contains the number of deleted documents
    if result.deleted_count:
        return {"status": "success", "message": f"Deleted {result.deleted_count} document."}
    else:
        return {"status": "failure", "message": "No documents matches the given parameters."}


# PUT METHODS
async def upload_financial_exercise(data) -> str:
    # Insert the document into the collection
    result = await exercises_collection.insert_one(data)
    # Return the inserted document id
    return str(result.inserted_id)



insurer_collection, exercises_collection = setup_database(uri)