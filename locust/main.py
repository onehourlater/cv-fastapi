from locust import HttpUser, task

'''

locust -f locust/main.py --headless --host http://127.0.0.1:8000 -u 1 -r 5

'''

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get(f'/api/v1/users/dev-info')
        self.client.get(f'/api/v1/users/dev-info-user-manager')

        '''
        self.client.post(f'/api/v1/signin', json={
        	"email": "hello@mail.com",
        	"password": "hellokitty"
        })
        '''
