from django import forms
from.models import *

class hosp_form(forms.ModelForm):
    class Meta:
        model=HospitalRegister
        fields=['hosp_name','hosp_address','hosp_city','hosp_district','hosp_state','hosp_contact']
        widget={
            'hosp_name':forms.TextInput(attrs={'class':'form-control'}),
            'hosp_address':forms.TextInput(attrs={'class':'form-control'}),
            'hosp_city':forms.TextInput(attrs={'class':'form-control'}),
            'hosp_district':forms.TextInput(attrs={'class':'form-control'}),
            'hosp_state':forms.TextInput(attrs={'class':'form-control'}),
            'hosp_contact':forms.TextInput(attrs={'class':'form-control'})
        }


class login_form(forms.ModelForm):
    class Meta:
        model=Login
        fields=['email','password']
        
class logincheck(forms.Form):
    email=forms.CharField(max_length=20)
    password=forms.CharField(max_length=20)


class doc_form(forms.ModelForm):
    gender_choices=(        
        ('male','Male'),('female','Female'),('others','Others')
    )
    gender=forms.ChoiceField(choices=gender_choices,widget=forms.RadioSelect())
    dept_choices=(        
        ('casualty','Casualty'),('operating theatre (OT)','Operating theatre (OT)'),('intensive care unit (ICU)','Intensive care unit (ICU)'),('anesthesiology','Anesthesiology'),('cardiology','Cardiology'),('ent','ENT'),('gastroenterology','Gastroenterology'),('general surgery','General surgery'),('gynaecology ','Gynaecology '),('pediatrics ','Pediatrics '),('oncology ','Oncology '),('opthalmology ','Opthalmology '),('orthopaedic ','Orthopaedic '),('psychiatry','Psychiatry')
    )
    department=forms.ChoiceField(choices=dept_choices,widget=forms.Select())
    class Meta:
        model=DoctorRegister
        fields=['doc_name','gender','age','department','specialisation', 'consultation_fee','doc_license','doc_contact']
        widget={
            'doc_name':forms.TextInput(attrs={'class':'form-control'}),
            'age':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'department':forms.TextInput(attrs={'class':'form-control'}),
            'specialisation':forms.TextInput(attrs={'class':'form-control'}),
            'consultation_fee':forms.TextInput(attrs={'class':'form-control'}),
            'doc_license':forms.FileInput(attrs={'class':'form-control'}),
            'doc_contact':forms.TextInput(attrs={'class':'form-control'})
        }

class patient_form(forms.ModelForm):
    gender_choices=(        
        ('male','Male'),('female','Female'),('others','Others')
    )
    gender=forms.ChoiceField(choices=gender_choices,widget=forms.RadioSelect())
    class Meta:
        model=PatientRegister
        fields=['patient_name','address','gender','age','patient_contact']
        widget={
            'patient_name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.FileInput(attrs={'class':'form-control'}),
            'age':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'patient_contact':forms.TextInput(attrs={'class':'form-control'})
        }

class appointment_form(forms.ModelForm):
    class Meta:
        model=Appointment
        fields=['date','time']
        widgets={
            'date':forms.TextInput(attrs={'class':'form-control','type':'date'}),
            'time':forms.TextInput(attrs={'class':'form-control','type':'time'}),
        }  
class consult_form(forms.ModelForm):
    class Meta:
        model=DoctorRegister
        fields=['consultation_fee']
        widget={
            'consultation_fee':forms.TextInput(attrs={'class':'form-control'}),
        }

class payment_form(forms.ModelForm):
    class Meta:
        model=Payment
        fields=['card_name','card_number','cvv','exp_date']
        widgets={
            'card_name':forms.TextInput(attrs={'class':'form-control'}),
            'card_number':forms.TextInput(attrs={'class':'form-control'}),
            'cvv':forms.TextInput(attrs={'class':'form-control'}),
            'exp_date':forms.TextInput(attrs={'class':'form-control','type':'date'}),
            
        }       

class refund_form(forms.ModelForm):
     class Meta:
        model=Payment
        fields=['card_name','card_number','cvv','exp_date']
class amb_form(forms.ModelForm):
    category_choices=(        
        ('basic life support','Basic Life Support'),('advanced life support','Advanced Life Support'),('critical care support','Critical Care Support')
    )
    vehicle_category=forms.ChoiceField(choices=category_choices,widget=forms.Select())
    type_choices=(        
        ('type I(truck-based)','Type I(Truck-based)'),('type II(van-based)','Type II(Van-based)'),('type III(modular)','Type III(Modular)')
    )
    vehicle_type=forms.ChoiceField(choices=type_choices,widget=forms.Select())
    class Meta:
        model=AmbulanceRegister
        fields=['vehicle_category','vehicle_type','vehicle_no','driver_name','driver_contact']
        widget={
            'vehicle_category':forms.Select(attrs={'class':'form-control'}),
            'vehicle_type':forms.Select(attrs={'class':'form-control'}),
            'vehicle_no':forms.TextInput(attrs={'class':'form-control'}),
            'driver_name':forms.TextInput(attrs={'class':'form-control'}),
            'driver_contact':forms.TextInput(attrs={'class':'form-control'})
        }
class amb_login_form(forms.ModelForm):
    class Meta:
        model=Login
        fields=['email']
        
class prescription_form(forms.ModelForm):
    class Meta:
        model=Appointment
        fields=['prescription']
        widget={
            'prescription':forms.TextInput(attrs={'class':'form-control'})
        }