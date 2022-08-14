from django.db import models
from apis.utils import AbstractModel
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class Company(AbstractModel):
    title = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(max_length=100, blank=False, null=False, unique=True)

    @property
    def context_data(self):
        return {
            'id': self.pk,
            'title': self.title,
            'code': self.code,
        }
    
    class Meta:
        indexes = [
            models.Index(fields=['code',]),
        ]


class User(AbstractModel, AbstractUser):
    objects = UserManager()
    email = models.EmailField(max_length=255, verbose_name='email address', unique=True, blank=False, null=False)
    created_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_accept_terms = models.BooleanField(default=False)
    accept_terms_date = models.DateField(blank=True, null=True, default=None)
    is_verified = models.BooleanField(default=False)
    verify_key = models.CharField(max_length=255, null=True, blank=True)
    verify_key_expires = models.DateTimeField(blank=True, null=True, default=None)
    company = models.ForeignKey(Company, blank=True, on_delete=models.CASCADE, null=True, related_name='company_user')

    def __str__(self):
        return self.get_full_name()

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def shortcut_name(self):
        return f'{self.first_name[0] if self.first_name else " "}{self.last_name[0] if self.last_name else " "}'.replace(
            ' ', '').upper()

    @property
    def context_data(self):
        return {
            'id': self.pk,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'shortcut_name': self.shortcut_name,
            'is_accept_terms': self.is_accept_terms,
            'company': self.company if self.company else None,
        }

    @property
    def abstract_context(self):
        return {
            'id': self.pk,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'shortcut_name': self.shortcut_name,
            'email': self.email,
        }
    
    class Meta:
        indexes = [
            models.Index(fields=['username',]),
        ]

class Book(AbstractModel):
    title = models.CharField(max_length=100, null=False, blank=False)
    price = models.IntegerField(default=0, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="owner_book")

    @property
    def context_data(self):
        return {
            'id': self.pk,
            'title': self.title,
            'price': self.price,
            'owner': self.owner.abstract_context if self.owner else None,
        }