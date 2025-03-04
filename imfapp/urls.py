from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
     path('',views.mainindex,name='mainindex'),
     path('admin',views.admin,name='admin'),
     path('login',views.loginprocess,name='login'),
     path('hosphome',views.hosphome,name='hosphome'),
     path('hosp_reg',views.hosp_reg,name='hosp_reg'),
     path('doc_reg',views.doc_reg,name='doc_reg'),
     path('view_doc',views.view_doc,name='view_doc'),
     path('adminhospview',views.adminhospview,name='adminhospview'),
     path('admindocview',views.admindocview,name='admindocview'),
     path('patient_reg',views.patient_reg,name='patient_reg'),
     path('patienthome',views.patienthome,name='patienthome'),
     path('docphome',views.dochome,name='dochome'),
     path('adminpatientview',views.adminpatientview,name='adminpatientview'),
     path('hospprofedit',views.hospprofedit,name='hospprofedit'),
     path('docprofedit',views.docprofedit,name='docprofedit'),
     path('patientprofedit',views.patientprofedit,name='patientprofedit'),
     path('search',views.search,name='search'),
     path('dept',views.dept,name='dept'),
     path('departmentsearch',views.search_Department,name='departmentsearch'),
     path('appointment/<int:login_id>/<int:amount>/',views.appointment,name='appointment'),
     path('viewappointment', views.viewappointment, name='viewappointment'),
     path('viewapp', views.viewapp, name='viewapp'),
     path('editviewapp/<int:id>/', views.editviewapp, name='editviewapp'),
     path('delete_appointment/<int:id>/', views.delete_appointment, name='delete_appointment'), 
     path('consultation_fee/<int:id>/', views.consultation_fee, name='consultation_fee'), 
     path('payment/<int:id>/<int:amount>/', views.payment, name='payment'),
     path('appointment_cancel/<int:id>/', views.appointment_cancel, name='appointment_cancel'), 
     path('amb_reg',views.amb_reg,name='amb_reg'),
     path('ambhome',views.ambhome,name='ambhome'),
     path('view_amb',views.view_amb,name='view_amb'),
     path('ambprof',views.ambprof,name='ambprof'),
     path('ambprofedit/<int:id>/',views.ambprofedit,name='ambprofedit'),
     path('delete_ambulance/<int:id>/', views.delete_ambulance, name='delete_ambulance'),
     path('refund/<int:id>/<int:amount>/', views.refund, name='refund'),



]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

