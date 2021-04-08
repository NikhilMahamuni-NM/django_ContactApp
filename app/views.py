from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.
#Function based views
# def home(request):
#     context = {
#         'contacts' : Contact.objects.all()
#     }
#     return render(request, 'app/index.html', context)

# def detail(request, id):
#     context = {
#         'contact' : get_object_or_404(Contact, pk=id)
#     }
#
#     return render(request, 'app/detail.html', context)

@login_required
def search(request):
    if request.GET:
        search_term = request.GET['search_term']

        #For a single search Query
        #search_results = Contact.objects.filter(name__icontains = search_term) #For a single search Query

        #for multiple search Query
        search_results = Contact.objects.filter(
            Q(name__icontains = search_term) |
            Q(email__icontains = search_term) |
            Q(info__icontains = search_term) |
            Q(phone__iexact = search_term)
        )
        context = {
            'search_term' : search_term,
            'contacts' : search_results.filter(manager=request.user) #to show the searh results from logged in user data
        }
        return render(request, 'app/search.html', context)
    else:
        return redirect('app:home')
#Class Based views
class HomePageView(LoginRequiredMixin, ListView):
    template_name = 'app/index.html'
    model = Contact
    context_object_name = 'contacts'

    # to display contacts of current logged in User
    def get_queryset(self):
        contacts = super().get_queryset()
        return contacts.filter(manager = self.request.user)

class ContactDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app/detail.html'
    model = Contact
    context_object_name = 'contact'

class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = 'app/create.html'
    fields = ['name', 'email', 'phone', 'info', 'gender', 'image']
    #success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.manager = self.request.user
        instance.save()
        messages.success(self.request, 'The Contact has been Successfully Created!!')
        return redirect('app:home')

class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'app/update.html'
    fields = ['name', 'email', 'phone', 'info', 'gender', 'image']
    #success_url = '/'

    #Returning to the Custom page (Detail Page) after updating the values
    def form_valid(self, form):
        instance = form.save()
        messages.success(self.request, 'The Contact has been Successfully Updated!!')
        return redirect('app:detail', instance.pk)

class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'app/delete.html'
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'The Contact has been Successfully Deleted!!')
        return super().delete(self, request, *args, **kwargs)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('app:home')
