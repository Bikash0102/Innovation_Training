import google.generativeai as genai

genai.configure(api_key="AIzaSyD2OoxR5OJwP48f83Sf3vlk3HxF2kB9Pds")

model = genai.GenerativeModel('gemini-1.5-flash')

print(model)


