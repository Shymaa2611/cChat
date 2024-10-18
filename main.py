from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from inference import inference


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get('/')
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.get('/get_answer/')
def get_answer(query: str):
    response={
        "answer":inference(query)
    }
    

    return response