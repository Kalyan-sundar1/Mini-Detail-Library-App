from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import Header
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SuggestRequest(BaseModel):
    host_element: str
    adjacent_element: str
    exposure: str


@app.get("/details")
def list_details():
    response = supabase.table("details").select("*").execute()
    return response.data

@app.get("/details/search")
def search_details(q: str):
    response = supabase.table("details") \
        .select("*") \
        .or_(f"title.ilike.%{q}%,tags.ilike.%{q}%,description.ilike.%{q}%") \
        .execute()
    return response.data

@app.post("/suggest-detail")
def suggest_detail(req: SuggestRequest):

    rules = supabase.table("detail_usage_rules").select("*").execute().data

    best_match = None

    for rule in rules:
        if (rule["host_element"].lower() == req.host_element.lower()
            and rule["adjacent_element"].lower() == req.adjacent_element.lower()
            and rule["exposure"].lower() == req.exposure.lower()):
            best_match = rule
            break

    if not best_match:
        return {
            "detail": None,
            "explanation": "No matching detail found for the given context."
        }

    detail = supabase.table("details") \
        .select("*") \
        .eq("id", best_match["detail_id"]) \
        .execute().data[0]

    explanation = (
        f"This detail was selected because it matches the host element "
        f"'{req.host_element}', adjacent element '{req.adjacent_element}', "
        f"and exposure condition '{req.exposure}'."
    )

    return {
        "detail": detail,
        "explanation": explanation
    }




@app.get("/secure/details")
def get_secure_details(
    x_role: str = Header(...),
    x_user_id: str = Header(...)
):
    response = supabase.rpc(
        "secure_details",
        {
            "p_role": x_role,
            "p_uid": x_user_id
        }
    ).execute()

    return response.data

