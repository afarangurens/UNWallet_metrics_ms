from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from typing import List
from pydantic import BaseModel, Field, validator, root_validator

app = FastAPI(
    title="UNWallet_metrics_ms",
    description="UNWallet API for the metrics and datavisualization microservice.",
    version="0.0.1"
)

# CORS Set up
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

client = MongoClient('mongodb://mongo:27017')
db = client.unwallet_metrics_db
# Suggestions collection


@app.get("/")
def index():
    return {"message": "Welcome To FastAPI World"}

class Suggestion(BaseModel):
    user_id: str
    suggestion_tittle: str
    start_date: datetime
    end_date: datetime
    savings: float
    suggested_actions: List[str]

@app.post("/suggestions/")
async def create_suggestion(suggestion: Suggestion = Body(...)):
    collection = db.UNWallet_metrics_ms_suggestions

    suggestion_dict = suggestion.dict()
    suggestion_dict['start_date'] = suggestion_dict['start_date'].isoformat()
    suggestion_dict['end_date'] = suggestion_dict['end_date'].isoformat()
    
    try:
        result = collection.insert_one(suggestion_dict)
        new_suggestion = collection.find_one({"_id": ObjectId(result.inserted_id)})

        print(new_suggestion)
        return {"status": "success", "message": "Suggestion added correctly"}

    except:
        raise HTTPException(status_code=500, detail="Failed to add suggestion")
    

@app.get("/suggestions")
async def get_all_suggestions():
    collection = db.UNWallet_metrics_ms_suggestions

    suggestions = []

    for suggestion in collection.find():
        suggestion["_id"] = str(suggestion["_id"])
        suggestions.append(suggestion)
    
    return suggestions


@app.get("/suggestions/{suggestions_id}")
async def get_suggestion(suggestion_id: str):
    collection = db.UNWallet_metrics_ms_suggestions

    suggestion = collection.find_one({"_id": ObjectId(suggestion_id)})

    if suggestion:
        suggestion["_id"] = str(suggestion["_id"])
        
        return suggestion
    
    else:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    

@app.put("/suggestions/{suggestion_id}")
async def update_suggestion(suggestion_id: str, suggestion: Suggestion = Body(...)):
    collection = db.UNWallet_metrics_ms_suggestions

    suggestion_dict = suggestion.dict()
    suggestion_dict['start_date'] = suggestion_dict['start_date'].isoformat()
    suggestion_dict['end_date'] = suggestion_dict['end_date'].isoformat()

    try:
        result = collection.update_one({"_id": ObjectId(suggestion_id)}, {"$set": suggestion_dict})
        if result.modified_count == 1:
            updated_suggestion = collection.find_one({"_id": ObjectId(suggestion_id)})
            updated_suggestion["_id"] = str(updated_suggestion["_id"])
            return {"status": "success", "message": "Suggestion updated correctly", "suggestion": updated_suggestion}
        else:
            raise HTTPException(status_code=404, detail="Suggestion not found")

    except:
        raise HTTPException(status_code=500, detail="Failed to update suggestion")


@app.delete("/suggestions/{suggestion_id}")
async def delete_suggestion(suggestion_id: str):
    collection = db.UNWallet_metrics_ms_suggestions

    result = collection.delete_one({"_id": ObjectId(suggestion_id)})

    if result.deleted_count == 1:
        return {"Status": "success", "message": "Suggestion deleted correctly"}
    
    else:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    

class Category(BaseModel):
    category_name: str
    total_amount: float

class Data(BaseModel):
    labels: List[str]
    values: List[float]

class Visualization(BaseModel):
    ty_of_chart: str
    data: Data

class Statistics(BaseModel):
    user_id: str
    analysis_type: str
    start_date: datetime
    end_date: datetime
    categories: List[Category]
    visualization: Visualization


@app.post("/statistics/")
async def create_statistic(statistic: Statistics = Body(...)):
    collection = db.UNWallet_metrics_ms_statistics

    statistics_dict = statistic.dict()
    statistics_dict['start_date'] = statistics_dict['start_date'].isoformat()
    statistics_dict['end_date'] = statistics_dict['end_date'].isoformat()

    try:

        result = collection.insert_one(statistics_dict)
        new_statistic = collection.find_one({"_id": ObjectId(result.inserted_id)})
        
        print(new_statistic)

        return {"Status": "success", "message": "Statistic added correctly"}
    
    except:
        raise HTTPException(status_code=500, detail="Failed to add statistic")
    

@app.get("/statistics")
async def get_all_statistics():

    collection = db.UNWallet_metrics_ms_statistics
    statistics = []

    for statistic in collection.find():
        statistic["_id"] = str(statistic["_id"])
        statistics.append(statistic)

    return statistics

@app.get("/statistics/{statistic_id}")
async def get_statistic(statistic_id: str):
    collection = db.UNWallet_metrics_ms_statistics
    statistic = collection.find_one({"_id": ObjectId(statistic_id)})

    if statistic:
        statistic["_id"] = str(statistic["_id"])
        
        return statistic
    
    else:
        raise HTTPException(status_code=404, detail="Statistic not found")
    

@app.put("/statistics/{statistic_id}")
async def update_statistic(statistic_id: str, statistic: Statistics = Body(...)):
    collection = db.UNWallet_metrics_ms_statistics
    statistics_dict = statistic.dict()
    statistics_dict['start_date'] = statistics_dict['start_date'].isoformat()
    statistics_dict['end_date'] = statistics_dict['end_date'].isoformat()

    try:
        result = collection.update_one({"_id": ObjectId(statistic_id)}, {"$set": statistics_dict})

        if result.modified_count == 1:
            updated_statistic = collection.find_one({"_id": ObjectId(statistic_id)})
            updated_statistic["_id"] = str(updated_statistic["_id"])

            return {"status": "success", "message": "Statistic updated correctly", "statistic": updated_statistic}
        else:
            raise HTTPException(status_code=404, detail="Statistic not found")
    except:
        raise HTTPException(status_code=500, detail="Failed to update statistic")


@app.delete("/statistics/{statistic_id}")
async def delete_statistic(statistic_id: str):
    collection = db.UNWallet_metrics_ms_statistics
    result = collection.delete_one({"_id": ObjectId(statistic_id)})

    if result.deleted_count == 1:
        return {"status": "success", "message": "Statistic deleted correctly"}
    else:
        raise HTTPException(status_code=404, detail="Document not found")

class Expense(BaseModel):
    category: str
    amount: float

class MonthPlan(BaseModel):
    month: str
    expenses_by_category: List[Expense]
    monthly_income: float

    @validator('expenses_by_category')
    def validate_expenses(cls, v):
        if not v:
            raise ValueError("expenses_by_category cannot be empty")
        return v
    
    @root_validator
    def calculate_total_expenses(cls, values):
        expenses = [expense.amount for expense in values.get('expenses_by_category')]
        total_expenses = sum(expenses)

        values['total_expenses'] = total_expenses

        return values
    
    @root_validator
    def calculate_savings(cls, values):
        total_expenses = values.get('total_expenses')
        monthly_income = values.get('monthly_income')
        savings_goal = values.get('savings_goal')

        if total_expenses > monthly_income:
            raise ValueError('total_expenses cannot be greater than monthly income')
        if savings_goal and monthly_income - total_expenses < savings_goal:
            raise ValueError('savings_goal cannot be greater than monthly_income - total_expenses')

        savings = monthly_income - total_expenses if monthly_income > total_expenses else 0

        values['savings'] = savings

        return values

class BudgetPlan(BaseModel):
    user_id: str
    record_id: str
    savings_goal: float = None
    plan: List[MonthPlan] = Field(min_items=1)

    @validator('plan')
    def validate_plan(cls, v):
        if len(set([plan.month for plan in v])) != len(v):
            raise ValueError('month values in plan must be unique')
        return v
    

@app.post("/budget_plan/")
async def create_budget_plan(budget_plan: BudgetPlan = Body(...)):
    collection = db.UNWallet_metrics_ms_budgetplan
    budget_plan_dict = budget_plan.dict()

    try:
        result = collection.insert_one(budget_plan_dict)
        new_budget_plan = collection.find_one({"_id": ObjectId(result.inserted_id)})

        print(new_budget_plan)

        return {"status": "success", "message":"Budget plan added correctly"}
    
    except:
        raise HTTPException(status_code=500, detail="Failed to add budget plan")
    

@app.get("/budgetplans/")
async def get_budget_plans():
    collection = db.UNWallet_metrics_ms_budgetplan
    budget_plans = []

    for budget_plan in collection.find():
        budget_plan["_id"] = str(budget_plan["_id"])
        budget_plans.append(budget_plan)
    
    return budget_plans


@app.get("/budgetplans/{budgetplan_id}")
async def get_budget_plan(budgetplan_id: str):
    collection = db.UNWallet_metrics_ms_budgetplan
    budget_plan = collection.find_one({"_id": ObjectId(budgetplan_id)})

    if budget_plan:
        budget_plan["_id"] = str(budget_plan["_id"])
        
        return budget_plan
    
    else:
        raise HTTPException(status_code=404, detail="Statistic not found")

@app.put("/budgetplans/{budgetplan_id}")
async def update_statistic(budgetplan_id: str, budgetplan: BudgetPlan = Body(...)):
    collection = db.UNWallet_metrics_ms_budgetplan
    budget_plan_dict = budgetplan.dict()

    try:
        result = collection.update_one({"_id": ObjectId(budgetplan_id)}, {"$set": budget_plan_dict})

        if result.modified_count == 1:
            updated_plan = collection.find_one({"_id": ObjectId(budgetplan_id)})
            updated_plan["_id"] = str(updated_plan["_id"])

            return {"status": "success", "message":"Budget plan updated correctly"}
        
        else:

            raise HTTPException(status_code=404, detail="Budget plan not found")
        
    except:

        raise HTTPException(status_code=500, detail="Failed to update budget plan")

@app.delete("/budgetplans/{budgetplan_id}")
async def delete_budgetplan(budgetplan_id: str):
    collection = db.UNWallet_metrics_ms_budgetplan

    result = collection.delete_one({"_id": ObjectId(budgetplan_id)})

    if result.deleted_count == 1:
        return {"status":"success", "message":"Budget plan deleted"}
    
    else:
        raise HTTPException(status_code=404, detail="Budget plan not found")
