from django.contrib import admin
from .models import Equipment, EquipmentBooking, LabBooking

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'available', 'free_time')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(EquipmentBooking)
class EquipmentBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment', 'student_class', 'booking_date', 'booking_time')
    list_filter = ('booking_date', 'equipment__category')
    search_fields = ('name', 'roll', 'equipment__name')

@admin.register(LabBooking)
class LabBookingAdmin(admin.ModelAdmin):
    list_display = ('teacher_name', 'lab', 'date', 'time', 'duration')
    list_filter = ('date', 'lab')
    search_fields = ('teacher_name', 'lab')
