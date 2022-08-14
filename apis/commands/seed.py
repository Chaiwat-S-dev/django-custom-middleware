
from django.core.management import BaseCommand
from apis.commands.seeders import seed_user
from apis.models import Company, User, Book


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.company_seeder()
        self.user_seeder()

    @staticmethod
    def company_seeder():
        company_list = [{"title": 'SwiftDynamics', "code": 'SWD'}, ]
        for org in company_list:
            if Company.objects.filter(title=org['title']).exists() is False:
                Company.objects.create(title=org['title'], code=org['code'])
    
    @staticmethod
    def user_seeder():
        for user in seed_user.dataset:
            if User.objects.filter(email=user['email'].lower()).exists() is False:
                company = Company.objects.get(code=user['project_code'])
                User.objects.create_user(
                    email=user['email'].lower(),
                    username=user['username'],
                    password=user['password'],
                    first_name=user['first_name'],
                    last_name=user['last_name'],
                    company_id=company.id,
                )
    
    @staticmethod
    def book_seeder():
        book_list = [{"title": 'cook_book', "price": 100, 
                        'owner': 'superadmin@swiftdynamics.co.th'},]
        for book in book_list:
            if Book.objects.filter(title=book['title'].lower()).exists() is False:
                owner = User.objects.get(email=book['owner'].lower())
                Book.objects.create(
                    title=book['title'].lower(),
                    price=book['price'],
                    owner_id=owner.id,
                )