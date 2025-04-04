from django.db import models
import csv
import os
from datetime import datetime
from django.conf import settings

class Voter(models.Model):
    """
    Model representing a registered voter in Newton, MA.
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    registration_date = models.DateField()
    party = models.CharField(max_length=2)
    precinct = models.CharField(max_length=10)

    voted_2020_state = models.BooleanField(default=False)
    voted_2021_town = models.BooleanField(default=False)
    voted_2021_primary = models.BooleanField(default=False)
    voted_2022_general = models.BooleanField(default=False)
    voted_2023_town = models.BooleanField(default=False)

    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.precinct})"


# Utility function to load data from CSV
def load_data(csv_path=None):
    """
    Load voter data from a CSV file into the database
    loads from data/newton_voters.csv inside the project
    """
    def parse_bool(val):
        return val.strip().lower() == 'true'

    if not csv_path:
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'newton_voters.csv')

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0

        for row in reader:
            try:
                voter = Voter(
                    first_name=row['First Name'].strip(),
                    last_name=row['Last Name'].strip(),
                    street_number=row['Residential Address - Street Number'].strip(),
                    street_name=row['Residential Address - Street Name'].strip(),
                    apartment_number=row['Residential Address - Apartment Number'].strip() or None,
                    zip_code=row['Residential Address - Zip Code'].strip(),
                    date_of_birth=datetime.strptime(row['Date of Birth'].strip(), '%Y-%m-%d').date(),
                    registration_date=datetime.strptime(row['Date of Registration'].strip(), '%Y-%m-%d').date(),

                    party=row['Party Affiliation'].strip(),
                    precinct=row['Precinct Number'].strip(),

                    voted_2020_state=parse_bool(row['v20state']),
                    voted_2021_town=parse_bool(row['v21town']),
                    voted_2021_primary=parse_bool(row['v21primary']),
                    voted_2022_general=parse_bool(row['v22general']),
                    voted_2023_town=parse_bool(row['v23town']),

                    voter_score=int(row['voter_score']),
                )
                voter.save()
                count += 1

            except Exception as e:
                print(f"Error on row {row}: {e}")

        print(f"{count} voters successfully loaded.")
