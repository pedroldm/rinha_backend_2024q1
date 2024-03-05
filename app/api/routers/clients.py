from fastapi import APIRouter, HTTPException
from app.db.models.client import Client
from app.db.models.transaction import Transaction
from app.db.database import SessionLocal
from app.api.utils import TransactionPayload
from sqlalchemy import select
from datetime import datetime

client_router = APIRouter()

@client_router.post('/{client_id}/transacoes')
async def make_transaction(client_id: int, payload: TransactionPayload):
    if not 0 < len(payload['descricao']) <= 10:
        raise HTTPException(status_code=422, detail="Malformatted description")

    async with SessionLocal() as session:
        if not (client := await session.get(Client, client_id)):
            raise HTTPException(status_code=404, detail="Unregistered client")
        
        match payload['tipo']:
            case 'c':
                client.balance = int(client.balance) + payload['valor']
            case 'd':
                if abs(client.balance - payload['valor']) > client.limit:
                    raise HTTPException(status_code=422, detail="Invalid operation")
                client.balance = int(client.balance) - payload['valor']
            case _:
                raise HTTPException(status_code=422, detail="Unknown operation")

        session.add(Transaction(
            client_id=client_id,
            value=payload['valor'],
            type=payload['tipo'],
            description=payload['descricao']
        ))

        response = {"limite": client.limit, "saldo": client.balance}
        await session.commit()
        return response

@client_router.get('/{client_id}/extrato')
async def get_client_extract(client_id: int):
    async with SessionLocal() as session:
        if not (client := await session.get(Client, client_id)):
            raise HTTPException(status_code=404, detail="Unregistered client")
        
        stmt = select(Transaction).where(Transaction.client_id == client_id).order_by(Transaction.date.desc()).limit(10)
        result = await session.execute(stmt)
        transactions = result.scalars().all()

        return {
            "saldo": {
                "total": int(client.balance),
                "data_extrato": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "limite": int(client.limit)
            },
            "ultimas_transacoes": [
                {
                    "valor": t.value,
                    "tipo": t.type,
                    "descricao": t.description,
                    "realizada_em": t.date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                } 
                for t in transactions
            ]
        }
