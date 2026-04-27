from django.db import models

class Equipment(models.Model):
    CATEGORY_CHOICES = [
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('biology', 'Biology'),
        ('computer', 'Computer'),
        ('geography', 'Geography'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    available = models.IntegerField(default=0)
    free_time = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class EquipmentBooking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Returned', 'Returned')
    ]
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=50)
    roll = models.CharField(max_length=50)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    duration_display = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.name} - {self.equipment.name}"

class LabBooking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]
    teacher_name = models.CharField(max_length=100)
    lab = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.teacher_name} - {self.lab}"
