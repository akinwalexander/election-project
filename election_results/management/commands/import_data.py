from django.core.management.base import BaseCommand
from election_results.models import State, LGA, Ward, PollingUnit, Party, AnnouncedPUResult, AnnouncedLGAResult
import MySQLdb
from django.conf import settings

class Command(BaseCommand):
    help = 'Import data from MySQL database'

    def handle(self, *args, **options):
        # Connect to MySQL database
        db = MySQLdb.connect(
            host=settings.DATABASES['default']['HOST'],
            user=settings.DATABASES['default']['USER'],
            passwd=settings.DATABASES['default']['PASSWORD'],
            db=settings.DATABASES['default']['NAME']
        )
        
        cursor = db.cursor()
        
        # Import States
        cursor.execute("SELECT * FROM states")
        for row in cursor.fetchall():
            State.objects.get_or_create(
                state_id=row[0],
                state_name=row[1]
            )
        
        # Import LGAs
        cursor.execute("SELECT * FROM lga")
        for row in cursor.fetchall():
            LGA.objects.get_or_create(
                uniqueid=row[0],
                lga_id=row[1],
                lga_name=row[2],
                state_id=row[3],
                lga_description=row[4],
                entered_by_user=row[5],
                date_entered=row[6],
                user_ip_address=row[7]
            )
        
        #Import Wards
        cursor.execute("SELECT * FROM wards")
        for row in cursor.fetchall():
            Ward.objects.get_or_create(
                uniqueid=row[0],
                ward_id=row[1],
                ward_name=row[2],
                lga_id=row[3],
                ward_description=row[4],
                entered_by_user=row[5],
                date_entered=row[6],
                user_ip_address=row[7]
            )
        # Import Polling Units
        cursor.execute("SELECT * FROM polling_units")
        for row in cursor.fetchall():
            PollingUnit.objects.get_or_create(
                uniqueid=row[0],
                polling_unit_id=row[1],
                ward_id=row[2],
                lga_id=row[3],
                uniquewardid=row[4],
                polling_unit_number=row[5],
                polling_unit_name=row[6],
                polling_unit_description=row[7],
                lat=row[8],
                long=row[9],
                entered_by_user=row[10],
                date_entered=row[11],
                user_ip_address=row[12]
            )
        # Import Parties
        cursor.execute("SELECT * FROM parties")
        for row in cursor.fetchall():
            Party.objects.get_or_create(
                partyid=row[0],
                partyname=row[1]
            )
        # Import Announced Polling Unit Results
        cursor.execute("SELECT * FROM announced_pu_results")
        for row in cursor.fetchall():
            AnnouncedPUResult.objects.get_or_create(
                polling_unit_id=row[0],
                party_abbreviation=row[1],
                party_score=row[2],
                entered_by_user=row[3],
                date_entered=row[4],
                user_ip_address=row[5]
            )
        # Import Announced LGA Results
        cursor.execute("SELECT * FROM announced_lga_results")
        for row in cursor.fetchall():
            AnnouncedLGAResult.objects.get_or_create(
                lga_id=row[0],
                party_abbreviation=row[1],
                party_score=row[2],
                entered_by_user=row[3],
                date_entered=row[4],
                user_ip_address=row[5]
            )
        
        
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))