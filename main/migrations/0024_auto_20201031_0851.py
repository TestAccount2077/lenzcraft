# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-10-31 06:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_cartproduct_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='product',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='products',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartProduct',
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
