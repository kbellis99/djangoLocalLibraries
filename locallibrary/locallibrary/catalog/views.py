from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.minins import PermissionRequiredMixin

def index(request):
    numBooks=Book.objects.all().count()
    numInstances=BookInstance.objects.all().count()
    numInstancesAvailable=BookInstance.objects.filter(status__exact='a').count()
    numAuthors=Author.objects.count()
    numVisits=request.session.get('numVisits', 0)
    request.session['numVisits'] = numVisits+1

    return render(
        request,
        'index.html',
        context={'numBooks':numBooks,'numInstances':numInstances,'numInstancesAvailabile':numInstancesAvailable,'numAuthors':numAuthors,'numVisits':numVisits},
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    contextObjectName = 'Recommended Books'
    queryset = Book.objects.filter(title__icontains='darkness')[:5]

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstanceListBorrowedUser.html'
    paginate_by = 10

    def getQueryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exat='o').order_by('dueBack')

class LoanedBooksAllListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    permissio_required = 'catalog.canMarkReturned'
    template_name ='catalog/bookinstanceListBorrowedAll.html'
    paginate_by = 10

    def getQueryset(self):
        return BookInstance.objects.filter(status__exact='o').orderBy('dueBack')

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from .forms import RenewBookForm

@permission_required('catalog.canMarkReturned')
def renewBookLibrarian(request, pk):
    bookInst=get_object_or_404(BookInstance, pk = pk)
    if request.method =='POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            bookInst.dueBack = form.cleaned_data['RenewalDate']
            bookInst.save()
            return HttpResponseRedirect(reverse('allBorrowed') )
    else:
        proposedRenewalDate = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'RenewalDate': proposedRenewalDate,})
    return render(request, 'catalog/bookRenewLibrarian.html', {'form': form, 'bookinst':bookInst})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial={'dateOfDeath':'04/23/2015',}
    permission_required = 'catalog.canMarkReturned'

class AuthorUpdate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['firstName', 'lastName', 'dateOfBirth', 'dateOfDeath']
    permission_required = 'catalog.canMarkReturned'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.canMarkReturned'

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.canMarkReturned'

class BookUpdate(PermissionRequiredMixin, DeleteView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.canMarkReturned'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.canMarkReturned'
