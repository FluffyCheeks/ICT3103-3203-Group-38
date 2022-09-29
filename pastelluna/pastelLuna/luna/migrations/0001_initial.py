# Generated by Django 4.1.1 on 2022-09-27 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('provider', models.CharField(max_length=50)),
                ('card_digits', models.CharField(max_length=4)),
                ('payment_status', models.CharField(max_length=50)),
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
                ('image', models.TextField(null=True)),
                ('ingredients', models.CharField(max_length=1000)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('stock_available', models.IntegerField(null=True)),
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
                ('email', models.CharField(max_length=1000)),
                ('address', models.CharField(max_length=1000)),
                ('phone', models.CharField(max_length=15)),
                ('allergies', models.CharField(max_length=1000)),
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
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('order_status', models.CharField(max_length=50)),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.cart')),
                ('payment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.payment_details')),
            ],
        ),
        migrations.CreateModel(
            name='Credit_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(max_length=20)),
                ('provider', models.CharField(max_length=50)),
                ('account_no', models.IntegerField(null=True)),
                ('expiry', models.DateField(null=True)),
                ('role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.roles')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.users')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.product_details'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luna.users'),
        ),
    ]
