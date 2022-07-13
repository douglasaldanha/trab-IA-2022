import hashgame as hg

def minmax(state, player):
    winner = hg.who_win(state)

    if winner != None or hg.state_full(state):
        return {
            '_': (0, None, None),
            'x': (-1, None, None),
            'o': (1, None, None),
            None: (1, None, None)
        }[winner]
    
    if player == 'x':
        max_found, i_found, j_found = -2, None, None

        for i in range(3):
            for j in range(3):
                if state[i][j] == '_':
                    new_state = hg.copy_state(state)
                    new_state[i][j] = 'o'
                    v = minmax(new_state, 'o')[0]
                    if v > max_found:
                        max_found, i_found, j_found = v, i, j

        return max_found, i_found, j_found

    else:
        min_found, i_found, j_found = 2, None, None

        for i in range(3):
            for j in range(3):
                if state[i][j] == '_':
                    new_state = hg.copy_state(state)
                    new_state[i][j] = 'x'
                    v = minmax(new_state, 'x')[0]
                    if v < min_found:
                        min_found, i_found, j_found = v, i, j

        return min_found, i_found, j_found

class HashGameMinMax(hg.HashGameGUI):
    def __init__(self):
        super().__init__()

    def on_click(self, i, j):
        #player x (Human)
        if self.end == False:
            if self.state[i][j] == '_': 
                self.state[i][j] = 'x' #change state
            else:
                return
            self.check_and_draw_winner()

        #player o (AI)
        if self.end == False:
            ov, oi, oj = minmax(hg.copy_state(self.state), 'x')
            self.state[oi][oj] = 'o'
            self.check_and_draw_winner()
            
if __name__ == '__main__':
    obj = HashGameMinMax()
    obj.show()