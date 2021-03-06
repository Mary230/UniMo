# Generated by Django 3.2 on 2021-06-03 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_student_competition'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='points',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='student',
            name='university_name',
            field=models.CharField(choices=[('КФУ', 'Казанский Федеральный Университет'), ('ИЭИП', 'Институт экологии и природопользования'), ('ИГНТ', 'Институт геологии и нефтегазовых технологий'), ('ИММЛ', 'Институт математики и механики им.Н.И.Лобачевского')], default='КФУ', help_text='Укажите полное название вашего института', max_length=50),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='catalog.user')),
                ('subject', models.CharField(max_length=70)),
                ('university_name', models.CharField(choices=[('КФУ', 'Казанский Федеральный Университет'), ('ИЭИП', 'Институт экологии и природопользования'), ('ИГНТ', 'Институт геологии и нефтегазовых технологий'), ('ИММЛ', 'Институт математики и механики им.Н.И.Лобачевского')], default='КФУ', help_text='Укажите полное название вашего института', max_length=50)),
                ('student_list', models.ManyToManyField(help_text='Select your students', to='catalog.Student')),
            ],
        ),
    ]
