from fastapi import FastAPI
from routes import users
from routes import books
from routes import issued_books
from auth import authentication
app=FastAPI()
app.include_router(users.route, tags=["Users"])
app.include_router(books.route, tags=["Books"])
app.include_router(authentication.route, tags=["Auth"])
app.include_router(issued_books.route, tags=["Issued_Books"])