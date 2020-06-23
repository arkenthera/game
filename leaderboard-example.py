from leaderboard.leaderboard import Leaderboard

highscore_lb = Leaderboard('highscores')

for index in range(110000, 112000):
    highscore_lb.rank_member('member_%s' % index, index, )

highscore_lb.all_leaders()