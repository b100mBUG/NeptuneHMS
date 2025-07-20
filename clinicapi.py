from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal
from collections import defaultdict
from fastapi import Depends
from datetime import datetime
import hashlib
from datetime import date
import re
from fastapi import HTTPException
from sqlalchemy import func
from database import (
    Patient,
    Worker,
    Drug,
    Diagnosis,
    Prescription,
    PrescriptionItem,
    LaboratoryRequest,
    LaboratoryResult,
    LaboratoryTest,
    Billing,
    Appointment,
    Service,
    Expiry
)
from clinicdantic import (
    PatientsIn, PatientsOut,
    WorkersIn, WorkersOut,
    DrugsIn, DrugsOut,
    DiagnosesIn, DiagnosesOut,
    Prescriptions,
    PrescriptionItems,
    Billings,
    LaboratoryRequests,
    LaboratoryResultsIn, LaboratoryResultsOut,
    LaboratoryTestsIn, LaboratoryTestsOut,
    AppointmentsIn, AppointmentsOut,
    ServicesIn, ServicesOut
)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# GET ENDPOINTS
# Getting patient data with search and sort criteria
@app.get("/all-patient-data/{sort_term}/{sort_dir}/{search_term}/")
def fetch_all_patient_data(sort_term: str, sort_dir: str, search_term: str, db: Session = Depends(get_db)):
    query = db.query(Patient)
    if sort_term == "Any":
        pats = query.all()

    elif sort_term == "Time":
        pats = query.order_by(Patient.date_added.desc()).all() if sort_dir == "desc" else query.order_by(Patient.date_added.asc()).all()

    elif sort_term == "Name":
        pats = query.order_by(Patient.patient_name.desc()).all() if sort_dir == "desc" else query.order_by(Patient.patient_name.asc()).all()

    elif sort_term == "Search":
        pats = query.filter(Patient.patient_name.ilike(f"%{search_term}%")).all()

    return [{
        "Name": pat.patient_name,
        "Email": pat.patient_email,
        "Phone": pat.patient_phone,
        "ID NO": pat.patient_id_number,
        "Gender": pat.patient_gender,
        "Address": pat.patient_address,
        "DOB": pat.patient_dob,
        "Date": pat.date_added
    } for pat in pats]
# Getting worker data with sort and search criteria
@app.get("/all-worker-data/{sort_term}/{sort_dir}/{search_term}/")
def fetch_all_worker_data(sort_term: str, sort_dir: str, search_term: str, db: Session = Depends(get_db)):
    query = db.query(Worker)
    if sort_term == "Any":
        wrks = query.all()
        
    elif sort_term == "Time":
        wrks = query.order_by(Worker.date_added.desc()).all() if sort_dir == "desc" else query.order_by(Worker.date_added.asc()).all()

    elif sort_term == "Name":
        wrks = query.order_by(Worker.worker_name.desc()).all() if sort_dir == "desc" else query.order_by(Worker.worker_name.asc()).all()

    elif sort_term == "Search":
        wrks = query.filter(Worker.worker_name.ilike(f"%{search_term}%")).all()

    return [{
        "ID": wrk.worker_id,
        "Name": wrk.worker_name,
        "Email": wrk.worker_email,
        "Phone": wrk.worker_phone,
        "ID NO": wrk.worker_id_number,
        "Gender": wrk.worker_gender,
        "Role": wrk.worker_role,
        "Password": wrk.worker_password,
        "DOB": wrk.worker_dob,
        "Date": wrk.date_added
    } for wrk in wrks]
# Getting drug data with search and sort criteria
@app.get("/all-drug-data/{sort_term}/{sort_dir}/{search_term}/")
def fetch_all_drug_data(sort_term: str, sort_dir: str, search_term: str, db: Session = Depends(get_db)):
    query = db.query(Drug)
    if sort_term == "Any":
        drugs = query.all()
        
    elif sort_term == "Time":
        drugs = query.order_by(Drug.date_added.desc()).all() if sort_dir == "desc" else query.order_by(Drug.date_added.asc()).all()

    elif sort_term == "Name":
        drugs = query.order_by(Drug.drug_name.desc()).all() if sort_dir == "desc" else query.order_by(Drug.drug_name.asc()).all()

    elif sort_term == "Search":
        drugs = query.filter(Drug.drug_name.ilike(f"%{search_term}%")).all()

    return [{
        "ID": drug.drug_id,
        "Name": drug.drug_name,
        "Category": drug.drug_category,
        "Desc": drug.drug_desc,
        "Qty": drug.drug_quantity,
        "Price": drug.drug_price,
        "Expiry": drug.drug_expiry,
        "Date": drug.date_added
    } for drug in drugs]
# Getting appointment data with search and sort criteria
@app.get("/all-appointment-data/{sort_term}/{sort_dir}/{search_term}/")
def fetch_all_appointment_data(sort_term: str, sort_dir: str, search_term: str, db: Session = Depends(get_db)):
    query = db.query(Appointment)
    if sort_term == "Any":
        apps = query.all()
        
    elif sort_term == "Time":
        apps = query.order_by(Appointment.date_requested.desc()).all() if sort_dir == "desc" else query.order_by(Appointment.date_requested.asc()).all()

    elif sort_term == "Name":
        apps = (
            query
            .join(Patient)
            .order_by(Patient.patient_name.desc() if sort_dir == "desc" else Patient.patient_name.asc())
            .all()
        )

    elif sort_term == "Search":
        apps = (
            query
            .join(Patient)
            .filter(Patient.patient_name.ilike(f"%{search_term}%"))
            .all()
        )

    return [{
        "Patient": app.patient.patient_name,
        "Doctor": app.consultant.worker_name,
        "Service": app.service.service_name,
        "Desc": app.appointment_desc,
        "Scheduled": app.date_scheduled,
        "Requested": app.date_requested,
        "Time": app.time_scheduled,
    } for app in apps]
# Getting prescription date with search and sort criteria
from collections import defaultdict

@app.get("/all-prescription-data/{sort_term}/{sort_dir}/{search_term}/")
def fetch_all_prescription_data(sort_term: str, sort_dir: str, search_term: str, db: Session = Depends(get_db)):
    query = db.query(Prescription)

    if sort_term == "Any":
        prescs = query.all()
    elif sort_term == "Time":
        prescs = query.order_by(Prescription.prescription_date.desc()).all() if sort_dir == "desc" else query.order_by(Prescription.prescription_date.asc()).all()
    elif sort_term == "Name":
        prescs = (
            query
            .join(Patient)
            .order_by(Patient.patient_name.desc() if sort_dir == "desc" else Patient.patient_name.asc())
            .all()
        )
    elif sort_term == "Search":
        prescs = (
            query
            .join(Patient)
            .filter(Patient.patient_name.ilike(f"%{search_term}%"))
            .all()
        )

    grouped = defaultdict(list)
    for presc in prescs:
        grouped[presc.patient.patient_name].append(presc)

    output = []
    for patient_name, presc_group in grouped.items():
        all_notes = []
        all_drugs = []
        all_qtys = []
        all_prescribers = set()
        all_dates = []

        for presc in presc_group:
            all_notes.extend([item.notes for item in presc.items])
            all_drugs.extend([item.drug.drug_name for item in presc.items])
            all_qtys.extend([item.drug_qty for item in presc.items])
            all_prescribers.add(presc.prescriber.worker_name)
            all_dates.append(str(presc.prescription_date).split(" ")[0])

        prescriber_display = ", ".join(all_prescribers)
        date_display = ", ".join(sorted(set(all_dates)))
        output.append({
            "Patient": patient_name,
            "Drugs": all_drugs,
            "Qty": all_qtys,
            "Presc": all_notes,
            "Prescriber": prescriber_display,
            "Date": date_display,
        })

    return output

# Getting all diagnosis data with search and sort criteria
@app.get("/all-diagnosis-data/{sort_term}/{sort_dir}/{search_term}/")
def fetch_all_diagnosis_data(sort_term: str, sort_dir: str, search_term: str, db: Session = Depends(get_db)):
    query = db.query(Diagnosis)
    if sort_term == "Any":
        diags = query.all()
        
    elif sort_term == "Time":
        diags = query.order_by(Diagnosis.date_diagnosed.desc()).all() if sort_dir == "desc" else query.order_by(Diagnosis.date_diagnosed.asc()).all()

    elif sort_term == "Name":
        diags = (
            query
            .join(Patient)
            .order_by(Patient.patient_name.desc() if sort_dir == "desc" else Patient.patient_name.asc())
            .all()
        )

    elif sort_term == "Search":
        diags = (
            query
            .join(Patient)
            .filter(Patient.patient_name.ilike(f"%{search_term}%"))
            .all()
        )

    return [{
        "Patient": diag.patient.patient_name,
        "Symptoms": diag.symptoms,
        "Findings": diag.findings,
        "Diagnosis": diag.suggested_diagnosis,
        "Doctor": diag.diagnoser.worker_name,
        "Date": diag.date_diagnosed,
    } for diag in diags]
# Getting all billing data with sort and search criteria
@app.get("/all-billing-data/{sort_term}/{sort_dir}/{search_term}/")
def fetch_all_billing_data(sort_term: str, sort_dir: str, search_term: str, db: Session = Depends(get_db)):
    query = db.query(Billing)
    if sort_term == "Any":
        bills = query.all()
        
    elif sort_term == "Time":
        bills = query.order_by(Billing.date.desc()).all() if sort_dir == "desc" else query.order_by(Billing.date.asc()).all()

    elif sort_term == "Name":
        bills = (
            query
            .join(Patient)
            .order_by(Patient.patient_name.desc() if sort_dir == "desc" else Patient.patient_name.asc())
            .all()
        )

    elif sort_term == "Search":
        bills = (
            query
            .join(Patient)
            .filter(Patient.patient_name.ilike(f"%{search_term}%"))
            .all()
        )

    return [{
        "Patient": bill.patient.patient_name,
        "Items": bill.items,
        "Total": bill.total,
        "Date": bill.date,
    } for bill in bills]
# Getting services data
@app.get("/all-services-data/")
def fetch_all_services_data(db: Session = Depends(get_db)):
    services = db.query(Service).all()

    return [{
        "Name": service.service_name,
        "Desc": service.service_desc,
        "Price": service.service_price,
    } for service in services]
# Getting tests data
@app.get("/all-test-data/")
def fetch_all_test_data(db: Session = Depends(get_db)):
    tests = db.query(LaboratoryTest).all()

    return [{
        "Name": test.test_name,
        "Desc": test.test_desc,
        "Price": test.test_price,
    } for test in tests]
# getting drugs by id
@app.get("/all-drug-data-by-id/{drug_id}")
def fetch_id_drug_data(drug_id: int, db: Session = Depends(get_db)):
    drug = db.query(Drug).filter_by(drug_id = drug_id).first()

    return {
        "ID": drug.drug_id,
        "Name": drug.drug_name,
        "Category": drug.drug_category,
        "Desc": drug.drug_desc,
        "Qty": drug.drug_quantity,
        "Price": drug.drug_price,
        "Expiry": drug.drug_expiry
    } 
@app.get("/ensure-admin-exist/", response_model=WorkersOut)
def validate_admin_exists(db: Session = Depends(get_db)):
    admin = db.query(Worker).filter_by(worker_role = "admin").first()
    if not admin:
        try:
            new_admin = Worker(
                worker_name = "admin",
                worker_email = "werefidelcastro@outlook.com",
                worker_phone = "0737841451",
                worker_id_number = "12345678",
                worker_role = "admin",
                worker_password = "Al.e.lunar4",
                worker_gender = "male",
                worker_dob = datetime.strptime("2006-05-02", "%Y-%m-%d").date()
            )
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
        except IntegrityError as e:
            raise HTTPException(status_code=500, detail="Error creating admin")
        return new_admin
    return admin
@app.get("/validate-expiry/")
def validate_app_expiry(db: Session = Depends(get_db)):
    expiry =  db.query(Expiry).first()
    if not expiry:
        expiry_record = Expiry()
        db.add(expiry_record)
        db.commit()
        return {"Message": "Expiry date created successfully"}
    if expiry.expiry_date <= datetime.today().date():
        return {"Message": "Expired"}

# Getting lab-results with search and sort criteria
@app.get("/all-labresult-data/{sort_term}/{sort_dir}/{search_term}/")
def fetch_all_labresult_data(sort_term: str, sort_dir: str, search_term: str, db: Session = Depends(get_db)):
    query = db.query(LaboratoryResult)
    if sort_term == "Any":
        resuls = query.all()
        
    elif sort_term == "Time":
        resuls = query.order_by(LaboratoryResult.date_requested.desc()).all() if sort_dir == "desc" else query.order_by(LaboratoryResult.date_requested.asc()).all()

    elif sort_term == "Name":
        resuls = (
            query
            .join(Patient)
            .order_by(Patient.patient_name.desc() if sort_dir == "desc" else Patient.patient_name.asc())
            .all()
        )

    elif sort_term == "Search":
        resuls = (
            query
            .join(Patient)
            .filter(Patient.patient_name.ilike(f"%{search_term}%"))
            .all()
        )

    return [{
        "Patient": resul.patient.patient_name,
        "Observations": resul.observations,
        "Conclusion": resul.conclusion,
        "Tech": resul.tech.worker_name,
        "Date": resul.date_requested,
    } for resul in resuls]
# Getting lab-requests with search and sort criteria
@app.get("/all-labrequest-data/{sort_term}/{sort_dir}/{search_term}/")
def fetch_all_labrequest_data(sort_term: str, sort_dir: str, search_term: str, db: Session = Depends(get_db)):
    query = db.query(LaboratoryRequest)
    if sort_term == "Any":
        reqs = query.all()
        
    elif sort_term == "Time":
        reqs = query.order_by(LaboratoryRequest.date_added.desc()).all() if sort_dir == "desc" else query.order_by(LaboratoryRequest.date_added.asc()).all()

    elif sort_term == "Name":
        reqs = (
            query
            .join(Patient)
            .order_by(Patient.patient_name.desc() if sort_dir == "desc" else Patient.patient_name.asc())
            .all()
        )

    elif sort_term == "Search":
        reqs = (
            query
            .join(Patient)
            .filter(Patient.patient_name.ilike(f"%{search_term}%"))
            .all()
        )

    return [{
        "Patient": req.patient.patient_name,
        "Doctor": req.doctor.worker_name,
        "Test": req.test.test_name,
        "Date": req.date_added
    } for req in reqs]
# Getting the workers by roles for signin purposes
@app.get("/signin-worker-data/{worker_name}/{worker_role}/")
def fetch_signin_data(worker_name: str, worker_role: str, db: Session = Depends(get_db)):

    query = db.query(Worker)

    worker = query.filter((Worker.worker_name == worker_name) & (Worker.worker_role == worker_role)).first()
    if not worker:
        print("Worker not found")
        return
    return {
        "ID": worker.worker_id,
        "Name": worker.worker_name,
        "Role": worker.worker_role,
        "Password": worker.worker_password,
    }
# Getting all the payments the patient is owing on that date
@app.get("/all-payments/{patient_name}")
def fetch_all_payments(patient_name: str, db: Session = Depends(get_db)):
    tests = (
        db
        .query(LaboratoryRequest)
        .join(Patient)
        .join(LaboratoryTest)
        .filter(
            (Patient.patient_name.ilike(f"%{patient_name}%")) & (func.date(LaboratoryRequest.date_added) == date.today())
        )
        .all()
    )

    pharmas = (
        db
        .query(Prescription)
        .join(Patient)
        .join(PrescriptionItem)
        .filter(
            (Patient.patient_name.ilike(f"%{patient_name}%")) & (func.date(Prescription.prescription_date) == date.today())
        )
        .all()
    )

    consultations = (
        db
        .query(Appointment)
        .join(Patient)
        .join(Service)
        .filter(
            (Patient.patient_name.ilike(f"%{patient_name}%")) & (func.date(Appointment.date_requested) == date.today())
        )
        .all()
    )


    test_fees = [{
        "Test": t.test.test_name,
        "Fee": t.test.test_price
    } for t in tests]

    drug_fees =  [
        {
            "Drug": i.drug.drug_name,
            "Count": i.drug_qty,
            "Fee": i.drug.drug_price * i.drug_qty
        }
        for p in pharmas for i in p.items
    ]
    cons_fees = [{
        "Service Name": c.service.service_name,
        "Fee": c.service.service_price
    } for c in consultations]

    return {
            "Tests": test_fees,
            "Drugs": drug_fees,
            "Cons": cons_fees,
        }
#PUT ENDPOINTS
# Adding patient data
@app.post("/add-patient-data", response_model=PatientsOut)
def add_patient(pat: PatientsIn, db: Session = Depends(get_db)):
    if pat.patient_gender not in ["male", "female"]:
        raise HTTPException(status_code=400, detail="Invalid gender selected!")
    if re.fullmatch(r"07\d{8}$", pat.patient_phone) is None:
        raise HTTPException(status_code=400, detail="Invalid phone number format!")
    if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", pat.patient_email) is None:
        raise HTTPException(status_code=400, detail="Invalid email format!")
    if not pat.patient_id_number.isdigit() or not (7 < len(pat.patient_id_number) <= 8):
        raise HTTPException(status_code=400, detail="Invalid ID number")
    try:
        new_patient = Patient(
            patient_name = pat.patient_name,
            patient_email = pat.patient_email,
            patient_phone = pat.patient_phone,
            patient_id_number = pat.patient_id_number,
            patient_address = pat.patient_address,
            patient_gender = pat.patient_gender,
            patient_dob = pat.patient_dob
        )
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="Data entered compromises database integrity!")
    return new_patient
# Adding worker data
@app.post("/add-worker-data", response_model=WorkersOut)
def add_worker(wrk: WorkersIn, db: Session = Depends(get_db)):
    if wrk.worker_gender not in ["male", "female"]:
        raise HTTPException(status_code=400, detail="Invalid gender selected!")
    if re.fullmatch(r"07\d{8}$", wrk.worker_phone) is None:
        raise HTTPException(status_code=400, detail="Invalid phone number format!")
    if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", wrk.worker_email) is None:
        raise HTTPException(status_code=400, detail="Invalid email format!")
    if not wrk.worker_id_number.isdigit() or not (7 < len(wrk.worker_id_number) <= 8):
        raise HTTPException(status_code=400, detail="Invalid ID number")
    try:
        new_worker = Worker(
            worker_name = wrk.worker_name,
            worker_email = wrk.worker_email,
            worker_phone = wrk.worker_phone,
            worker_id_number = wrk.worker_id_number,
            worker_role = wrk.worker_role,
            worker_password = wrk.worker_password,
            worker_gender = wrk.worker_gender,
            worker_dob = wrk.worker_dob
        )
        db.add(new_worker)
        db.commit()
        db.refresh(new_worker)
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="Data entered compromises database integrity!")
    return new_worker
# Adding appointment data
@app.post("/add-appointment-data/{patient_name}/{doctor_name}/{service_name}", response_model=AppointmentsOut)
def add_appointment(patient_name: str, doctor_name: str, service_name: str, app: AppointmentsIn, db: Session = Depends(get_db)):

    pat = db.query(Patient).filter_by(patient_name = patient_name).first()
    cons = db.query(Worker).filter_by(worker_name = doctor_name).first()
    serv = db.query(Service).filter_by(service_name = service_name).first()
    if not pat:
        raise HTTPException(status_code=400, detail = f"No patient with name {patient_name}")
    if not cons:
        raise HTTPException(status_code=400, detail = f"No consultant with name {doctor_name}")
    if not serv:
        raise HTTPException(status_code=400, detail = f"No service with name {service_name}")
    try:
        new_appointment = Appointment(
            patient_id = pat.patient_id,
            consultant_id = cons.worker_id,
            service_id = serv.service_id,
            appointment_desc = app.appointment_desc,
            time_scheduled = app.time_scheduled,
            date_scheduled = app.date_scheduled,
        )
        # Calculating appointment fee
        appointment_fee = Billing(
            patient_id = pat.patient_id,
            items = serv.service_name,
            total = serv.service_price
        )
        db.add(new_appointment)
        db.add(appointment_fee)
        db.commit()
        db.refresh(new_appointment)
        db.refresh(appointment_fee)
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="Data entered compromises database integrity!")
    return new_appointment
# Adding drug data
@app.post("/add-drug-data", response_model=DrugsOut)
def add_drug(drug: DrugsIn, db: Session = Depends(get_db)):
    try:
        new_drug = Drug(
            drug_name = drug.drug_name,
            drug_category = drug.drug_category,
            drug_desc = drug.drug_desc,
            drug_quantity = drug.drug_quantity,
            drug_price = drug.drug_price,
            drug_expiry = drug.drug_expiry,
        )
        db.add(new_drug)
        db.commit()
        db.refresh(new_drug)
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="Data entered compromises database integrity!")
    return new_drug
# Adding prescription data
@app.post("/add-prescription-data/{patient_name}/{drug_name}/{user_id}", response_model=PrescriptionItems)
def add_prescription(patient_name: str, drug_name: str, user_id: str, presc: PrescriptionItems, db: Session = Depends(get_db)):

    pat = db.query(Patient).filter_by(patient_name=patient_name).first()
    drug = db.query(Drug).filter_by(drug_name=drug_name).first()

    try:
        new_prescription = Prescription(
            patient_id = pat.patient_id,
            prescriber_id = user_id,
        )
        db.add(new_prescription)
        db.flush()
        # Adding prescribed drugs and their notes for each prescription added
        item = PrescriptionItem(
            prescription_id = new_prescription.prescription_id,
            drug_id = drug.drug_id,
            drug_qty = presc.drug_qty,
            notes = presc.notes
        )
        # Calculating fees for each drug prescribed
        drug_fees = Billing(
            patient_id = pat.patient_id,
            items = drug.drug_name,
            total = drug.drug_price * presc.drug_qty
        )
        db.add(item)
        db.add(drug_fees)
        drug.drug_quantity -= presc.drug_qty
        db.commit()
        db.refresh(item)
        db.refresh(new_prescription)
        db.refresh(drug_fees)
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="Data entered compromises database integrity!")
    return item
# Adding diagnosis data
@app.post("/add-diagnosis-data/{patient_name}/{user_id}", response_model=DiagnosesOut)
def add_diagnosis(patient_name: str, user_id: str, diags: DiagnosesIn, db: Session = Depends(get_db)):
    pat = db.query(Patient).filter_by(patient_name=patient_name).first()
    if not pat:
        raise HTTPException(status_code=400, detail=f"No patient with name {patient_name}")
    try:
        new_diagnosis = Diagnosis(
            patient_id = pat.patient_id,
            symptoms = diags.symptoms,
            findings = diags.findings,
            suggested_diagnosis = diags.suggested_diagnosis,
            diagnoser_id = user_id
        )

        db.add(new_diagnosis)
        db.commit()
        db.refresh(new_diagnosis)
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="Data entered compromises database integrity!")
    return new_diagnosis
# Adding services data
@app.post("/add-services-data/", response_model=ServicesOut)
def add_service(service: ServicesIn, db: Session = Depends(get_db)):
    try:
        new_service = Service(
            service_name = service.service_name,
            service_desc = service.service_desc,
            service_price = service.service_price,
        )

        db.add(new_service)
        db.commit()
        db.refresh(new_service)
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="Data entered compromises database integrity!")
    return new_service
# Adding tests data
@app.post("/add-tests-data/", response_model=LaboratoryTestsOut)
def add_test(test: LaboratoryTestsIn, db: Session = Depends(get_db)):
    try:
        new_test = LaboratoryTest(
            test_name = test.test_name,
            test_desc = test.test_desc,
            test_price = test.test_price,
        )

        db.add(new_test)
        db.commit()
        db.refresh(new_test)
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="Data entered compromises database integrity!")
    return new_test
# Adding lab-results data
@app.post("/add-labresult-data/{patient_name}/{user_id}", response_model=LaboratoryResultsOut)
def add_labresult(patient_name: str, user_id: int, result: LaboratoryResultsIn, db: Session = Depends(get_db)):
    pat = db.query(Patient).filter_by(patient_name = patient_name).first()
    if not pat:
        raise HTTPException(status_code=400, detail=f"No patient with name {patient_name}")
    try:
        new_result = LaboratoryResult(
            patient_id = pat.patient_id,
            observations = result.observations,
            conclusion = result.conclusion,
            tech_id = user_id
        )

        db.add(new_result)
        db.commit()
        db.refresh(new_result)
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="Data entered compromises database integrity!")
    return new_result
# Adding lab_requests data
@app.post("/add-labrequest-data/{patient_name}/{user_id}/{test_name}", response_model=LaboratoryRequests)
def add_labrequest(patient_name: str, user_id: int, test_name: str, db: Session = Depends(get_db)):
    pat = db.query(Patient).filter_by(patient_name = patient_name).first()
    test = db.query(LaboratoryTest).filter_by(test_name = test_name).first()
    if not pat:
        raise HTTPException(status_code=400, detail=f"No patient with name {patient_name}")
    if not test:
        raise HTTPException(status_code=400, detail=f"No test with name {test_name}")
    try:
        new_request = LaboratoryRequest(
            patient_id = pat.patient_id,
            test_id = test.test_id,
            doctor_id = user_id
        )
        # Calculating fees for each lab test.
        lab_fees = Billing(
            patient_id = pat.patient_id,
            items = test.test_name,
            total = test.test_price
        )
        db.add(new_request)
        db.add(lab_fees)
        db.commit()
        db.refresh(new_request)
        db.refresh(lab_fees)
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="Data entered compromises database integrity!")
    return new_request

@app.put("/update-drug-data/{drug_id}")
def edit_drugs(drug_id: int, dru: DrugsIn, db: Session = Depends(get_db)):
    drug = db.query(Drug).filter_by(drug_id = drug_id).first()
    if drug:
        try:
            drug.drug_name = dru.drug_name
            drug.drug_category = dru.drug_category
            drug.drug_desc = dru.drug_desc
            drug.drug_quantity = dru.drug_quantity
            drug.drug_price = dru.drug_price
            drug.drug_expiry = dru.drug_expiry
            db.commit()
            return {"Message": f"{drug.drug_name} updated successfully!"}
        except IntegrityError as e:
            raise HTTPException(status_code=500, detail="Data entered compromises database integrity!")
    else:
        return {"Message": "Drug not found"}
@app.put("/renew-activation/{activation_key}")
def renew_plan(activation_key: str, db: Session = Depends(get_db)):
    if not activation_key:
        return {"Message": "Activation key empty!"}
    SECRET_KEY = "DROSOPHILLAMELANOGASTER"
    if not "|" in activation_key or len(activation_key.split("|")) != 3:
        return {"Message": "Invalid key format. Expected 3 parts seperated by '|'"}
    username, expiry_str, checksum = activation_key.split("|")
    expected_data = f"{username}-{expiry_str}-{SECRET_KEY}"
    expected_checksum = hashlib.sha256(expected_data.encode()).hexdigest()[:10].upper()

    if checksum != expected_checksum:
        return {"Message": "Checksum mismatch"}

    expiry_time = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
    if datetime.utcnow() > expiry_time:
        return {"Message": "Activation key expired!"}
    try:
        expiry = db.query(Expiry).first()
        expiry.expiry_date = expiry_time
        db.commit()
    except Exception as e:
        return {"Message": "Error validating activation key!"}
    return {"Message": "Renewed"}

@app.delete("/delete-drug-data/{drug_id}/")
def delete_drug(drug_id: int, db: Session = Depends(get_db)):
    drug = db.query(Drug).filter_by(drug_id = drug_id).first()
    if drug:
        if drug.prescriptions:
            return {"Message": f"{drug.drug_name} can't be deleted since is in use by other records"}
    else:
        return {"Message": "Drug not found!"}
    db.delete(drug)
    db.commit()
    return {"Message": "Drug deleted successfully!"}

@app.delete("/delete-worker-data/{worker_id}/")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter_by(worker_id = worker_id).first()
    if worker:
            has_links = (
                worker.diagnoses or
                worker.lab_requests or
                worker.lab_results or
                worker.appointments or
                worker.prescriptions
            )
            if has_links:
                return {"Message": f"{worker.worker_name} can't be deleted since is in use by other records"}
    db.delete(worker)
    db.commit()
    return {"Message": "Worker deleted successfully!"}