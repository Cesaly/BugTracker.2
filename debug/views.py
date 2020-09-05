from django.shortcuts import render, reverse, HttpResponseRedirect
from debug.forms import Login, Ticketadd, Edit, Adduser
from debug.models import Ticket, MyUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def index(request):
    html = 'index.html'

    new = Ticket.objects.filter(ticket_status='New')
    inprogress = Ticket.objects.filter(ticket_status=Ticket.INP)
    invalid = Ticket.objects.filter(ticket_status=Ticket.IN)
    finished = Ticket.objects.filter(ticket_status=Ticket.F)

    return render(request, html, {
        'inprogress': inprogress,
        'invalid': invalid,
        'new': new,
        'finished': finished
    })


@login_required
def authorsview(request, id):
    html = 'authorsview.html'
    name = MyUser.objects.filter(id=id)
    tickets = Ticket.objects.all()
    working = tickets.filter(ticket_person=id)
    filed = tickets.filter(author=id)
    finished = tickets.filter(ticket_done_by=id)

    return render(request, html, {
        'name': name, 'working': working,
        'filed': filed,
        'finished': finished
    })


@login_required
def info(request, id):
    html = "ticketinfo.html"
    detail = Ticket.objects.get(id=id)
    return render(request, html, {'detail': detail})


@login_required
def newticket(request):
    form = None
    html = "genericform.html"

    if request.method == 'POST':
        form = Ticketadd(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(
                title=data['title'],
                author=request.user,
                description=data['description'],
                
            )
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = Ticketadd()
    return render(request, html, {'form': form})


@login_required
def register(request):
    form = None
    html = "genericform.html"

    if request.method == "POST":
        form = Adduser(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            MyUser.objects.create(
                username=data['username'],
                password=data['password']
            )
        return HttpResponseRedirect(reverse('homepage'))
    else:
        form = Adduser()
    return render(request, html, {"form": form})


@login_required
def editticket(request, id):
    form = None
    html = 'genericform.html'
    instance = Ticket.objects.get(id=id)
    if request.method == 'POST':
        form = Edit(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('homepage'))
    else:
        form = Edit(instance=instance)
        return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def login_view(request):
    html = 'genericform.html'
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data.get('username'),
                                password=data.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('homepage')))
    form = Login()
    return render(request, html, {'form': form})


@login_required
def inprogress(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.ticket_status = "In Progress"
    ticket.ticket_person = request.user
    ticket.ticket_done_by = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticket', args=(id,)))


@login_required
def invalid(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.ticket_status = "Invalid"
    ticket.ticket_person = None
    ticket.ticket_done_by = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticket', args=(id,)))


@login_required
def finished(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.ticket_status = 'Finished'
    ticket.ticket_done_by = ticket.ticket_person
    ticket.ticket_person = None
    ticket.save()
    return HttpResponseRedirect(reverse('homepage'))
