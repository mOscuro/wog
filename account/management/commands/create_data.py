#===============================================================================
# Created on 30 nov. 2016
# @author: Matthieu
#===============================================================================

from django.core.management.base import BaseCommand

from account.models import User
from exercise.exercise_constants import AMATEUR, MEDIUM, BODYWEIGHT
from exercise.models import Exercise
from workout.models import Workout, Step, Round


class Command(BaseCommand):
    
    help = 'Populates the database (used during development)'
    
    def handle(self, *args, **options):
        self.create_dev_data()
        self.stdout.write(self.style.SUCCESS('Successfully created'))

    def create_dev_data(self):

        # Constants used to identify workout category
        STAFF = 1
        ONESHOT = 2
        PRIVATE = 3
        PUBLIC = 4
        
        #=======================================================================
        # CREATE 1 SUPERUSER
        #=======================================================================
        print("Creating 1 superuser...")
        try:
            User.objects.create_superuser(username="moscuro",
                                          email="root@root.com",
                                          password="Password44$")
            #From AllAuth > todo later
            #EmailAddress.objects.create(user=suser, email=suser.email, primary=True, verified=True)
        except Exception as e:
            self.stdout.write(self.style.SUCCESS('Problem occured during superuser creation'))
            self.stdout.write(e)

        #=======================================================================
        # CREATE 10 USERS
        #=======================================================================
        print("Creating 10 users...")
        for i in range(1, 11):
            # Create 10 standard users
            User.objects.create_user(email="user%d@wogether.com" % i,
                                        username="user%d" % i,
                                        password="Password44$")

        admin_user = User.objects.get(email="root@root.com")

        #=======================================================================
        # CREATE SOME EXERCISES
        #=======================================================================
        print("Creating some exercise...")
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
        
        #=======================================================================
        # ADMINISTRATORS WORKOUTS
        #=======================================================================
        
        # Aphrodite Workout pattern
        print("Creating some admin workout...")
        admin_workout1 = Workout.objects.create(name="Aphrodite", type=STAFF, creator=admin_user)
        cpt_rep = 50
        for cpt_round in range(1, 5):
            admin_workout1_rounds = Round.objects.create(workout=admin_workout1, nb_repeat=1)
            Step.objects.create(round=admin_workout1_rounds, exercise=burpees, nb_rep=cpt_rep)
            Step.objects.create(round=admin_workout1_rounds, exercise=air_squats, nb_rep=cpt_rep)
            Step.objects.create(round=admin_workout1_rounds, exercise=situps, nb_rep=cpt_rep)
            cpt_rep -= 10
        
        # Metis Workout pattern ============================================================
        admin_workout2 = Workout.objects.create(name="Metis", type=STAFF, creator=admin_user)
        # Metis - Round 1
        admin_workout2_round1 = Round.objects.create(workout=admin_workout2, nb_repeat=1)
        Step.objects.create(round=admin_workout2_round1, exercise=burpees, nb_rep=10)
        Step.objects.create(round=admin_workout2_round1, exercise=climbers, nb_rep=10)
        Step.objects.create(round=admin_workout2_round1, exercise=jumps, nb_rep=10)
        # Metis - Round 2
        admin_workout2_round2 = Round.objects.create(workout=admin_workout2, nb_repeat=1)
        Step.objects.create(round=admin_workout2_round2, exercise=burpees, nb_rep=25)
        Step.objects.create(round=admin_workout2_round2, exercise=climbers, nb_rep=25)
        Step.objects.create(round=admin_workout2_round2, exercise=jumps, nb_rep=25)
        # Metis - Round 3
        admin_workout2_round3 = Round.objects.create(workout=admin_workout2, nb_repeat=1)
        Step.objects.create(round=admin_workout2_round3, exercise=burpees, nb_rep=10)
        Step.objects.create(round=admin_workout2_round3, exercise=climbers, nb_rep=10)
        Step.objects.create(round=admin_workout2_round3, exercise=jumps, nb_rep=10)

        # Nyx Workout pattern =============================================================
        admin_workout3 = Workout.objects.create(name="Nyx", type=STAFF, creator=admin_user)
        # Nyx - Round 1
        admin_workout3_round1 = Round.objects.create(workout=admin_workout3, nb_repeat=1)
        Step.objects.create(round=admin_workout3_round1, exercise=situps, nb_rep=10)
        Step.objects.create(round=admin_workout3_round1, exercise=leg_levers, nb_rep=10)
        Step.objects.create(round=admin_workout3_round1, exercise=standups, nb_rep=10)
        # Nyx - Round 2
        admin_workout3_round2 = Round.objects.create(workout=admin_workout3, nb_repeat=1)
        Step.objects.create(round=admin_workout3_round2, exercise=situps, nb_rep=25)
        Step.objects.create(round=admin_workout3_round2, exercise=leg_levers, nb_rep=25)
        Step.objects.create(round=admin_workout3_round2, exercise=standups, nb_rep=25)
        # Nyx - Round 3
        admin_workout3_round3 = Round.objects.create(workout=admin_workout3, nb_repeat=1)
        Step.objects.create(round=admin_workout3_round3, exercise=situps, nb_rep=10)
        Step.objects.create(round=admin_workout3_round3, exercise=leg_levers, nb_rep=10)
        Step.objects.create(round=admin_workout3_round3, exercise=standups, nb_rep=10)
               
        #=======================================================================
        # USER 1 WORKOUTS
        #=======================================================================
        print("Creating users workout...")
        user1 = User.objects.get(email="user1@wogether.com")
        user1_workout1 = Workout.objects.create(name="Private Custom Workout 1", type=PRIVATE, creator=user1)
        # 5 Rounds pattern
        user1_workout1_5round = Round.objects.create(workout=user1_workout1, nb_repeat=5)
        Step.objects.create(round=user1_workout1_5round, exercise=pullups, nb_rep=10)
        Step.objects.create(round=user1_workout1_5round, exercise=pushups, nb_rep=20)
        Step.objects.create(round=user1_workout1_5round, exercise=situps, nb_rep=30)
        Step.objects.create(round=user1_workout1_5round, exercise=lunges, nb_rep=40)
            
        user1_workout2 = Workout.objects.create(name="Public Custom Workout 1", type=PUBLIC, creator=user1)
        # 4 Rounds pattern
        user1_workout2_4round = Round.objects.create(workout=user1_workout2, nb_repeat=4)
        Step.objects.create(round=user1_workout2_4round, exercise=burpees, nb_rep=20)
        Step.objects.create(round=user1_workout2_4round, exercise=pushups, nb_rep=20)
        Step.objects.create(round=user1_workout2_4round, exercise=situps, nb_rep=20)
        Step.objects.create(round=user1_workout2_4round, exercise=air_squats, nb_rep=20)
 
        #=======================================================================
        # USER 2 WORKOUTS
        #=======================================================================
        user2 = User.objects.get(email="user2@wogether.com")
        # 10 minutes AMRAP pattern
        user2_workout1 = Workout.objects.create(name="Private Custom Workout 2", type=PRIVATE, creator=user2, amrap=10)
        user2_workout1_default_round = Round.objects.create(workout=user2_workout1, default=True)
        Step.objects.create(round=user2_workout1_default_round, exercise=lunges, nb_rep=15)
        Step.objects.create(round=user2_workout1_default_round, exercise=pushups, nb_rep=10)
        Step.objects.create(round=user2_workout1_default_round, exercise=lunges, nb_rep=15)
        Step.objects.create(round=user2_workout1_default_round, exercise=situps, nb_rep=20)
        
        # 20 minutes AMRAP pattern            
        user2_workout2 = Workout.objects.create(name="Public Custom Workout 2", type=PUBLIC, creator=user2, amrap=20)
        user2_workout2_default_round = Round.objects.create(workout=user2_workout2, default=True)
        Step.objects.create(round=user2_workout2_default_round, exercise=burpees, nb_rep=15)
        Step.objects.create(round=user2_workout2_default_round, exercise=situps, nb_rep=15)
        Step.objects.create(round=user2_workout2_default_round, exercise=air_squats, nb_rep=15)

        print("Done.")