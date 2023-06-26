from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

admin.site.register(Usuario, UserAdmin)
admin.site.register(Frota)
admin.site.register(Colaboradores)
admin.site.register(Escala)
admin.site.register(Remessa)
# Register your models here.
