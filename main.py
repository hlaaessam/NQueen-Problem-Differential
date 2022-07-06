import numpy as np
import random
import time

queens_num=int(input('Enter Number of N Queens \n'))
maxiter=int(input('Enter Number of maxiter Queens \n'))

# N Queens indices : [[0,0], [1,2], [2,3], [3,0]]
def cost_func(queens):
    score = 0

    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            x1, y1 = queens[i][0], queens[i][1]
            x2, y2 = queens[j][0], queens[j][1]
            x_diff = x1 - x2
            y_diff = y1 - y2
            if x_diff != 0 and y_diff != 0 and abs(x_diff / y_diff) != 1:
                score += 1

    return score
#bounds=[x:(0,n-1), y:(0,n-1)]
#bound(0,3)
#queens (Q1,Q2,Q3,Q4)
#Q1=(x,y)
#Q2=(x,y)
def ensure_bounds(queens, bounds):
    #cycle through each variable in queens
    new_queens = []
    for i in range(len(queens)):
        queen = queens[i]
        new_queen = []
        for j in range(len(queen)):
            #variable exceedes the minumimum boundary (x[0)
            if queen[j] < bounds[j][0]:
                new_queen.append(bounds[j][0])
            # variable exceedes the maximum boundary
            if queen[j] > bounds[j][1]:
                new_queen.append(bounds[j][1])
            # the varibale is fine
            if bounds[j][0] <= queen[j] <= bounds[j][1]:
                new_queen.append(queen[j])

        new_queens.append(new_queen)

    return new_queens


def create_population(popsize, bounds, queens_num):
    population = []

    for i in range(0, popsize):
        queens = []

        for j in range(queens_num):
            queen = []
            # bounds=[x:(0,n-1), y:(0,n-1)]
            queen.append(random.randint(bounds[0][0], bounds[0][1]))
            queen.append(random.randint(bounds[1][0], bounds[1][1]))

            queens.append(queen)

        population.append(queens)

    return population



def queens_to_board(queens):
    board = []
    for i in range(len(queens)):
        row = []
        for j in range(len(queens)):
            row.append('0')
        board.append(row)

    for i in range(len(queens)):
        queen = queens[i]
        # queen => [0, 3]
        x, y = queen[0], queen[1]
        board[x][y] = '1'

    return board


def print_board(board):
    print('--------------------------------\n')
    for i in range(len(board)):
        for j in range(len(board)):
            print(board[i][j] + "  ", end=" ")
        print()
        print()
    print('--------------------------------')


def main(cost_func, bounds, popsize, mutate, recombination, maxiter, queens_num):
    random.seed(time.time())
    population = create_population(popsize, bounds, queens_num)
    print("population : ", population)
    #cycle through each generation
    for i in range(1, maxiter + 1):
        random.seed(time.time())
        print('GENERATION :', i)
        gen_score = []
        #cycle through eash individual(board or matrix) in population
        for j in range(0, popsize):
            #Select matrix
            canidates = list(range(0, popsize))
            canidates.remove(j)
            random_index = random.sample(canidates, 3)

            queens1 = population[random_index[0]]
            queens2 = population[random_index[1]]
            queens3 = population[random_index[2]]
            target_queens = population[j]

            # queens1 = [Q1, Q2, Q3, Q4]
            # queens2 = [Qa, Qb, Qc, Qd]
            # q1_q2_diff = [Q1-Qa, Q2-Qb, Q3-Qb, Q4-Qc]
            q1_q2_diff = []
            for k in range(len(queens1)):
                q1_q2_diff.append([abs(index1 - index2) for index1, index2 in zip(queens1[k], queens2[k])])

            mutant_queens = []
            for k in range(len(queens1)):
                mutant_queens.append([int(index3 + mutate * diff) for index3, diff in zip(queens3[k], q1_q2_diff[k])])

            mutant_queens = ensure_bounds(mutant_queens, bounds)

            trial_queens = []
            for k in range(len(mutant_queens)):
                target_queen = target_queens[k]
                mutant_queen = mutant_queens[k]
                trial_queen = []
                for l in range(len(mutant_queen)):
                    crossover = random.random()
                    if crossover <= recombination:
                        trial_queen.append(mutant_queen[l])
                    else:
                        trial_queen.append(target_queen[l])

                trial_queens.append(trial_queen)

            trial_score = cost_func(trial_queens)
            target_score = cost_func(target_queens)

            if trial_score > target_score:
                population[j] = trial_queens
                gen_score.append(trial_score)
                print('  > score:', trial_score, ', queens:', trial_queens)
            else:
                gen_score.append(target_score)
                print('  > score:', target_score, ', queens:', target_queens)

        gen_avg = sum(gen_score) / popsize
        gen_best = max(gen_score)
        gen_sol = population[gen_score.index(gen_best)]

        print()
        print('       >GENERATION AVERAGE:', gen_avg)
        print('       >GENERATION BEST:', gen_best)
        print('       >BEST SOLUTION:', gen_sol)
        print('       >Queens number:', queens_num)
        print('       >Optimal score:', int(queens_num * (queens_num - 1) / 2), '\n')

        print_board(queens_to_board(gen_sol))

        if gen_best == (queens_num * (queens_num - 1) / 2):
            print('The optimal solution has been reached.')
            return gen_sol

    return gen_sol


#queens_num = 6
bounds = [(0, queens_num - 1), (0, queens_num - 1)]
popsize = queens_num * 3
mutate = .5
recombination = 0.7
#maxiter = 2000

main(cost_func, bounds, popsize, mutate, recombination, maxiter, queens_num)

