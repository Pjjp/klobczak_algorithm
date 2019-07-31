
class ProductManager(models.Manager):

    def filter_cosmetics(self):

        return self.filter(name__in=['toothbrush', 'lotion'])


class Product(models.Model):
    
    objects = ProductManager()

    name = models.CharField(max_length=64)



Product.objects.create(name='toothbrush')
Product.objects.all()
Product.objects.filter(name__contains='tooth')
Product.objects.create(name='toothbrush')
Product.objects.filter_cosmetics()
