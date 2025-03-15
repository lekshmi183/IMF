from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from.forms import *
from.models import *
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def mainindex(request):
    return render(request,'mainindex.html')

def admin(request):
    a=HospitalRegister.objects.count()
    print(a)
    b=PatientRegister.objects.count()
    print(b)
    c=DoctorRegister.objects.count()
    print(c)
    d=AmbulanceRegister.objects.count()
    print(d)
    return render(request,'admin.html',{'a':a ,'b':b,'c':c, 'd':d})   

def hosp_reg(request):
    if request.method == 'POST':
        form=hosp_form(request.POST)
        login=login_form(request.POST)
        if form.is_valid() and login.is_valid():
            a=login.save(commit=False)
            a.usertype=1
            a.save()
            b=form.save(commit=False)
            b.login_id=a
            b.latitude = request.POST.get('latitude', '')  # Get latitude from form
            b.longitude = request.POST.get('longitude', '')  
            b.save()
            messages.success(request,"Form succesfully submitted")
            return redirect('mainindex')
    else:
        form=hosp_form()
        login=login_form()
    return render(request,'hospitalreg.html',{'form':form,'login':login})


def hosphome(request):
    return render(request,'hosphome.html')

def loginprocess(request):
    if request.method == 'POST':
        form=logincheck(request.POST)
        if form.is_valid():
            print('hi1')
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            try:
                user=Login.objects.get(email=email)
                if user.password==password:
                    if user.usertype==1 and user.login_status==1:
                        request.session['hosp_id']=user.id
                        return redirect('hosphome')
                    
                    elif user.usertype==2:
                        request.session['doc_id']=user.id
                        return redirect('dochome')
                    elif user.usertype==3:
                        request.session['patient_id']=user.id
                        return redirect('patienthome')
                    elif user.usertype==4:
                        request.session['amb_id']=user.id
                        return redirect('ambhome')
                    elif user.usertype==0:
                        request.session['admin_id']=user.id
                        return redirect('admin')
                else:
                    messages.error(request,'invalid password')    
            except Login.DoesNotExist:
                messages.error(request,'User Does Not Exist')
    else:
        form=logincheck()   
    return render(request,'login.html',{'form':form})

def doc_reg(request):
    id=request.session.get('hosp_id')
    hid=get_object_or_404(Login,id=id)
    print(id)
    if request.method == 'POST':
        form = doc_form(request.POST,request.FILES)
        login = login_form(request.POST)

        
        if form.is_valid() and login.is_valid():
            try:
                a = login.save(commit=False)
                a.usertype = 2
                a.save()
                
                b = form.save(commit=False)
                b.login_id = a
                b.hosp_id=hid
                b.save()
                messages.success(request, "Form successfully submitted")
                return redirect('hosphome')
            except Exception as e:
                messages.error(request, f"Error occurred: {str(e)}")
                # Optionally log the exception as well for debugging
        else:
            messages.error(request, "There were errors in the form. Please check and try again.")
    else:
        form = doc_form()
        login = login_form()
    
    return render(request, 'docreg.html', {'form': form, 'login': login})

def view_doc(request):
    id=request.session.get('hosp_id')
    hid=get_object_or_404(Login,id=id)
    doc_id=DoctorRegister.objects.filter(hosp_id=hid)
    return render(request,'viewdoc.html',{'data':doc_id})

def adminhospview(request):
    view_id=HospitalRegister.objects.all()
    return render(request,'adminhospview.html',{'data':view_id})

def admindocview(request):
    view_doc_id=DoctorRegister.objects.all()
    return render(request,'admindocview.html',{'data':view_doc_id})           

def patient_reg(request):
    if request.method == 'POST':
        form=patient_form(request.POST)
        login=login_form(request.POST)
        if form.is_valid() and login.is_valid():
            a=login.save(commit=False)
            a.usertype=1
            a.save()
            b=form.save(commit=False)
            b.login_id=a
            b.save()
            messages.success(request,"Form succesfully submitted")
            return redirect('patienthome')
    else:
        form=patient_form()
        login=login_form()
    return render(request,'patientregister.html',{'form':form,'login':login})

def patienthome(request):
    return render(request,'patienthome.html')

def dochome(request):
    return render(request,'dochome.html')
 
def adminpatientview(request):
    view_id=PatientRegister.objects.all()
    return render(request,'adminpatview.html',{'data':view_id}) 

def hospprofedit(request):
    userid=request.session.get('hosp_id')
    login=get_object_or_404(Login,id=userid)
    hosp_data=get_object_or_404(HospitalRegister,login_id=userid)
    if request.method=='POST': 
        form1=hosp_form(request.POST,instance=hosp_data)
        form2=login_form(request.POST,instance=login)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('hosphome')
    else:
        form1=hosp_form(instance=hosp_data)
        form2=login_form(instance=login)
    return render(request,'hospprofedit.html',{'form':form1,'login':form2})

def docprofedit(request):
    userid=request.session.get('doc_id')
    login=get_object_or_404(Login,id=userid)
    doc_data=get_object_or_404(DoctorRegister,login_id=userid)
    if request.method=='POST': 
        form1=doc_form(request.POST,instance=doc_data)
        form2=login_form(request.POST,instance=login)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('dochome')
    else:
        form1=doc_form(instance=doc_data)
        form2=login_form(instance=login)
    return render(request,'docprofedit.html',{'form':form1,'login':form2})
 
def patientprofedit(request):
    userid=request.session.get('patient_id')
    login=get_object_or_404(Login,id=userid)
    patient_data=get_object_or_404(PatientRegister,login_id=userid)
    if request.method=='POST': 
        form1=patient_form(request.POST,instance=patient_data)
        form2=login_form(request.POST,instance=login)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('patienthome')
    else:
        form1=patient_form(instance=patient_data)
        form2=login_form(instance=login)
    return render(request,'patientprofedit.html',{'form':form1,'login':form2})   

def search(request):
    data = request.GET.get('search', '')
    result = []
    if data:
        hospitals = HospitalRegister.objects.filter(
            Q(hosp_name__icontains=data) |
            Q(hosp_city__icontains=data) |
            Q(hosp_district__icontains=data)
        )
        # Prepare the data in a format that can be used by JavaScript
        result = [{
            'hosp_name': hospital.hosp_name,
            'hosp_city': hospital.hosp_city,
            'hosp_district': hospital.hosp_district,
            'hosp_state': hospital.hosp_state,  
            'hosp_address': hospital.hosp_address,
            'hosp_contact':hospital.hosp_contact,
            'hosp_id':hospital.id,



        } for hospital in hospitals]

    # Return the result as JSON
    return JsonResponse({'results': result})
def dept(request):
    return render(request,'dept.html')

def search_Department(request):
    query = request.GET.get('q', '') 
    results = DoctorRegister.objects.all()  

    if query:
        results = results.filter(
            Q(department__icontains=query)  
        )

    return render(request, 'departmentsearch.html', {'results': results, 'query': query})

def appointment(request,login_id,amount):
    patient=request.session.get('patient_id')
    login=get_object_or_404(Login,id=patient)
    amt=int(amount)
    doctor=get_object_or_404(DoctorRegister,login_id__id=login_id)
    if request.method=='POST':
        form=appointment_form(request.POST)
        if form.is_valid():
            p=form.save(commit=False)
            p.patient_id=login
            p.login_id=doctor.login_id
            p.save()
            return redirect('payment',p.id,amt)
    else:
        form=appointment_form()
    return render(request,'appointment.html',{'form':form,'amt':amt})
    
def viewappointment(request):
    doctor_id = request.session.get('doc_id')
    doctor = get_object_or_404(Login, id=doctor_id) 
    fee=get_object_or_404(DoctorRegister, login_id=doctor_id)
    print(fee)
    appointments = Appointment.objects.filter(login_id=doctor,payment_status=1)
    
    for appointment in appointments:
        try:
            appointment.patient_register = PatientRegister.objects.get(login_id=appointment.patient_id)
        except PatientRegister.DoesNotExist:
            appointment.patient_register = None    
        return render(request, 'viewappointment.html', {'appointments': appointments,'fee':fee})

def viewapp(request):
    patient_id = request.session.get('patient_id')
    patient = get_object_or_404(Login, id=patient_id)   
    appointments = Appointment.objects.filter(patient_id=patient)
    for appointment in appointments:
        appointment.doctor_register = DoctorRegister.objects.get(login_id=appointment.login_id)  
    return render(request, 'viewapp.html', {'appointments': appointments})


def editviewapp(request, id):
    patient_id = request.session.get('patient_id')
    login = get_object_or_404(Login, id=patient_id)
    appointment = get_object_or_404(Appointment, id=id, patient_id=login)

    if request.method == 'POST':
        form = appointment_form(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('viewapp')
    else:
        form = appointment_form(instance=appointment)

    return render(request, 'editviewapp.html', {'form': form})


def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.delete()
    return redirect('viewapp') 

def consultation_fee(request,id):
    doctor=get_object_or_404(DoctorRegister,id=id)
    if request.method=='POST': 
        form1=consult_form(request.POST)
        if form1.is_valid():
            a=form1.cleaned_data['consultation_fee']
            doctor.consultation_fee=a
            doctor.save()
            return redirect('view_doc')
    else:
        form1=consult_form()
    return render(request,'consultation_fee.html',{'form':form1})

def payment(request,id,amount):
    am=int(amount)
    print(am)
    appid = get_object_or_404(Appointment,id = id)
    if request.method=='POST': 
        form1=payment_form(request.POST)
        print(form1)
        if form1.is_valid():
            a=form1.save(commit=False)
            a.amount=am
            a.app_id=appid
            a.save()
            appid.payment_status=1
            appid.save()
            return redirect('viewapp')

    else:
        form1=payment_form()
    return render(request,'payment.html',{'form': form1})

def appointment_cancel(request,id):
     appid = get_object_or_404(Appointment,id = id)
     appid.cancel_status=1
     appid.save()
     return redirect('viewapp')
def refund(request,id,amount):
    am=int(amount)
    print(am)
    appid = get_object_or_404(Appointment,id = id)
    if request.method=='POST': 
        form1=refund_form(request.POST)
        print(form1)
        if form1.is_valid():
            a=form1.save(commit=False)
            a.amount=am
            a.app_id=appid
            a.save()
            appid.refund_status=1
            appid.save()
            return redirect('viewappointment')

    else:
        form1=refund_form()
    return render(request,'refund.html',{'form': form1})        
def amb_reg(request):
    id=request.session.get('hosp_id')
    hid=get_object_or_404(Login,id=id)
    if request.method == 'POST':
        form = amb_form(request.POST)
        login = login_form(request.POST)
        
        if form.is_valid() and login.is_valid():
            try:
                a = login.save(commit=False)
                a.usertype = 4
                a.save()
                
                b = form.save(commit=False)
                b.amb_login_id = a
                b.hosp_id=hid
                b.save()
                
                messages.success(request, "Form successfully submitted")
                return redirect('hosphome')
            except Exception as e:
                messages.error(request, f"Error occurred: {str(e)}")
        else:
            messages.error(request, "There were errors in the form. Please check and try again.")
    else:
        form = amb_form()
        login = login_form()
    
    return render(request, 'ambreg.html', {'form': form, 'login': login})

def ambhome(request):
    return render(request,'ambhome.html')

def view_amb(request):
    id=request.session.get('hosp_id')
    hid=get_object_or_404(Login,id=id)
    amb_id=AmbulanceRegister.objects.filter(hosp_id=hid)
    return render(request,'viewamb.html',{'data':amb_id})

def ambprof(request):
   userid=request.session.get('amb_id')
   login=get_object_or_404(Login,id=userid)
   amb_data=get_object_or_404(AmbulanceRegister,amb_login_id=userid)
   if request.method=='POST':
        form1=amb_form(request.POST,instance=amb_data)
        form2=login_form(request.POST,instance=login)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('ambhome')
   else:
        form1=amb_form(instance=amb_data)
        form2=login_form(instance=login)
   return render(request,'ambprof.html',{'form':form1,'login':form2})

def ambprofedit(request,id):
   
   amb_data=get_object_or_404(AmbulanceRegister,amb_login_id=id)
   if request.method=='POST':
        form1=amb_form(request.POST,instance=amb_data)
        form2=amb_login_form(request.POST,instance=amb_data.amb_login_id)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('view_amb')
   else:
        form1=amb_form(instance=amb_data)
        form2=amb_login_form(instance=amb_data.amb_login_id)
   return render(request,'ambprofedit.html',{'form':form1,'login':form2})
    
def delete_ambulance(request, id):
    ambulance = get_object_or_404(AmbulanceRegister, id=id)
    ambulance.delete()
    return redirect('view_amb') 

def viewtransferpatients(request):
    view_id=PatientRegister.objects.all()
    return render(request,'viewtransferpatients.html',{'data':view_id}) 

# def viewambdata(request,id):
#     pat_id=get_object_or_404(PatientRegister,id=id)
#     hosp_id=request.session.get('hosp_id')
#     hid=get_object_or_404(Login,id=hosp_id)
#     amb_id=AmbulanceRegister.objects.filter(hosp_id=hid)
#     a=[]
#     for b in amb_id:
#         a=Location.objects.filter(amb_login_id= b.id,complete_status=0)
#         print(a)
#     return render(request,'viewambdata.html',{'data':amb_id,'patient':pat_id})

def viewambdata(request, id):
    pat_id = get_object_or_404(PatientRegister, id=id)
    hosp_id = request.session.get('hosp_id')
    hid = get_object_or_404(Login, id=hosp_id)

    # Fetch ambulances from the logged-in hospital
    ambulances = AmbulanceRegister.objects.filter(hosp_id=hid)

    # Filter out ambulances that already have a location record with complete_status = 0
    # These ambulances should not be shown
    ambulances_to_display = []

    for ambulance in ambulances:
        # Check if the ambulance has a location with complete_status=0
        location = Location.objects.filter(amb_login_id=ambulance, complete_status=1).first()
        if not location:  # If no such location exists, show the ambulance
            ambulances_to_display.append(ambulance)
    
    return render(request, 'viewambdata.html', {'data': ambulances_to_display, 'patient': pat_id})

# # def location(request):
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
# def save_location(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         ambulance_id = data.get('ambulanceId')
#         latitude = data.get('latitude')
#         longitude = data.get('longitude')

#         # Optionally, you can use reverse geocoding to get the location name based on the coordinates
#         # (Here, we assume you already know the location or will retrieve it from a service)

#         location_name = "Some Address"  # You can either get this from the map click, or use a geocoding service

#         # Save the new Location
#         location = Location(
#             location=location_name,
#             latitude=latitude,
#             longitude=longitude,
#             amb_login_id_id=ambulance_id  # Link the ambulance driver via the ForeignKey
#         )
#         location.save()

#         return JsonResponse({"status": "success"})
#     return JsonResponse({"status": "error"}, status=400)
@csrf_exempt
def save_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        latitude = data.get('latitude')
        longitude = data.get('longitude')
        patid= data.get('patid')
        ambid= data.get('ambid')
        p=get_object_or_404(PatientRegister,id=patid)
        amb=get_object_or_404(AmbulanceRegister,id=ambid)

        if not all([latitude, longitude,patid,ambid]):
            return JsonResponse({"status": "error", "message": "Missing required fields"}, status=400)

        # Create and save the Location instance
        location = Location(
            latitude=latitude,
            longitude=longitude,
            pat_id=p,
            amb_login_id=amb,
            complete_status=1

        )
        location.save()

        return JsonResponse({"status": "success"})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


def view_location(request):
    # Retrieve all locations from the database (you may filter based on some condition)
    locations = Location.objects.all()  # You can filter for specific location if needed

    # Send the locations (latitude and longitude) to the template
    return render(request, 'map.html', {'locations': locations})

def viewtransferedpatients(request):
    amb_id=request.session.get('amb_id')
    hid=get_object_or_404(AmbulanceRegister,amb_login_id=amb_id)
    am_id=Location.objects.filter(amb_login_id=hid)
    return render(request,'viewtransferedpatients.html',{'data':am_id})

def add_prescription(request,id):
    appid = get_object_or_404(Appointment,id=id)
    if request.method=='POST': 
        form1=prescription_form(request.POST)
        print(form1)
        if form1.is_valid():
            b=form1.cleaned_data['prescription']
            # a=form1.save(commit=False)
            appid.prescription=b 
            appid.prescription_status=1
            appid.save()
            return redirect('viewappointment')

    else:
        form1=prescription_form()
    return render(request,'addprescription.html',{'form': form1})   

def editprescription(request,id):

    appid = get_object_or_404(Appointment, id=id )

    if request.method == 'POST':
        form1= prescription_form(request.POST, instance=appid)
        if form1.is_valid():
            form1.save()
            return redirect('viewappointment')
    else:
        form1= prescription_form(instance=appid)
    
    return render(request,'editprescription.html',{'form': form1})


def delete_prescription(request,id):
    prescription = get_object_or_404(Appointment,id=id)
    prescription.prescription='no prescription'
    prescription.save()
    return redirect('viewappointment') 

def viewhosptransfer(request):
    hosp_id = request.session.get('hosp_id')
    print(hosp_id)
    hid = get_object_or_404(Login, id=hosp_id)
    am_id = Location.objects.filter(amb_login_id__hosp_id=hid)

    query = request.GET.get('q', '')

    if query:
        am_id = am_id.filter(pat_id__MRnumber__icontains=query)

    return render(request, 'viewhosptransfer.html', {'data': am_id, 'query': query})

def cancel(request, id):
    location = get_object_or_404(Location, id=id)
    if location.cancel != 1:
        location.cancel = 1
        location.save()
    return redirect('viewhosptransfer')

def approve(request,id):
    a=get_object_or_404(Login,id=id)
    a.login_status=1
    a.save()
    return redirect('adminhospview')

def reject(request,id):
    a=get_object_or_404(Login,id=id)
    a.login_status=2
    a.save()
    return redirect('adminhospview')


def viewpatientdata(request):
    hosp_id = request.session.get('hosp_id')
    hid = get_object_or_404(HospitalRegister, login_id=hosp_id)
    pat_data = PatientRegister.objects.all()
    query = request.GET.get('q', '')
    if query:
        pat_data = PatientRegister.objects.filter(MRnumber__icontains=query)
    return render(request, 'viewpatientdata.html', {'data': pat_data, 'query': query})


# def viewhospdata(request, id):
#     hosp_id = request.session.get('hosp_id')
#     pat_id = get_object_or_404(PatientRegister, id=id)
#     hid = get_object_or_404(HospitalRegister, login_id=hosp_id)
#     hosp_data = HospitalRegister.objects.all()
#     query = request.GET.get('q', '')
#     if query:
#         hosp_data = hosp_data.filter(hosp_name__icontains=query)
#         hosp_data = hosp_data.exclude(id=hid.id)
#     return render(request, 'viewhospdata.html', {'data': hosp_data, 'query': query, 'patient': pat_id})
# def viewhospdata(request, id):
#     hosp_id = request.session.get('hosp_id')
#     pat_id = get_object_or_404(PatientRegister, id=id)
#     hid = get_object_or_404(HospitalRegister, login_id=hosp_id)
#     hosp_data = HospitalRegister.objects.all()
#     query = request.GET.get('q', '')
#     if query:
#         hosp_data = hosp_data.filter(hosp_name__icontains=query)
#         hosp_data = hosp_data.exclude(id=hid.id)
#     return render(request, 'viewhospdata.html', {'data': hosp_data, 'query': query, 'patient': pat_id})
def viewhospdata(request, id):
    hosp_id = request.session.get('hosp_id')
    pat_id = get_object_or_404(PatientRegister, id=id)
    hid = get_object_or_404(HospitalRegister, login_id=hosp_id)
    
    hosp_data = HospitalRegister.objects.exclude(id=hid.id)
    
    query = request.GET.get('q', '')
    if query:
        hosp_data = hosp_data.filter(hosp_name__icontains=query)
    
    return render(request, 'viewhospdata.html', {'data': hosp_data, 'query': query, 'patient': pat_id})


def transfer_store(request, hid, pat_id):
    pat_id = get_object_or_404(PatientRegister, id=pat_id)
    hid = get_object_or_404(HospitalRegister, id=hid)
    hosp_id = request.session.get('hosp_id')
    hid2 = get_object_or_404(HospitalRegister, login_id=hosp_id)
    
    Transfer.objects.create(
        from_hosp_id=hid2,
        to_hosp_id=hid,
        pat_id=pat_id
    )
    
    return redirect('hosphome')

def add_notification(request):
    hosp_id=request.session.get('hosp_id')
    login_details = get_object_or_404(HospitalRegister, login_id=hosp_id)
    if request.method=='POST': 
        form1=notification_form(request.POST)
        print(form1)
        if form1.is_valid():
            b=form1.save(commit=False)
            b.hosp_id=login_details
            b.save()
            return redirect('hosphome')

    else:
        form1=notification_form()
    return render(request,'notification.html',{'form': form1}) 

def view_notification(request):
    hosp_id=request.session.get('hosp_id')
    nid=get_object_or_404(HospitalRegister,id=hosp_id)
    notification_id=Notification.objects.filter(hosp_id=nid)
    return render(request,'viewnotification.html',{'data':notification_id})

def viewtransferdetails(request):
    hosp_id = request.session.get('hosp_id')
    hid=get_object_or_404(HospitalRegister,id=hosp_id)
    data_id=Transfer.objects.filter(to_hosp_id=hid)
    return render(request,'viewtransferdetails.html',{'data':data_id})

# def viewrecords(request):
#     hosp_id=request.session.get('hosp_id')
#     rid=get_object_or_404(HospitalRegister,id=hosp_id)
#     hid=get_object_or_404(HospitalRegister,login_id_id=hosp_id)
#     data_id=Transfer.objects.filter(to_hosp_id=hid.id)
#     return render(request,'viewtransferdetails.html',{'data':data_id})

def viewrecords(request,id):
    pat_id =  get_object_or_404(PatientRegister,id=id)
    appointments = Appointment.objects.filter(patient_id=pat_id.login_id).select_related('login_id__login_id')
    return render(request, 'viewrecords.html', {'doctor_details': appointments})

def vidconference(request,id):
    sid=get_object_or_404(Appointment,id=id)
    return render(request,'vidconference.html',{'form':sid})   

    
@csrf_exempt  
def save_appointment_url(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')

        if url:
            appointment = get_object_or_404(Appointment, id=id)
            
            appointment.url = url
            
            appointment.save()

            return JsonResponse({'success': True, 'message': 'URL saved successfully'})

        return JsonResponse({'success': False, 'message': 'No URL provided'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

# def viewrecords(request,id):
#     pat_id =  get_object_or_404(PatientRegister,login_id=id)
#     appointments = Appointment.objects.filter(patient_id=pat_id.login_id).select_related('login_id__login_id')
#     return render(request, 'viewrecords.html', {'doctor_details': appointments})

# def emerencynotify(request):
#     hosp_id = request.session.get('hosp_id')g
#     print(hosp_id)
#     pat_id =  get_object_or_404(PatientRegister,login_id=id)
#     hid = get_object_or_404(Login, id=hosp_id)
#     am_id = Location.objects.filter(amb_login_id__hosp_id=hid)

#     query = request.GET.get('q', '')

#     if query:
#         am_id = am_id.filter(pat_id__MRnumber__icontains=query)

#     return render(request, 'viewhosptransfer.html', {'data': am_id, 'query': query})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import EmergencyNotify, HospitalRegister
from django.contrib.auth.models import User
import json

# def track_location(request, hospital_id):
#     if request.method == 'POST':
#         try:
#             # Get the hospital and patient from the database
#             hospital = get_object_or_404(HospitalRegister, id=hospital_id)

#             # Assuming the patient is the logged-in user, you can adjust as per your application logic
#             patient = request.session.get('patient_id')  # Adjust this based on how your system identifies patients

#             # Parse the latitude and longitude from the request body
#             data = json.loads(request.body)
#             latitude = data.get('latitude')
#             longitude = data.get('longitude')

#             # Create a new EmergencyNotify record
#             emergency_notify = EmergencyNotify(
#                 hosp_id=hospital,
#                 pat_id=patient,
#                 latitude=latitude,
#                 longitude=longitude
#             )
#             emergency_notify.save()

#             return JsonResponse({'status': 'success', 'message': 'Location saved successfully.'})

#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})

#     return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import EmergencyNotify, HospitalRegister
from django.contrib.auth.models import User
import json

def track_location(request, hospital_id):
    if request.method == 'POST':
        try:
            # Get the hospital using the hospital_id from the URL
            hospital = get_object_or_404(HospitalRegister, id=hospital_id)

            # Assuming the patient is the logged-in user, adjust if needed based on how you manage patients
            patient = request.session.get('patient_id')  # If PatientRegister is linked to the User model
            
            if not patient:
                return JsonResponse({'status': 'error', 'message': 'Patient not found.'})
            
            # Parse the latitude and longitude from the request body
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if latitude is None or longitude is None:
                return JsonResponse({'status': 'error', 'message': 'Latitude and longitude are required.'})

            # Create a new EmergencyNotify record
            emergency_notify = EmergencyNotify(
                hosp_id=hospital,
                pat_id=patient,
                latitude=latitude,
                longitude=longitude
            )
            emergency_notify.save()

            return JsonResponse({'status': 'success', 'message': 'Location saved successfully.'})

        except Exception as e:
            # Log the exception for debugging
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import PatientRegister, HospitalRegister, EmergencyNotify

@csrf_exempt
def store_location(request):
    pat = request.session.get('patient_id')
    
    if request.method == "POST":
        try:
            raw_body = request.body.decode("utf-8")  # Decode body to string
            print("Received JSON:", raw_body)  # Debugging log
            
            data = json.loads(raw_body)
            hosp_id = data.get("hosp_id")
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if not all([hosp_id, latitude, longitude]):  # Ensure data is present
                return JsonResponse({"success": False, "error": "Missing required data"}, status=400)

            # Get the logged-in patient
            patient = get_object_or_404(PatientRegister, login_id=pat)
            print(patient)

            # Get the hospital instance
            hospital = get_object_or_404(HospitalRegister, id=hosp_id)

            # Save location to the database
            EmergencyNotify.objects.create(
                hosp_id=hospital,
                pat_id=patient,
                latitude=latitude,
                longitude=longitude
            )

            return JsonResponse({"success": True, "message": "Location stored successfully!"})
        
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def viewalert(request):
    hosp_id=request.session.get('hosp_id')
    hid = get_object_or_404(HospitalRegister,login_id=hosp_id)
    alert_id=EmergencyNotify.objects.filter(hosp_id=hid)
    return render(request,'viewalert.html',{'data':alert_id})


def upload(request):
    if request.method == 'POST':
        form = upload_form(request.POST, request.FILES)  
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            
            with open(f"some_path/{uploaded_file.name}", 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            
            return render(request, 'upload.html', {'form': form, 'message': 'File uploaded successfully!'})
    else:
        form = upload_form()  

    return render(request, 'upload.html', {'form': form})
def complete_status(request,id):
    appid = get_object_or_404(Location,id = id)
    appid.complete_status=0
    appid.save()
    return redirect('viewtransferedpatients')

def feedback(request):
    pat_id=request.session.get('patient_id')
    login_details = get_object_or_404(PatientRegister, login_id=pat_id)
    if request.method=='POST': 
        form1=feedback_form(request.POST)
        print(form1)
        if form1.is_valid():
            b=form1.save(commit=False)
            b.pat_id=login_details
            b.save()
            return redirect('patienthome')

    else:
        form1=feedback_form()
    return render(request,'feedback.html',{'form': form1})

def adminfeedbackview(request):
    view_id=Feedback.objects.all()
    return render(request,'adminfeedbackview.html',{'data':view_id})

def reply(request,id):
    feedback_details = get_object_or_404(Feedback,id=id)
    reply=request.POST.get('reply')
    if reply is not None:
        feedback_details.reply=reply
        feedback_details.save()
        return redirect('adminfeedbackview')
    else:
        return render(request,'reply.html')
    
def viewfeedback(request):
    id=request.session.get('patient_id')
    hid=get_object_or_404(PatientRegister,login_id=id)
    feed_id=Feedback.objects.filter(pat_id=hid)
    print(feed_id)
    return render(request,'viewfeedback.html',{'data':feed_id})

def editfeedback(request, id):
    pat_id = request.session.get('patient_id')
    login = get_object_or_404(PatientRegister, login_id=pat_id)
    feedback = get_object_or_404(Feedback, id=id, pat_id=login)

    if request.method == 'POST':
        form = feedback_form(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('viewfeedback')
    else:
        form = feedback_form(instance=feedback)

    return render(request, 'editfeedback.html', {'form': form})


def deletefeedback(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    feedback.delete()
    return redirect('viewfeedback')

