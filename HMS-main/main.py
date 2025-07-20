from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.dropdownitem import MDDropDownItem, MDDropDownItemText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDockedDatePicker, MDTimePickerDialHorizontal
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.widget import Widget
from kivymd.uix.divider import MDDivider
from kivymd.uix.boxlayout import MDBoxLayout
import csv
import hashlib
from kivymd.uix.label import MDIcon
from sqlalchemy import func
from kivymd.uix.filemanager import MDFileManager
from collections import defaultdict
from functools import partial
import os, sys
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
import database
import json
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.metrics import dp, sp
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogButtonContainer, MDDialogContentContainer, MDDialogSupportingText

def resource_path(relative_path):
    return os.path.join(sys._MEIPASS, relative_path) if hasattr(sys, '_MEIPASS') else os.path.join(os.path.abspath('.'), relative_path)

class PatientsRow(MDCard):
    patient_name = StringProperty("")
    patient_email = StringProperty("")
    patient_phone = StringProperty("")
    patient_id_no = StringProperty("")
    patient_gender = StringProperty("")
    patient_address = StringProperty("")
    patient_dob = StringProperty("")
    patient_age = StringProperty("")
    patient_date_added = StringProperty("")
    show_profile = ObjectProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)
        self.radius = (0, 0, 0, 0)

        self.on_release = lambda: self.show_profile()

        self.name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.email_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.phone_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.id_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.gender_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.dob_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.address_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.age_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.date_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")


        self.add_widget(self.name_label)
        self.add_widget(self.email_label)
        self.add_widget(self.phone_label)
        self.add_widget(self.id_label)
        self.add_widget(self.gender_label)
        self.add_widget(self.address_label)
        self.add_widget(self.dob_label)
        self.add_widget(self.age_label)
        self.add_widget(self.date_label)

        self.bind(patient_name=lambda inst, val: setattr(self.name_label, 'text', val))
        self.bind(patient_email=lambda inst, val: setattr(self.email_label, 'text', val))
        self.bind(patient_phone=lambda inst, val: setattr(self.phone_label, 'text', val))
        self.bind(patient_id_no=lambda inst, val: setattr(self.id_label, 'text', val))
        self.bind(patient_gender=lambda inst, val: setattr(self.gender_label, 'text', val))
        self.bind(patient_address=lambda inst, val: setattr(self.address_label, 'text', val))
        self.bind(patient_dob=lambda inst, val: setattr(self.dob_label, 'text', val))
        self.bind(patient_age=lambda inst, val: setattr(self.age_label, 'text', val))
        self.bind(patient_date_added=lambda inst, val: setattr(self.date_label, 'text', val)) 

class WorkersRow(MDCard):
    worker_name = StringProperty("")
    worker_email = StringProperty("")
    worker_phone = StringProperty("")
    worker_id_no = StringProperty("")
    worker_gender = StringProperty("")
    worker_role = StringProperty("")
    worker_dob = StringProperty("")
    worker_age = StringProperty("")
    worker_date_added = StringProperty("")
    remove_worker = ObjectProperty("")
    show_profile = ObjectProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)
        self.radius = (0, 0, 0, 0)
        self.on_release = lambda: self.show_profile()

        self.name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.email_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.phone_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.id_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.gender_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.dob_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.role_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.age_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.date_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")

        remove_worker_btn = MDIconButton(icon = "trash-can", on_release = lambda x: self.remove_worker())

        self.add_widget(self.name_label)
        self.add_widget(self.email_label)
        self.add_widget(self.phone_label)
        self.add_widget(self.id_label)
        self.add_widget(self.gender_label)
        self.add_widget(self.role_label)
        self.add_widget(self.dob_label)
        self.add_widget(self.age_label)
        self.add_widget(self.date_label)
        self.add_widget(remove_worker_btn)

        self.bind(worker_name=lambda inst, val: setattr(self.name_label, 'text', val))
        self.bind(worker_email=lambda inst, val: setattr(self.email_label, 'text', val))
        self.bind(worker_phone=lambda inst, val: setattr(self.phone_label, 'text', val))
        self.bind(worker_id_no=lambda inst, val: setattr(self.id_label, 'text', val))
        self.bind(worker_gender=lambda inst, val: setattr(self.gender_label, 'text', val))
        self.bind(worker_role=lambda inst, val: setattr(self.role_label, 'text', val))
        self.bind(worker_dob=lambda inst, val: setattr(self.dob_label, 'text', val))
        self.bind(worker_age=lambda inst, val: setattr(self.age_label, 'text', val))
        self.bind(worker_date_added=lambda inst, val: setattr(self.date_label, 'text', val)) 

class DrugsRow(MDCard):
    drug_name = StringProperty("")
    drug_category = StringProperty("")
    drug_desc = StringProperty("")
    drug_quantity = StringProperty("")
    drug_price = StringProperty("")
    drug_expiry = StringProperty("")
    best_before = StringProperty("")
    status = StringProperty("")
    edit_drug = ObjectProperty("")
    remove_drug = ObjectProperty("")
    show_profile = ObjectProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)
        self.radius = (0, 0, 0, 0)
        self.on_release = lambda : self.show_profile()

        self.name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.category_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.desc_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.quantity_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.price_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.expiry_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.best_before_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.status_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        remove_drug_btn = MDIconButton(icon = "trash-can", on_release = lambda x: self.remove_drug())
        edit_drug_btn = MDIconButton(icon = "pencil-outline", on_release = lambda x: self.edit_drug())

        self.add_widget(self.name_label)
        self.add_widget(self.category_label)
        self.add_widget(self.desc_label)
        self.add_widget(self.quantity_label)
        self.add_widget(self.price_label)
        self.add_widget(self.expiry_label)
        self.add_widget(self.best_before_label)
        self.add_widget(self.status_label)
        self.add_widget(edit_drug_btn)
        self.add_widget(remove_drug_btn)

        self.bind(drug_name=lambda inst, val: setattr(self.name_label, 'text', val))
        self.bind(drug_category=lambda inst, val: setattr(self.category_label, 'text', val))
        self.bind(drug_desc=lambda inst, val: setattr(self.desc_label, 'text', val))
        self.bind(drug_quantity=lambda inst, val: setattr(self.quantity_label, 'text', val))
        self.bind(drug_price=lambda inst, val: setattr(self.price_label, 'text', f"Ksh. {val}"))
        self.bind(drug_expiry=lambda inst, val: setattr(self.expiry_label, 'text', val))
        self.bind(best_before=lambda inst, val: setattr(self.best_before_label, 'text', val))
        self.bind(status=lambda inst, val: setattr(self.status_label, 'text', val))
        self.bind(status=self.on_status_change)
        self.bind(best_before = self.on_safety_change)

    def on_status_change(self, instance, value):
        self.status_label.text = value
        if value.lower() == "restock":
            self.status_label.text_color = "red"
        else:
            self.status_label.text_color = "green"
    
    def on_safety_change(self, instance, value):
        self.best_before_label.text = value
        if value.lower() == "expired":
            self.best_before_label.text_color = "red"
        else:
            self.best_before_label.text_color = "green"


class AppointmentsRow(MDCard):
    patient_name = StringProperty("")
    consultant_name = StringProperty("")
    service_name = StringProperty("")
    service_desc = StringProperty("")
    date_scheduled = StringProperty("")
    time_scheduled = StringProperty("")
    date_added = StringProperty("")
    show_profile = ObjectProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)
        self.radius = (0, 0, 0, 0)
        self.on_release =  lambda: self.show_profile()

        self.pat_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.cons_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.service_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.service_desc_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.date_scheduled_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.time_scheduled_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.date_added_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
    
        self.add_widget(self.pat_name_label)
        self.add_widget(self.cons_name_label)
        self.add_widget(self.service_name_label)
        self.add_widget(self.service_desc_label)
        self.add_widget(self.date_scheduled_label)
        self.add_widget(self.time_scheduled_label)
        self.add_widget(self.date_added_label)

        self.bind(patient_name=lambda inst, val: setattr(self.pat_name_label, 'text', val))
        self.bind(consultant_name=lambda inst, val: setattr(self.cons_name_label, 'text', val))
        self.bind(service_name=lambda inst, val: setattr(self.service_name_label, 'text', val))
        self.bind(service_desc=lambda inst, val: setattr(self.service_desc_label, 'text', val))
        self.bind(date_scheduled=lambda inst, val: setattr(self.date_scheduled_label, 'text', val))
        self.bind(time_scheduled=lambda inst, val: setattr(self.time_scheduled_label, 'text', val))
        self.bind(date_added=lambda inst, val: setattr(self.date_added_label, 'text', val))

class PrescriptionsRow(MDCard):
    patient_name = StringProperty("")
    prescription = ListProperty("")
    drug_name = ListProperty("")
    drug_quantity = ListProperty("")
    pharmacist = StringProperty("")
    date_added = StringProperty("")
    show_profile = ObjectProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)
        self.radius = (0, 0, 0, 0)
        self.on_release = lambda: self.show_profile()

        self.pat_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.prescription_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.drug_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.drug_quantity_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.pharmacist_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.date_added_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
    
        self.add_widget(self.pat_name_label)
        self.add_widget(self.prescription_label)
        self.add_widget(self.drug_name_label)
        self.add_widget(self.drug_quantity_label)
        self.add_widget(self.pharmacist_label)
        self.add_widget(self.date_added_label)

        self.bind(patient_name=lambda inst, val: setattr(self.pat_name_label, 'text', val))
        self.bind(prescription=lambda inst, val: setattr(self.prescription_label, 'text', f"{val}"))
        self.bind(drug_name=lambda inst, val: setattr(self.drug_name_label, 'text', f"{val}"))
        self.bind(drug_quantity=lambda inst, val: setattr(self.drug_quantity_label, 'text', f"{val}"))
        self.bind(pharmacist=lambda inst, val: setattr(self.pharmacist_label, 'text', val))
        self.bind(date_added=lambda inst, val: setattr(self.date_added_label, 'text', val))

class DiagnosisRow(MDCard):
    patient_name = StringProperty("")
    symptoms = StringProperty("")
    findings = StringProperty("")
    suggested_diagnosis = StringProperty("")
    diagnoser = StringProperty("")
    date_added = StringProperty("")
    show_profile = ObjectProperty("")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)
        self.radius = (0, 0, 0, 0)
        self.on_release = lambda: self.show_profile()

        self.pat_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.symptoms_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.findings_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.suggested_diagnosis_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.diagnoser_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.date_added_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
    
        self.add_widget(self.pat_name_label)
        self.add_widget(self.symptoms_label)
        self.add_widget(self.findings_label)
        self.add_widget(self.suggested_diagnosis_label)
        self.add_widget(self.diagnoser_label)
        self.add_widget(self.date_added_label)

        self.bind(patient_name=lambda inst, val: setattr(self.pat_name_label, 'text', val))
        self.bind(symptoms=lambda inst, val: setattr(self.symptoms_label, 'text', val))
        self.bind(findings=lambda inst, val: setattr(self.findings_label, 'text', val))
        self.bind(suggested_diagnosis=lambda inst, val: setattr(self.suggested_diagnosis_label, 'text', val))
        self.bind(diagnoser=lambda inst, val: setattr(self.diagnoser_label, 'text', val))
        self.bind(date_added=lambda inst, val: setattr(self.date_added_label, 'text', val))

class ServicesRow(MDBoxLayout):
    service_name = StringProperty("")
    service_price = StringProperty("")
    service_desc = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)

        self.service_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.service_price_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.service_desc_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
    
        self.add_widget(self.service_name_label)
        self.add_widget(self.service_desc_label)
        self.add_widget(self.service_price_label)

        self.bind(service_name=lambda inst, val: setattr(self.service_name_label, 'text', val))
        self.bind(service_price=lambda inst, val: setattr(self.service_price_label, 'text', f"Ksh. {val}"))
        self.bind(service_desc=lambda inst, val: setattr(self.service_desc_label, 'text', val))
    

class LabTestsRow(MDBoxLayout):
    test_name = StringProperty("")
    test_desc = StringProperty("")
    test_price = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)

        self.test_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.test_price_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.test_desc_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
    
        self.add_widget(self.test_name_label)
        self.add_widget(self.test_desc_label)
        self.add_widget(self.test_price_label)

        self.bind(test_name=lambda inst, val: setattr(self.test_name_label, 'text', val))
        self.bind(test_desc=lambda inst, val: setattr(self.test_desc_label, 'text', val))
        self.bind(test_price=lambda inst, val: setattr(self.test_price_label, 'text', f"Ksh. {val}"))

class LabRequestsRow(MDCard):
    patient_name = StringProperty("")
    doctor_name = StringProperty("")
    test_name = StringProperty("")
    date_added = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)
        self.radius = (0, 0, 0, 0)

        self.patient_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.doctor_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.test_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.date_requested_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
    
        self.add_widget(self.patient_name_label)
        self.add_widget(self.doctor_name_label)
        self.add_widget(self.test_name_label)
        self.add_widget(self.date_requested_label)

        self.bind(patient_name=lambda inst, val: setattr(self.patient_name_label, 'text', val))
        self.bind(doctor_name=lambda inst, val: setattr(self.doctor_name_label, 'text', val))
        self.bind(test_name=lambda inst, val: setattr(self.test_name_label, 'text', val))
        self.bind(date_added=lambda inst, val: setattr(self.date_requested_label, 'text', val))

class LabResultsRow(MDCard):
    patient_name = StringProperty("")
    observations = StringProperty("")
    conclusions = StringProperty("")
    labtech = StringProperty("")
    date_added = StringProperty("")
    show_profile = ObjectProperty("")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)
        self.radius = (0, 0, 0, 0)
        self.on_release = lambda: self.show_profile()

        self.pat_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.observations_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.conclusions_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.labtech_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.date_added_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="blue", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
    
        self.add_widget(self.pat_name_label)
        self.add_widget(self.observations_label)
        self.add_widget(self.conclusions_label)
        self.add_widget(self.labtech_label)
        self.add_widget(self.date_added_label)

        self.bind(patient_name=lambda inst, val: setattr(self.pat_name_label, 'text', val))
        self.bind(observations=lambda inst, val: setattr(self.observations_label, 'text', val))
        self.bind(conclusions=lambda inst, val: setattr(self.conclusions_label, 'text', val))
        self.bind(labtech=lambda inst, val: setattr(self.labtech_label, 'text', val))
        self.bind(date_added=lambda inst, val: setattr(self.date_added_label, 'text', val))

class BillingsRow(MDBoxLayout):
    patient_name = StringProperty("")
    items = StringProperty("")
    total = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)

        self.pat_name_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.items_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
        self.total_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center", shorten = True, shorten_from = "right")
    
        self.add_widget(self.pat_name_label)
        self.add_widget(self.items_label)
        self.add_widget(self.total_label)

        self.bind(patient_name=lambda inst, val: setattr(self.pat_name_label, 'text', val))
        self.bind(items=lambda inst, val: setattr(self.items_label, 'text', f"{val}"))
        self.bind(total=lambda inst, val: setattr(self.total_label, 'text', f"Ksh. {val}"))

class NeptuneHMS(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.images_path = resource_path('assets')
        self.icon = resource_path('assets/neptune.png')

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )
        self.export_path = None

    def build(self):
        self.theme_cls.theme_name = "Light"
        self.theme_cls.primary_palette = "Lightgreen"
        return Builder.load_file(resource_path("clinicmanager.kv"))
    
    def on_start(self):
        database.make_admin()
    def sign_in_form(self, role):
        self.user_name = MDTextField(MDTextFieldHintText(text = "Username"))
        self.user_password = MDTextField(MDTextFieldHintText(text = "Password"), password = True)
        content = MDDialogContentContainer(orientation = "vertical", spacing = "10", padding = dp(5))
        content.add_widget(self.user_name)
        content.add_widget(self.user_password)
        self.signin_dialog = MDDialog(
            MDDialogIcon(icon = "account"),
            MDDialogHeadlineText(text = f"Sign In as {role}"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text = "Sign In"), 
                    on_release = lambda x, wrole = role.lower() : self.validate_worker(wrole)),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x :self.signin_dialog.dismiss()),
                spacing = dp(15)
            )
        )
        self.signin_dialog.open()
    
    def first_signin(self, val):
        self.sign_in_form(role=val)

    def validate_worker(self, worker_role):
        worker_name = self.user_name.text.strip().lower()
        worker = database.session.query(database.Worker).filter(
            (database.Worker.worker_name == worker_name) & (database.Worker.worker_role == worker_role)
        ).first()
        expiry = database.session.query(database.Expiry).first()
        if not expiry:
            expiry_record = database.Expiry()
            database.session.add(expiry_record)
            database.session.commit()
            return
        
        if expiry.expiry_date < datetime.utcnow().date():
            self.subscription_form()
            return
        
        if not worker:
            self.show_snack("Worker not found")
            return
        
        if self.user_password.text.strip() != worker.worker_password:
            self.show_snack("Incorrect password!!")
            return
        
        if worker_role == "admin":
             self.signin_dialog.dismiss()
             self.root.current = "admin_screen"
             self.show_patients("Any", "Any", "Any", self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)
             self.signed_in_user = worker
        elif worker_role.lower() == "receptionist":
            self.signin_dialog.dismiss()
            self.root.current = "reception_screen"
            self.signed_in_user = worker
        elif worker_role.lower() == "pharmacist":
            self.signin_dialog.dismiss()
            self.root.current = "chemist_screen"
            self.show_prescriptions("Any", "Any", "Any", self.root.ids.chem_prev, self.root.ids.chemrvb, self.root.ids.chem_cont_header)
            self.signed_in_user = worker
        elif worker_role.lower() == "doctor":
            self.signin_dialog.dismiss()
            self.root.current = "diagnosis_screen"
            self.show_diagnosis("Any", "Any", "Any", self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header)
            self.signed_in_user = worker
        elif worker_role.lower() == "labtech":
            self.signin_dialog.dismiss()
            self.show_diagnosis("Any", "Any", "Any", self.root.ids.lab_prev, self.root.ids.labrvb, self.root.ids.lab_cont_header)
            self.root.current = "lab_screen"
            self.signed_in_user = worker
    
    def subscription_form(self):
        self.activation_key = MDTextField(MDTextFieldHintText(text = "Enter Activation Key"))

        contact_cont = MDGridLayout(cols = 3, size_hint_y = None, height = dp(60))

        phone_box = MDBoxLayout(spacing = dp(5), size_hint_y = None, height = dp(60))
        phone_box.add_widget(MDIcon(icon = "phone", pos_hint = {"center_y":.5}, theme_icon_color = "Custom", icon_color = "blue"))
        phone_box.add_widget(MDLabel(text = "0737 841 451", bold = True, pos_hint = {"center_y":.5}, theme_text_color = "Custom", text_color = "navy"))

        whatsapp_box = MDBoxLayout(spacing = dp(5), size_hint_y = None, height = dp(60))
        whatsapp_box.add_widget(MDIcon(icon = "whatsapp", pos_hint = {"center_y":.5}, theme_icon_color = "Custom", icon_color = "green"))
        whatsapp_box.add_widget(MDLabel(text = "0737 841 451", bold = True, pos_hint = {"center_y":.5}, theme_text_color = "Custom", text_color = "teal"))

        email_box = MDBoxLayout(spacing = dp(5), size_hint_y = None, height = dp(60))
        email_box.add_widget(MDIcon(icon = "gmail", pos_hint = {"center_y":.5}, theme_icon_color = "Custom", icon_color = "purple"))
        email_box.add_widget(MDLabel(text = "werecastro2006@gmail.com", bold = True, pos_hint = {"center_y":.5}, theme_text_color = "Custom", text_color = "purple"))

        contact_cont.add_widget(phone_box)
        contact_cont.add_widget(whatsapp_box)
        contact_cont.add_widget(email_box)

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(30))
        content.add_widget(self.activation_key)
        content.add_widget(MDDivider())
        content.add_widget(MDLabel(text = "Get in touch", halign = "center"))
        content.add_widget(contact_cont)
        
        self.subscription_dialog = MDDialog(
            MDDialogIcon(icon = "cancel", theme_icon_color = "Custom", icon_color = "red"),
            MDDialogHeadlineText(text = "Caution!!"),
            MDDialogSupportingText(text = "Your plan expired! Please enter activation key bellow"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Submit"), on_release = lambda x: self.renew_plan()),
                Widget()
            ),
            auto_dismiss = False
            
        )

        self.subscription_dialog.open()
    
    def renew_plan(self):
        activation_key = self.activation_key.text.strip()
        if not activation_key:
            self.show_snack("Activation key empty")
            return
        SECRET_KEY = "DROSOPHILLAMELANOGASTER"
        try:
            username, expiry_str, checksum = activation_key.split("|")
            expected_data = f"{username}-{expiry_str}-{SECRET_KEY}"
            expected_checksum = hashlib.sha256(expected_data.encode()).hexdigest()[:10].upper()

            if checksum != expected_checksum:
                self.show_snack("Invalid activation key!!")
                return

            expiry_time = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S").date()
            if datetime.utcnow() > expiry_time:
                self.show_snack("Activation key expired!!")
                return

            expiry = database.session.query(database.Expiry).first()
            expiry.expiry_date = expiry_time
            database.session.commit()
            self.subscription_dialog.dismiss()
            self.show_snack("Subscription renewed. Enjoy")

        except Exception as e:
            self.show_snack("Error occured during processing of the key")
            return

    def patient_personal(self):
        self.patient_name = MDTextField(MDTextFieldHintText(text = "Full Name"))
        self.patient_email = MDTextField(MDTextFieldHintText(text = "Email Address"))
        self.patient_phone = MDTextField(MDTextFieldHintText(text = "Contact"), input_filter = "int")
        self.patient_id = MDTextField(MDTextFieldHintText(text = "ID Number"), input_filter = "int")
        self.patient_address = MDTextField(MDTextFieldHintText(text = "Address"))
        gender_box = MDBoxLayout(spacing = dp(10), size_hint_y = None, height = dp(80))
        dob_box = MDBoxLayout(spacing = dp(10), size_hint_y = None, height = dp(80))
        self.patient_gender = MDTextField(MDTextFieldHintText(text = "Gender"), pos_hint = {"center_y":.5})
        gender_btn = MDIconButton(icon = "chevron-down", pos_hint = {"center_y":.5}, on_release = lambda x: self.show_dropdown(["Male", "Female"], gender_btn, self.fill_pat_gender))
        dob_btn = MDIconButton(icon = "calendar", pos_hint = {"center_y":.5}, on_release = lambda x: self.show_date("patient_dob"))
        self.patient_dob = MDTextField(MDTextFieldHintText(text = "D.O.B"), pos_hint = {"center_y":.5})
        gender_box.add_widget(self.patient_gender)
        gender_box.add_widget(gender_btn)

        dob_box.add_widget(self.patient_dob)
        dob_box.add_widget(dob_btn)

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        content.add_widget(self.patient_name)
        content.add_widget(self.patient_email)
        content.add_widget(self.patient_phone)
        content.add_widget(self.patient_id)
        content.add_widget(self.patient_address)
        content.add_widget(gender_box)
        content.add_widget(dob_box)

        self.patient_dialog = MDDialog(
            MDDialogIcon(icon = "account-heart"),
            MDDialogHeadlineText(text = "Register Patients"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Register"), on_release = lambda x: self.add_patients()),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.patient_dialog.dismiss()),
                spacing = dp(10),
                padding = dp(10)
            )
        )
        self.patient_dialog.open()

    def add_patients(self, *args):
        name = self.patient_name.text.strip().lower() if self.patient_name.text.strip() else "patient_name"
        email = self.patient_email.text.strip().lower() if self.patient_email.text.strip() else "patient_email"
        phone = self.patient_phone.text.strip() if self.patient_phone.text.strip() else "123456789"
        id_no = self.patient_id.text.strip().lower() if self.patient_phone.text.strip() else "123456789"
        address = self.patient_address.text.strip().lower() if self.patient_address.text.strip() else "patient_address"
        gender = self.patient_gender.text.strip().lower() if self.patient_gender.text.strip() else "patient_gender"
        dob = datetime.strptime(self.patient_dob.text.strip(), "%d-%m-%Y").date() if self.patient_dob.text.strip() else datetime.strptime("1-1-2000", "%d-%m-%Y").date()

        new_patient = database.Patient(
            patient_name = name,
            patient_email = email,
            patient_phone = phone,
            patient_id_number = id_no,
            patient_address = address,
            patient_gender = gender,
            patient_dob = dob
        )
        try:
            database.session.add(new_patient)
            database.session.commit()
            self.show_snack(f"{name} added successfully!!")
        except IntegrityError as e:
            self.show_snack(f"Error: {e}!!")
            database.session.rollback()
            database.session.close()
            database.session = database.Session()
        self.show_patients("Any", "Any", "Any", self.root.ids.rec_prev, self.root.ids.rvb, self.root.ids.rec_cont_header)
    
    def appointment_form(self):
        self.pat_name = MDTextField(MDTextFieldHintText(text = "Patient Name"))
        self.consultant_name = MDTextField(MDTextFieldHintText(text = "Consultant Name"))
        name_box = MDBoxLayout(spacing = dp(10), size_hint_y = None, height = dp(80))
        self.service_name = MDTextField(MDTextFieldHintText(text = "Service Name"), pos_hint = {"center_y":.5})
        services = database.session.query(database.Service).all()
        service_btn = MDIconButton(icon = "chevron-down", pos_hint = {"center_y":.5}, on_release = lambda x: self.show_dropdown([service.service_name for service in services], service_btn, self.fill_services))
        name_box.add_widget(self.service_name)
        name_box.add_widget(service_btn)
        self.service_desc = MDTextField(MDTextFieldHintText(text = "Service Description"))
        schedule_box = MDBoxLayout(spacing = dp(10), size_hint_y = None, height = dp(80))
        time_box = MDBoxLayout(spacing = dp(10), size_hint_y = None, height = dp(80))
        self.schedule_date = MDTextField(MDTextFieldHintText(text = "Set On"), pos_hint = {"center_y":.5})
        date_btn = MDIconButton(icon = "calendar", pos_hint = {"center_y":.5}, on_release = lambda x: self.show_date("schedule_date"))
        time_btn = MDIconButton(icon = "clock", pos_hint = {"center_y":.5}, on_release = lambda x: self.time_dialog())
        self.schedule_time = MDTextField(MDTextFieldHintText(text = "Start At"), pos_hint = {"center_y":.5})
        schedule_box.add_widget(self.schedule_date)
        schedule_box.add_widget(date_btn)

        time_box.add_widget(self.schedule_time)
        time_box.add_widget(time_btn)

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        content.add_widget(self.pat_name)
        content.add_widget(self.consultant_name)
        content.add_widget(name_box)
        content.add_widget(self.service_desc)
        content.add_widget(schedule_box)
        content.add_widget(time_box)

        self.appointment_dialog = MDDialog(
            MDDialogIcon(icon = "calendar-clock"),
            MDDialogHeadlineText(text = "Schedule Appointments"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Schedule"), on_release = lambda x: self.add_appointments()),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.appointment_dialog.dismiss()),
                spacing = dp(10),
                padding = dp(10)
            )
        )
        self.appointment_dialog.open()
    
    def add_appointments(self, *args):
        patient_name = self.pat_name.text.strip().lower() if self.pat_name.text.strip() else "patient_name"
        consultant_name = self.consultant_name.text.strip().lower() if self.consultant_name.strip() else "consultant_name"
        service_name = self.service_name.text.strip().lower() if self.service_name.strip() else "service_name"
        service_desc = self.service_desc.text.strip().lower() if self.service_desc.strip() else "service_desc"
        date_scheduled = self.schedule_date.text.strip() if self.schedule_date.strip() else "1-1-2000"
        time_string = self.schedule_time.text.strip() if self.scedule_time.strip() else "00:00 AM"
        time_scheduled = datetime.strptime(time_string, "%H:%M %p").time()

        pat = (database.session.query(database.Patient).filter(database.Patient.patient_name == patient_name).first())
        cons = database.session.query(database.Worker).filter(database.Worker.worker_name == consultant_name).first()
        serv = database.session.query(database.Service).filter(database.Service.service_name == service_name).first()

        new_appointment = database.Appointment(
            patient_id = pat.patient_id,
            consultant_id = cons.worker_id,
            service_id = serv.service_id,
            appointment_desc = service_desc,
            time_scheduled = time_scheduled,
            date_scheduled = datetime.strptime(date_scheduled, "%d-%m-%Y").date(),
        )
        appointment_fee = database.Billing(
            patient_id = pat.patient_id,
            items = serv.service_name,
            total = serv.service_price
        )
        try:
            database.session.add(new_appointment)
            database.session.add(appointment_fee)
            database.session.commit()
            self.show_snack(f"Appointment added successfully!!")
        except IntegrityError as e:
            self.show_snack(f"Error: {e}!!")
            database.session.rollback()
            database.session.close()
            database.session = database.Session()
        self.show_appointments("Any", "Any", "Any", self.root.ids.rec_prev, self.root.ids.rvb, self.root.ids.rec_cont_header)
    
    def show_patients(self, sort_term, sort_dir, search_term, prev, prev_box, pat_header):
        if prev == self.root.ids.adm_prev or prev == self.root.ids.rec_prev:
            self.root.ids.rec_dialog_open.on_release = lambda : self.patient_personal()
            self.root.ids.adm_dialog_open.on_release = lambda : self.patient_personal()
        if sort_term == "Any":
            pats = database.session.query(database.Patient).all()
        elif sort_term == "Time":
            if sort_dir == "desc":
                pats = (
                    database.session
                    .query(database.Patient)
                    .order_by(database.Patient.date_added.desc())
                ).all()
            elif sort_dir == "asc":
                pats = (
                    database.session
                    .query(database.Patient)
                    .order_by(database.Patient.date_added.asc())
                ).all()
        elif sort_term == "Name":
            if sort_dir == "desc":
                pats = (
                    database.session
                    .query(database.Patient)
                    .order_by(database.Patient.patient_name.desc())
                ).all()
            elif sort_dir == "asc":
                pats = (
                    database.session
                    .query(database.Patient)
                    .order_by(database.Patient.patient_name.asc())
                ).all()
        elif sort_term == "Search":
            pats = database.session.query(database.Patient).filter(
                database.Patient.patient_name.ilike(f"%{search_term}%")
            ).all()
        prev = prev

        header = pat_header
        header.clear_widgets()

        header.add_widget(MDLabel(text = "Name", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Email", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Phone", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "ID NO", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Gender", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Address", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "D.O.B", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Age", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Date Added", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))


        data = []

        prev_box.default_size = (None, dp(50))

        prev.viewclass = "PatientsRow"
        for pat in pats:
            dob = pat.patient_dob
            added = pat.date_added

            age = added.year - dob.year - ((added.month, added.day) < (dob.month, dob.day))

            data.append({
                'patient_name': pat.patient_name,
                'patient_email': pat.patient_email,
                'patient_phone': pat.patient_phone,
                'patient_id_no': pat.patient_id_number,
                'patient_gender': pat.patient_gender,
                'patient_address': pat.patient_address,
                'patient_dob': dob.strftime("%Y-%m-%d"),
                'patient_age': str(age),
                'patient_date_added': added.strftime("%Y-%m-%d"),
                'show_profile': lambda pat_name = pat.patient_name, pat_email = pat.patient_email, pat_phone = pat.patient_phone, pat_id = pat.patient_id_number, pat_gender = pat.patient_gender, pat_address = pat.patient_address: self.display_patients(pat_name, pat_email, pat_id, pat_phone, pat_gender, pat_address)
            })
        
        prev.data = data

    def show_drugs(self, sort_term, sort_dir, search_term, prev, prev_cont, prev_header):
        if prev == self.root.ids.adm_prev or prev == self.root.ids.lab_prev:
            self.root.ids.adm_dialog_open.on_release = lambda : self.drugs_form()
            self.root.ids.chem_dialog_open.on_release = lambda : self.drugs_form()
        if sort_term == "Any":
            drugs = database.session.query(database.Drug).all()
        elif sort_term == "Time":
            if sort_dir == "desc":
                drugs = (
                    database.session
                    .query(database.Drug)
                    .order_by(database.Drug.date_added.desc())
                ).all()
            elif sort_dir == "asc":
                drugs = (
                    database.session
                    .query(database.Drug)
                    .order_by(database.Drug.date_added.asc())
                ).all()
        elif sort_term == "Name":
            if sort_dir == "desc":
                drugs = (
                    database.session
                    .query(database.Drug)
                    .order_by(database.Drug.drug_name.desc())
                ).all()
            elif sort_dir == "asc":
                drugs = (
                    database.session
                    .query(database.Drug)
                    .order_by(database.Drug.drug_name.asc())
                ).all()
        elif sort_term == "Search":
            drugs = database.session.query(database.Drug).filter(
                database.Drug.drug_name.ilike(f"%{search_term}%")
            ).all()
        prev = prev

        header = prev_header
        header.clear_widgets()

        header.add_widget(MDLabel(text = "Drug", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Category", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Desc", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Qty", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Price", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Expiry", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Safety", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Availability", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(Widget(size_hint_x = None, width = dp(110)))

        data = []

        prev_cont.default_size = (None, dp(50))

        prev.viewclass = "DrugsRow"
        for drug in drugs:
            data.append({
                'drug_name': drug.drug_name,
                'drug_category': drug.drug_category,
                'drug_desc': drug.drug_desc,
                'drug_quantity': str(drug.drug_quantity),
                'drug_price': str(drug.drug_price),
                'drug_expiry': str(drug.drug_expiry),
                'best_before': "Safe" if drug.drug_expiry > datetime.utcnow() else "Expired",
                'status': "Sufficient" if drug.drug_quantity > 10 else "Restock",
                'remove_drug': lambda x = drug.drug_id: self.remove_drug(x),
                'edit_drug': lambda x = drug.drug_id: self.edit_drugs_form(x),
                'show_profile': lambda drug_name = drug.drug_name, drug_cat = drug.drug_category, drug_desc = drug.drug_desc, drug_qty = drug.drug_quantity, drug_price = drug.drug_price, drug_expiry = drug.drug_expiry : self.display_drugs(drug_name, drug_cat, drug_desc, drug_price, drug_qty, drug_expiry)
            })
        
        prev.data = data

    def show_appointments(self, sort_term, sort_dir, search_term, prev, prev_box, app_header):
        if prev == self.root.ids.rec_prev or prev == self.root.ids.adm_prev:
            self.root.ids.rec_dialog_open.on_release = lambda : self.appointment_form()
            self.root.ids.adm_dialog_open.on_release = lambda : self.appointment_form()
        if sort_term == "Any":
            apps = database.session.query(database.Appointment).all()
        elif sort_term == "Time":
            if sort_dir == "desc":
                apps = (
                    database.session
                    .query(database.Appointment)
                    .order_by(database.Appointment.date_requested.desc())
                ).all()
            elif sort_dir == "asc":
                apps = (
                    database.session
                    .query(database.Appointment)
                    .order_by(database.Appointment.date_requested.asc())
                ).all()
        elif sort_term == "Name":
            if sort_dir == "desc":
                apps = (
                    database.session
                    .query(database.Appointment)
                    .join(database.Appointment.patient)
                    .order_by(database.Patient.patient_name.desc())
                ).all()
            elif sort_dir == "asc":
                apps = (
                    database.session
                    .query(database.Appointment)
                    .join(database.Appointment.patient)
                    .order_by(database.Patient.patient_name.asc())
                ).all()
        elif sort_term == "Search":
            apps = (
                database.session
                .query(database.Appointment)
                .join(database.Appointment.patient)
                .filter(database.Patient.patient_name.ilike(f"%{search_term}%"))
            ).all()
        prev = prev

        header = app_header
        header.clear_widgets()

        header.add_widget(MDLabel(text = "Patient", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Consultant", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Service", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Objective", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Set On", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Start At", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Date", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))

        data = []

        prev_box.default_size = (None, dp(50))

        prev.viewclass = "AppointmentsRow"
        for app in apps:
            data.append({
                'patient_name': app.patient.patient_name,
                'consultant_name': app.consultant.worker_name,
                'service_name': app.service.service_name,
                'service_desc': app.appointment_desc,
                'date_scheduled': str(app.date_scheduled),
                'time_scheduled': str(app.time_scheduled),
                'date_added': str(app.date_requested),
                'show_profile': lambda pat_name = app.patient.patient_name, consultant = app.consultant.worker_name, service = app.service.service_name, objective = app.appointment_desc, set_on = app.date_scheduled, start_at = app.time_scheduled: self.display_appointments(pat_name, consultant, service, objective, set_on, start_at)
            })
        
        prev.data = data

    def workers_personal(self):
        self.worker_name = MDTextField(MDTextFieldHintText(text = "Full Name"))
        self.worker_email = MDTextField(MDTextFieldHintText(text = "Email Address"))
        self.worker_phone = MDTextField(MDTextFieldHintText(text = "Contact"), input_filter = "int")
        self.worker_id = MDTextField(MDTextFieldHintText(text = "ID Number"), input_filter = "int")
        self.worker_password = MDTextField(MDTextFieldHintText(text = "Password"))
        gender_box = MDBoxLayout(spacing = dp(10), size_hint_y = None, height = dp(80))
        role_box = MDBoxLayout(spacing = dp(10), size_hint_y = None, height = dp(80))
        role_btn = MDIconButton(icon = "chevron-down", pos_hint = {"center_y":.5}, on_release = lambda x: self.show_dropdown(["Doctor", "Nurse", "Support Staff", "Pharmacist", "LabTech", "Admin", "Receptionist"], role_btn, self.fill_worker_role))
        self.worker_role = MDTextField(MDTextFieldHintText(text = "Role"), pos_hint = {"center_y":.5})
        dob_box = MDBoxLayout(spacing = dp(10), size_hint_y = None, height = dp(80))
        self.worker_gender = MDTextField(MDTextFieldHintText(text = "Gender"), pos_hint = {"center_y":.5})
        gender_btn = MDIconButton(icon = "chevron-down", pos_hint = {"center_y":.5}, on_release = lambda x: self.show_dropdown(["Male", "Female"], gender_btn, self.fill_worker_gender))
        dob_btn = MDIconButton(icon = "calendar", pos_hint = {"center_y":.5}, on_release = lambda x: self.show_date("worker_dob"))
        self.worker_dob = MDTextField(MDTextFieldHintText(text = "D.O.B"), pos_hint = {"center_y":.5})
        gender_box.add_widget(self.worker_gender)
        gender_box.add_widget(gender_btn)
        role_box.add_widget(self.worker_role)
        role_box.add_widget(role_btn)

        dob_box.add_widget(self.worker_dob)
        dob_box.add_widget(dob_btn)

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        content.add_widget(self.worker_name)
        content.add_widget(self.worker_email)
        content.add_widget(self.worker_phone)
        content.add_widget(self.worker_id)
        content.add_widget(self.worker_password)
        content.add_widget(role_box)
        content.add_widget(gender_box)
        content.add_widget(dob_box)

        self.worker_dialog = MDDialog(
            MDDialogIcon(icon = "account-plus"),
            MDDialogHeadlineText(text = "Register Workers"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Register"), on_release = lambda x: self.add_workers()),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.worker_dialog.dismiss()),
                spacing = dp(10),
                padding = dp(10)
            )
        )
        self.worker_dialog.open()

    def add_workers(self, *args):
        name = self.worker_name.text.strip().lower() if self.worker_name.text.strip() else "worker_name"
        email = self.worker_email.text.strip().lower() if self.worker_email.text.strip() else "worker_email"
        phone = self.worker_phone.text.strip() if self.worker_phone.text.strip() else "0123456789"
        id_no = self.worker_id.text.strip().lower() if self.worker_id.text.strip() else "01234567"
        role = self.worker_role.text.strip().lower() if self.worker_role.text.strip() else "worker_role"
        gender = self.worker_gender.text.strip().lower() if self.worker_gender.text.strip() else "worker_gender"
        password = self.worker_password.text.strip() if self.worker_password.text.strip() else ""
        dob = datetime.strptime(self.worker_dob.text.strip(), "%d-%m-%Y").date() if self.worker_dob.text.strip() else datetime.strptime("1-1-2000", "%d-%m-%Y").date()

        new_worker = database.Worker(
            worker_name = name,
            worker_email = email,
            worker_phone = phone,
            worker_id_number = id_no,
            worker_role = role,
            worker_password = password,
            worker_gender = gender,
            worker_dob = dob
        )
        
        database.session.add(new_worker)
        database.session.commit()
        self.show_snack(f"{name} added successfully!!")
        
        self.show_workers("Any", "Any", "Any")
    
    def drugs_form(self):
        self.drug_name = MDTextField(MDTextFieldHintText(text = "Drug Name"))
        self.drug_desc = MDTextField(MDTextFieldHintText(text = "Description"))
        self.drug_category = MDTextField(MDTextFieldHintText(text = "Category"))
        self.drug_price = MDTextField(MDTextFieldHintText(text = "Price"), input_filter = "float")
        self.drug_quantity = MDTextField(MDTextFieldHintText(text = "Quantity"), input_filter = "int")
        expiry_box = MDBoxLayout(spacing = dp(10), size_hint_y = None, height = dp(80))
        expiry_btn = MDIconButton(icon = "calendar", pos_hint = {"center_y":.5}, on_release = lambda x: self.show_date("drug_expiry"))
        self.drug_expiry = MDTextField(MDTextFieldHintText(text = "Expiry Date"), pos_hint = {"center_y":.5})
        expiry_box.add_widget(self.drug_expiry)
        expiry_box.add_widget(expiry_btn)

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        content.add_widget(self.drug_name)
        content.add_widget(self.drug_category)
        content.add_widget(self.drug_desc)
        content.add_widget(self.drug_quantity)
        content.add_widget(self.drug_price)
        content.add_widget(expiry_box)


        self.drug_dialog = MDDialog(
            MDDialogIcon(icon = "pill"),
            MDDialogHeadlineText(text = "Add Drugs"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Add"), on_release = lambda x: self.add_drugs()),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.drug_dialog.dismiss()),
                spacing = dp(10),
                padding = dp(10)
            )
        )
        self.drug_dialog.open()
    
    def prescription_form(self):
        self.pati_name = MDTextField(MDTextFieldHintText(text = "Patient Name"))
        self.prescription = MDTextField(MDTextFieldHintText(text = "Prescription"))
        self.dru_name = MDTextField(MDTextFieldHintText(text = "Drug Name"))
        self.dru_quantity = MDTextField(MDTextFieldHintText(text = "Quantity"), input_filter = "int")

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        content.add_widget(self.pati_name)
        content.add_widget(self.prescription)
        content.add_widget(self.dru_name)
        content.add_widget(self.dru_quantity)
  
        self.prescription_dialog = MDDialog(
            MDDialogIcon(icon = "medical-bag"),
            MDDialogHeadlineText(text = "Add Prescription"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Add"), on_release = lambda x: self.add_prescriptions()),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.prescription_dialog.dismiss()),
                spacing = dp(10),
                padding = dp(10)
            )
        )
        self.prescription_dialog.open()
    
    def diagnosis_form(self):
        self.patie_name = MDTextField(MDTextFieldHintText(text = "Patient Name"))
        self.symptoms = MDTextField(MDTextFieldHintText(text = "Symptoms"))
        self.findings = MDTextField(MDTextFieldHintText(text = "Findings"))
        self.diagnosis = MDTextField(MDTextFieldHintText(text = "Diagnosis"))

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        content.add_widget(self.patie_name)
        content.add_widget(self.symptoms)
        content.add_widget(self.findings)
        content.add_widget(self.diagnosis)
  
        self.diagnosis_dialog = MDDialog(
            MDDialogIcon(icon = "stethoscope"),
            MDDialogHeadlineText(text = "Add Diagnosis"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Add"), on_release = lambda x: self.add_diagnosis()),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.diagnosis_dialog.dismiss()),
                spacing = dp(10),
                padding = dp(10)
            )
        )
        self.diagnosis_dialog.open()
    
    def payment_form(self):
        self.pa_name = MDTextField(MDTextFieldHintText(text = "Patient Name"))
        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        content.add_widget(self.pa_name)
  
        self.payment_dialog = MDDialog(
            MDDialogIcon(icon = "wallet"),
            MDDialogHeadlineText(text = "Start Billing"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Next"), on_release = lambda x: self.billing_form()),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.payment_dialog.dismiss()),
                spacing = dp(10),
                padding = dp(10)
            )
        )
        self.payment_dialog.open()

    def billing_form(self):
        self.payment_dialog.dismiss()
        pat_name = self.pa_name.text.strip()
        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(35))
        tests = (
            database.session
            .query(
                database.LaboratoryRequest
            )
            .join(database.LaboratoryRequest.patient)
            .join(database.LaboratoryRequest.test)
            .filter((database.Patient.patient_name.ilike(f"%{pat_name}%")) & (func.date(database.LaboratoryRequest.date_added) == date.today()))
        ).all()
        pharmas = (
            database.session
            .query(
                database.Prescription
            )
            .join(database.Prescription.patient)
            .join(database.Prescription.items)
            .filter((database.Patient.patient_name.ilike(f"%{pat_name}%")) & (func.date(database.Prescription.prescription_date) == date.today()))
        ).all()
        consultations = (
            database.session
            .query(
                database.Appointment
            )
            .join(database.Appointment.patient)
            .join(database.Appointment.service)
            .filter((database.Patient.patient_name.ilike(f"%{pat_name}%")) & (func.date(database.Appointment.date_requested) == date.today()))
        ).all()
        test_fees = 0
        pharma_fees = 0
        cont_fees = 0
        for test in tests:
            test_fees += test.test.test_price
            content.add_widget(MDLabel(text = f"Lab Test Fees({test.test.test_name})                      {test.test.test_price}"))
        for pharma in pharmas:
            for item in pharma.items:
                pharma_fees += item.drug.drug_price * item.drug_qty
                content.add_widget(MDLabel(text = f"{item.drug.drug_name} x {item.drug_qty}                                           {item.drug.drug_price * item.drug_qty}"))
        for cons in consultations:
            cont_fees += cons.service.service_price
            content.add_widget(MDLabel(text = f"{cons.service.service_name} :                                           {cons.service.service_price}"))
        content.add_widget(MDDivider())
        content.add_widget(MDLabel(text = f"Total :                                                          {test_fees + pharma_fees + cont_fees}"))
  
        self.billing_dialog = MDDialog(
            MDDialogIcon(icon = "wallet"),
            MDDialogHeadlineText(text = f"Invoice for {pat_name.split(" ")[1].capitalize()}"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Print")),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.billing_dialog.dismiss()),
                spacing = dp(10),
                padding = dp(10)
            )
        )
        self.billing_dialog.open()
    
    def services_form(self):
        self.serv_name = MDTextField(MDTextFieldHintText(text = "Service Name"))
        self.serv_price = MDTextField(MDTextFieldHintText(text = "Price"), input_filter = "float")
        self.serv_desc = MDTextField(MDTextFieldHintText(text = "Description"))

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        content.add_widget(self.serv_name)
        content.add_widget(self.serv_price)
        content.add_widget(self.serv_desc)
  
        self.services_dialog = MDDialog(
            MDDialogIcon(icon = "account-cog"),
            MDDialogHeadlineText(text = "Add Services"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Add"), on_release = lambda x: self.add_services()),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.services_dialog.dismiss()),
                spacing = dp(10),
                padding = dp(10)
            )
        )
        self.services_dialog.open()
    
    def tests_form(self):
        self.test_name = MDTextField(MDTextFieldHintText(text = "Test Name"))
        self.test_price = MDTextField(MDTextFieldHintText(text = "Price"), input_filter = "float")
        self.test_desc = MDTextField(MDTextFieldHintText(text = "Description"))

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        content.add_widget(self.test_name)
        content.add_widget(self.test_desc)
        content.add_widget(self.test_price)
        
        self.tests_dialog = MDDialog(
            MDDialogIcon(icon = "magnify"),
            MDDialogHeadlineText(text = "Add Tests"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Add"), on_release = lambda x: self.add_tests()),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.tests_dialog.dismiss()),
                spacing = dp(10),
                padding = dp(10)
            )
        )
        self.tests_dialog.open()

    def laboratory_form(self):
        self.patien_name = MDTextField(MDTextFieldHintText(text = "Patient Name"))
        self.observations = MDTextField(MDTextFieldHintText(text = "Observations"))
        self.conclusions = MDTextField(MDTextFieldHintText(text = "Conclusion"))

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        content.add_widget(self.patien_name)
        content.add_widget(self.observations)
        content.add_widget(self.conclusions)
  
        self.lab_dialog = MDDialog(
            MDDialogIcon(icon = "test-tube"),
            MDDialogHeadlineText(text = "Add Lab Result"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Add"), on_release = lambda x: self.add_lab_result()),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.lab_dialog.dismiss()),
                spacing = dp(10),
                padding = dp(10)
            )
        )
        self.lab_dialog.open()
    
    def request_form(self):
        self.pa_name = MDTextField(MDTextFieldHintText(text = "Patient Name"))
        name_box = MDBoxLayout(spacing = dp(10), size_hint_y = None, height = dp(80))
        self.tes_name = MDTextField(MDTextFieldHintText(text = "Test Name"), pos_hint = {"center_y":.5})
        tests = database.session.query(database.LaboratoryTest).all()
        service_btn = MDIconButton(icon = "chevron-down", pos_hint = {"center_y":.5}, on_release = lambda x: self.show_dropdown([test.test_name for test in tests], service_btn, self.fill_tests))
        name_box.add_widget(self.tes_name)
        name_box.add_widget(service_btn)

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        content.add_widget(self.pa_name)
        content.add_widget(name_box)
  
        self.req_dialog = MDDialog(
            MDDialogIcon(icon = "account-magnify"),
            MDDialogHeadlineText(text = "Add Lab Request"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Add"), on_release = lambda x: self.add_lab_request()),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.req_dialog.dismiss()),
                spacing = dp(10),
                padding = dp(10)
            )
        )
        self.req_dialog.open()


    def add_drugs(self, *args):
        name = self.drug_name.text.strip().lower() if self.drug_name.text.strip() else "drug_name"
        cat = self.drug_category.text.strip().lower() if self.drug_category.text.strip() else "drug_categroy"
        desc = self.drug_desc.text.strip() if self.drug_desc.text.strip() else "drug_desc"
        qty = int(self.drug_quantity.text.strip()) if self.drug_quantity.text.strip() else 0
        price = float(self.drug_price.text.strip()) if self.drug_price.text.strip() else 0
        expiry = datetime.strptime(self.drug_expiry.text.strip(), "%d-%m-%Y").date() if self.drug_expiry.text.strip() else datetime.strptime("1-1-2000", "%d-%m-%Y").date()


        new_drug = database.Drug(
            drug_name = name,
            drug_category = cat,
            drug_desc = desc,
            drug_quantity = qty,
            drug_price = price,
            drug_expiry = expiry,
        )
        try:
            database.session.add(new_drug)
            database.session.commit()
            self.show_snack(f"{name} added successfully!!")
        except IntegrityError as e:
            self.show_snack(f"Error: {e}!!")
            database.session.rollback()
            database.session.close()
            database.session = database.Session()
        self.show_drugs("Any", "Any", "Any", self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)
    
    def add_prescriptions(self, *args):
        pat_name = self.pati_name.text.strip().lower() if self.pati_name.text.strip() else "patient_name"
        prescription_note = self.prescription.text.strip().lower() if self.prescription.text.strip() else "prescription_note"
        drug_name = self.dru_name.text.strip().lower() if self.dru_name.text.strip() else "drug_name"
        qty = int(self.dru_quantity.text.strip()) if self.dru_quantity.text.strip() else 0

        pat = database.session.query(database.Patient).filter_by(patient_name=pat_name).first()
        drug = database.session.query(database.Drug).filter_by(drug_name=drug_name).first()

        if not pat or not drug:
            self.show_snack("Invalid patient or drug name!")
            return
        if drug.drug_expiry < datetime.utcnow():
            self.show_snack(f"{drug.drug_name} is expired and unsafe!!")
            return
        if drug.drug_quantity < qty:
            self.show_snack(f"Insufficient {drug.drug_name} available is {drug.drug_quantity}!!")
            return
        
        new_prescription = database.Prescription(
            patient_id=pat.patient_id,
            prescriber_id=self.signed_in_user.worker_id
        )

        item = database.PrescriptionItem(
            drug_id=drug.drug_id,
            drug_qty=qty,
            notes=prescription_note
        )

        drug_fees = database.Billing(
            patient_id = pat.patient_id,
            items = drug.drug_name,
            total = drug.drug_price * qty
        )

        new_prescription.items.append(item)
        drug.drug_quantity -= qty
        try:
            database.session.add(new_prescription)
            database.session.add(drug_fees)
            database.session.commit()
            self.show_snack("Prescription added successfully!!")
        except IntegrityError as e:
            database.session.rollback()
            database.session.close()
            database.session = database.Session()
            self.show_snack(f"Error: {e}!!")

        self.show_prescriptions("Any", "Any", "Any", self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header)


    def add_diagnosis(self, *args):
        pat_name = self.patie_name.text.strip().lower() if self.patie_name.text.strip() else "patient_name"
        symptoms = self.symptoms.text.strip().lower() if self.symptoms.text.strip() else "symptoms"
        findings = self.findings.text.strip().lower() if self.findings.text.strip() else "findings"
        diagnosis = self.diagnosis.text.strip().lower() if self.diagnosis.text.strip() else "diagnosis"

        pat = database.session.query(database.Patient).filter_by(patient_name = pat_name).first()
  
        new_diagnosis = database.Diagnosis(
            patient_id = pat.patient_id,
            symptoms = symptoms,
            findings = findings,
            suggested_diagnosis = diagnosis,
            diagnoser_id = self.signed_in_user.worker_id
        )
        try:
            database.session.add(new_diagnosis)
            database.session.commit()
            self.show_snack(f"Diagnosis added successfully!!")
        except IntegrityError as e:
            self.show_snack(f"Error: {e}!!")
            database.session.rollback()
            database.session.close()
            database.session = database.Session()
        self.show_diagnosis("Any", "Any", "Any", self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header)
    
    def add_services(self, *args):
        service_name = self.serv_name.text.strip().lower() if self.serv_name.text.strip() else "service_name"
        service_price = self.serv_price.text.strip() if self.serv_price.text.strip() else 0
        service_desc = self.serv_desc.text.strip().lower() if self.service_desc.text.strip() else "service_desc"
  
        new_service = database.Service(
            service_name = service_name,
            service_price = float(service_price),
            service_desc = service_desc,
        )
        try:
            database.session.add(new_service)
            database.session.commit()
            self.show_snack(f"Service added successfully!!")
        except IntegrityError as e:
            self.show_snack(f"Error: {e}!!")
            database.session.rollback()
            database.session.close()
            database.session = database.Session()
        self.show_services(self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)
    
    def add_tests(self, *args):
        test_name = self.test_name.text.strip().lower() if self.test_name.text.strip() else "test_name"
        test_price = self.test_price.text.strip() if self.test_price.text.strip() else 0
        test_desc = self.test_desc.text.strip().lower() if self.test_desc.text.strip() else "test_desc"
  
        new_test = database.LaboratoryTest(
            test_name = test_name,
            test_price = float(test_price),
            test_desc = test_desc,
        )
        try:
            database.session.add(new_test)
            database.session.commit()
            self.show_snack(f"Test added successfully!!")
        except IntegrityError as e:
            self.show_snack(f"Error: {e}!!")
            database.session.rollback()
            database.session.close()
            database.session = database.Session()
        self.show_tests(self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)

    def add_lab_result(self, *args):
        pat_name = self.patien_name.text.strip().lower() if self.patien_name.text.strip() else "patient_name"
        observation = self.observations.text.strip().lower() if self.observations.text.strip() else "observations"
        conclusion = self.conclusions.text.strip().lower() if self.conclusion.text.strip() else "conclusions"
  
        pat = database.session.query(database.Patient).filter_by(patient_name = pat_name).first()
  
        new_lab_result = database.LaboratoryResult(
            patient_id = pat.patient_id,
            observations = observation,
            conclusion = conclusion,
            tech_id = self.signed_in_user.worker_id
        )
        try:
            database.session.add(new_lab_result)
            database.session.commit()
            self.show_snack(f"Lab result added successfully!!")
        except IntegrityError as e:
            self.show_snack(f"Error: {e}!!")
            database.session.rollback()
            database.session.close()
            database.session = database.Session()
        self.show_lab_results("Any", "Any", "Any", self.root.ids.lab_prev, self.root.ids.labrvb, self.root.ids.lab_cont_header)

    def add_lab_request(self, *args):
        pat_name = self.pa_name.text.strip().lower() 
        test_name = self.tes_name.text.strip().lower()

        if not pat_name or test_name:
            self.show_snack("Please enter patient of test name(s)")
  
        pat = database.session.query(database.Patient).filter_by(patient_name = pat_name).first()
        test = database.session.query(database.LaboratoryTest).filter_by(test_name = test_name).first()
  
        new_lab_request = database.LaboratoryRequest(
            patient_id = pat.patient_id,
            test_id = test.test_id,
            doctor_id = self.signed_in_user.worker_id
        )
        lab_fees = database.Billing(
            patient_id = pat.patient_id,
            items = test.test_name,
            total = test.test_price
        )
        try:
            database.session.add(new_lab_request)
            database.session.add(lab_fees)
            database.session.commit()
            self.show_snack(f"Lab request added successfully!!")
        except IntegrityError as e:
            self.show_snack(f"Error: {e}!!")
            database.session.rollback()
            database.session.close()
            database.session = database.Session()
        self.show_lab_requests("Any", "Any", "Any", self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header)


    def show_workers(self, sort_term, sort_dir, search_term):
        self.root.ids.adm_dialog_open.on_release = lambda : self.workers_personal()
        if sort_term == "Any":
            wrks = database.session.query(database.Worker).all()
        elif sort_term == "Time":
            if sort_dir == "desc":
                wrks = (
                    database.session
                    .query(database.Worker)
                    .order_by(database.Worker.date_added.desc())
                ).all()
            elif sort_dir == "asc":
                wrks = (
                    database.session
                    .query(database.Worker)
                    .order_by(database.Worker.date_added.asc())
                ).all()
        elif sort_term == "Name":
            if sort_dir == "desc":
                wrks = (
                    database.session
                    .query(database.Worker)
                    .order_by(database.Worker.worker_name.desc())
                ).all()
            elif sort_dir == "asc":
                wrks = (
                    database.session
                    .query(database.Worker)
                    .order_by(database.Worker.worker_name.asc())
                ).all()
        elif sort_term == "Search":
            wrks = database.session.query(database.Worker).filter(
                database.Worker.worker_name.ilike(f"%{search_term}%")
            ).all()
        prev = self.root.ids.adm_prev

        header = self.root.ids.adm_cont_header
        header.clear_widgets()

        header.add_widget(MDLabel(text = "Name", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Email", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Phone", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "ID NO", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Gender", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Role", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "D.O.B", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Age", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Date Added", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(Widget(size_hint_x = None, width = dp(48)))


        data = []

        self.root.ids.adrvb.default_size = (None, dp(50))

        prev.viewclass = "WorkersRow"
        for wrk in wrks:
            dob = wrk.worker_dob
            added = wrk.date_added

            age = added.year - dob.year - ((added.month, added.day) < (dob.month, dob.day))

            data.append({
                'worker_name': wrk.worker_name,
                'worker_email': wrk.worker_email,
                'worker_phone': wrk.worker_phone,
                'worker_id_no': wrk.worker_id_number,
                'worker_gender': wrk.worker_gender,
                'worker_role': wrk.worker_role,
                'worker_dob': dob.strftime("%Y-%m-%d"),
                'worker_age': str(age),
                'worker_date_added': added.strftime("%Y-%m-%d"),
                'remove_worker': lambda x = wrk.worker_id: self.remove_worker(x),
                'show_profile': lambda wrk_name = wrk.worker_name, wrk_email = wrk.worker_email, wrk_phone = wrk.worker_phone, wrk_id = wrk.worker_id_number, wrk_gender = wrk.worker_gender, wrk_role = wrk.worker_role: self.display_workers(wrk_name, wrk_email, wrk_id, wrk_phone, wrk_gender, wrk_role)
            })
        
        prev.data = data
    
    def show_prescriptions(self, sort_term, sort_dir, search_term, prev, prev_cont, prev_header):
        if prev == self.root.ids.diag_prev or prev == self.root.ids.adm_prev:
            self.root.ids.diag_dialog_open.on_release = lambda : self.prescription_form()
            self.root.ids.adm_dialog_open.on_release = lambda : self.prescription_form()
        if sort_term == "Any":
            prescs = database.session.query(database.Prescription).all()
        elif sort_term == "Time":
            if sort_dir == "desc":
                prescs = (
                    database.session
                    .query(database.Prescription)
                    .order_by(database.Prescription.prescription_date.desc())
                ).all()
            elif sort_dir == "asc":
                prescs = (
                    database.session
                    .query(database.Prescription)
                    .order_by(database.Prescription.prescription_date.asc())
                ).all()
        elif sort_term == "Name":
            if sort_dir == "desc":
                prescs = (
                    database.session
                    .query(database.Prescription)
                    .join(database.Prescription.patient)
                    .order_by(database.Patient.patient_name.desc())
                ).all()
            elif sort_dir == "asc":
                prescs = (
                    database.session
                    .query(database.Prescription)
                    .join(database.Prescription.patient)
                    .order_by(database.Patient.patient_name.asc())
                ).all()
        elif sort_term == "Search":
            prescs = (
                database.session
                .query(database.Prescription)
                .join(database.Prescription.patient)
                .filter(database.Patient.patient_name.ilike(f"%{search_term}%"))
            ).all()
        prev = prev

        header = prev_header
        header.clear_widgets()

        header.add_widget(MDLabel(text = "Patient", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Prescription", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Drugs", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Qty", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Prescriber", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Date Prescribed", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
    
        data = []

        prev_cont.default_size = (None, dp(50))

        prev.viewclass = "PrescriptionsRow"
        grouped = defaultdict(list)

        for presc in prescs:
            grouped[presc.patient.patient_name].append(presc)

        data = []

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

            data.append({
                'patient_name': patient_name,
                'prescription': all_notes,
                'drug_name': all_drugs,
                'drug_quantity': all_qtys,
                'pharmacist': prescriber_display,
                'date_added': date_display,
                'show_profile': partial(
                    self.display_prescriptions,
                    patient_name,
                    all_notes,
                    all_drugs,
                    all_qtys,
                    prescriber_display
                )
            })
                
        prev.data = data

    def show_diagnosis(self, sort_term, sort_dir, search_term, prev, prev_cont, prev_header):
        if prev == self.root.ids.diag_prev or prev == self.root.ids.adm_prev:
            self.root.ids.diag_dialog_open.on_release = lambda : self.diagnosis_form()
            self.root.ids.adm_dialog_open.on_release = lambda : self.diagnosis_form()
        if sort_term == "Any":
            diags = database.session.query(database.Diagnosis).all()
        elif sort_term == "Time":
            if sort_dir == "desc":
                diags = (
                    database.session
                    .query(database.Diagnosis)
                    .order_by(database.Diagnosis.date_diagnosed.desc())
                ).all()
            elif sort_dir == "asc":
                diags = (
                    database.session
                    .query(database.Diagnosis)
                    .order_by(database.Diagnosis.date_diagnosed.asc())
                ).all()
        elif sort_term == "Name":
            if sort_dir == "desc":
                diags = (
                    database.session
                    .query(database.Diagnosis)
                    .join(database.Diagnosis.patient)
                    .order_by(database.Patient.patient_name.desc())
                ).all()
            elif sort_dir == "asc":
                diags = (
                    database.session
                    .query(database.Diagnosis)
                    .join(database.Diagnosis.patient)
                    .order_by(database.Patient.patient_name.asc())
                ).all()
        elif sort_term == "Search":
            diags = (
                database.session
                .query(database.Diagnosis)
                .join(database.Diagnosis.patient)
                .filter(database.Patient.patient_name.ilike(f"%{search_term}%"))
            ).all()
        prev = prev

        header = prev_header
        header.clear_widgets()

        header.add_widget(MDLabel(text = "Patient", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Symptoms", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Findings", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Diagnosis", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Diagnosed By", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Date Diagnosed", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
    
        data = []

        prev_cont.default_size = (None, dp(50))

        prev.viewclass = "DiagnosisRow"
        for diag in diags:

            data.append({
                'patient_name': diag.patient.patient_name,
                'symptoms': diag.symptoms,
                'findings': diag.findings,
                'suggested_diagnosis': diag.suggested_diagnosis,
                'diagnoser': diag.diagnoser.worker_name,
                'date_added': str(diag.date_diagnosed).split(" ")[0],
                'show_profile': lambda pat_name = diag.patient.patient_name, symptoms = diag.symptoms, findings = diag.findings, diagnosis = diag.suggested_diagnosis, diagnoser = diag.diagnoser.worker_name: self.display_diagnoses(pat_name, symptoms, findings, diagnosis, diagnoser)
            })
        
        prev.data = data
    
    def show_billings(self, sort_term, sort_dir, search_term, prev, prev_cont, prev_header):
        if sort_term == "Any":
            bills = database.session.query(database.Billing).all()
        elif sort_term == "Time":
            if sort_dir == "desc":
                bills = (
                    database.session
                    .query(database.Billing)
                    .order_by(database.Billing.date.desc())
                ).all()
            elif sort_dir == "asc":
                bills = (
                    database.session
                    .query(database.Billing)
                    .order_by(database.Billing.date.asc())
                ).all()
        elif sort_term == "Name":
            if sort_dir == "desc":
                bills = (
                    database.session
                    .query(database.Billing)
                    .join(database.Billing.patient)
                    .order_by(database.Patient.patient_name.desc())
                ).all()
            elif sort_dir == "asc":
                bills = (
                    database.session
                    .query(database.Billing)
                    .join(database.Billing.patient)
                    .order_by(database.Patient.patient_name.asc())
                ).all()
        elif sort_term == "Search":
            bills = (
                database.session
                .query(database.Billing)
                .join(database.Billing.patient)
                .filter(database.Patient.patient_name.ilike(f"%{search_term}%"))
            ).all()
        prev = prev

        header = prev_header
        header.clear_widgets()

        header.add_widget(MDLabel(text = "Patient", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Items", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Total", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
    
        data = []

        prev_cont.default_size = (None, dp(50))

        prev.viewclass = "BillingsRow"
        for bill in bills:

            data.append({
                'patient_name': bill.patient.patient_name,
                'items': bill.items,
                'total': str(bill.total),
            })
        
        prev.data = data
    
    def show_services(self, prev, prev_cont, prev_header):
        if prev == self.root.ids.adm_prev:
            self.root.ids.adm_dialog_open.on_release = lambda : self.services_form()
        servs = database.session.query(database.Service).all()

        header = prev_header
        header.clear_widgets()

        header.add_widget(MDLabel(text = "Service Name", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Description", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Price", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
    
        data = []

        prev_cont.default_size = (None, dp(50))

        prev.viewclass = "ServicesRow"
        for serv in servs:

            data.append({
                'service_name': serv.service_name,
                'service_price': str(serv.service_price),
                'service_desc': serv.service_desc,
            })
        
        prev.data = data
    
    
    def show_tests(self, prev, prev_cont, prev_header):
        if prev == self.root.ids.adm_prev:
            self.root.ids.adm_dialog_open.on_release = lambda : self.tests_form()
        tests = database.session.query(database.LaboratoryTest).all()

        header = prev_header
        header.clear_widgets()

        header.add_widget(MDLabel(text = "Test Name", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Description", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Price", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
    
        data = []

        prev_cont.default_size = (None, dp(50))

        prev.viewclass = "LabTestsRow"
        for test in tests:

            data.append({
                'test_name': test.test_name,
                'test_price': str(test.test_price),
                'test_desc': test.test_desc,
            })
        
        prev.data = data

    def show_lab_results(self, sort_term, sort_dir, search_term, prev, prev_cont, prev_header):
        if prev == self.root.ids.lab_prev or prev == self.root.ids.adm_prev:
            self.root.ids.lab_dialog_open.on_release = lambda : self.laboratory_form()
            self.root.ids.adm_dialog_open.on_release = lambda : self.laboratory_form()
        if sort_term == "Any":
            resuls = database.session.query(database.LaboratoryResult).all()
        elif sort_term == "Time":
            if sort_dir == "desc":
                resuls = (
                    database.session
                    .query(database.LaboratoryResult)
                    .order_by(database.LaboratoryResult.date_requested.desc())
                ).all()
            elif sort_dir == "asc":
                resuls = (
                    database.session
                    .query(database.LaboratoryResult)
                    .order_by(database.LaboratoryResult.date_requested.asc())
                ).all()
        elif sort_term == "Name":
            if sort_dir == "desc":
                resuls = (
                    database.session
                    .query(database.LaboratoryResult)
                    .join(database.LaboratoryResult.patient)
                    .order_by(database.Patient.patient_name.desc())
                ).all()
            elif sort_dir == "asc":
                resuls = (
                    database.session
                    .query(database.LaboratoryResult)
                    .join(database.LaboratoryResult.patient)
                    .order_by(database.Patient.patient_name.asc())
                ).all()
        elif sort_term == "Search":
           resuls = (
               database.session
               .query(database.LaboratoryResult)
               .join(database.LaboratoryResult.patient)
               .filter(database.Patient.patient_name.ilike(f"%{search_term}%"))
            ).all()
        prev = prev

        header = prev_header
        header.clear_widgets()

        header.add_widget(MDLabel(text = "Patient", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Observations", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Conclusions", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Lab Tech", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Date Tested", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
    
        data = []

        prev_cont.default_size = (None, dp(50))

        prev.viewclass = "LabResultsRow"
        for resul in resuls:

            data.append({
                'patient_name': resul.patient.patient_name,
                'observations': resul.observations,
                'conclusions': resul.conclusion,
                'labtech': resul.tech.worker_name,
                'date_added': str(resul.date_requested).split(" ")[0],
                'show_profile': lambda pat_name = resul.patient.patient_name, obs = resul.observations, conc = resul.conclusion, labtech = resul.tech.worker_name: self.display_resuls(pat_name, obs, conc, labtech)
            })
        
        prev.data = data
    
    def show_lab_requests(self, sort_term, sort_dir, search_term, prev, prev_cont, prev_header):
        if prev == self.root.ids.diag_prev or prev == self.root.ids.adm_prev:
            self.root.ids.diag_dialog_open.on_release = lambda : self.request_form()
            self.root.ids.adm_dialog_open.on_release = lambda : self.request_form()
        if sort_term == "Any":
            requests = database.session.query(database.LaboratoryRequest).all()
        elif sort_term == "Time":
            if sort_dir == "desc":
                requests = (
                    database.session
                    .query(database.LaboratoryRequest)
                    .order_by(database.LaboratoryRequest.date_added.desc())
                ).all()
            elif sort_dir == "asc":
                requests = (
                    database.session
                    .query(database.LaboratoryRequest)
                    .order_by(database.LaboratoryRequest.date_added.asc())
                ).all()
        elif sort_term == "Name":
            if sort_dir == "desc":
                requests = (
                    database.session
                    .query(database.LaboratoryRequest)
                    .join(database.LaboratoryRequest.patient)
                    .order_by(database.Patient.patient_name.desc())
                ).all()
            elif sort_dir == "asc":
                requests = (
                    database.session
                    .query(database.LaboratoryRequest)
                    .join(database.LaboratoryRequest.patient)
                    .order_by(database.Patient.patient_name.asc())
                ).all()
        elif sort_term == "Search":
           requests = (
               database.session
               .query(database.LaboratoryRequest)
               .join(database.LaboratoryRequest.patient)
               .filter(database.Patient.patient_name.ilike(f"%{search_term}%"))
            ).all()
        prev = prev

        header = prev_header
        header.clear_widgets()

        header.add_widget(MDLabel(text = "Patient", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Doctor", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Test", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
        header.add_widget(MDLabel(text = "Date Requested", halign = "center", theme_text_color = "Custom", text_color = "navy", bold = True, theme_font_size = "Custom", font_size = sp(17)))
    
        data = []

        prev_cont.default_size = (None, dp(50))

        prev.viewclass = "LabRequestsRow"
        for request in requests:

            data.append({
                'patient_name': request.patient.patient_name,
                'test_name': request.test.test_name,
                'doctor_name': request.doctor.worker_name,
                'date_added': str(request.date_added).split(" ")[0]
            })
        
        prev.data = data

    def show_snack(self, text):
        MDSnackbar(
            MDSnackbarText(text=text), 
            pos_hint={'center_x': 0.5}, 
            size_hint_x=0.5, 
            orientation='horizontal'
        ).open()
    
    def show_date(self, target_field):
        self.day = 0
        self.month = 0
        self.year = 0
        self.target_field = target_field
        self.date_dialog = MDDockedDatePicker()
        self.date_dialog.pos_hint = {"center_x":.5, "center_y":.5}
        self.date_dialog.open()
        self.date_dialog.bind(
            on_select_day=self.on_select_day, 
            on_select_month = self.on_select_month, 
            on_select_year = self.on_select_year,
            on_ok = self.create_date,
            on_cancel = self.close_date_dialog
        )

    def on_select_day(self, instance, value):
        self.day =  value if value else 0
    def on_select_month(self, instance, value):
        self.month =  value if value else 0
    def on_select_year(self, instance, value):
        self.year =  value if value else 0
    def create_date(self, *args):
        date = f"{self.day}-{self.month}-{self.year}"
        if hasattr(self, 'target_field'):
            target = getattr(self, self.target_field, None)
            if target:
                target.text = date
    
    def remove_worker(self, worker_id):
        worker = database.session.query(database.Worker).filter_by(worker_id = worker_id).first()
        if worker:
            has_links = (
                worker.diagnoses or
                worker.lab_requests or
                worker.lab_results or
                worker.appointments or
                worker.prescriptions
            )
            if has_links:
                self.show_snack(f"{worker.worker_name} can't be deleted since they are in use by other records!")
                return
            try:
                database.session.delete(worker)
                database.session.commit()
                self.show_workers("Any", "Any", "Any")
            except IntegrityError as e:
                self.show_snack(f"Error: {e}")
                database.session.rollback()
                database.session.close()
                database.session = database.Session()
        else:
            self.show_snack("Worker not found!!")
    
    def remove_drug(self, drug_id):
        drug = database.session.query(database.Drug).filter_by(drug_id = drug_id).first()
        if self.root.current == "admin_screen":
            prev, prev_cont, prev_header = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
        elif self.root.current == "chemist_screen":
            prev, prev_cont, prev_header = self.root.ids.chem_prev, self.root.ids.chemrvb, self.root.ids.chem_cont_header
        else:
            return
        if drug:
            if drug.prescriptions:
                self.show_snack(f"{drug.drug_name} can't be deleted since it's in use by other records.")
                return
            try:
                database.session.delete(drug)
                database.session.commit()
                self.show_drugs("Any", "Any", "Any", prev, prev_cont, prev_header)
            except IntegrityError as e:
                self.show_snack(f"Error: {e}")
                database.session.rollback()
                database.session.close()
                database.session = database.Session()
        else:
            self.show_snack("Drug not found!!")
        
    
    def close_date_dialog(self, *args):
        self.date_dialog.dismiss()
    
    def time_dialog(self):
        self.hour = 0
        self.minute = 0
        self.am_pm = ""
        self.time_form = MDTimePickerDialHorizontal()
        self.time_form.open()
        self.time_form.bind(
            on_selector_hour = self.show_hour,
            on_selector_minute = self.show_minute,
            on_am_pm = self.show_am_pm,
            on_cancel = self.close_time_dialog,
            on_ok = self.create_time
        )
    
    def show_hour(self, instance, value):
        self.hour = value
    def show_minute(self, instance, value):
        self.minute = value
    def show_am_pm(self, instance, value):
        self.am_pm = value
    
    def create_time(self, *args):
        time = f"{self.hour}:{self.minute} {self.am_pm.upper()}"
        self.schedule_time.text = time
    
    def close_time_dialog(self, *args):
        self.time_form.dismiss()

    def show_dropdown(self, vals, caller, func):
        self.drop_down_items = [
            {
                "text": val,
                "theme_text_color": "Custom",
                "text_color": [0, .75, 0, 1],
                "bold": True,
                "on_release": lambda x = val: func(x)
            }
            for val in vals
        ]
        MDDropdownMenu(
            caller = caller,
            items = self.drop_down_items
        ).open()
    def fill_pat_gender(self, val):
        self.patient_gender.text = val
    def fill_services(self, val):
        self.service_name.text = val
    def fill_tests(self, val):
        self.tes_name.text = val
    def fill_worker_gender(self, val):
        self.worker_gender.text = val
    def fill_worker_role(self, val):
        self.worker_role.text = val
    
    def set_sort_btn(self, btn_id, sort_func):
        btn_id.on_release = lambda: self.show_dropdown(
            vals=["Newest First", "Oldest First", "A to Z", "Z to A"],
            caller=btn_id,
            func=sort_func
        )

    def rec_nav(self, val):
        self.root.ids.rec_dest_label.text = val
        self.root.ids.rec_search_field_hint.text = f"Search {val}"
        if val == "Patients":
            self.root.ids.rec_search_btn.on_release = lambda: self.search_pats()
            self.set_sort_btn(self.root.ids.rec_sort_btn, self.sort_pats_by)
            self.show_patients("Any", "Any", "Any", self.root.ids.rec_prev, self.root.ids.rvb, self.root.ids.rec_cont_header)
        elif val == "Appointments":
            self.root.ids.rec_search_btn.on_release = lambda: self.search_appts()
            self.set_sort_btn(self.root.ids.rec_sort_btn, self.sort_appts_by)
            self.show_appointments("Any", "Any", "Any", self.root.ids.rec_prev, self.root.ids.rvb, self.root.ids.rec_cont_header)
        elif val == "Billings":
            self.payment_form()

    def adm_nav(self, val):
        self.root.ids.adm_dest_label.text = val
        self.root.ids.adm_search_field_hint.text = f"Search {val}"
        if val == "Patients":
            self.root.ids.adm_search_btn.on_release = lambda: self.search_pats()
            self.root.ids.adm_export_btn.on_release = lambda: self.export_file_dialog(name=val, func = self.export_pat_data)
            self.set_sort_btn(self.root.ids.adm_sort_btn, self.sort_pats_by)
            self.show_patients("Any", "Any", "Any", self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)

        elif val == "Appointments":
            self.root.ids.adm_search_btn.on_release = lambda: self.search_appts()
            self.root.ids.adm_export_btn.on_release = lambda: self.export_file_dialog(name=val, func = self.export_app_data)
            self.set_sort_btn(self.root.ids.adm_sort_btn, self.sort_appts_by)
            self.show_appointments("Any", "Any", "Any", self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)

        elif val == "Workers":
            self.root.ids.adm_search_btn.on_release = lambda: self.search_wrks()
            self.root.ids.adm_export_btn.on_release = lambda: self.export_file_dialog(name=val, func = self.export_wrk_data)
            self.set_sort_btn(self.root.ids.adm_sort_btn, self.sort_wrks_by)
            self.show_workers("Any", "Any", "Any")

        elif val == "Pharmacy":
            self.root.ids.adm_search_btn.on_release = lambda: self.search_drugs()
            self.root.ids.adm_export_btn.on_release = lambda: self.export_file_dialog(name=val, func = self.export_drug_data)
            self.set_sort_btn(self.root.ids.adm_sort_btn, self.sort_drugs_by)
            self.show_drugs("Any", "Any", "Any", self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)

        elif val == "Diagnoses":
            self.root.ids.adm_search_btn.on_release = lambda: self.search_diags()
            self.root.ids.adm_export_btn.on_release = lambda: self.export_file_dialog(name=val, func = self.export_diag_data)
            self.set_sort_btn(self.root.ids.adm_sort_btn, self.sort_diags_by)
            self.show_diagnosis("Any", "Any", "Any", self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)
        
        elif val == "Prescriptions":
            self.root.ids.adm_search_btn.on_release = lambda: self.search_prescs()
            self.set_sort_btn(self.root.ids.adm_sort_btn, self.sort_prescs_by)
            self.root.ids.adm_export_btn.on_release = lambda: self.export_file_dialog(name=val, func = self.export_presc_data)
            self.show_prescriptions("Any", "Any", "Any", self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)
        
        elif val == "Lab Results":
            self.root.ids.adm_search_btn.on_release = lambda: self.search_resuls()
            self.root.ids.adm_export_btn.on_release = lambda: self.export_file_dialog(name=val, func = self.export_lab_result_data)
            self.set_sort_btn(self.root.ids.adm_sort_btn, self.sort_resuls_by)
            self.show_lab_results("Any", "Any", "Any", self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)
        
        elif val == "Lab Requests":
            self.root.ids.adm_search_btn.on_release = lambda: self.search_requests()
            self.root.ids.adm_export_btn.on_release = lambda: self.export_file_dialog(name=val, func = self.export_lab_requests_data)
            self.set_sort_btn(self.root.ids.adm_sort_btn, self.sort_requests_by)
            self.show_lab_requests("Any", "Any", "Any", self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)

        elif val == "Services":
            self.show_services(self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)
            self.root.ids.adm_export_btn.on_release = lambda: self.export_file_dialog(name=val, func = self.export_services_data)
        
        elif val == "Lab Tests":
            self.show_tests(self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)
            self.root.ids.adm_export_btn.on_release = lambda: self.export_file_dialog(name=val, func = self.export_lab_test_data)

        elif val == "Billings":
            self.root.ids.adm_search_btn.on_release = lambda: self.search_billings()
            self.set_sort_btn(self.root.ids.adm_sort_btn, self.sort_billings_by)
            self.root.ids.adm_export_btn.on_release = lambda: self.export_file_dialog(name=val, func = self.export_billings_data)
            self.show_billings("Any", "Any", "Any", self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)
        elif val == "Payments":
            self.payment_form()
    
    def chem_nav(self, val):
        self.root.ids.chem_dest_label.text = val
        self.root.ids.chem_search_field_hint.text = f"Search {val}"
        if val == "Drugs":
            self.root.ids.chem_search_btn.on_release = lambda: self.search_drugs()
            self.show_drugs("Any", "Any", "Any", self.root.ids.chem_prev, self.root.ids.chemrvb, self.root.ids.chem_cont_header)
            self.set_sort_btn(self.root.ids.chem_sort_btn, self.sort_drugs_by)
        elif val == "Prescriptions":
            self.root.ids.chem_search_btn.on_release = lambda: self.search_prescs()
            self.set_sort_btn(self.root.ids.chem_sort_btn, self.sort_prescs_by)
            self.show_prescriptions("Any", "Any", "Any", self.root.ids.chem_prev, self.root.ids.chemrvb, self.root.ids.chem_cont_header)
        elif val == "Diagnoses":
            self.root.ids.chem_search_btn.on_release = lambda: self.search_diags()
            self.set_sort_btn(self.root.ids.chem_sort_btn, self.sort_diags_by)
            self.show_diagnosis("Any", "Any", "Any", self.root.ids.chem_prev, self.root.ids.chemrvb, self.root.ids.chem_cont_header)

    def diag_nav(self, val):
        self.root.ids.diag_dest_label.text = val
        self.root.ids.diag_search_field_hint.text = f"Search {val}"
        if val == "Prescriptions":
            self.root.ids.diag_search_btn.on_release = lambda: self.search_prescs()
            self.set_sort_btn(self.root.ids.diag_sort_btn, self.sort_prescs_by)
            self.show_prescriptions("Any", "Any", "Any", self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header)
        elif val == "Diagnoses":
            self.set_sort_btn(self.root.ids.diag_sort_btn, self.sort_diags_by)
            self.root.ids.diag_search_btn.on_release = lambda: self.search_diags()
            self.show_diagnosis("Any", "Any", "Any", self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header)
        elif val == "Lab Results":
            self.root.ids.diag_search_btn.on_release = lambda: self.search_resuls()
            self.set_sort_btn(self.root.ids.diag_sort_btn, self.sort_resuls_by)
            self.show_lab_results("Any", "Any", "Any", self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header)
        elif val == "Lab Requests":
            self.root.ids.diag_search_btn.on_release = lambda: self.search_requests()
            self.set_sort_btn(self.root.ids.diag_sort_btn, self.sort_requests_by)
            self.show_lab_requests("Any", "Any", "Any", self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header)
    
    def lab_nav(self, val):
        self.root.ids.lab_dest_label.text = val
        self.root.ids.lab_search_field_hint.text = f"Search {val}"
        if val == "Lab Results":
            self.root.ids.lab_search_btn.on_release = lambda: self.search_resuls()
            self.set_sort_btn(self.root.ids.lab_sort_btn, self.sort_resuls_by)
            self.show_lab_results("Any", "Any", "Any", self.root.ids.lab_prev, self.root.ids.labrvb, self.root.ids.lab_cont_header)
        elif val == "Diagnoses":
            self.root.ids.diag_search_btn.on_release = lambda: self.search_diags()
            self.set_sort_btn(self.root.ids.lab_sort_btn, self.sort_diags_by)
            self.show_diagnosis("Any", "Any", "Any", self.root.ids.lab_prev, self.root.ids.labrvb, self.root.ids.lab_cont_header)
        elif val == "Lab Requests":
            self.root.ids.lab_search_btn.on_release = lambda: self.search_requests()
            self.set_sort_btn(self.root.ids.lab_sort_btn, self.sort_requests_by)
            self.show_lab_requests("Any", "Any", "Any", self.root.ids.lab_prev, self.root.ids.labrvb, self.root.ids.lab_cont_header)

    def change_user(self, val):
        if val == "Admin":
            self.sign_in_form(val)
        elif val == "Receptionist":
            self.sign_in_form(val)
        elif val == "Pharmacist":
            self.sign_in_form(val)
        elif val == "Doctor":
            self.sign_in_form(val)
        elif val == "LabTech":
            self.sign_in_form(val)

# Applying sorting to various records by conditions

    def sort_pats_by(self, val):
        if self.root.current == "reception_screen":
            prev, prev_box, prev_cont = self.root.ids.rec_prev, self.root.ids.rvb, self.root.ids.rec_cont_header
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
        else:
            return
        if val == "Newest First":
            self.show_patients("Time", "desc", "Any", prev, prev_box, prev_cont)
        elif val == "Oldest First":
            self.show_patients("Time", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "A to Z":
            self.show_patients("Name", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "Z to A":
            self.show_patients("Name", "desc", "Any", prev, prev_box, prev_cont)

    def sort_wrks_by(self, val):
        if val == "Newest First":
            self.show_workers("Time", "desc", "Any")
        elif val == "Oldest First":
            self.show_workers("Time", "asc", "Any")
        elif val == "A to Z":
            self.show_workers("Name", "asc", "Any")
        elif val == "Z to A":
            self.show_workers("Name", "desc", "Any")

    def sort_drugs_by(self, val):
        if self.root.current == "chemist_screen":
            prev, prev_box, prev_cont = self.root.ids.chem_prev, self.root.ids.chemrvb, self.root.ids.chem_cont_header
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
        elif self.root.current == "diagnosis_screen":
            prev, prev_box, prev_cont = self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header
        if val == "Newest First":
            self.show_drugs("Time", "desc", "Any", prev, prev_box, prev_cont)
        elif val == "Oldest First":
            self.show_drugs("Time", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "A to Z":
            self.show_drugs("Name", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "Z to A":
            self.show_drugs("Name", "desc", "Any", prev, prev_box, prev_cont)

    def sort_diags_by(self, val):
        if self.root.current == "chemist_screen":
            prev, prev_box, prev_cont = self.root.ids.chem_prev, self.root.ids.chemrvb, self.root.ids.chem_cont_header
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
        elif self.root.current == "diagnosis_screen":
            prev, prev_box, prev_cont = self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header
        elif self.root.current == "lab_screen":
            prev, prev_box, prev_cont = self.root.ids.lab_prev, self.root.ids.labrvb, self.root.ids.lab_cont_header
        if val == "Newest First":
            self.show_diagnosis("Time", "desc", "Any", prev, prev_box, prev_cont)
        elif val == "Oldest First":
            self.show_diagnosis("Time", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "A to Z":
            self.show_diagnosis("Name", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "Z to A":
            self.show_diagnosis("Name", "desc", "Any", prev, prev_box, prev_cont)

    def sort_resuls_by(self, val):
        if self.root.current == "lab_screen":
            prev, prev_box, prev_cont = self.root.ids.lab_prev, self.root.ids.labrvb, self.root.ids.lab_cont_header
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
        elif self.root.current == "diagnosis_screen":
            prev, prev_box, prev_cont = self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header
        if val == "Newest First":
            self.show_lab_results("Time", "desc", "Any", prev, prev_box, prev_cont)
        elif val == "Oldest First":
            self.show_lab_results("Time", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "A to Z":
            self.show_lab_results("Name", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "Z to A":
            self.show_lab_results("Name", "desc", "Any", prev, prev_box, prev_cont)
    
    def sort_requests_by(self, val):
        if self.root.current == "lab_screen":
            prev, prev_box, prev_cont = self.root.ids.lab_prev, self.root.ids.labrvb, self.root.ids.lab_cont_header
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
        elif self.root.current == "diagnosis_screen":
            prev, prev_box, prev_cont = self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header
        if val == "Newest First":
            self.show_lab_requests("Time", "desc", "Any", prev, prev_box, prev_cont)
        elif val == "Oldest First":
            self.show_lab_requests("Time", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "A to Z":
            self.show_lab_requests("Name", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "Z to A":
            self.show_lab_requests("Name", "desc", "Any", prev, prev_box, prev_cont)
        
    def sort_billings_by(self, val):
        prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
        if val == "Newest First":
            self.show_billings("Time", "desc", "Any", prev, prev_box, prev_cont)
        elif val == "Oldest First":
            self.show_billings("Time", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "A to Z":
            self.show_billings("Name", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "Z to A":
            self.show_billings("Name", "desc", "Any", prev, prev_box, prev_cont)
    
    def sort_prescs_by(self, val):
        if self.root.current == "chemist_screen":
            prev, prev_box, prev_cont = self.root.ids.chem_prev, self.root.ids.chemrvb, self.root.ids.chem_cont_header
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
        elif self.root.current == "diagnosis_screen":
            prev, prev_box, prev_cont = self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header
        if val == "Newest First":
            self.show_prescriptions("Time", "desc", "Any", prev, prev_box, prev_cont)
        elif val == "Oldest First":
            self.show_prescriptions("Time", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "A to Z":
            self.show_prescriptions("Name", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "Z to A":
            self.show_prescriptions("Name", "desc", "Any", prev, prev_box, prev_cont)
    
    def sort_appts_by(self, val):
        if self.root.current == "reception_screen":
            prev, prev_box, prev_cont = self.root.ids.rec_prev, self.root.ids.rvb, self.root.ids.rec_cont_header
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
        elif self.root.current == "diagnosis_screen":
            prev, prev_box, prev_cont = self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header
        if val == "Newest First":
            self.show_appointments("Time", "desc", "Any", prev, prev_box, prev_cont)
        elif val == "Oldest First":
            self.show_appointments("Time", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "A to Z":
            self.show_appointments("Name", "asc", "Any", prev, prev_box, prev_cont)
        elif val == "Z to A":
            self.show_appointments("Name", "desc", "Any", prev, prev_box, prev_cont)

# Applying searching to various records by conditions

    def search_pats(self):
        if self.root.current == "reception_screen":
            prev, prev_box, prev_cont = self.root.ids.rec_prev, self.root.ids.rvb, self.root.ids.rec_cont_header
            term = self.root.ids.rec_search_field.text.strip().lower()
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
            term = self.root.ids.adm_search_field.text.strip().lower()
        else:
            return
        if not term:
            return
        self.show_patients("Search", "Any", term, prev, prev_box, prev_cont)
    
    def search_wrks(self):
        term = self.root.ids.adm_search_field.text.strip().lower()
        self.show_patients("Search", "Any", term, self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)

    def search_drugs(self):
        if self.root.current == "chemist_screen":
            prev, prev_box, prev_cont = self.root.ids.chem_prev, self.root.ids.chemrvb, self.root.ids.chem_cont_header
            term = self.root.ids.chem_search_field.text.strip().lower()
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
            term = self.root.ids.adm_search_field.text.strip().lower()
        elif self.root.current == "diagnosis_screen":
            prev, prev_box, prev_cont = self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header
            term = self.root.ids.diag_search_field.text.strip().lower()
        else:
            return
        if not term:
            return
        self.show_drugs("Search", "Any", term, prev, prev_box, prev_cont)
    
    def search_diags(self):
        if self.root.current == "chemist_screen":
            prev, prev_box, prev_cont = self.root.ids.chem_prev, self.root.ids.chemrvb, self.root.ids.chem_cont_header
            term = self.root.ids.chem_search_field.text.strip().lower()
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
            term = self.root.ids.adm_search_field.text.strip().lower()
        elif self.root.current == "diagnosis_screen":
            prev, prev_box, prev_cont = self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header
            term = self.root.ids.diag_search_field.text.strip().lower()
        elif self.root.current == "lab_screen":
            prev, prev_box, prev_cont = self.root.ids.lab_prev, self.root.ids.labrvb, self.root.ids.lab_cont_header
            term = self.root.ids.lab_search_field.text.strip().lower()
        else:
            return
        if not term:
            return
        self.show_diagnosis("Search", "Any", term, prev, prev_box, prev_cont)
    
    def search_prescs(self):
        if self.root.current == "chemist_screen":
            prev, prev_box, prev_cont = self.root.ids.chem_prev, self.root.ids.chemrvb, self.root.ids.chem_cont_header
            term = self.root.ids.chem_search_field.text.strip().lower()
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
            term = self.root.ids.adm_search_field.text.strip().lower()
        elif self.root.current == "diagnosis_screen":
            prev, prev_box, prev_cont = self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header
            term = self.root.ids.diag_search_field.text.strip().lower()
        else:
            return
        if not term:
            return
        self.show_prescriptions("Search", "Any", term, prev, prev_box, prev_cont)
    
    def search_resuls(self):
        if self.root.current == "lab_screen":
            prev, prev_box, prev_cont = self.root.ids.lab_prev, self.root.ids.labrvb, self.root.ids.lab_cont_header
            term = self.root.ids.lab_search_field.text.strip().lower()
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
            term = self.root.ids.adm_search_field.text.strip().lower()
        elif self.root.current == "diagnosis_screen":
            prev, prev_box, prev_cont = self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header
            term = self.root.ids.diag_search_field.text.strip().lower()
        else:
            return
        if not term:
            return
        self.show_lab_results("Search", "Any", term, prev, prev_box, prev_cont)
    
    def search_requests(self):
        if self.root.current == "lab_screen":
            prev, prev_box, prev_cont = self.root.ids.lab_prev, self.root.ids.labrvb, self.root.ids.lab_cont_header
            term = self.root.ids.lab_search_field.text.strip().lower()
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
            term = self.root.ids.adm_search_field.text.strip().lower()
        elif self.root.current == "diagnosis_screen":
            prev, prev_box, prev_cont = self.root.ids.diag_prev, self.root.ids.diagrvb, self.root.ids.diag_cont_header
            term = self.root.ids.diag_search_field.text.strip().lower()
        else:
            return
        if not term:
            return
        self.show_lab_requests("Search", "Any", term, prev, prev_box, prev_cont)

    def search_billings(self):
        prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
        term = self.root.ids.adm_search_field.text.strip().lower()
        if not term:
            return
        self.show_billings("Search", "Any", term, prev, prev_box, prev_cont)


    def search_appts(self):
        if self.root.current == "reception_screen":
            prev, prev_box, prev_cont = self.root.ids.rec_prev, self.root.ids.rvb, self.root.ids.rec_cont_header
            term = self.root.ids.rec_search_field.text.strip().lower()
        elif self.root.current == "admin_screen":
            prev, prev_box, prev_cont = self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header
            term = self.root.ids.adm_search_field.text.strip().lower()
        else:
            return
        if not term:
            return
        self.show_appointments("Search", "Any", term, prev, prev_box, prev_cont)

    def display_patients(self, pat_name, pat_email, pat_id, pat_phone, pat_gender, pat_address):
        pat_name = MDLabel(text = f"Name:   {pat_name}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        pat_email = MDLabel(text = f"Email:   {pat_email}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        pat_id = MDLabel(text = f"ID Number:    {pat_id}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        pat_phone = MDLabel(text = f"Phone Number:  {pat_phone}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        pat_gender = MDLabel(text = f"Gender:   {pat_gender}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        pat_address = MDLabel(text = f"Address:   {pat_address}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)

        cont = MDDialogContentContainer(orientation = "vertical", spacing = dp(35))
        cont.add_widget(pat_name)
        cont.add_widget(pat_email)
        cont.add_widget(pat_id)
        cont.add_widget(pat_phone)
        cont.add_widget(pat_gender)
        cont.add_widget(pat_address)

        self.patients_display = MDDialog(
            MDDialogIcon(icon = "account"),
            MDDialogHeadlineText(text = "Patient Profile"),
            cont,
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text = "Okay"),
                    on_release = lambda x: self.patients_display.dismiss()
                ),
                Widget()
            )
        )
        self.patients_display.open()
    
    def display_workers(self, wrk_name, wrk_email, wrk_id, wrk_phone, wrk_gender, wrk_role):
        wrk_name = MDLabel(text = f"Name:   {wrk_name}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        wrk_email = MDLabel(text = f"Email:   {wrk_email}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        wrk_id = MDLabel(text = f"ID Number:    {wrk_id}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        wrk_phone = MDLabel(text = f"Phone Number:  {wrk_phone}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        wrk_gender = MDLabel(text = f"Gender:   {wrk_gender}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        wrk_role = MDLabel(text = f"Role:   {wrk_role}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)

        cont = MDDialogContentContainer(orientation = "vertical", spacing = dp(35))
        cont.add_widget(wrk_name)
        cont.add_widget(wrk_email)
        cont.add_widget(wrk_id)
        cont.add_widget(wrk_phone)
        cont.add_widget(wrk_gender)
        cont.add_widget(wrk_role)

        self.workers_display = MDDialog(
            MDDialogIcon(icon = "account"),
            MDDialogHeadlineText(text = "Worker Profile"),
            cont,
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text = "Okay"),
                    on_release = lambda x: self.workers_display.dismiss()
                ),
                Widget()
            )
        )
        self.workers_display.open()

    def display_drugs(self, drug_name, drug_category, drug_desc, drug_price, drug_qty, drug_expiry):
        drug_name = MDLabel(text = f"Name:   {drug_name}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        drug_category = MDLabel(text = f"Category:   {drug_category}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        drug_desc = MDLabel(text = f"Description:    {drug_desc}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        drug_price = MDLabel(text = f"Price:  Ksh. {drug_price}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        drug_qty = MDLabel(text = f"Quantity:   {drug_qty}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        drug_expiry = MDLabel(text = f"Expiry:   {drug_expiry}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)

        cont = MDDialogContentContainer(orientation = "vertical", spacing = dp(35))
        cont.add_widget(drug_name)
        cont.add_widget(drug_category)
        cont.add_widget(drug_desc)
        cont.add_widget(drug_price)
        cont.add_widget(drug_qty)
        cont.add_widget(drug_expiry)

        self.drugs_display = MDDialog(
            MDDialogIcon(icon = "pill"),
            MDDialogHeadlineText(text = "Drug Profile"),
            cont,
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text = "Okay"),
                    on_release = lambda x: self.drugs_display.dismiss()
                ),
                Widget()
            )
        )
        self.drugs_display.open()

    def display_appointments(self, pat_name, consultant, service_name, objective, set_on, start_at):
        pat_name = MDLabel(text = f"Patient:   {pat_name}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        consultant = MDLabel(text = f"Consultant:   {consultant}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        service_name = MDLabel(text = f"Service:    {service_name}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        objective = MDLabel(text = f"Objective:  {objective}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        set_on = MDLabel(text = f"Set On:   {set_on}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        start_at = MDLabel(text = f"Start At:   {start_at}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)

        cont = MDDialogContentContainer(orientation = "vertical", spacing = dp(35))
        cont.add_widget(pat_name)
        cont.add_widget(consultant)
        cont.add_widget(service_name)
        cont.add_widget(objective)
        cont.add_widget(set_on)
        cont.add_widget(start_at)

        self.appointments_display = MDDialog(
            MDDialogIcon(icon = "calender-clock"),
            MDDialogHeadlineText(text = "Appointment Profile"),
            cont,
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text = "Okay"),
                    on_release = lambda x: self.appointments_display.dismiss()
                ),
                Widget()
            )
        )
        self.appointments_display.open()
    
    def display_prescriptions(self, pat_name, prescription, drug, qty, prescriber):
        comb_presc = [{"Drug": d, "Qty": q, "Prescription": p } for d, q, p in zip(drug, qty, prescription)]
        pat_name = MDLabel(text = f"Patient:   {pat_name}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        prescriber = MDLabel(text = f"Prescriber:   {prescriber}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        
        cont = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        cont.add_widget(pat_name)
        count = 1

        prescs_layout = MDGridLayout(
            cols=1,
            adaptive_height=True,
            size_hint_y=None,
            spacing=dp(10),
            padding=dp(10)
        )
        prescs_layout.bind(minimum_height=prescs_layout.setter("height"))

        for presc in comb_presc:
            count_label = MDLabel(text = f"{count}. ", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True, size_hint_y = None, height = dp(30))
            drug_label = MDLabel(text = f"     Drug: {presc['Drug']}", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True, size_hint_y = None, height = dp(30))
            qty_label = MDLabel(text = f"      Qty: {presc['Qty']}", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True, size_hint_y = None, height = dp(30))
            presc_label = MDLabel(text = f"    Notes: {presc['Prescription']}", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True, size_hint_y = None, height = dp(30))
            prescs_layout.add_widget(count_label)
            prescs_layout.add_widget(drug_label)
            prescs_layout.add_widget(qty_label)
            prescs_layout.add_widget(presc_label)
            count += 1
        presc_scroll = MDScrollView(size_hint = (1, None), height = dp(300))
        presc_scroll.add_widget(prescs_layout)
        cont.add_widget(presc_scroll)

        cont.add_widget(prescriber)

        self.prescriptions_display = MDDialog(
            MDDialogIcon(icon = "medical-bag"),
            MDDialogHeadlineText(text = "Prescription Profile"),
            cont,
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text = "Okay"),
                    on_release = lambda x: self.prescriptions_display.dismiss()
                ),
                Widget()
            )
        )
        self.prescriptions_display.open()

    def display_diagnoses(self, pat_name, symptoms, findings, diagnosis, diagnoser):
        pat_name = MDLabel(text = f"Patient:   {pat_name}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        symptoms = MDLabel(text = f"Symptoms:   {symptoms}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        findings = MDLabel(text = f"Findings:    {findings}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        diagnosis = MDLabel(text = f"Diagnosis:  {diagnosis}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        diagnoser = MDLabel(text = f"Diagnoser:   {diagnoser}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        
        cont = MDDialogContentContainer(orientation = "vertical", spacing = dp(35))
        cont.add_widget(pat_name)
        cont.add_widget(symptoms)
        cont.add_widget(findings)
        cont.add_widget(diagnosis)
        cont.add_widget(diagnoser)

        self.diagnosis_display = MDDialog(
            MDDialogIcon(icon = "stethoscope"),
            MDDialogHeadlineText(text = "Diagnosis Profile"),
            cont,
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text = "Okay"),
                    on_release = lambda x: self.diagnosis_display.dismiss()
                ),
                Widget()
            )
        )
        self.diagnosis_display.open()
    
    def display_resuls(self, pat_name, observations, conclusion, labtech):
        pat_name = MDLabel(text = f"Patient:   {pat_name}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        observation = MDLabel(text = f"Observations:   {observations}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        conclusion = MDLabel(text = f"Conclusion:    {conclusion}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        labtech = MDLabel(text = f"LabTech:  {labtech}", halign = "center", theme_text_color = "Custom", text_color = "teal", theme_font_size = "Custom", font_size = sp(16), bold = True)
        
        cont = MDDialogContentContainer(orientation = "vertical", spacing = dp(35))
        cont.add_widget(pat_name)
        cont.add_widget(observation)
        cont.add_widget(conclusion)
        cont.add_widget(labtech)

        self.resuls_display = MDDialog(
            MDDialogIcon(icon = "test-tube"),
            MDDialogHeadlineText(text = "Lab Results Profile"),
            cont,
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text = "Okay"),
                    on_release = lambda x: self.resuls_display.dismiss()
                ),
                Widget()
            )
        )
        self.resuls_display.open()

    def edit_drugs_form(self, drug_id):
        drug = database.session.query(database.Drug).filter_by(drug_id = drug_id).first()
        self.d_name = MDTextField(MDTextFieldHintText(text = "Drug Name"), text = drug.drug_name)
        self.d_category = MDTextField(MDTextFieldHintText(text = "Category"), text = drug.drug_category)
        self.d_desc = MDTextField(MDTextFieldHintText(text = "Description"), text = drug.drug_desc)
        self.d_price = MDTextField(MDTextFieldHintText(text = "Price"), text = str(drug.drug_price), input_filter = "float")
        self.d_qty = MDTextField(MDTextFieldHintText(text = "Quantity"), text = str(drug.drug_quantity), input_filter = "int")
        self.d_expiry = MDTextField(MDTextFieldHintText(text = "Expiry Date"), text = str(drug.drug_expiry).split(" ")[0])

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(10))
        content.add_widget(self.d_name)
        content.add_widget(self.d_category)
        content.add_widget(self.d_desc)
        content.add_widget(self.d_price)
        content.add_widget(self.d_qty)
        content.add_widget(self.d_expiry)

        self.drug_edit_dialog = MDDialog(
            MDDialogIcon(icon = "pencil"),
            MDDialogHeadlineText(text = "Edit Drug"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Edit"), on_release = lambda x: self.edit_drugs(drug=drug)),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.drug_edit_dialog.dismiss()),
                spacing = dp(20)
            )
        )
        self.drug_edit_dialog.open()
    
    def edit_drugs(self, drug):
        drug_name = self.d_name.text.strip().lower()
        drug_cat = self.d_category.text.strip().lower()
        drug_desc = self.d_desc.text.strip().lower()
        drug_price = self.d_price.text.strip()
        drug_qty = self.d_qty.text.strip()
        drug_expiry = self.d_expiry.text.strip().lower()

        drug.drug_name = drug_name
        drug.drug_category = drug_cat
        drug.drug_desc = drug_desc
        drug.drug_price = drug_price
        drug.drug_quantity = drug_qty
        drug.drug_expiry = datetime.strptime(drug_expiry, "%Y-%m-%d").date()

        database.session.commit()
        if self.root.current == "admin_screen":
            self.show_drugs("Any", "Any", "Any", self.root.ids.adm_prev, self.root.ids.adrvb, self.root.ids.adm_cont_header)
        elif self.root.current == "chemist_screen":
            self.show_drugs("Any", "Any", "Any", self.root.ids.chem_prev, self.root.ids.chemrvb, self.root.ids.chem_cont_header)
        else:
            return
        self.show_snack("Drug edited successfully!!")
    
    def export_file_dialog(self, name, func):
        self.file_name = MDTextField(MDTextFieldHintText(text = "Enter File Name"))
        self.file_path = MDTextField(MDTextFieldHintText(text = "Enter File Path"), pos_hint = {"center_y":.5})
        file_path_cont = MDBoxLayout(size_hint_y = None, height = dp(50), spacing = dp(10))
        browser_btn = MDIconButton(icon = "folder-open", pos_hint = {"center_y":.5}, on_release = lambda x: self.open_file_manager())
        file_path_cont.add_widget(self.file_path)
        file_path_cont.add_widget(browser_btn)

        content = MDDialogContentContainer(orientation = "vertical", spacing = dp(25))
        content.add_widget(self.file_name)
        content.add_widget(file_path_cont)

        self.file_dialog = MDDialog(
            MDDialogIcon(icon = "file-export"),
            MDDialogHeadlineText(text = f"Export {name} Records"),
            content,
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text = "Export"), on_release = lambda x: func()),
                MDButton(MDButtonText(text = "Cancel"), on_release = lambda x: self.file_dialog.dismiss()),
                spacing = dp(25)
            )
        )
        self.file_dialog.open()

    def open_file_manager(self):
        start_path = os.path.expanduser("~")
        self.file_manager.show(start_path)
    def select_path(self, path: str):
        self.exit_manager()
        self.file_path.text = path
    def exit_manager(self, *args):
        self.file_manager.close()
    
    def export_pat_data(self):
        path = self.file_path.text.strip()
        file_name = self.file_name.text.strip()
        full_path = os.path.join(path, f"{file_name}.csv")

        with open(full_path, mode="w", encoding="utf-8", newline="") as file:
            patients = database.session.query(database.Patient).all()
            writer = csv.writer(file)
            writer.writerow(["Patient", "Email", "Phone", "ID NO", "Gender", "Address", "D.O.B", "Date Added"])
            for p in patients:
                writer.writerow([p.patient_name, p.patient_email, p.patient_phone, p.patient_id_number, p.patient_gender, p.patient_address, p.patient_dob, p.date_added])
            database.session.close()
            self.show_snack("Patients records exported successfully!")

    def export_wrk_data(self):
        path = self.file_path.text.strip()
        file_name = self.file_name.text.strip()
        full_path = os.path.join(path, f"{file_name}.csv")

        with open(full_path, mode="w", encoding="utf-8", newline="") as file:
            workers = database.session.query(database.Worker).all()
            writer = csv.writer(file)
            writer.writerow(["Worker", "Email", "Phone", "ID NO", "Gender", "Role", "D.O.B", "Date Added"])
            for w in workers:
                writer.writerow([w.worker_name, w.worker_email, w.worker_phone, w.worker_id_number, w.worker_gender, w.worker_role, w.worker_dob, w.date_added])
            database.session.close()
            self.show_snack("Workers records exported successfully!")
    
    def export_app_data(self):
        path = self.file_path.text.strip()
        file_name = self.file_name.text.strip()
        full_path = os.path.join(path, f"{file_name}.csv")

        with open(full_path, mode="w", encoding="utf-8", newline="") as file:
            appointments = database.session.query(database.Appointment).all()
            writer = csv.writer(file)
            writer.writerow(["Patient", "Consultant", "Service", "Objective", "Set On", "Start At", "Date Scheduled"])
            for a in appointments:
                writer.writerow([a.patient.patient_name, a.consultant.worker_name, a.service.service_name, a.date_scheduled, a.time_scheduled, a.date_requested])
            database.session.close()
            self.show_snack("Appointment records exported successfully!")
    
    def export_drug_data(self):
        path = self.file_path.text.strip()
        file_name = self.file_name.text.strip()
        full_path = os.path.join(path, f"{file_name}.csv")

        with open(full_path, mode="w", encoding="utf-8", newline="") as file:
            drugs = database.session.query(database.Drug).all()
            writer = csv.writer(file)
            writer.writerow(["Drug", "Category", "Description", "Quantity", "Price", "Expiry Date"])
            for d in drugs:
                writer.writerow([d.drug_name, d.drug_category, d.drug_desc, d.drug_quantity, d.drug_price, d.drug_expiry])
            database.session.close()
            self.show_snack("Drug records exported successfully!")
    
    def export_presc_data(self):
        path = self.file_path.text.strip()
        file_name = self.file_name.text.strip()
        full_path = os.path.join(path, f"{file_name}.csv")

        with open(full_path, mode="w", encoding="utf-8", newline="") as file:
            prescriptions = database.session.query(database.Prescription).all()
            grouped = defaultdict(list)
            writer = csv.writer(file)
            writer.writerow(["Patient", "Prescription", "Drugs", "Quantity", "Prescribed By", "Date Prescribed"])

            for presc in prescriptions:
                grouped[presc.patient.patient_name].append(presc)

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
                writer.writerow([patient_name, all_drugs, all_qtys, prescriber_display, all_dates])
            database.session.close()
            self.show_snack("Prescription records exported successfully!")
    
    def export_lab_result_data(self):
        path = self.file_path.text.strip()
        file_name = self.file_name.text.strip()
        full_path = os.path.join(path, f"{file_name}.csv")

        with open(full_path, mode="w", encoding="utf-8", newline="") as file:
            results = database.session.query(database.LaboratoryResult).all()
            writer = csv.writer(file)
            writer.writerow(["Patient", "Observations", "Conclusions", "Lab Technician", "Date Conveyed"])
            for r in results:
                writer.writerow([r.patient.patient_name, r.observations, r.conclusion, r.tech.worker_name, r.date_requested])
            database.session.close()
            self.show_snack("Laboratory results records exported successfully!")
    
    def export_lab_requests_data(self):
        path = self.file_path.text.strip()
        file_name = self.file_name.text.strip()
        full_path = os.path.join(path, f"{file_name}.csv")

        with open(full_path, mode="w", encoding="utf-8", newline="") as file:
            requests = database.session.query(database.LaboratoryRequest).all()
            writer = csv.writer(file)
            writer.writerow(["Patient", "Doctor", "Test Name", "Date Requested"])
            for r in requests:
                writer.writerow([r.patient.patient_name, r.doctor.worker_name, r.test.test_name, r.date_added])
            database.session.close()
            self.show_snack("Laboratory requests records exported successfully!")
    
    def export_diag_data(self):
        path = self.file_path.text.strip()
        file_name = self.file_name.text.strip()
        full_path = os.path.join(path, f"{file_name}.csv")

        with open(full_path, mode="w", encoding="utf-8", newline="") as file:
            diags = database.session.query(database.Diagnosis).all()
            writer = csv.writer(file)
            writer.writerow(["Patient", "Symptoms", "Findings", "Diagnoses", "Doctor", "Date Diagnosed"])
            for d in diags:
                writer.writerow([d.patient.patient_name, d.symptoms, d.findings, d.suggested_diagnosis, d.diagnoser.worker_name, d.date_diagnosed])
            database.session.close()
            self.show_snack("Diagnosis records exported successfully!")
    
    def export_lab_test_data(self):
        path = self.file_path.text.strip()
        file_name = self.file_name.text.strip()
        full_path = os.path.join(path, f"{file_name}.csv")

        with open(full_path, mode="w", encoding="utf-8", newline="") as file:
            tests = database.session.query(database.LaboratoryTest).all()
            writer = csv.writer(file)
            writer.writerow(["Lab Test", "Description", "Price"])
            for t in tests:
                writer.writerow([t.test_name, t.test_desc, t.test_price])
            database.session.close()
            self.show_snack("Lab test records exported successfully!")
    
    def export_services_data(self):
        path = self.file_path.text.strip()
        file_name = self.file_name.text.strip()
        full_path = os.path.join(path, f"{file_name}.csv")

        with open(full_path, mode="w", encoding="utf-8", newline="") as file:
            services = database.session.query(database.Service).all()
            writer = csv.writer(file)
            writer.writerow(["Service", "Description", "Price"])
            for s in services:
                writer.writerow([s.service_name, s.service_desc, s.service_price])
            database.session.close()
            self.show_snack("Service records exported successfully!")

    def export_billings_data(self):
        path = self.file_path.text.strip()
        file_name = self.file_name.text.strip()
        full_path = os.path.join(path, f"{file_name}.csv")

        with open(full_path, mode="w", encoding="utf-8", newline="") as file:
            bills = database.session.query(database.Billing).all()
            writer = csv.writer(file)
            writer.writerow(["Patient", "Items", "Total"])
            for b in bills:
                writer.writerow([b.patient.patient_name, b.items, b.total])
            database.session.close()
            self.show_snack("Billing records exported successfully!")

if __name__ == "__main__":
    app = NeptuneHMS()
    app.run()

# Try Kivymd. It's the best framework...😂😂😂😂