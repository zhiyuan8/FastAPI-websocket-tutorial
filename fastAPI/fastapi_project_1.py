from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional

class Book(BaseModel):
    id: Optional[int] = None  # Add an ID field
    title: str
    author: str
    category: Optional[str] = None
    publication_year: Optional[int] = None

app = FastAPI()
books_db: List[Book] = []  


@app.get("/")
async def health():
    return {"status": "ok","message": "Service is running"}

@app.get("/books/author/{book_author}")
async def get_books_by_author(book_author: str, category: Optional[str] = None):
    filtered_books = [book for book in books_db if book.author == book_author and (category is None or book.category == category)]
    return filtered_books

@app.get("/books/category")
async def get_books_by_category(category: Optional[str] = None):
    filtered_books = [book for book in books_db if book.category == category]
    if not filtered_books:
        raise HTTPException(status_code=404, detail="No books found in the specified category")
    return filtered_books

@app.post("/books")
async def create_book(new_book: Book):
    new_book.id = len(books_db) + 1  # Simple way to generate a unique ID
    books_db.append(new_book)
    return {"message": "Book created successfully", "book": new_book}

"""
The update_book endpoint is designed for complete updates of a resource. When a client sends a request to this endpoint, 
it is expected to provide all the relevant fields of the resource, not just the ones that have changed. 
"""
@app.put("/books/{book_id}")
async def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            updated_book.id = book_id  # Ensure the updated book retains its original ID
            books_db[i] = updated_book
            return {"message": f"Book with id {book_id} has been updated", "book": updated_book}
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

"""
Clients only need to send the fields that should be changed, without affecting other existing fields
"""
@app.patch("/books/{book_id}")
async def patch_book(book_id: int, patch_data: Book):
    stored_book_data = None
    for book in books_db:
        if book.id == book_id:
            stored_book_data = book
            update_data = patch_data.dict(exclude_unset=True)
            updated_book = stored_book_data.copy(update=update_data)
            books_db[books_db.index(book)] = updated_book
            return {"message": f"Book with id {book_id} has been patched", "book": updated_book}
    if stored_book_data is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[i]
            return {"message": f"Book with id {book_id} has been deleted"}
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

# uvicorn first_api:app --port 8101 --reload