from sqlalchemy import create_engine, Integer, Column, Date, String, Text, Float, ForeignKey, func, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timedelta

def get_db_path(folder="ClinicManagerData", filename="database.db"):
    from pathlib import Path

    base_dir = Path.home() / folder
    base_dir.mkdir(parents=True, exist_ok=True)

    return str(base_dir / filename)

print("db at: ", get_db_path())

Base = declarative_base()
engine = create_engine(f"sqlite:///{get_db_path()}", connect_args={"check_same_thread": False, "timeout": 10})

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class Worker(Base):
    __tablename__ = "workers"
    worker_id = Column(Integer, primary_key=True)
    worker_name = Column(String, nullable=False)
    worker_email = Column(String, nullable=True, unique=True)
    worker_phone = Column(String, nullable=False)
    worker_id_number = Column(String, nullable=False, unique=True)
    worker_password = Column(String, nullable=True)
    worker_role = Column(String, nullable=False)
    worker_gender = Column(String, nullable=False)
    worker_dob = Column(Date)
    date_added = Column(Date, default=func.current_date())

    diagnoses = relationship("Diagnosis", back_populates="diagnoser")
    lab_requests = relationship("LaboratoryRequest", back_populates="doctor")
    lab_results = relationship("LaboratoryResult", back_populates="tech")
    appointments = relationship("Appointment", back_populates="consultant")
    prescriptions = relationship("Prescription", back_populates="prescriber")

class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(Integer, primary_key=True)
    patient_name = Column(String, nullable=False)
    patient_email = Column(String, nullable=True, unique=True)
    patient_phone = Column(String, nullable=False)
    patient_id_number = Column(String, nullable=False, unique=True)
    patient_gender = Column(String, nullable=False)
    patient_address = Column(String, nullable=False)
    patient_dob = Column(Date)
    patient_weight = Column(Float, nullable=True, default=0)
    patient_chronic_condition = Column(String, nullable=True, default="Null")
    patient_allergy = Column(String, nullable=True, default="Null")
    date_added = Column(Date, default=func.current_date())

    diagnoses = relationship("Diagnosis", back_populates="patient")
    lab_requests = relationship("LaboratoryRequest", back_populates="patient")
    lab_results = relationship("LaboratoryResult", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
    prescriptions = relationship("Prescription", back_populates="patient")
    billings = relationship("Billing", back_populates="patient")

class Drug(Base):
    __tablename__ = "drugs"
    drug_id = Column(Integer, primary_key=True)
    drug_name = Column(String, nullable=False)
    drug_category = Column(String, nullable=True)
    drug_desc = Column(Text, nullable=False)
    drug_quantity = Column(Integer, nullable=False)
    drug_price = Column(Float, nullable=False)
    drug_expiry = Column(Date)
    date_added = Column(Date, default=func.current_date())

    prescriptions = relationship("PrescriptionItem", back_populates="drug")

class Service(Base):
    __tablename__ = "services"
    service_id = Column(Integer, primary_key=True)
    service_name = Column(String, nullable=False)
    service_price = Column(Float, nullable=False)
    service_desc = Column(Text, nullable=False)

    appointments = relationship("Appointment", back_populates="service")

class Diagnosis(Base):
    __tablename__ = "diagnosis"
    diagnosis_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete = "RESTRICT"))
    diagnoser_id = Column(Integer, ForeignKey("workers.worker_id", ondelete = "RESTRICT"))

    symptoms = Column(Text)
    findings = Column(Text)
    suggested_diagnosis = Column(String, nullable=False)
    date_diagnosed = Column(Date, default=func.current_date())

    patient = relationship("Patient", back_populates="diagnoses")
    diagnoser = relationship("Worker", back_populates="diagnoses")

class LaboratoryTest(Base):
    __tablename__ = "lab_tests"
    test_id = Column(Integer, primary_key=True)
    test_name = Column(String, nullable=False)
    test_desc = Column(Text, nullable=False)
    test_price = Column(Float, nullable=False)

    lab_requests = relationship("LaboratoryRequest", back_populates="test")

class LaboratoryRequest(Base):
    __tablename__ = "lab_requests"
    request_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete = "RESTRICT"))
    doctor_id = Column(Integer, ForeignKey("workers.worker_id", ondelete = "RESTRICT"))
    test_id = Column(Integer, ForeignKey("lab_tests.test_id", ondelete = "RESTRICT"))
    date_added = Column(Date, default=func.current_date())

    doctor = relationship("Worker", back_populates="lab_requests")
    patient = relationship("Patient", back_populates="lab_requests")
    test = relationship("LaboratoryTest", back_populates="lab_requests")

class LaboratoryResult(Base):
    __tablename__ = "lab_results"
    result_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete = "RESTRICT"))
    tech_id = Column(Integer, ForeignKey("workers.worker_id", ondelete = "RESTRICT"))

    observations = Column(Text)
    conclusion = Column(Text)
    date_requested = Column(Date, default=func.current_date())

    patient = relationship("Patient", back_populates="lab_results")
    tech = relationship("Worker", back_populates="lab_results")

class Appointment(Base):
    __tablename__ = "appointments"
    appointment_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete = "RESTRICT"))
    consultant_id = Column(Integer, ForeignKey("workers.worker_id", ondelete = "RESTRICT"))
    service_id = Column(Integer, ForeignKey("services.service_id", ondelete = "RESTRICT"))

    appointment_desc = Column(Text)
    date_requested = Column(Date, default=func.current_date())
    date_scheduled = Column(Date)
    time_scheduled = Column(Time)

    patient = relationship("Patient", back_populates="appointments")
    consultant = relationship("Worker", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")

class Prescription(Base):
    __tablename__ = "prescriptions"
    prescription_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete = "RESTRICT"))
    prescriber_id = Column(Integer, ForeignKey("workers.worker_id", ondelete = "RESTRICT"))
    prescription_date = Column(Date, default=func.current_date())

    patient = relationship("Patient", back_populates="prescriptions")
    prescriber = relationship("Worker", back_populates="prescriptions")
    items = relationship("PrescriptionItem", back_populates="prescription")

class PrescriptionItem(Base):
    __tablename__ = "prescription_items"
    item_id = Column(Integer, primary_key=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.prescription_id", ondelete = "RESTRICT"))
    drug_id = Column(Integer, ForeignKey("drugs.drug_id", ondelete = "RESTRICT"))
    drug_qty = Column(Integer)
    notes = Column(Text, nullable=True)

    prescription = relationship("Prescription", back_populates="items")
    drug = relationship("Drug", back_populates="prescriptions")

class Billing(Base):
    __tablename__ = "billings"
    billing_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete = "RESTRICT"))
    items = Column(String, nullable=True)
    total = Column(Float, default=0)
    date = Column(Date, default=func.current_date())

    patient = relationship("Patient", back_populates="billings")

def get_trial_expiry():
    return datetime.utcnow() + timedelta(minutes=2)

class Expiry(Base):
    __tablename__ = "expiry"
    expiry_id = Column(Integer, primary_key=True)
    expiry_date = Column(Date, default=get_trial_expiry)

Base.metadata.create_all(engine)

