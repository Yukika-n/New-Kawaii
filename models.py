from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Department(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_parent(self):
        return self.parent

class Position(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Country(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to=r'C:\Users\y0879\venv_employee_master\employee_master\employee\img',
                              default=r'C:\Users\y0879\venv_employee_master\employee_master\employee\default_img\Nishimura.png',
                              null=True, blank=True)
    empcode = models.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(999)],
    )
    name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    start = models.DateField(null=True)
    dob = models.DateField(null=True, blank=True)
    WORKPLACE_CHOICES = (
        ('Tokyo', 'Tokyo',),
        ('Osaka', 'Osaka'),
        ('Nagoya', 'Nagoya'),
        ('Hiroshima', 'Hiroshima'),
    )
    workplace = models.CharField(max_length=100, choices=WORKPLACE_CHOICES)

    def __str__(self):
        return str(self.id)


