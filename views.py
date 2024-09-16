import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from django.db.models import Q, Count
from .models import Employee, Department, Position, Country
from .forms import EmployeeForm, DepartmentForm, PositionForm, CountryForm

class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = Employee.objects.all()
        context['positions'] = Position.objects.all()
        context['departments'] = Department.objects.exclude(parent=None)
        context['total_employees'] = Employee.objects.count()
        return context

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            empcode = form.cleaned_data['empcode']
            name = form.cleaned_data['name']
            department = form.cleaned_data['department']  # もし部署が必要ならここに追加
            position = form.cleaned_data['position']
            gender = form.cleaned_data['gender']
            country = form.cleaned_data['country']
            email = form.cleaned_data['email']
            start = form.cleaned_data['start']
            dob = form.cleaned_data['dob']
            workplace= form.cleaned_data['workplace']


            # 手動でモデルを作成し、保存する
            Employee.objects.create(
                image=image,
                empcode=empcode,
                name=name,
                department=department,
                position=position,
                gender=gender,
                country=country,
                email=email,
                start=start,
                dob=dob,
                workplace=workplace

            )
            return redirect('employee:index')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            # フォームからデータを取得
            image = form.cleaned_data['image']
            empcode = form.cleaned_data['empcode']
            name = form.cleaned_data['name']
            department = form.cleaned_data['department']  # もし部署が必要ならここに追加
            position = form.cleaned_data['position']
            gender = form.cleaned_data['gender']
            country = form.cleaned_data['country']
            email = form.cleaned_data['email']
            start = form.cleaned_data['start']
            dob = form.cleaned_data['dob']
            workplace= form.cleaned_data['workplace']

            # モデルを手動で保存
            employee.image = image
            employee.empcode = empcode
            employee.name = name
            employee.department = department
            employee.position = position
            employee.gender = gender
            employee.country = country
            employee.email = email
            employee.start = start
            employee.dob = dob
            employee.workplace = workplace
            employee.save()

            return redirect('employee:index')
    else:
        # フォームをインスタンス化し、初期値を設定
        form = EmployeeForm(initial={
            'empcode': employee.empcode,
            'name': employee.name,
            'department': employee.department,
            'position': employee.position,
            'gender': employee.gender,
            'country': employee.country,
            'email': employee.email,
            'start': employee.start,
            'dob': employee.dob,
            'workplace': employee.workplace

        })
    return render(request, 'edit_employee.html', {'form': form})
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee:index')
    return render(request, 'delete_employee.html', {'employee': employee})

def search_employee(request):
    keyword = request.GET.get('keyword', '')
    position = request.GET.get('position', '')
    department = request.GET.get('department', '')

    employees = Employee.objects.all()

    if keyword:
        employees = employees.filter(
            Q(name__icontains=keyword) |
            Q(position__name__icontains=keyword) |
            Q(department__name__icontains=keyword)
        )

    return render(
        request,
        'search_employee.html',
        {'employees':employees}
    )

def advanced_search(request):
    if request.method == 'POST':
        selected_positions = request.POST.getlist('position')
        selected_departments = request.POST.getlist('department')
        selected_workplaces = request.POST.getlist('workplace')
        # <input type="radio" name="search_type" value="and" checked>
        search_type = request.POST.get('search_type', 'and')

        employees = Employee.objects.all()

        if search_type == 'and':
            for position in selected_positions:
                employees = employees.filter(position=position)
            for department in selected_departments:
                employees = employees.filter(department=department)
            for workplace in selected_workplaces:
                employees = employees.filter(workplace=workplace)
        else:

            #from django.db.models import Q
            q_objects = Q()
            for position in selected_positions:
                q_objects |= Q(position=position)
            for department in selected_departments:
                q_objects |= Q(department=department)
            for workplace in selected_workplaces:
                q_objects |= Q(workplace=workplace)
            employees = employees.filter(q_objects)

        return render(request, 'advanced_search.html', {'employees': employees})
    else:
        
        return render(request, 'advanced_search.html', {})


def index_dpt(request):
    departments = Department.objects.all()
    department_counts = Department.objects.exclude(parent=None).order_by('id').annotate(count=Count('employee'))
    parent_departments = Department.objects.filter(parent=None).order_by('id').values()
    department_labels = [department.name for department in department_counts]
    department_data = [department.count for department in department_counts]

    return render(request,
                  'index_dpt.html',
                  {
                      'departments':departments,
                      'department_counts':department_counts,
                      'parent_departments':parent_departments,
                      'department_labels':department_labels,
                      'department_data':department_data
                  })

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_detail.html', {'employee':employee})

def dpt_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    employees = Employee.objects.filter(department_id=pk)
    return render(request, 'department_detail.html', {'department':department, 'employees':employees})

def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            parent = form.cleaned_data['parent']
            Department.objects.create(name=name, parent=parent)
            return redirect('employee:index_dpt')
    else:
        form = DepartmentForm()
    return render(request, 'add_department.html', {'form': form})

def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            parent = form.cleaned_data['parent']

            department.name = name
            department.parent = parent
            department.save()

            return redirect('employee:index_dpt')
    else:
        # フォームをインスタンス化し、初期値を設定
        form = DepartmentForm(initial={
            'name': department.name,
        })
    return render(request, 'edit_department.html', {'form': form})

def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('employee:index_dpt')
    return render(request, 'delete_department.html', {'department': department})

def dashboard(request):
    employees = Employee.objects.all()
    total_employees = Employee.objects.count()
    department_counts = Department.objects.exclude(parent=None).order_by('id').annotate(count=Count('employee'))
    parent_departments = Department.objects.filter(parent=None).order_by('id').values()
    workplace_counts = Employee.objects.values('workplace').annotate(count=Count('workplace'))
    position_counts = Position.objects.order_by('id').annotate(count=Count('employee'))
    country_counts = Country.objects.order_by('id').annotate(count=Count('employee'))
    gender_counts = Employee.objects.values('gender').annotate(count=Count('gender'))

    # Prepare data for Chart.js
    gender_labels = [item['gender'] for item in gender_counts]
    gender_data = [item['count'] for item in gender_counts]

    workplace_labels = [item['workplace'] for item in workplace_counts]
    workplace_data = [item['count'] for item in workplace_counts]

    position_labels = [position.name for position in position_counts]
    position_data = [position.count for position in position_counts]

    country_labels = [country.name for country in country_counts]
    country_data = [country.count for country in country_counts]

    department_labels = [department.name for department in department_counts]
    department_data = [department.count for department in department_counts]

    return render(request,
                  'dashboard.html',
                  {
                      'employees': employees,
                      'total_employees': total_employees,
                      'department_counts': department_counts,
                      'parent_departments': parent_departments,
                      'workplace_counts': workplace_counts,
                      'position_counts': position_counts,
                      'country_counts': country_counts,
                      'gender_counts': gender_counts,
                      'gender_data': gender_data,
                      'gender_labels': gender_labels,
                      'workplace_data': workplace_data,
                      'workplace_labels': workplace_labels,
                      'position_data': position_data,
                      'position_labels': position_labels,
                      'country_data': country_data,
                      'country_labels': country_labels,
                      'department_data': department_data,
                      'department_labels': department_labels

                  }
)

def index_pst(request):
    positions = Position.objects.all()
    position_counts = Position.objects.order_by('id').annotate(count=Count('employee'))
    position_labels = [position.name for position in position_counts]
    position_data = [position.count for position in position_counts]

    return render(request,
                  'index_pst.html',
                  {
                      'positions':positions,
                      'position_counts':position_counts,
                      'position_labels':position_labels,
                      'position_data':position_data
                  }
                  )

def index_nt(request):
    nationalities = Country.objects.all()
    country_counts = Country.objects.order_by('id').annotate(count=Count('employee'))
    country_labels = [country.name for country in country_counts]
    country_data = [country.count for country in country_counts]

    return render(request,
                  'index_nt.html',
                  {
                      'nationalities':nationalities,
                      'country_counts':country_counts,
                      'country_labels':country_labels,
                      'country_data':country_data
                  })

def add_pst(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Position.objects.create(name=name)
            return redirect('employee:index_pst')
    else:
        form = PositionForm()
    return render(request, 'add_pst.html', {'form': form})

def add_nt(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Country.objects.create(name=name)
            return redirect('employee:index_nt')
    else:
        form = CountryForm()
    return render(request, 'add_nt.html', {'form': form})

def edit_pst(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            position.name = name
            position.save()
            return redirect('employee:index_pst')
    else:
        form = PositionForm(initial={
            'name': position.name,
        })

    return render(request, 'edit_pst.html', {'form': form})

def delete_pst(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        position.delete()
        return redirect('employee:index_pst')
    return render(request, 'delete_pst.html', {'position': position})

def edit_nt(request, pk):
    nationality = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            nationality.name = name
            nationality.save()
            return redirect('employee:index_nt')
    else:
        form = CountryForm(initial={
            'name': nationality.name,
        })

    return render(request, 'edit_nt.html', {'form': form})

def delete_nt(request, pk):
    nationality = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        nationality.delete()
        return redirect('employee:index_nt')
    return render(request, 'delete_nt.html', {'nationality': nationality})

def export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    writer = csv.writer(response)
    for employee in Employee.objects.all():
        writer.writerow([
            employee.id,
            employee.image,
            employee.empcode,
            employee.name,
            employee.position,
            employee.department,
            employee.gender,
            employee.country,
            employee.email,
            employee.start,
            employee.dob,
            employee.workplace
        ])
    return response


def schedule(request):
    magma_composition_data = [
        {"label": "Oxygen", "symbol": "O", "y": 46.6},
        {"label": "Silicon", "symbol": "Si", "y": 27.7},
        {"label": "Aluminium", "symbol": "Al", "y": 13.9},
        {"label": "Iron", "symbol": "Fe", "y": 5},
        {"label": "Calcium", "symbol": "Ca", "y": 3.6},
        {"label": "Sodium", "symbol": "Na", "y": 2.6},
        {"label": "Magnesium", "symbol": "Mg", "y": 2.1},
        {"label": "Others", "symbol": "Others", "y": 1.5}
    ]

    return render(request, 'schedule.html', {"magma_composition_data": magma_composition_data})
