from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('landaddExperiment/', LandAddExperiment.as_view(), name='landaddExperiment'),
    path('landqueryExperimentType/', LandQueryExperimentType.as_view(), name='landqueryExperimentType'),
    path('landqueryExperiment/', LandQueryExperiment.as_view(), name='landqueryExperiment'),
    path('landhostManager/', LandHostManager.as_view(), name='landhostManager'),
    path('landvalidateGenID/', LandValidateGenID.as_view(), name='landvalidateGenID'),
    path('addExperiment/', AddExperiment.as_view(), name='addExperiment'),
    path('queryExperimentType/', QueryExperimentType.as_view(), name='queryExperimentType'),
    path('landnewExperimentType/', LandNewExperimentType.as_view(), name='landnewExperimentType'),
    path('newExperimentType/', NewExperimentType.as_view(), name='newExperimentType'),
    path('queryExperiment/', QueryExperiment.as_view(), name='queryExperiment'),
    path('hostManager/', HostRegister.as_view(), name='hostRegister'),
    # path('validateGenID/', ValidateGenID.as_view(), name='validateGenID')
    # path('addUser/', AddUser.as_view(), name="addUser")
]