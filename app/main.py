from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from openai import OpenAIError 
from .database import create_db_and_tables, get_session, engine
from .services import handle_purchase, initialize_stock
from .models import Soda 

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        
        if not session.exec(select(Soda)).first():
            initialize_stock(session)

@app.post("/buy")
async def buy_soda_endpoint(message: str, session: Session = Depends(get_session)):
    try:
        result = handle_purchase(message, session)
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        return result
    except HTTPException as e:
        raise e 
    except OpenAIError as e: 
        
        error_message = e.body.get('message', str(e)) if e.body else str(e)
        raise HTTPException(status_code=500, detail=f"Erro da OpenAI: {error_message}")
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@app.get("/parse")
async def parse_message_endpoint(message: str):
    from .instructor_utils import parse_message 
    try:
        parsed_result = parse_message(message)
        return {
            "intent": parsed_result.intent,
            "soda_type": parsed_result.soda_type,
            "quantity": parsed_result.quantity
        }
    except OpenAIError as e: 
        error_message = e.body.get('message', str(e)) if e.body else str(e)
        raise HTTPException(status_code=500, detail=f"Erro da OpenAI: {error_message}")
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"Erro ao processar mensagem com AI: {str(e)}")