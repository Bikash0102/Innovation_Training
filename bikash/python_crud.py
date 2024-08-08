import os
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from pydantic import BaseModel

from typing import Optional
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI")

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Failed to connect to MongoDB:", e)

app = FastAPI()




collection = client.dashboard["bikash"]




class employee(BaseModel):
    emp_id: Optional[int] = None
    emp_name: Optional[str] = None
    emp_role: Optional[str] = None
    emp_place: Optional[str] = None
    emp_salary: Optional[int] = None



@app.post("/insert-data")
def insert_data(employee: employee):
  
    try:
        collection.insert_one(employee.model_dump())
        return {"message": "employee inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert employee: {e}")


@app.put("/update-product/{emp_id}")
def update_data(*,emp_id: Optional[int]=None, employee: employee):
   

    try:
        print(emp_id)
        result = collection.update_one({"emp_id": emp_id}, {"$set": employee.model_dump()})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="employee not found")
        return {"message": "employee  updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product: {e}")


@app.delete("/delete-employee/{emp_id}")
def delete_data(emp_id: int):
    try:
        result = collection.delete_one({"emp_id" :emp_id })
        print(result)
        return {"message": "employee deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to update product: {e}")

@app.get("/get-employee")
def get_data():
    try:
        documents = list(collection.find())
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        return{"employee":documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to update product: {e}")
    
    
@app.post("/get-total-salary")
def total_employee_count(employee: employee):
    try:
        print(employee)
        # Correct query format: use $gt for greater than operator
        query = {"emp_salary": {"$gt": employee.emp_salary}}
        total_count = collection.count_documents(query)
        return {"employee_count": total_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to count employees: {e}")