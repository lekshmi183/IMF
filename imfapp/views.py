from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from.forms import *
from.models import *
from django.db.models import Q
from django.http import JsonResponse


# Create your views here.
def mainindex(request):
    return render(request,'mainindex.html')
def admin(request):
    return render(request,'admin.html')   

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
                    if user.usertype==1:
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
            a.usertype=3
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
            'hosp_contact':hospital.hosp_contact


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
    appointments = Appointment.objects.filter(login_id=doctor)
    
    for appointment in appointments:
        appointment.patient_register = PatientRegister.objects.get(login_id=appointment.patient_id)  
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