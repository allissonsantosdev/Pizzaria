from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "API está funcionando!", "docs": "/docs"}

app.include_router(auth_router)
app.include_router(order_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
