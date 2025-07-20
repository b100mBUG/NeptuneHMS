from pydantic import BaseModel, EmailStr
from datetime import date, time
from typing import Optional
class PatientsIn(BaseModel):
    patient_name: str
    patient_email: EmailStr
    patient_phone: str
    patient_id_number: str
    patient_gender: str
    patient_address: str
    patient_dob: date

    class Config:
        orm_mode = True

class PatientsOut(BaseModel):
    patient_id: int
    patient_name: str
    patient_email: EmailStr
    patient_phone: str
    patient_id_number: str
    patient_gender: str
    patient_address: str
    patient_dob: date

    class Config:
        orm_mode = True

class WorkersIn(BaseModel):
    worker_name: str
    worker_email: EmailStr
    worker_phone: str
    worker_id_number: str
    worker_role: str
    worker_password: str
    worker_gender: str
    worker_dob: date

    class Config:
        orm_mode = True

class WorkersOut(BaseModel):
    worker_id: int
    worker_name: str
    worker_email: EmailStr
    worker_phone: str
    worker_id_number: str
    worker_role: str
    worker_password: str
    worker_gender: str
    worker_dob: date

    class Config:
        orm_mode = True

class DrugsIn(BaseModel):
    drug_name: str
    drug_category: str
    drug_desc: str
    drug_quantity: int
    drug_price: float
    drug_expiry: date

    class Config:
        orm_mode = True

class DrugsOut(BaseModel):
    drug_id: int
    drug_name: str
    drug_category: str
    drug_desc: str
    drug_quantity: int
    drug_price: float
    drug_expiry: date

    class Config:
        orm_mode = True

class ServicesIn(BaseModel):
    service_name: str
    service_desc: str
    service_price: float

    class Config:
        orm_mode = True

class ServicesOut(BaseModel):
    service_id: int
    service_name: str
    service_desc: str
    service_price: float

    class Config:
        orm_mode = True

class DiagnosesIn(BaseModel):

    symptoms: str
    findings: str
    suggested_diagnosis: str

    class Config:
        orm_mode = True
class DiagnosesOut(BaseModel):
    diagnosis_id: int
    patient_id: int
    diagnoser_id: int

    symptoms: str
    findings: str
    suggested_diagnosis: str

    class Config:
        orm_mode = True

class LaboratoryTestsIn(BaseModel):
    test_name: str
    test_desc: str
    test_price: float

    class Config:
        orm_mode = True

class LaboratoryTestsOut(BaseModel):
    test_id: int
    test_name: str
    test_desc: str
    test_price: float

    class Config:
        orm_mode = True
class LaboratoryRequests(BaseModel):
    request_id: Optional[int] = None
    patient_id: int
    doctor_id: int
    test_id: int

    class Config:
        orm_mode = True

class LaboratoryResultsIn(BaseModel):

    observations: str
    conclusion: str

    class Config:
        orm_mode = True

class LaboratoryResultsOut(BaseModel):
    result_id: int
    patient_id: int
    tech_id: int

    observations: str
    conclusion: str

    class Config:
        orm_mode = True


class AppointmentsIn(BaseModel):

    appointment_desc: str
    date_scheduled: date
    time_scheduled: time

    class Config:
        orm_mode = True

class AppointmentsOut(BaseModel):
    appointment_id: Optional[int] = None
    consultant_id: int
    patient_id: int
    service_id: int

    appointment_desc: str
    date_scheduled: date
    time_scheduled: time

    class Config:
        orm_mode = True
    
class Prescriptions(BaseModel):
    prescription_id: Optional[int] = None
    patient_id: int
    prescriber_id: int

    class Config:
        orm_mode = True

class PrescriptionItems(BaseModel):
    drug_qty: int
    notes: str

    class Config:
        orm_mode = True

class Billings(BaseModel):
    billing_id: Optional[int] = None
    patient_id: int
    items: str
    total: float

    class Config:
        orm_mode = True


