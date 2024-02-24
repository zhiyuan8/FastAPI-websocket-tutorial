from fastapi import FastAPI
from routers import auth, todos, admin, users, database, models

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# uvicorn main:app --reload --port 8081