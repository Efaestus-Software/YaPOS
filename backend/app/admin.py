from django.contrib import admin
from django.apps import apps
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
    
admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)