from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,conlist
from typing import List,Optional
import pandas as pd
from model import recommend,output_recommended_recipes
import uvicorn
import pandas as pd


print("Loading dataset...")

try:
    dataset=pd.read_csv('dataset2.csv')
    print("✅ Dataset loaded successfully!")
    print("Loaded columns:", dataset.columns.tolist())
    print(dataset.head())
except FileNotFoundError:
    print("❌ Dataset file not found. Check the path and file name.")
    dataset = None
except Exception as e:
    print("❌ Failed to load dataset:", str(e))
    dataset = None


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class params(BaseModel):
    n_neighbors:int=5
    return_distance:bool=False

class PredictionIn(BaseModel):
    nutrition_input: list[float]
    ingredients: list[str] = []
    params: Optional[params]


class Recipe(BaseModel):
    Name:str
    CookTime:int
    PrepTime:int
    TotalTime:int
    RecipeIngredientParts:list[str]
    Calories:float
    FatContent:float
    SaturatedFatContent:float
    CholesterolContent:float
    SodiumContent:float
    CarbohydrateContent:float
    FiberContent:float
    SugarContent:float
    ProteinContent:float
    RecipeInstructions:list[str]

class PredictionOut(BaseModel):
    output: Optional[List[Recipe]] = None


@app.get("/")
def home():
    return {"health_check": "OK"}


@app.post("/predict",response_model=PredictionOut)
def update_item(prediction_input:PredictionIn):
    print(prediction_input)
    recommendation_dataframe=recommend(dataset,prediction_input.nutrition_input,prediction_input.ingredients,prediction_input.params.dict())
    print(recommendation_dataframe)
    output=output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output":None}
    else:
        return {"output":output}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)