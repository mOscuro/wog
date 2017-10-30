#===============================================================================
# Created on 30 nov. 2016
# @author: Matthieu
#===============================================================================

from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand

from wog_exercise.exercise_constants import AMATEUR, MEDIUM, BODYWEIGHT, CROSSTRAINING
from wog_exercise.models import Exercise, Equipment
from wog_round.helpers import create_round, create_step
from wog_user.models import User
from wog_workout.models import Workout


def create_equipments():
    barbell = Equipment.objects.create(name="Barbell")
    dumbell = Equipment.objects.create(name="Dumbell")
    jumprope = Equipment.objects.create(name="Jump Rope")

def create_exercises():
    burpees = Exercise.objects.create(name="Burpees", level=AMATEUR, type=BODYWEIGHT)
    air_squats = Exercise.objects.create(name="Air Squats", level=AMATEUR, type=BODYWEIGHT)
    lunges = Exercise.objects.create(name="Lunges", level=AMATEUR, type=BODYWEIGHT)
    situps = Exercise.objects.create(name="Situps", level=AMATEUR, type=BODYWEIGHT)
    leg_levers = Exercise.objects.create(name="Leg Levers", level=AMATEUR, type=BODYWEIGHT)
    standups = Exercise.objects.create(name="Standups", level=MEDIUM, type=BODYWEIGHT)
    climbers = Exercise.objects.create(name="Climbers", level=AMATEUR, type=BODYWEIGHT)
    jumps = Exercise.objects.create(name="Jumps", level=AMATEUR, type=BODYWEIGHT)
    pushups = Exercise.objects.create(name="Pushups", level=AMATEUR, type=BODYWEIGHT)
    pullups = Exercise.objects.create(name="Pullups", level=MEDIUM, type=BODYWEIGHT)
    running = Exercise.objects.create(name="Running", level=AMATEUR, type=BODYWEIGHT)

    double_unders = Exercise.objects.create(name="Double Unders", level=MEDIUM, type=CROSSTRAINING, equipment=jumprope)
    dumbell_deadlift = Exercise.objects.create(name="Dumbell Deadlift", level=MEDIUM, type=CROSSTRAINING, equipment=dumbell)
    dumbell_front_squat = Exercise.objects.create(name="Dumbell Front Squat", level=MEDIUM, type=CROSSTRAINING, equipment=dumbell)

class Command(BaseCommand):
    
    help = 'Populates the database (used during development)'
    
    def handle(self, *args, **options):
        self.create_dev_data()
        self.stdout.write(self.style.SUCCESS('Data successfully created'))

    def create_dev_data(self):

        #=======================================================================
        # CREATE 1 SUPERUSER
        #=======================================================================
        print("Creating 1 superuser...")
        try:
            super_user = User.objects.create_superuser(username="moscuro",
                                          email="root@root.com",
                                          password="Password44$")
            #From AllAuth
            EmailAddress.objects.create(user=super_user, email=super_user.email, primary=True, verified=True)
        except Exception as e:
            self.stdout.write(self.style.SUCCESS('Problem occured during superuser creation'))
            self.stdout.write(e)

        #=======================================================================
        # CREATE 10 USERS
        #=======================================================================
        print("Creating 10 users...")
        for i in range(1, 11):
            # Create 10 standard users
            basic_user = User.objects.create_user(email="user%d@wogether.com" % i,
                                        username="user%d" % i,
                                        password="Password44$")
            EmailAddress.objects.create(user=basic_user, email=basic_user.email, primary=True, verified=True)
        admin_user = User.objects.get(email="root@root.com")

        #=======================================================================
        # CREATE SOME EQUIPMENTS
        #=======================================================================
        print("Creating some equiments...")
        create_equipments()

        #=======================================================================
        # CREATE SOME EXERCISES
        #=======================================================================
        print("Creating some exercises...")
        create_exercises()

        #=======================================================================
        # ADMINISTRATORS WORKOUTS
        #=======================================================================
        
        # Aphrodite Workout pattern
        print("Creating some admin workout...")
        admin_workout1 = Workout.objects.create(name="Aphrodite", is_public=True, is_staff=True, creator=admin_user)
        cpt_rep = 50
        for cpt_round in range(5):
            admin_workout1_rounds = create_round({'workout' : admin_workout1})
            create_step({'round' : admin_workout1_rounds, 'exercise' : burpees, 'nb_rep' : cpt_rep})
            create_step({'round' : admin_workout1_rounds, 'exercise' : air_squats, 'nb_rep' : cpt_rep})
            create_step({'round' : admin_workout1_rounds, 'exercise' : situps, 'nb_rep' : cpt_rep})
            cpt_rep -= 10
        
        # Metis Workout pattern ============================================================
        admin_workout2 = Workout.objects.create(name="Metis", is_public=False, is_staff=True, creator=admin_user)
        # Metis - Round 1
        admin_workout2_round1 = create_round({'workout' : admin_workout2})
        create_step({'round' : admin_workout2_round1, 'exercise' : burpees, 'nb_rep' : 10})
        create_step({'round' : admin_workout2_round1, 'exercise' : climbers, 'nb_rep' : 10})
        create_step({'round' : admin_workout2_round1, 'exercise' : jumps, 'nb_rep' : 10})
        # Metis - Round 2
        admin_workout2_round2 = create_round({'workout' : admin_workout2})
        create_step({'round' : admin_workout2_round2, 'exercise' : burpees, 'nb_rep' : 25})
        create_step({'round' : admin_workout2_round2, 'exercise' : climbers, 'nb_rep' : 25})
        create_step({'round' : admin_workout2_round2, 'exercise' : jumps, 'nb_rep' : 25})
        # Metis - Round 3
        admin_workout2_round3 = create_round({'workout' : admin_workout2})
        create_step({'round' : admin_workout2_round3, 'exercise' : burpees, 'nb_rep' : 10})
        create_step({'round' : admin_workout2_round3, 'exercise' : climbers, 'nb_rep' : 10})
        create_step({'round' : admin_workout2_round3, 'exercise' : jumps, 'nb_rep' : 10})

        # Nyx Workout pattern =============================================================
        admin_workout3 = Workout.objects.create(name="Nyx", is_public=True, is_staff=True, creator=admin_user)
        # Nyx - Round 1
        admin_workout3_round1 = create_round({'workout' : admin_workout3})
        create_step({'round' : admin_workout3_round1, 'exercise' : situps, 'nb_rep' : 10})
        create_step({'round' : admin_workout3_round1, 'exercise' : leg_levers, 'nb_rep' : 10})
        create_step({'round' : admin_workout3_round1, 'exercise' : standups, 'nb_rep' : 10})
        # Nyx - Round 2
        admin_workout3_round2 = create_round({'workout' : admin_workout3})
        create_step({'round' : admin_workout3_round2, 'exercise' : situps, 'nb_rep' : 25})
        create_step({'round' : admin_workout3_round2, 'exercise' : leg_levers, 'nb_rep' : 25})
        create_step({'round' : admin_workout3_round2, 'exercise' : standups, 'nb_rep' : 25})
        # Nyx - Round 3
        admin_workout3_round3 = create_round({'workout' : admin_workout3})
        create_step({'round' : admin_workout3_round3, 'exercise' : situps, 'nb_rep' : 10})
        create_step({'round' : admin_workout3_round3, 'exercise' : leg_levers, 'nb_rep' : 10})
        create_step({'round' : admin_workout3_round3, 'exercise' : standups, 'nb_rep' : 10})
               
        #=======================================================================
        # USER 1 WORKOUTS
        #=======================================================================
        print("Creating users workout...")
        user1 = User.objects.get(email="user1@wogether.com")
        user1_workout1 = Workout.objects.create(name="Private Custom Workout 1", creator=user1)
        # 5 Rounds pattern
        user1_workout1_5round = create_round({'workout' : user1_workout1, 'nb_repeat' : 5})
        create_step({'round' : user1_workout1_5round, 'exercise' : pullups, 'nb_rep' : 10})
        create_step({'round' : user1_workout1_5round, 'exercise' : pushups, 'nb_rep' : 20})
        create_step({'round' : user1_workout1_5round, 'exercise' : situps, 'nb_rep' : 30})
        create_step({'round' : user1_workout1_5round, 'exercise' : lunges, 'nb_rep' : 40})
            
        user1_workout2 = Workout.objects.create(name="Public Custom Workout 1", is_public=True, creator=user1)
        # 4 Rounds pattern
        user1_workout2_4round = create_round({'workout' : user1_workout2, 'nb_repeat' : 4})
        create_step({'round' : user1_workout2_4round, 'exercise' : burpees, 'nb_rep' : 20})
        create_step({'round' : user1_workout2_4round, 'exercise' : pushups, 'nb_rep' : 20})
        create_step({'round' : user1_workout2_4round, 'exercise' : situps, 'nb_rep' : 20})
        create_step({'round' : user1_workout2_4round, 'exercise' : air_squats, 'nb_rep' : 20})
        
        user1_workout3 = Workout.objects.create(name="Public Custom Workout 2", is_public=True, creator=user1)
        # Mixing Steps and Rounds pattern
        user1_workout3_round1 = create_round({'workout' : user1_workout3, 'nb_repeat' : 1})
        create_step({'round' : user1_workout3_round1, 'exercise' : running, 'nb_rep' : 1, 'distance' : '1000'})
        user1_workout3_5rounds = create_round({'workout' : user1_workout3, 'nb_repeat' : 5})
        create_step({'round' : user1_workout3_5rounds, 'exercise' : pullups, 'nb_rep' : 20})
        create_step({'round' : user1_workout3_5rounds, 'exercise' : pushups, 'nb_rep' : 40})
        create_step({'round' : user1_workout3_5rounds, 'exercise' : air_squats, 'nb_rep' : 60})
        user1_workout3_round7 = create_round({'workout' : user1_workout3, 'nb_repeat' : 1})
        create_step({'round' : user1_workout3_round7, 'exercise' : running, 'nb_rep' : 1, 'distance' : '1000'})
 
        #=======================================================================
        # USER 2 WORKOUTS
        #=======================================================================
        user2 = User.objects.get(email="user2@wogether.com")
        # 10 minutes AMRAP pattern
        user2_workout1 = Workout.objects.create(name="Private Custom Workout 2", creator=user2, amrap=10)
        user2_workout1_round1 = create_round({'workout' : user2_workout1, 'nb_repeat' : 1})
        create_step({'round' : user2_workout1_round1, 'exercise' : pushups, 'nb_rep' : 10})
        create_step({'round' : user2_workout1_round1, 'exercise' : lunges, 'nb_rep' : 15})
        create_step({'round' : user2_workout1_round1, 'exercise' : lunges, 'nb_rep' : 15})
        create_step({'round' : user2_workout1_round1, 'exercise' : situps, 'nb_rep' : 20})
        
        # 20 minutes AMRAP pattern            
        user2_workout2 = Workout.objects.create(name="Public Custom Workout 2", is_public=True, creator=user2, amrap=20)
        user2_workout2_round1 = create_round({'workout' : user2_workout2, 'nb_repeat' : 1})
        create_step({'round' : user2_workout2_round1, 'exercise' : burpees, 'nb_rep' : 15})
        create_step({'round' : user2_workout2_round1, 'exercise' : situps, 'nb_rep' : 15})
        create_step({'round' : user2_workout2_round1, 'exercise' : air_squats, 'nb_rep' : 15})

        print("Done.")