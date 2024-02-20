from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from utilisateur import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . tokens import generateToken
from django.shortcuts import render , HttpResponseRedirect, get_object_or_404 , redirect
from .resources import BeneficiaireResource
from tablib import Dataset
from .forms import BeneficiaireRegistration
from .models import Beneficiaire, BeneficiaireModifie 
from django.core.paginator import Paginator

# Create your views here.


def home(request, *args, **kwargs):
    return render(request, 'authentification/index.html')

# Creation de Compte
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpwd = request.POST['comfirmpwd']
        if User.objects.filter(username=username):
            messages.add_message(request,messages.ERROR, 'username already taken please try another.')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})
        #messages.error(request,'messages error') affiche le msg dans l'interface admin,il faut configurer dans l'interface utilisateurs
        if User.objects.filter(email=email):
            messages.add_message(request,messages.ERROR, 'This email has an account.')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})
        if len(username)>10:
            messages.add_message(request,messages.ERROR, 'Please the username must not be more than 10 character.')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})
        if len(username)<5:
            messages.add_message(request,messages.ERROR, 'Please the username must be at leat 5 characters.')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})
        if not username.isalnum():
            messages.add_message(request,messages.ERROR, 'username must be alphanumeric')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})

        if password != confirmpwd:
            messages.add_message(request,messages.ERROR, 'The password did not match! ')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name =firstname
        my_user.last_name = lastname
        my_user.is_active = False
        my_user.save()
        messages.add_message(request,messages.SUCCESS, 'Your account has been successfully created. we have sent you an email You must comfirm in order to activate your account.')
# send email when account has been created successfully
        subject = "Activation"
        message = "Tongasoa "+ my_user.first_name + "," + my_user.last_name + "\n Mankasiatraka anao nisafidy ahy\n Raha te andefa ny Kaonty ianao dia araho ny rohy etsy ambany"
        
        from_email = settings.EMAIL_HOST_USER
        to_list = [my_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

# send the the confirmation email
        current_site = get_current_site(request) 
        email_suject = "confirm your email DonaldPro Django Login!"
        messageConfirm = render_to_string("emailConfimation.html", {
            'name': my_user.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(my_user.pk)),
            'token': generateToken.make_token(my_user)
        })       

        email = EmailMessage(
            email_suject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [my_user.email]
        )

        email.fail_silently = False
        email.send()
        return render(request,'authentification/signin.html',{'messages':messages.get_messages(request)})
    return render(request, 'authentification/signup.html')    

# Cennexion au compte
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        my_user = User.objects.get(username=username)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'authentification/index.html', {"firstname":firstname})
        elif my_user.is_active == False:
            messages.add_message(request,messages.ERROR, 'you have not confirm your  email do it, in order to activate your account')
            return render(request,'authentification/signin.html')
        else:
            messages.add_message(request,messages.ERROR, 'bad authentification')
            return render(request,'authentification/index.html',{'messages':messages.get_messages(request)})

    return render(request, 'authentification/signin.html')    
# Se deconnecter au compte
def signout(request):
    logout(request)
    messages.success(request, 'logout successfully!')
    return redirect('home')

# Activation des comptes
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        my_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        my_user = None

    if my_user is not None and generateToken.check_token(my_user, token):
        my_user.is_active  = True        
        my_user.save()
        messages.add_message(request,messages.SUCCESS, "You are account is activated you can login by filling the form below.")
        return render(request,"authentification/signin.html",{'messages':messages.get_messages(request)})
    else:
        messages.add_message(request,messages.ERROR, 'Activation failed please try again')
        return render(request,'authentification/index.html',{'messages':messages.get_messages(request)})

#affichage des donnees
def afficher(request):
    query = request.GET.get('q')
    benef = Beneficiaire.objects.all() 
    
    #recherche
    if query:
        benef = benef.filter(
            nom__icontains=query) | \
                                benef.filter(prenom__icontains=query) | \
                                benef.filter(matricule__icontains=query)
     # Nombre d'éléments à afficher par page
    elements_par_page = 15
    paginator = Paginator(benef, elements_par_page)
    
    # Récupérez le numéro de la page à afficher
    page = request.GET.get('page', 1)
    
    # Obtenez les éléments de la page spécifiée
    beneficiaires_pages = paginator.get_page(page)
    return render(request,'tafika/liste.html',{'benefici':beneficiaires_pages} )

def afficher_modifications(request):
    query = request.GET.get('q')
    beneficiaires_modifies = BeneficiaireModifie.objects.all()
    #recherche
    if query:
        beneficiaires_modifies = beneficiaires_modifies.filter(
            beneficiaire__nom__icontains=query) | \
                                beneficiaires_modifies.filter(beneficiaire__prenom__icontains=query) | \
                                beneficiaires_modifies.filter(beneficiaire__matricule__icontains=query)
                                
    # Nombre d'éléments à afficher par page
    elements_par_page = 15
    paginator = Paginator(beneficiaires_modifies, elements_par_page)
    # Récupérez le numéro de la page à afficher
    page = request.GET.get('page', 1)
    # Obtenez les éléments de la page spécifiée
    beneficiaires_modifies_page = paginator.get_page(page)
    
    return render(request, 'tafika/donneModif.html',{'beneficiaires_modifies': beneficiaires_modifies_page})

#imporation
def importation(request):
    if request.method == 'POST':
        beneficiaire_resource = BeneficiaireResource()
        dataset = Dataset()
        new_benenef = request.FILES['fichier']

        try:
            # Charger les données du fichier dans le dataset
            imported_data = dataset.load(new_benenef.read(), format='xlsx')

            # Utiliser les données du dataset pour créer des instances de Beneficiaire
            for data in imported_data:
                 value = Beneficiaire(
                      data[0],
                      data[1],
                      data[2],
                      data[3],
                      data[4],
                      data[5],
                      data[6],
                      data[7],
                      data[8],
                      data[9],
                      data[10],
                      data[11],
                      data[12],
                )
            value.save(),

            # Message de confirmation
            message_confirmation = "Les bénéficiaires ont été importés avec succès."
            return render(request, 'tafika/liste.html', {'message_confirmation': message_confirmation})

        except Exception as e:
            # Gérer les erreurs d'importation
            return HttpResponse(f"Erreur lors de l'importation : {str(e)}")

    return render(request, 'tafika/liste.html') 

#suppression des donnees

def suppression(request , id):
    if request.method =='POST':
            sup = Beneficiaire.objects.get(pk= id)
            sup.delete()
    return HttpResponseRedirect('/')

#Modification des donnees

def modifier_beneficiaire(request, beneficiaire_id):
    beneficiaire = get_object_or_404(Beneficiaire, id=beneficiaire_id)

    if request.method == 'POST':
        form = BeneficiaireRegistration(request.POST, instance=beneficiaire)
        if form.is_valid():
            form.save()
            # Après la modification, vous pouvez rediriger vers une page spécifique ou afficher un message de succès
            return redirect('afficher_modifications')
    else:
        form = BeneficiaireRegistration(instance=beneficiaire)

    return render(request, 'tafika/modification.html', {'form': form})


