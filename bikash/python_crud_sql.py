
from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel

app=FastAPI()
 
def createConnection():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="bikash"
    )
    return mydb
# Define the User data model
class User(BaseModel):
    Name: str
    Email: str

# Define CRUD operations for User

@app.post("/users/")
def create_user(user: User):
    conn = createConnection()
    cursor = conn.cursor()
    query = "INSERT INTO User (Name, Email) VALUES (%s, %s)"
    values = (user.Name, user.Email)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User created successfully"}

@app.get("/users/")
def get_users():
    conn = createConnection()
    cursor = conn.cursor()
    query = "SELECT * FROM User"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"users": result}

@app.get("/users/{id}")
def get_user(id: int):
    conn = createConnection()
    cursor = conn.cursor()
    query = "SELECT * FROM User WHERE UserID = %s"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return {"user": result}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{id}")
def update_user(id: int, user: User):
    conn = createConnection()
    cursor = conn.cursor()
    query = "UPDATE User SET Name = %s, Email = %s WHERE UserID = %s"
    values = (user.Name, user.Email, id)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount > 0:
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{id}")
def delete_user(id: int):
    conn = createConnection()
    cursor = conn.cursor()
    query = "DELETE FROM User WHERE UserID = %s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount > 0:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
