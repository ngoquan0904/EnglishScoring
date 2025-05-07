from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scoring import grade_writing, extract_final_scores, API_KEYS

app = FastAPI()

class EssayRequest(BaseModel):
    essay_text: str

# API endpoint
@app.post("/grade")
def grade_api(req: EssayRequest):
    result = grade_writing(req.essay_text, API_KEYS)
    score = extract_final_scores(result)
    return {"score": score}
