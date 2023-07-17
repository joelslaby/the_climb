import numpy as np
from traits import Traits
from climber import Climber, Team

class Boulder():
    def __init__(self):
        self.zone = Traits(*list(np.random.randint(low = 0, high = 5, size = 4)))
        self.top = self.zone + Traits(*list(np.random.randint(low = 0, high = 5, size = 4)))

    def calc_score(self, climbers: list[Climber] ) -> list:
        score_list = []
        for climber in climbers:
            top, zone, top_attempts, zone_attempts = 0, 0, 0, 0
            if all(c >= b for c, b in zip(climber.skills.list(), self.zone.list())):
                zone = 1

                zone_attempts = 6 - (sum(climber.skills.list()) - sum(self.zone.list()))
                if zone_attempts <= 0:
                    zone_attempts =  1

                if all(c >= b for c, b in zip(climber.skills.list(), self.top.list())):
                    top = 1

                    top_attempts = 6 - (sum(climber.skills.list()) - sum(self.top.list()))
                    if top_attempts <= 0:
                        top_attempts =  1
            
            boulder_score = [top, zone, top_attempts, zone_attempts]
            score_list.append(boulder_score)

        return score_list

class BoulderRound():
    def __init__(self, climbers: list[Climber] , boulders: list[Boulder] = None, nboulders = 4, pre='') -> None:
        self.climbers = climbers
        self.nc = len(climbers)
        self.scores = []
        self.total_score = []
        self.ranked_score = []
        self.ranked_climbers = []
        self.prefix=pre

        if not boulders:
            self.boulders = []
            for i in range(nboulders):
                self.boulders.append(Boulder())
        else:
            self.boulders = boulders


        for boulder in self.boulders:
            self.scores.append(boulder.calc_score(self.climbers))

        self.total_score = np.sum(self.scores, axis = 0)

        sorted_indices = sorted(
            range(self.nc), 
            key=lambda x: (
                -self.total_score[x][0], 
                -self.total_score[x][1], 
                self.total_score[x][2], 
                self.total_score[x][3]
            ))

        for rank, i in enumerate(sorted_indices):
            self.climbers[i].cup_rank[self.prefix] = rank
            self.climbers[i].cup_score[self.prefix] = list(self.total_score[i])
            self.ranked_climbers.append(self.climbers[i]) 
            self.ranked_score.append(self.total_score[i])
    
    def rank_boulder(self, boulder_idx = 0):
        ranked_score = []
        ranked_climbers = []

        sorted_indices = sorted(
            range(self.nc), 
            key=lambda x: (
                -self.scores[boulder_idx][x][0], 
                -self.scores[boulder_idx][x][1], 
                self.scores[boulder_idx][x][2], 
                self.scores[boulder_idx][x][3]
            ))

        for i in sorted_indices:
            self.climbers[i].cup_rank[self.prefix] = i
            ranked_climbers.append(self.climbers[i]) 
            ranked_score.append(self.scores[boulder_idx][i])

        return ranked_climbers, ranked_score

    def list_boulders(self):
        print('Boulders:')
        for i, boulder in enumerate(self.boulders):
            print(f"{i}) Z: {boulder.zone.list()} \t T: {boulder.top.list()}")
        print()

    def print_scores(self, climber_name = None, boulder_idx = None, ranked=False, top=None):
        if not ranked and not top:
            top = len(self.climbers)
        if climber_name:
            for i, climber in enumerate(self.climbers):
                if climber.name == climber_name:
                    if boulder_idx is not None:
                        print(f"Climber {climber_name} scored {get_score_string(self.scores[boulder_idx][i])} on boulder {boulder_idx}")
                        print()
                    else:
                        print(f"Climber {climber_name} scored:")
                        for j, _ in enumerate(self.boulders):
                            print(f"{j}) {get_score_string(self.scores[j][i])}")
                        print(f"For a total score of {get_score_string(self.total_score[i])}")
                        print()

        elif boulder_idx is not None:
            if ranked:
                ranked_climbers, ranked_scores = self.rank_boulder(boulder_idx=boulder_idx)
                print(f"For boulder {boulder_idx}:")
                for i, climber in enumerate(ranked_climbers):
                    print(f"{climber.name}) {get_score_string(ranked_scores[i])}")
                print()
            else:
                print(f"For boulder {boulder_idx}:")
                for i, climber in enumerate(self.climbers):
                    print(f"{climber.name}) {get_score_string(self.scores[boulder_idx][i])}")
                print()

        else:
            if ranked:
                print(f'{self.prefix} Round Total Ranked Scores:')
                for i, climber in enumerate(self.ranked_climbers[0:top]):
                    print(f"{i}) {climber.name}: {get_score_string(self.ranked_score[i])}")
                print()
            else:
                print(f'{self.prefix} Round Total Scores:')
                for i, climber in enumerate(self.climbers):
                    print(f"{climber.name}) {get_score_string(self.total_score[i])}")
                print()
        return

def get_score_string(score_list):
    return f"{score_list[0]}t_{score_list[1]}z_{score_list[2]}ta_{score_list[3]}za"