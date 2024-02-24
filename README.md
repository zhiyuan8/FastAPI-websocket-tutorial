# Python-restfulAPI

# FAST API
HTTP request CRUD
- get : read and retrieve data
    - Path paramters, `@app.get("/books/author/{book_author}")`
- post : create method and submit data
- put : update the entire resource, it is expected to provide all the relevant fields of the resource
- patch : update part of the resource, Clients only need to send the fields that should be changed, without affecting other existing fields
- delete : delete the resource
- head
- options

## FastAPI Practices
### Pydantic
Compare with Pydantic v1
- .dict() function is now renamed to .model_dump()
- schema_extra function within a Config class is now renamed to json_schema_extra
- Optional variables need a =None example: id: Optional[int] = None

### HTTPException


### router


# Reference
- [fastapi-the-complete-course](https://github.com/codingwithroby/fastapi-the-complete-course)