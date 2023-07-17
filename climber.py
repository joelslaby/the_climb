from traits import Traits
import numpy as np

class Climber():
    def __init__(self, skills: Traits, name='tbd'):
        self.skills = skills
        self.cup_score = {
            'Qual': [],
            'Semi': [],
            'Final': [],
        }
        self.cup_rank = {
            'Qual': -1,
            'Semi': -1,
            'Final': -1,
        }
        
        self.name = name

class Team():
    def __init__(self, team_size = 5, names=None):
        self.team_size = team_size
        self.climbers = [Climber(
            Traits(
                *list(np.random.randint(
                        low = 0, 
                        high = 10, 
                        size = 4
            ))),
            name = names[i] if names else None
            ) for i in range(team_size)]