from fastapi import FastAPI 
from routes import base_router
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI() 
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # يسمح بالوصول من أي مصدر. قم بتقييد هذا في الإنتاج
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
app.include_router(base_router)




