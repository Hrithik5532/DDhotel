from django.urls import path
from .views import contact_us,reservation,review
urlpatterns = [
    path('contact-us',contact_us,name="contact_us"),
    path('make-reservation',reservation,name="reservation"),
    path('Review-us',review,name="review")
]