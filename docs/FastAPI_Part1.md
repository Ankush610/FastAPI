## 📌 Defining FastAPI

**FastAPI** represents a contemporary, high-efficiency Python web framework tailored for the construction of web APIs, predicated upon **Python’s type hinting system**. The framework is engineered to facilitate rapid development of RESTful APIs, integrating native support for:

* ✅ Declarative data validation using the **Pydantic** library.
* ✅ Auto-generated, interactive API documentation conforming to **OpenAPI** specifications.
* ✅ Asynchronous request processing, ensuring enhanced scalability and responsiveness.
* ✅ Type-safe, modern, and syntactically coherent Python codebases.

> 🚀 **Rationale for FastAPI Adoption**

* Demonstrates performance metrics commensurate with leading Python frameworks.
* Facilitates automatic generation of API documentation via Swagger UI and ReDoc.
* Embeds robust data validation and parsing using **Pydantic** models.
* Supports clean, type-enforced code conducive to modern software engineering practices.
* Integrates seamlessly with contemporary Python tooling ecosystems.

---

## 📌 Minimal Code Example

Illustrating foundational route definition:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello FastAPI"}
```
```bash
run_command : uvicorn main:app --host 0.0.0.0 --port 80
```

---

## 📌 Automatic API Documentation

FastAPI auto-generates interactive and static documentation:

* **Swagger UI (Interactive API explorer)** 👉 `http://localhost:8000/docs`
* **ReDoc (Structured static documentation)** 👉 `http://localhost:8000/redoc`

---

## 📌 CRUD Operation Semantics

CRUD represents the foundational operations in data-centric applications:

| Operation | HTTP Method | Operational Intent          |
| --------- | ----------- | --------------------------- |
| Create    | `POST`      | Instantiate new resource    |
| Read      | `GET`       | Retrieve existing resources |
| Update    | `PUT`       | Modify existing resources   |
| Delete    | `DELETE`    | Remove resource instances   |

---

## 📌 Defining Route Handlers

### 1️⃣ `GET` Method

Retrieve data entities from server endpoints.

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

### 2️⃣ `POST` Method

Create new resource records.

```python
@app.post("/items/")
def create_item(item: dict):
    return item
```

### 3️⃣ `PUT` Method

Update existing resource entities.

```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"item_id": item_id, "updated_item": item}
```

### 4️⃣ `DELETE` Method

Eliminate specified resource records.

```python
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": "Item deleted"}
```

---

## 📌 Path Parameters

Path parameters extract variable components directly from endpoint URLs:

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
```

👉 Here, `item_id` is dynamically parsed from the request path.

---

## 📌 Query Parameters

Query parameters retrieve values from URL query strings:

```python
@app.get("/items/")
def get_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

👉 Example URL: `/items/?skip=5&limit=20`

---

## 📌 Annotating Path and Query Parameters

FastAPI's `Path` and `Query` utilities permit:

* Inclusion of descriptive metadata.
* Imposition of constraints (e.g., minimum/maximum values, regex patterns).
* Provision of illustrative example values.

```python
from fastapi import Path, Query

@app.get("/items/{item_id}")
def get_item(item_id: int = Path(..., description="Identifier for the item"),
             q: str = Query(None, description="Search query parameter")):
    return {"item_id": item_id, "q": q}
```

---

## 📌 Data Validation with Pydantic Models

Utilize Pydantic for structured data validation, serialization, and documentation automation.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
```

---

## 📌 Request Body Parsing via Pydantic Models

FastAPI seamlessly parses incoming JSON payloads into Pydantic model instances.

```python
@app.post("/items/")
def create_item(item: Item):
    return item
```

---

## 📌 Computed Fields in Pydantic Models

Leverage `@computed_field` for derived attribute computations within model definitions.

```python
from pydantic import computed_field

class Patient(BaseModel):
    height: float
    weight: float

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
```

---

## 📌 Custom JSON Responses

Deploy `JSONResponse` for explicit status codes and customized response payloads.

```python
from fastapi.responses import JSONResponse

@app.post("/success")
def success():
    return JSONResponse(status_code=200, content={"message": "Success!"})
```

---

## 📌 Structured Error Handling with `HTTPException`

Implement structured exception raising with FastAPI’s native `HTTPException` class.

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id != 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```

---
