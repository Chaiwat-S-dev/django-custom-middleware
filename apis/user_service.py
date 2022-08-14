import time
import json
import threading
from apis.models import User, Company
from redis import StrictRedis
from django.db.models import Q

class SubscribeService:
    
    def event_handler(self):
        self.pubsub.subscribe(self.channel)
        
        while True:
            # print("subscribe thread running...")
            message = self.pubsub.get_message()
            if message:
                # TODO: handle message subscribe for get_or_create user
                # TODO: clean code
                if message['type'] == 'message':
                    # print(f'subscribe message: {message}')
                    raw_message = message['data'].decode('utf-8').replace("'",'"')
                    raw_message = json.loads(raw_message)
                    # print(f"{raw_message=}")
                    
                    created_by_id, company = None, None
                    
                    if created_by := raw_message['created_by']:
                        created_by_id = created_by['id']
                    
                    if raw_comapny := raw_message['company']:
                        company, _ = Company.objects.get_or_create(
                            title=raw_comapny['title'],
                            code=raw_comapny['code'],
                        )
                        # print(f'{company=}')
                    
                    if user_list := User.objects.filter(
                            Q(email=raw_message['email']) | Q(username=raw_message['username'])
                        ):
                        print(f'{user_list=}')
                        print(f'User {raw_message["username"]} is already existed, check data company')
                        
                        user = user_list.get(email=raw_message['email'])
                        
                        print(f'get user by email: {user=}')
                        
                        if user.company and user.company.code != company.code:
                            print(f'company code not equal new, then update company')
                            user.company = company
                            user.save()
                        else:
                            print(f'user don\'t have company, then update company')
                            user.company = company
                            user.save()
                    
                    else:
                        print(f'Create user')
                        user = User.objects.create(
                            email=raw_message['email'],
                            username=raw_message['username'],
                            first_name=raw_message['first_name'], 
                            last_name=raw_message['last_name'],
                            is_accept_terms=raw_message['is_accept_term_cm'],
                            created_by_id=created_by_id,
                            accept_terms_date=raw_message['accept_term_cm'],
                            is_verified=raw_message['is_verify'],
                            password=raw_message['password'],
                            verify_key=raw_message['verify_key'],
                            verify_key_expires=raw_message['verify_key_expire'],
                            is_active=raw_message['is_active'],
                            is_superuser=raw_message['cm_admin'],
                            company=company,
                        )
                        print(f'{user=}')

            else:
                # print("message is not arriving, waiting for 1 sec")
                time.sleep(1)
    
    def __init__(self, redis=None, host='localhost', port=6379, channel='*', callback=None) -> None:
        self.host, self.port, self.channel = host, port, channel
        self.redis = redis or StrictRedis(host='localhost', port=6379)
        self.pubsub = self.redis.pubsub()
        self.callback = callback or self.event_handler
    
    def set_host(self, host) -> None:
        self.host(host)
    
    def get_host(self) -> str:
        return self.host
    
    def set_port(self, port) -> None:
        self.port(port)
    
    def get_port(self) -> int:
        return self.port
    
    def set_channel(self, channel) -> None:
        self.channel(channel)
    
    def get_channel(self) -> str:
        return self.channel
    
    def run_daemon(self) -> None:
        threading.Thread(target=self.callback, daemon=True).start()

    def run(self) -> None:
        self.event_handler()