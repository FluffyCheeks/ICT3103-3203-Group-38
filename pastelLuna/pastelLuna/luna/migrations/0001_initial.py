# Generated by Django 4.1.2 on 2022-11-04 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authorised_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/img/')),
                ('ingredients', models.CharField(max_length=1000)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('stock_available', models.IntegerField(null=True)),
                ('slug', models.SlugField(null=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.product_category')),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissions', models.CharField(max_length=20)),
                ('role_desc', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=1000, unique=True)),
                ('address', models.CharField(default=None, max_length=1000, null=True)),
                ('phone', models.CharField(default=None, max_length=15, null=True)),
                ('allergies', models.CharField(max_length=1000, null=True)),
                ('email_valid', models.BooleanField(default=False)),
                ('attempt', models.IntegerField(default=0)),
                ('role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.roles')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.product_details')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20, null=True)),
                ('created', models.CharField(max_length=50, null=True)),
                ('updated', models.CharField(max_length=50, null=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.product_details')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.authorised_user')),
                ('user_pk_id_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.users')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_mode', models.CharField(max_length=150, null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=1000, null=True)),
                ('address', models.CharField(max_length=1000, null=True)),
                ('phone', models.CharField(max_length=8, null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('order_status', models.CharField(default='Pending', max_length=50)),
                ('tracking_no', models.CharField(max_length=50, null=True)),
                ('ccard_digits', models.CharField(blank=True, max_length=16, null=True)),
                ('orderDate', models.CharField(max_length=50, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='luna.users')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.orders')),
                ('productID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.product_details')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.product_details')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.users')),
            ],
        ),
        migrations.AddField(
            model_name='authorised_user',
            name='role_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.roles'),
        ),
    ]
