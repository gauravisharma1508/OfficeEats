from django.contrib import admin

# Register your models here.
from .models import Customer,Menu,Category,Order


#class CustomerAdmin(admin.ModelAdmin):
    #fields = ['fname','oname','emp_id','mob','email','image','password','order_id','reg_id']
    #readonly_fields = ['reg_id']


    #class Meta:
        #model= Customer




#class ProductInline(admin.TabularInline):
    #model = Menu
    #extra = 3

#class CategoryAdmin(admin.ModelAdmin):
    #list_display = ['name','product_count']

    #fieldsets = (
        #(
            #None,{
                #'fields':('name',)
            #}
        #),
    #)
    #inlines = (ProductInline,)

    #def product_count(self,obj):
        #return obj.product_set.count()

    #def get_ordering(self,request):
        #return ('name')

class MenuAdmin(admin.ModelAdmin):
    list_display = ['name','price','slug','category','image']

    class Meta:
        model= Menu

class OrderAdmin(admin.ModelAdmin):
    list_display = ['menu','customer','takeaway']

    class Meta:
        model= Order

admin.site.register(Customer)#,CustomerAdmin)
#admin.site.register(Category,CategoryAdmin)
admin.site.register(Category)
admin.site.register(Menu,MenuAdmin)
admin.site.register(Order,OrderAdmin)