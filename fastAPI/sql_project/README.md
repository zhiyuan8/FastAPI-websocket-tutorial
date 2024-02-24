In postman, here are a few examples

```
POST http://127.0.0.1:8081/auth

{
    "email": "user@example.com",
    "username": "username",
    "first_name": "First",
    "last_name": "Last",
    "password": "password123",
    "role": "user"
}
```

```
POST http://127.0.0.1:8081/auth/token

{
    "username": "username",
    "password": "password123"
}
```

Get user info:
Need to provide BEARER token in the header
```
GET http://127.0.0.1:8081/user
```