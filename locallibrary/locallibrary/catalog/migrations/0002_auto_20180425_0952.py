# Generated by Django 2.0.4 on 2018-04-25 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Enter a Book's Natural Language (e.g. English, German, French, etc.)", max_length=200)),
            ],
        ),
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['lastName', 'firstName']},
        ),
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['dueBack'], 'permissions': (('canMarkReturned', 'Set Book As Returned'),)},
        ),
        migrations.RenameField(
            model_name='author',
            old_name='date_of_birth',
            new_name='dateOfBirth',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='date_of_death',
            new_name='dateOfDeath',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='first_name',
            new_name='firstName',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='last_name',
            new_name='lastName',
        ),
        migrations.RenameField(
            model_name='bookinstance',
            old_name='due_back',
            new_name='dueBack',
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='borrower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Enter a Book Genre (e.g. Science Fiction, Romance, Horror, etc.)', max_length=200),
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Language'),
        ),
    ]