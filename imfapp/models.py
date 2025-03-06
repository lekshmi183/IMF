from django.db import models
import uuid
class HospitalRegister(models.Model):
    hosp_name=models.CharField(max_length=255)
    hosp_address=models.CharField(max_length=255)
    hosp_city=models.CharField(max_length=100)
    hosp_district=models.CharField(max_length=100)
    hosp_state=models.CharField(max_length=100)
    hosp_contact=models.CharField(max_length=15)
    login_id=models.ForeignKey('Login',on_delete=models.CASCADE)
    

   
class Login(models.Model):
    email = models.EmailField() 
    password = models.CharField(max_length=255)
    usertype=models.IntegerField(default=0,null=True)
    login_status=models.IntegerField(default=0)

class DoctorRegister(models.Model):
   doc_name=models.CharField(max_length=255)
   gender=models.CharField(max_length=255)
   age=models.IntegerField()
   department=models.CharField(max_length=255)
   specialisation=models.CharField(max_length=255)
   consultation_fee=models.IntegerField(default=0)
   doc_license=models.FileField(upload_to='license')
   hosp_id=models.ForeignKey('Login',on_delete=models.CASCADE,related_name='hosp_id')
   doc_contact=models.CharField(max_length=15)
   login_id=models.ForeignKey('Login',on_delete=models.CASCADE,related_name='login_id')
   


class PatientRegister(models.Model):
   patient_name=models.CharField(max_length=255)
   address=models.CharField(max_length=255)
   gender=models.CharField(max_length=255)
   age=models.IntegerField()
   patient_contact=models.CharField(max_length=20)
   login_id=models.ForeignKey('Login',on_delete=models.CASCADE)
   MRnumber = models.CharField(max_length=20, unique=True, editable=False)
   def save(self, *args, **kwargs):
        if not self.MRnumber:  # Only generate if not already assigned
            self.MRnumber = self.generate_unique_mrnumber()
        super().save(*args, **kwargs)

   def generate_unique_mrnumber(self):
        """Generate a unique MR number"""
        while True:
            new_mrnumber = f"MR-{uuid.uuid4().hex[:5].upper()}"  # Example: MR-AB12CD34E5
            if not PatientRegister.objects.filter(MRnumber=new_mrnumber).exists():
                return new_mrnumber

   def __str__(self):
        return f"{self.patient_name} - {self.MRnumber}"

    

class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()
    current_date = models.DateTimeField(auto_now_add=True)
    payment_status=models.IntegerField(default=0)
    patient_id=models.ForeignKey(Login,on_delete=models.CASCADE,related_name='patient_login')
    login_id=models.ForeignKey(Login,on_delete=models.CASCADE,related_name='doctor_login')
    cancel_status=models.IntegerField(default=0)
    refund_status=models.IntegerField(default=0)
    prescription=models.CharField(max_length=100)
    prescription_status=models.IntegerField(default=0)
    

class Payment(models.Model):
    card_name=models.CharField(max_length=255)
    card_number=models.IntegerField()
    cvv=models.IntegerField()
    amount=models.IntegerField()
    exp_date = models.CharField(max_length=255)
    current_date = models.DateTimeField(auto_now_add=True)
    current_time = models.DateTimeField(auto_now_add=True)
    app_id=models.ForeignKey('Appointment',on_delete=models.CASCADE)

class AmbulanceRegister(models.Model):
   vehicle_category=models.CharField(max_length=255)
   vehicle_type=models.CharField(max_length=255)
   vehicle_no=models.CharField(max_length=255)
   driver_name=models.CharField(max_length=255)
   driver_contact=models.CharField(max_length=15)
   hosp_id=models.ForeignKey('HospitalRegister',on_delete=models.CASCADE,related_name='hosp_loginid')
   amb_login_id=models.ForeignKey('Login',on_delete=models.CASCADE,related_name='amb_login')

class Location(models.Model):
   latitude = models.FloatField()  # Store the latitude of the selected location
   longitude = models.FloatField() 
   current_date = models.DateTimeField(auto_now_add=True)
   pat_id=models.ForeignKey('PatientRegister',on_delete=models.CASCADE,related_name='pat_loginid',null=True)
   amb_login_id=models.ForeignKey('AmbulanceRegister',on_delete=models.CASCADE,related_name='amb_loginid',null=True)
   def __str__(self):
        return f"Location {self.location} ({self.latitude}, {self.longitude})"
   cancel=models.IntegerField(default=0)
