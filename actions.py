import database as db

def show_prescriptions():
    prescs = db.session.query(db.Prescription).all()
    for presc in prescs:
        print(f"\nPatient: {presc.patient.patient_name}\nPrescription: {presc.prescription}\nDrug: {presc.drug.drug_name}\nDrug Ammount: {presc.drug_qty}")
    

show_prescriptions()