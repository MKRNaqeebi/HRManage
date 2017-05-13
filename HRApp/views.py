from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.core.mail import send_mail

User = get_user_model()

menu_hrp = ['Post a Job', 'Review Applications & Send Letter']
url_menu_hrp = ['PostJob', 'application']
menu_sme = ['Give Rating To Applicant']
url_menu_sme = ['application']
menu_hrm = ['Create HRP', 'Create SME', 'See Top 5']
url_menu_hrm = ['RegisterHRP', 'RegisterSME', 'application']
menu_applicant = ['Post CV']
url_menu_applicant = ['apply']


def api_json(request):
    jobs = Job.objects.all()
    job = '<root>'
    for j in jobs:
        job = job + '<title>' + j.title + '</title>'
        job = job + '<description>' + j.description + '</description>'
        job = job + '<location>' + j.location + '</location>'
        job = job + '<salary>' + j.salary.__str__() + '</salary>'
        job = job + '<created_at>' + j.created_at.__str__() + '</created_at>'
        job = job + '<updated_at>' + j.updated_at.__str__() + '</updated_at>'

    job = job + '</root>'
    return HttpResponse(job.__str__())


def application(request):
    my_type = UserType.objects.filter(user=request.user.id)
    if request.user.is_authenticated() and (my_type[0].user_type == "HRP" or my_type[0].user_type == "SME" or my_type[0].user_type == "HRM"):
        menu = zip(menu_hrp, url_menu_hrp)
        if my_type[0].user_type == "HRM":
            menu = zip(menu_hrm, url_menu_hrm)
        template = loader.get_template('index.html')
        context = {
            'menu': menu,
            'user': request.user,
            'type': my_type[0].user_type,
            'title': "Application By Job",
            'jobs': Job.objects.all(),
        }
        return HttpResponse(template.render(context, request))
    return HttpResponse("Login as HRP")


def apply(request):
    my_type = UserType.objects.filter(user=request.user.id)
    if request.user.is_authenticated() and my_type[0].user_type == "A":
        menu = zip(menu_applicant, url_menu_applicant)
        template = loader.get_template('index.html')
        context = {
            'menu': menu,
            'user': request.user,
            'title': "Post CV",
            'jobs': Job.objects.all(),
        }
        return HttpResponse(template.render(context, request))
    return HttpResponse("Login as Applicant")


def index(request):
    if request.user.is_authenticated():
        my_type = UserType.objects.filter(user=request.user.id)
        if len(my_type) > 0 and my_type[0].user_type == "HRM":
            menu = zip(menu_hrm, url_menu_hrm)
        elif len(my_type) > 0 and my_type[0].user_type == "HRP":
            menu = zip(menu_hrp, url_menu_hrp)
        elif len(my_type) > 0 and my_type[0].user_type == "SME":
            menu = zip(menu_sme, url_menu_sme)
        else:
            menu = zip(menu_applicant, url_menu_applicant)
        template = loader.get_template('profile.html')
        context = {
            'type': my_type[0].user_type,
            'menu': menu,
            'user': request.user,
            'title': "Profile",
        }
        return HttpResponse(template.render(context, request))
    template = loader.get_template('index.html')
    context = {
        'jobs': Job.objects.all(),
        'title': "Job Feed",
    }
    return HttpResponse(template.render(context, request))


def user_type(request):
    template = loader.get_template('test.html')
    context = {
        'types': UserType.objects.all(),
        'title': "User Type",
    }
    return HttpResponse(template.render(context, request))


def apply_job(request, job):
    if request.user.is_authenticated():
        title = "Apply for Job"
        if request.method == 'POST':
            form = ApplyForm(request.POST, request.FILES)
            if form.is_valid():
                var_apply = form.save(commit=False)
                var_apply.user = request.user
                var_apply.job = Job.objects.get(id=job)
                var_apply.save()
                return redirect("/")

        return render(request, "form.html", {"form": ApplyForm(), "title": title, "job": Job.objects.get(id=job)})
    return HttpResponse("Login First")


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponse("Logout First")
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/")

    return render(request, "form.html", {"form": form, "title": title})


def register_view(request):
    if request.user.is_authenticated():
        return HttpResponse("Logout First")
    title = "Register"
    form = UserRegisterFoam(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        type_user = UserType(user_type="A", user=request.user)
        type_user.save()
        return redirect("/")

    context = {
        "form": form,
        "title": title,
    }
    return render(request, "form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")


def post_job_view(request):
    my_type = UserType.objects.filter(user=request.user.id)
    if my_type.count() > 0 and my_type[0].user_type == "HRM":
        title = "Post a JOB"
        form = PostJob(request.POST or None)
        if form.is_valid():
            job = form.save(commit=False)
            job.save()
            return redirect("/")

        context = {
            "form": form,
            "title": title,
        }
        return render(request, "form.html", context)
    return HttpResponse("Not Authorize")


def create_category_view(request):
    my_type = UserType.objects.filter(user=request.user.id)
    if my_type.count() > 0 and my_type[0].user_type == "HRM":
        title = "Create a Category"
        form = CreateCategory(request.POST or None)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect("/")

        context = {
            "form": form,
            "title": title,
        }
        return render(request, "form.html", context)
    return HttpResponse("Not authorize")


def create_company_view(request):
    my_type = UserType.objects.filter(user=request.user.id)
    if my_type.count() > 0 and my_type[0].user_type == "HRM":
        title = "Create a Company"
        form = CreateCompany(request.POST or None)
        if form.is_valid():
            company = form.save(commit=False)
            company.save()
            return redirect("/")

        context = {
            "form": form,
            "title": title,
        }
        return render(request, "form.html", context)
    return HttpResponse("Not authorize")


def get_all_apply(request, job):
    my_type = UserType.objects.filter(user=request.user.id)
    if my_type.count() > 0 and (my_type[0].user_type == "HRP" or my_type[0].user_type == "SME" or my_type[0].user_type == "HRM"):
        title = "Interview or Rejection Letters"
        menu = zip(menu_hrp, url_menu_hrp)
        my_list = Apply.objects.filter(job=Job.objects.get(id=job))[:5]
        if my_type[0].user_type == "HRM":
            menu = zip(menu_hrm, url_menu_hrm)
            my_list = Apply.objects.filter(job=Job.objects.get(id=job))[:5]
        context = {
            "menu": menu,
            "list": my_list,
            "title": title,
            "type": my_type[0].user_type,
        }
        if request.method == 'POST':
            user_list = request.POST.getlist("userID[]")
            for ul in user_list:
                my_apply = Apply.objects.get(id=ul)
                send_mail('Subject here', 'Here is the message.', 'mkrnaqeebi@gmail.com', [my_apply.user.email],
                          fail_silently=False)
                interview = InterviewCall()
                interview.apply = my_apply
                interview.save()

            return render(request, "index.html", context)

        return render(request, "listApps.html", context)
    return HttpResponse("Not Authorize")


def register_sme(request):
    my_type = UserType.objects.filter(user=request.user.id)
    if my_type.count() > 0 and my_type[0].user_type == "HRM":
        title = "Register SME"
        form = UserRegisterFoam(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            type_user = UserType(user_type="SME", user=request.user)
            type_user.save()
            return redirect("/")

        context = {
            "form": form,
            "title": title,
        }
        return render(request, "form.html", context)
    return HttpResponse("Not Authorize")


def register_hrm(request):
    if request.user.is_superuser:
        title = "Register HRM"
        form = UserRegisterFoam(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            type_user = UserType(user_type="HRM", user=request.user)
            type_user.save()
            return redirect("/")

        context = {
            "form": form,
            "title": title,
        }
        return render(request, "form.html", context)
    return HttpResponse("Not authorize")


def register_hrp(request):
    my_type = UserType.objects.filter(user=request.user.id)
    if my_type.count() > 0 and my_type[0].user_type == "HRM":
        title = "Register HRP"
        form = UserRegisterFoam(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            type_user = UserType(user_type="HRP", user=request.user)
            type_user.save()
            return redirect("/")

        context = {
            "form": form,
            "title": title,
        }
        return render(request, "form.html", context)
    return HttpResponse("505 login as hrm")


def rate_all_apply(request, job):
    my_type = UserType.objects.filter(user=request.user.id)
    if my_type.count() > 0 and my_type[0].user_type == "SME":
        title = "All Application"
        context = {
            "list": Apply.objects.filter(job=Job.objects.get(id=job)),
            "title": title,
        }
        return render(request, "rateApps.html", context)
    return HttpResponse("Not Authorize")


def rate_apply(request, var_apply):
    my_type = UserType.objects.filter(user=request.user.id)
    if request.user.is_superuser or (my_type.count() > 0 and my_type[0].user_type == "SME"):
        title = "Rate Application"
        form = RateApplyForm(request.POST or None)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.sme = request.user
            rate.apply = Apply.objects.get(id=var_apply)
            rate.save()
            return redirect("/")

        context = {
            "type": my_type[0].user_type,
            "app": Apply.objects.get(id=var_apply),
            "form": form,
            "title": title,
        }
        return render(request, "form.html", context)
    return HttpResponse("Not Authorize")


def get_top_five(request):
    my_type = UserType.objects.filter(user=request.user.id)
    if request.user.is_superuser or (my_type.count() > 0 and my_type[0].user_type == "SME"):
        title = "Rate Top 5 Application"
        top_five = RateApply.objects.order_by('-rate')[:5]
        context = {
            "type": my_type[0].user_type,
            "title": title,
            'list': top_five,
        }
        return render(request, "listApps.html", context)