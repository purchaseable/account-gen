from fastapi import FastAPI, Request
from generator import create_account
import uvicorn

app = FastAPI()

@app.post("/create_account")
async def create_account_endpoint(request: Request):
    data = await request.json()
    result = await create_account(
        email=data["email"],
        proxy=data["proxy"],
        niche=data["niche"]
    )
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)