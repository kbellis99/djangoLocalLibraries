from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a Book Genre (e.g. Science Fiction, Romance, Horror, etc.)")
    
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a Book's Natural Language (e.g. English, German, French, etc.)")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN' ,max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def displayGenre(self):
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
        displayGenre.shortDescription = 'Genre'

    def getAbsoluteUrl(self):
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book accross whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    dueBack = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def isOverdue(self):
        if self.dueBack and date.today() > self.dueBack:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["dueBack"]
        permissions = (('canMarkReturned', 'Set Book As Returned'),)

    def __str__(self):
        return '{0} ({1})'.format(self.id,self.book.title)

class Author(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    dateOfBirth = models.DateField(null=True, blank=True)
    dateOfDeath = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ["lastName", "firstName"]

    def getAbsoluteUrl(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.lastName,self.firstName)
