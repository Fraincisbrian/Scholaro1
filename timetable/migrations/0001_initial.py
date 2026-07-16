import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimetableEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday')], max_length=3)),
                ('period', models.PositiveSmallIntegerField(choices=[(1, '1st Period (7:30 - 8:15)'), (2, '2nd Period (8:15 - 9:00)'), (3, '3rd Period (9:00 - 9:45)'), (4, '4th Period (10:00 - 10:45)'), (5, '5th Period (10:45 - 11:30)'), (6, '6th Period (11:30 - 12:15)'), (7, '7th Period (13:00 - 13:45)'), (8, '8th Period (13:45 - 14:30)')])),
                ('school_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable_entries', to='academics.schoolclass')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetable_entries', to='academics.subject')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='timetable_entries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Timetable entries',
                'ordering': ['day', 'period'],
                'unique_together': {('school_class', 'day', 'period')},
            },
        ),
    ]
