import random
from django.core.management.base import BaseCommand
from academics.models import Subject, ClassLevel

class Command(BaseCommand):
    help = 'Populate the database with pre-defined Pakistani and Montessori subjects.'

    def handle(self, *args, **options):
        pak_subjects = [
            'English', 'Urdu', 'Mathematics', 'Science', 
            'Biology', 'Computer', 'Islamiat', 'Pak Studies'
        ]
        
        montessori_subjects = [
            'Practical Life', 'Sensorial', 'Language', 
            'Mathematics', 'Culture & Geography'
        ]

        classes = ClassLevel.objects.all()
        if not classes:
            self.stdout.write(self.style.NOTICE("No ClassLevels found. Creating default classes..."))
            default_classes = [
                ('Playgroup', 0), ('Nursery', 0), ('Prep', 0),
                ('Grade 1', 1), ('Grade 2', 2), ('Grade 3', 3),
                ('Grade 4', 4), ('Grade 5', 5), ('Grade 6', 6),
                ('Grade 7', 7), ('Grade 8', 8), ('Grade 9', 9),
                ('Grade 10', 10)
            ]
            for name, val in default_classes:
                ClassLevel.objects.get_or_create(name=name, defaults={'numeric_value': val})
            classes = ClassLevel.objects.all()

        all_predefined = list(set(pak_subjects + montessori_subjects))
        
        count = 0
        for name in all_predefined:
            # Generate a random 6-digit code
            code = str(random.randint(100000, 999999))
            
            # Use filter to avoid MultipleObjectsReturned
            subject = Subject.objects.filter(name=name).first()
            created = False
            
            if not subject:
                subject = Subject.objects.create(name=name, code=code)
                created = True
            
            if created or subject:
                # Assign to all classes
                subject.class_levels.set(classes)
                if created:
                    count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created subject: {name} ({code})'))
                else:
                    self.stdout.write(self.style.NOTICE(f'Subject already exists: {name}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {count} subjects.'))
