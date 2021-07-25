# Generated by Django 3.2.5 on 2021-07-21 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_alter_order_status_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status_order',
            field=models.CharField(choices=[('Recipient', (('DR', 'Draft'), ('TD', 'To Do'), ('DN', 'Done'), ('СR', 'Canceled by Recipient'), ('L', 'Lost'))), ('Sender', (('IP', 'In Progress'), ('IR', 'In Road'), ('CS', 'Canceled by Sender'))), ('Creator', (('CC', 'Canceled by Creator'),))], default='DR', max_length=2),
        ),
    ]