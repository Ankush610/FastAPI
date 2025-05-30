from fastapi import FastAPI, HTTPException , Path , Query
from pydantic import BaseModel , Field , computed_field
from typing import Annotated , Literal , Optional
from fastapi.responses import JSONResponse
import json

app = FastAPI()

class Patient(BaseModel):
    id : Annotated[str,Field(...,description="Id of the patient",examples=["P001"])]
    name : Annotated[str,Field(...,description="Name of the patient")]
    city : Annotated[str,Field(...,description="City where the patient is living")]
    age : Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    gender : Annotated[Literal['male','female','others'],Field(...,description="Gender of the patient")]
    height : Annotated[float,Field(...,gt=0,description="Height of the patient in meters")]
    weight : Annotated[float,Field(...,gt=0,description="Weight of the patient in kgs")]

    @computed_field
    @property 
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:   # here self.bmi will execute bmi method and use output here 
            return "underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"
        
class UpdatePatient(BaseModel):
    name : Annotated[Optional[str],Field(default=None)]
    city : Annotated[Optional[str],Field(default=None)]
    age : Annotated[Optional[int],Field(default=None)]
    gender : Annotated[Optional[Literal['male','female','others']],Field(default=None)]
    height : Annotated[Optional[float],Field(default=None)]
    weight : Annotated[Optional[float],Field(default=None)]


def load_data():
    with open('./data.json','r') as file:
        data = json.load(file)
        return data
    
def save_data(data):
    with open('./data.json','w') as file:
        json.dump(data,file)


#=============================== GET METHODS ==========================================

@app.get('/view')
def view_patient():
    data = load_data()
    return data

@app.get("/view/{item_id}")
def root(item_id: str = Path(...,description="Passing ID of Paitent Returns Deatils",example="P001")):  # Make sure an item is str using pydantic validation
    data = load_data()
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    # Get the filtered record(s) as a dict
    return data[item_id]   

@app.get("/sort")
def sort_patients(sort_by: str = Query(...,description="Sort on the basis of height / weight / bmi"),
                  order: str = Query("asc",description="sort in asc or desc order")):
    
    valid_sort_fields = ['height','weight','bmi']
    valid_order_fields = ['asc','desc']

    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400,detail=f"Invalid Field , Select from : {valid_sort_fields}")
    
    if order not in valid_order_fields:
        raise HTTPException(status_code=400,detail=f"Invalid Field , Select from : {valid_order_fields}")
    
    data = load_data()

    if order == 'asc':
        sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=False)
    else:
        sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=True)

    return sorted_data

#=============================== POST METHODS ==========================================

@app.post("/create")
def create_patient(patient : Patient): # expects json like form with Patient class parameters

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient Already Exist")
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    save_data(data)

    return JSONResponse(status_code=200,content="Patient Created Sucessfully")


@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: UpdatePatient):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient Record Does Not Exist")

    existing_patient_record = data[patient_id]

    updated_patient_dict = patient_update.model_dump(exclude_unset=True)

    for key , value in updated_patient_dict.items():

        existing_patient_record[key] = value

    existing_patient_record["id"] = patient_id

    modified_record = Patient(**existing_patient_record)

    final_output_dict = modified_record.model_dump(exclude=['id'])

    data[patient_id] = final_output_dict

    save_data(data)

    return JSONResponse(status_code=200,content="Data Updated Successfully")


@app.delete("/delete/{patient_id}")
def delete_record(patient_id : str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Record Does Not Exist")
    
    data.pop(patient_id)

    save_data(data)

    return JSONResponse(status_code=200,content="Data Deleted Successfully")
