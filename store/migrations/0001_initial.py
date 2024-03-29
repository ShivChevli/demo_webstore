# Generated by Django 3.2.9 on 2022-07-15 14:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Discount Offer Name')),
                ('desc', models.CharField(blank=True, max_length=128, null=True, verbose_name='Discount Description')),
                ('discount_percent', models.FloatField()),
                ('active', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(default=datetime.datetime.now)),
                ('modifiedAt', models.DateTimeField(default=datetime.datetime.now)),
                ('deletedAt', models.DateTimeField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField()),
                ('discount_percentage', models.FloatField(blank=True, default=0, null=True)),
                ('discounted_price', models.FloatField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(default=datetime.datetime.now)),
                ('modifiedAt', models.DateTimeField(default=datetime.datetime.now)),
                ('applied_offer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.discount', verbose_name='Applied Discount')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('desc', models.CharField(blank=True, max_length=128, null=True, verbose_name='Product description')),
                ('img_url', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('actual_price', models.FloatField(blank=True, null=True)),
                ('display_price', models.FloatField()),
                ('brand', models.CharField(blank=True, max_length=16, null=True)),
                ('createdAt', models.DateTimeField(default=datetime.datetime.now)),
                ('modifiedAt', models.DateTimeField(default=datetime.datetime.now)),
                ('deletedAt', models.DateTimeField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Product Category Name')),
                ('desc', models.CharField(blank=True, max_length=120, null=True, verbose_name='Category Description')),
                ('createdAt', models.DateTimeField(default=datetime.datetime.now)),
                ('modifiedAt', models.DateTimeField(default=datetime.datetime.now)),
                ('deletedAt', models.DateTimeField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SiteUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.EmailField(max_length=50, verbose_name='User Name')),
                ('password', models.CharField(max_length=32)),
                ('firstName', models.CharField(blank=True, max_length=20, null=True, verbose_name='First Name')),
                ('lastName', models.CharField(blank=True, max_length=20, null=True, verbose_name='Last Name ')),
                ('telephone', models.CharField(blank=True, max_length=11, null=True, verbose_name='Mobile Number')),
                ('createdAt', models.DateTimeField(default=datetime.datetime.now)),
                ('modifyAt', models.DateTimeField(default=datetime.datetime.now)),
                ('deletedAt', models.DateTimeField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addressLine1', models.CharField(max_length=32)),
                ('addressLine2', models.CharField(blank=True, max_length=32, null=True)),
                ('city', models.CharField(max_length=16)),
                ('postelCode', models.CharField(max_length=16)),
                ('country', models.CharField(blank=True, max_length=16)),
                ('addressContactNumber_1', models.CharField(blank=True, max_length=11, null=True)),
                ('addressContactNumber_2', models.CharField(blank=True, max_length=11, null=True)),
                ('createdAt', models.DateTimeField(default=datetime.datetime.now)),
                ('modifyAt', models.DateTimeField(default=datetime.datetime.now)),
                ('deletedAt', models.DateTimeField(blank=True, default=None, null=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.siteuser', verbose_name='User Name')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField()),
                ('createdAt', models.DateTimeField(default=datetime.datetime.now)),
                ('modifiedAt', models.DateTimeField(default=datetime.datetime.now)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.siteuser', verbose_name='User Detail')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('createdAt', models.DateTimeField(default=datetime.datetime.now)),
                ('modifiedAt', models.DateTimeField(default=datetime.datetime.now)),
                ('deletedAt', models.DateTimeField(blank=True, default=None, null=True)),
                ('product_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetailInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rear_Camara', models.CharField(max_length=64)),
                ('front_camara', models.CharField(blank=True, max_length=64, null=True)),
                ('ram', models.PositiveSmallIntegerField()),
                ('inbuilt_storage', models.PositiveSmallIntegerField()),
                ('expandable_storage', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('processor_brand', models.CharField(blank=True, max_length=16, null=True)),
                ('operating_system', models.CharField(max_length=16)),
                ('screen', models.CharField(blank=True, max_length=16, null=True)),
                ('battery_power', models.FloatField()),
                ('battery_type', models.CharField(blank=True, max_length=16, null=True)),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Product Id')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category_id',
            field=models.ForeignKey(on_delete=models.SET(0), to='store.productcategory', verbose_name='Product Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.discount', verbose_name='Active Discount Offer'),
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('createdAt', models.DateTimeField(default=datetime.datetime.now)),
                ('modifiedAt', models.DateTimeField(default=datetime.datetime.now)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.orderdetails', verbose_name='Order Detail')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Product Name')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='cartId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.shoppingsession', verbose_name='Cart ID'),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.siteuser', verbose_name='User Detail'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('createdAt', models.DateTimeField(default=datetime.datetime.now)),
                ('modifiedAt', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('deletedAt', models.DateTimeField(blank=True, default=None, null=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Cart Product Detail')),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session', to='store.shoppingsession')),
            ],
        ),
    ]
