## 📖 What are HTTP Status Codes?

HTTP **status codes** are 3-digit numbers returned by a server in response to a client's request to indicate the result of the request. They tell the client whether:

* the request was successful,
* there was an error, or
* some further action is needed.

---

## 📊 HTTP Status Code Classes

They’re grouped by their first digit:

| Class   | Range   | Meaning                                                                   |
| :------ | :------ | :------------------------------------------------------------------------ |
| **1xx** | 100–199 | Informational — request received, continuing process                      |
| **2xx** | 200–299 | Success — the request was successfully received, understood, and accepted |
| **3xx** | 300–399 | Redirection — further action needs to be taken to complete the request    |
| **4xx** | 400–499 | Client Error — the request contains bad syntax or cannot be fulfilled     |
| **5xx** | 500–599 | Server Error — the server failed to fulfill an apparently valid request   |

---

## 📋 Common Status Codes per Category

| Code    | Class | Meaning               | When it’s Used / Example                                                                  |
| :------ | :---- | :-------------------- | :---------------------------------------------------------------------------------------- |
| **100** | 1xx   | Continue              | Interim response indicating to continue the request                                       |
| **200** | 2xx   | OK                    | Standard response for successful HTTP requests                                            |
| **201** | 2xx   | Created               | Request has succeeded and created a new resource                                          |
| **204** | 2xx   | No Content            | Request succeeded, but no content to return                                               |
| **301** | 3xx   | Moved Permanently     | The resource has been moved to a new URL                                                  |
| **302** | 3xx   | Found                 | Temporarily redirected to a different URL                                                 |
| **304** | 3xx   | Not Modified          | Resource has not been modified since last request                                         |
| **400** | 4xx   | Bad Request           | Server cannot process request due to client error                                         |
| **401** | 4xx   | Unauthorized          | Request needs authentication                                                              |
| **403** | 4xx   | Forbidden             | Server understood the request but refuses to authorize it                                 |
| **404** | 4xx   | Not Found             | Requested resource could not be found                                                     |
| **409** | 4xx   | Conflict              | Conflict in the current state of the resource                                             |
| **422** | 4xx   | Unprocessable Entity  | Server understands the request but can’t process it (common in FastAPI validation errors) |
| **500** | 5xx   | Internal Server Error | A generic error when the server encounters an unexpected condition                        |
| **502** | 5xx   | Bad Gateway           | Server acting as a gateway received an invalid response                                   |
| **503** | 5xx   | Service Unavailable   | Server cannot handle the request (overloaded or down)                                     |
| **504** | 5xx   | Gateway Timeout       | Server acting as a gateway timed out waiting for a response                               |

---

## 📌 Quick FastAPI Example of Using Status Codes

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

@app.get("/resource/{item_id}")
def read_resource(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"item_id": item_id}
```
