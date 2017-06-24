from django.utils import timezone
import numpy as np
from ranking.models import *
for i in range(10):
    user = User(
        username='test_user{0}'.format(i),
        arc_user_name='user{0}'.format(i),
        email='email{0}@email.com'.format(i),
    )
    user.set_password('password{0}'.format(i))
    user.save()

for i in range(1000):
    num = np.random.randint(1, 11)
    language = ['Python', 'C++', 'Others']
    no = np.random.randint(3)
    result = Result(user=User(id=num),
                    result_problem=AtCoderProblem.objects.get(id=1),
                    result_language=language[no],
                    result_coding_time=3,
                    result_running_time=4,
                    pub_date=timezone.now(),
                    result_code='sample_code'
                    )
    result.save()
