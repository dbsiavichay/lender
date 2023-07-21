from .customers import urls as customer_urls
from .loans import urls as loans_urls
from .payments import urls as payment_urls

urlpatterns = []
urlpatterns.extend(customer_urls.urlpatterns)
urlpatterns.extend(loans_urls.urlpatterns)
urlpatterns.extend(payment_urls.urlpatterns)
