from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os
from mangum import Mangum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

current_dir = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_dir, 'q-vercel-python.json')) as f:
        students_data = json.load(f)
except FileNotFoundError:
    students_data = []
    print("Warning: 'q-vercel-python.json' not found. Proceeding with empty data.")
except json.JSONDecodeError:
    students_data = []
    print("Warning: 'q-vercel-python.json' contains invalid JSON. Proceeding with empty data.")

@app.get("/api")
async def get_marks(name: List[str] = Query(None)):
    if not name:
        return {"error": "Please provide at least one name"}

    results = []
    for student_name in name:
        mark = next((student["marks"] for student in students_data
                     if student["name"].lower() == student_name.lower()), None)
        if mark is not None:
            results.append({"name": student_name, "marks": mark})
        else:
            results.append({"name": student_name, "error": "Student not found"})
    return {"results": results}

@app.get("/")
async def root():
    return {"message": "Student Marks API. Use /api?name=X&name=Y to get marks."}

handler = Mangum(app)
