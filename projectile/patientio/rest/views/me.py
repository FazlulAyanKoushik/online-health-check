from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework import filters

from appointmentio.models import SeekHelp, Medicine

from doctorio.rest.serializers.doctors import MedicineSerializer

from patientio.models import Patient, RelativePatient

from ..permissions import IsPatient
from ..serializers.me import (
    PrivatePatientDetailSerializer,
    PrivateRelativePatientSerializer,
    PrivatePatientSeekHelpSerializer,
)


class PrivatePatientDetail(RetrieveUpdateAPIView):
    queryset = Patient.objects.filter()
    serializer_class = PrivatePatientDetailSerializer
    permission_classes = [IsPatient]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("uid", None)}
        return get_object_or_404(Patient.objects.filter(), **kwargs)


class PrivateRelativePatientList(ListAPIView):
    serializer_class = PrivateRelativePatientSerializer
    permission_classes = [IsPatient]
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "patient_relation"]

    def get_queryset(self):
        patient = get_object_or_404(Patient.objects.filter(), user=self.request.user)

        return RelativePatient.objects.filter(patient=patient)


class PrivateRelativePatientDetail(RetrieveAPIView):
    serializer_class = PrivateRelativePatientSerializer
    permission_classes = [IsPatient]

    def get_object(self):
        patient = get_object_or_404(Patient.objects.filter(), user=self.request.user)
        kwargs = {"patient": patient, "uid": self.kwargs.get("uid")}
        relative = get_object_or_404(RelativePatient.objects.filter(), **kwargs)

        return relative


class PrivatePatientSeekHelpList(ListAPIView):
    serializer_class = PrivatePatientSeekHelpSerializer
    permission_classes = [IsPatient]

    def get_queryset(self):
        return SeekHelp.objects.filter()


class PrivatePatientMedicineList(ListAPIView):
    queryset = Medicine.objects.filter().prefetch_related("ingredient").order_by("name")
    serializer_class = MedicineSerializer
    permission_classes = [IsPatient]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "ingredient__name"]
