from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Equipment, EquipmentBooking, LabBooking
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        login_type = request.POST.get('login_type')
        if login_type == 'admin':
            u = request.POST.get('admin_user')
            p = request.POST.get('admin_pass')
            if u == 'admin' and p == 'admin':
                return redirect('dashboard')
            else:
                from django.contrib import messages
                messages.error(request, "🛑 Access Denied: This portal is strictly for Laboratory Administrators. Students are not permitted here.")
                return redirect('login')
        else:
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    return redirect('login')

def home(request):
    category = request.GET.get('category')
    q = request.GET.get('q', '')
    data = Equipment.objects.all().order_by('name')
    if category:
        data = data.filter(category=category)
    if q:
        data = data.filter(name__icontains=q)
        
    paginator = Paginator(data, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'home.html', {'page_obj': page_obj, 'q': q, 'category': category})

def history(request):
    bookings_list = EquipmentBooking.objects.all().order_by('-id')
    paginator = Paginator(bookings_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'history.html', {'page_obj': page_obj})

def book_lab(request):
    if request.method == "POST":
        teacher_name = request.POST.get('teacher_name')
        lab = request.POST.get('lab')
        date = request.POST.get('date')
        time = request.POST.get('time')
        duration = request.POST.get('duration')
        
        LabBooking.objects.create(
            teacher_name=teacher_name,
            lab=lab.capitalize() + " Lab" if lab else "",
            date=date,
            time=time,
            duration=duration,
            status='Pending'
        )
        return redirect('lab_success')
        
    return render(request, 'book_lab.html')

def book_equipment(request, id):
    item = get_object_or_404(Equipment, id=id)
    
    if request.method == "POST":
        name = request.POST.get('name')
        student_class = request.POST.get('student_class')
        roll = request.POST.get('roll')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        duration = request.POST.get('duration')
        quantity = int(request.POST.get('quantity', 1))
        purpose = request.POST.get('purpose')
        
        if quantity > item.available:
            messages.error(request, f"Sorry, only {item.available} units of {item.name} are available.")
            return render(request, 'book.html', {'item': item})
        
        EquipmentBooking.objects.create(
            name=name,
            student_class=student_class,
            roll=roll,
            equipment=item,
            booking_date=booking_date,
            booking_time=booking_time,
            duration_display=f"{duration} minutes",
            quantity=quantity,
            purpose=purpose,
            status='Pending'
        )
        return redirect('success')
        
    return render(request, 'book.html', {'item': item})

def success(request):
    booking = EquipmentBooking.objects.last()
    return render(request, 'success.html', {'booking': booking})

def lab_success(request):
    booking = LabBooking.objects.last()
    return render(request, 'lab_success.html', {'booking': booking})

def dashboard(request):
    pending_equipment = EquipmentBooking.objects.filter(status='Pending').order_by('-id')
    pending_lab = LabBooking.objects.filter(status='Pending').order_by('-id')
    active_equipment = EquipmentBooking.objects.filter(status='Approved').order_by('-id')
    
    stats = {
        'total_equipment_pending': pending_equipment.count(),
        'total_lab_pending': pending_lab.count(),
        'total_active': active_equipment.count(),
    }
    
    return render(request, 'dashboard.html', {
        'pending_equipment': pending_equipment,
        'pending_lab': pending_lab,
        'active_equipment': active_equipment,
        'stats': stats
    })

def approve_booking(request, stype, id):
    if stype == 'equipment':
        booking = get_object_or_404(EquipmentBooking, id=id)
        if booking.status == 'Pending':
            booking.status = 'Approved'
            booking.equipment.available -= booking.quantity
            booking.equipment.save()
            booking.save()
            messages.success(request, f"Approved equipment booking for {booking.name}")
    elif stype == 'lab':
        booking = get_object_or_404(LabBooking, id=id)
        if booking.status == 'Pending':
            booking.status = 'Approved'
            booking.save()
            messages.success(request, f"Approved lab booking for {booking.teacher_name}")
    return redirect('dashboard')

def reject_booking(request, stype, id):
    if stype == 'equipment':
        booking = get_object_or_404(EquipmentBooking, id=id)
        booking.status = 'Rejected'
        booking.save()
        messages.info(request, f"Rejected equipment booking for {booking.name}")
    elif stype == 'lab':
        booking = get_object_or_404(LabBooking, id=id)
        booking.status = 'Rejected'
        booking.save()
        messages.info(request, f"Rejected lab booking for {booking.teacher_name}")
    return redirect('dashboard')

def return_equipment(request, id):
    booking = get_object_or_404(EquipmentBooking, id=id)
    if booking.status == 'Approved':
        booking.status = 'Returned'
        booking.equipment.available += booking.quantity
        booking.equipment.save()
        booking.save()
        messages.success(request, f"Marked {booking.equipment.name} as returned.")
    return redirect('dashboard')

def calendar_view(request):
    lab_bookings = LabBooking.objects.filter(status='Approved')
    eq_bookings = EquipmentBooking.objects.filter(status='Approved')
    events = []
    
    for lb in lab_bookings:
        start_dt = f"{lb.date}T{lb.time}"
        events.append({
            'title': f"{lb.lab} - {lb.teacher_name}",
            'start': start_dt,
            'color': '#22c55e'
        })
        
    for eb in eq_bookings:
        start_dt = f"{eb.booking_date}T{eb.booking_time}"
        events.append({
            'title': f"{eb.equipment.name} ({eb.quantity}) - {eb.name}",
            'start': start_dt,
            'color': '#3b82f6'
        })
        
    events_json = json.dumps(events)
    return render(request, 'calendar.html', {'events_json': events_json})