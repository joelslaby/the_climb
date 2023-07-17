import numpy as np
from traits import Traits
from climber import Climber, Team
from boulder import Boulder
from boulder import BoulderRound as Boulder_Round

class WorldCup:
    def __init__(self, climbers, move_on: list[int] = [20, 6]):
        self.climbers = climbers
        self.move_on = move_on
        
        self.qual_round = Boulder_Round(self.climbers, nboulders=4, pre='Qual')
        self.semi_round = Boulder_Round(self.qual_round.ranked_climbers[0:self.move_on[0]], nboulders=4, pre='Semi')
        self.final_round = Boulder_Round(self.semi_round.ranked_climbers[0:self.move_on[1]], nboulders=4, pre='Final')
        self.stats = self.cup_stats()

    def round_progression_likelihood(self, output=False):
        '''
        Determine how often the top climbers in a round stay in the top in future rounds. 
        Note this doesn't consider their rank, only whether they stay in a high enough rank to move on.
        '''
        climbers_same_in_qual_to_final = 0
        climbers_same_in_semi_to_position = 0
        climbers_same_in_qual_to_position = 0
        climbers_same_in_qual_and_semi_to_position = 0

        for climber in self.qual_round.ranked_climbers[0:self.move_on[1]]:
            if climber in self.semi_round.ranked_climbers[0:self.move_on[1]]:
                climbers_same_in_qual_to_final  += 1

        for climber in self.semi_round.ranked_climbers[0:3]:
            if climber in self.final_round.ranked_climbers[0:3]:
                climbers_same_in_semi_to_position  += 1

        for climber in self.qual_round.ranked_climbers[0:3]:
            if climber in self.final_round.ranked_climbers[0:3]:
                climbers_same_in_qual_to_position  += 1
                if climber in self.semi_round.ranked_climbers[0:3]:
                    climbers_same_in_qual_and_semi_to_position  += 1

        if output:
            print(f"top {self.move_on[1]} in qual and semi: {climbers_same_in_qual_to_final}")
            print(f"top 3 in semi and final: {climbers_same_in_semi_to_position}")
            print(f"top 3 in qual and final: {climbers_same_in_qual_to_position}")
            print(f"top 3 in qual and semi and final: {climbers_same_in_qual_and_semi_to_position}")
            print()

        return {'qs': climbers_same_in_qual_to_final,
                'sf': climbers_same_in_semi_to_position,
                'qf': climbers_same_in_qual_to_position,
                'qsf': climbers_same_in_qual_and_semi_to_position}

    def same_rank_likelihood(self, output=False):
        same_qual_semi_rank = 0
        same_semi_final_rank = 0
        same_qual_final_rank = 0
        same_qual_semi_final_rank = 0

        for rank, climber in enumerate(self.qual_round.ranked_climbers[0:self.move_on[0]]):
            if climber == self.semi_round.ranked_climbers[rank]:
                same_qual_semi_rank += 1

        for rank, climber in enumerate(self.qual_round.ranked_climbers[0:self.move_on[1]]):
            if climber == self.final_round.ranked_climbers[rank]:
                same_qual_final_rank += 1
                if climber == self.semi_round.ranked_climbers[rank]:
                    same_qual_semi_final_rank += 1

        for rank, climber in enumerate(self.semi_round.ranked_climbers[0:self.move_on[1]]):
            if climber == self.final_round.ranked_climbers[rank]:
                same_semi_final_rank += 1

        if output:
            print(f"Same rank qual and semi: {same_qual_semi_rank}")
            print(f"Same rank semi and final: {same_semi_final_rank}")
            print(f"Same rank qual and final: {same_qual_final_rank}")
            print(f"Same rank qual and semi and final: {same_qual_semi_final_rank}")
            print()

        return {'qs': same_qual_semi_rank,
                'sf': same_semi_final_rank,
                'qf': same_qual_final_rank,
                'qsf': same_qual_semi_final_rank}

    def tied_round_likelihood(self, output=False):
        nbr_climbers_tied_qual = 0
        nbr_climbers_tied_semi = 0
        nbr_climbers_tied_final = 0

        for rank, climber in enumerate(self.qual_round.ranked_climbers[:-1]):
            if climber.cup_score['Qual'] == self.qual_round.ranked_climbers[rank+1].cup_score['Qual']:
                nbr_climbers_tied_qual += 1

        for rank, climber in enumerate(self.final_round.ranked_climbers[:-1]):
            if climber.cup_score['Semi'] == self.final_round.ranked_climbers[rank+1].cup_score['Semi']:
                nbr_climbers_tied_semi += 1

        for rank, climber in enumerate(self.final_round.ranked_climbers[:-1]):
            if climber.cup_score['Final'] == self.final_round.ranked_climbers[rank+1].cup_score['Final']:
                nbr_climbers_tied_final += 1
        
        if output:
            print(f'Quals ties: {nbr_climbers_tied_qual}')
            print(f'Semis ties: {nbr_climbers_tied_semi}')
            print(f'Finals ties: {nbr_climbers_tied_final}')

        return {'q': nbr_climbers_tied_qual,
                's': nbr_climbers_tied_semi,
                'f': nbr_climbers_tied_final}

    def same_score_likelihood(self, output=False):
        same_score_qual_semi = 0
        same_score_semi_final = 0
        same_score_qual_final = 0
        same_score_qual_semi_final = 0

        for climber in self.climbers:
            if climber.cup_rank['Semi'] != -1:
                if climber.cup_score['Qual'] == climber.cup_score['Semi']:
                    same_score_qual_semi += 1
                if climber.cup_rank['Final'] != -1:
                    if climber.cup_score['Semi'] == climber.cup_score['Final']:
                        same_score_semi_final += 1
                    if climber.cup_score['Qual'] == climber.cup_score['Final']:
                        same_score_qual_final += 1
                        if climber.cup_score['Semi'] == climber.cup_score['Final']:
                            same_score_qual_semi_final += 1

        if output:
            print(f"Same score qual and semi: {same_score_qual_semi}")
            print(f"Same score semi and final: {same_score_semi_final}")
            print(f"Same score qual and final: {same_score_qual_final}")
            print(f"Same score qual and semi and final: {same_score_qual_semi_final}")

        return {'qs': same_score_qual_semi,
                'sf': same_score_semi_final,
                'qf': same_score_qual_final,
                'qsf': same_score_qual_semi_final}

    def cup_stats(self):
        stats = {}
        stats['progression'] = self.round_progression_likelihood()
        stats['same_rank'] = self.same_rank_likelihood()
        stats['tied'] = self.tied_round_likelihood()
        stats['same_score'] = self.same_score_likelihood()
        return stats