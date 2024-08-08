from fastapi import FastAPI
from pydantic import BaseModel

import google.generativeai as genai
app = FastAPI()
genai.configure(api_key="")
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
 
 # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
history=[
    ]
    )

def generatedata(prompt):



   

    response = chat_session.send_message(prompt)

    return response.text




class data(BaseModel):
    code: str
    function: str
 
@app.post('/users2/test_code')
def getdata(input:data):
    prompt = f'''{input.code} \n Analyse this code and find the function named {input.function}.
    Understand that function more carefully and find if there any scope for optimization. If the
    function is optimized then return the response in the json format which contains 2 keys. One key is
    <function name>" and value is {input.function}. Another key is "definition" and value is optimized or normal function code.
    If there is no function with the name {input.function} then create a function with the suitable definition.
    Only give the json response nothing more. Dont add thrible quotes or titles or anything to the response. Give only the Json value.
    dont give unnecessary information.'''
    return generatedata(prompt)
