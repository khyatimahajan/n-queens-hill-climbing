import random
from pprint import pprint

def input_size_board():
	''' Take input from user for size of board '''
	n = input("Enter an integer for the size of the board: ")
	return int(n)

def print_board(board, n):
	''' Helper function for printing board '''
	print('Board:')
	for i in range(len(board)):
		print(str(board[i]) + ' ', end='')
		if (i + 1) % n == 0:
			print()
	print('H value: ', determine_h_cost(board, n))
	print('---------------------')

def generate_random_board(n):
	''' Generates a random board for initialization, queens have been calculated row-wise '''
	generated_board = []
	for i in range(n):
		j = random.randint(0, n-1)
		row = [0]*n
		row[j] = 1
		generated_board.extend(row)
	return generated_board

def find_collisions(board, n):
	''' Helper function for calculating queen position collisions '''
	collisions = 0
	occurences = []
	max_index = len(board)
	for i in range(max_index):
		# For each queen on the board, count collisions with other queens, and which kind of collisions they are
		if board[i] == 1:
			for x in range(1, n):
				# checking above current index
				if (i - n*x >= 0):
					north = i - n*x
					# direction north
					if (board[north] == 1):
						collisions += 1
						occurences.append('north: '+str(i)+' and '+str(north))
					# direction northwest
					if (int((north - x)/n) == int(north/n)) and (north - x) >= 0:
						northwest = north - x
						if (board[northwest] == 1):
							collisions += 1
							occurences.append('northwest: '+str(i)+' and '+str(northwest))
					# direction northeast
					if (int((north + x)/n) == int(north/n)):
						northeast = north + x
						if (board[northeast] == 1):
							collisions += 1
							occurences.append('northeast: '+str(i)+' and '+str(northeast))
				# checking below current index
				if (i + n*x < max_index):
					south = i + n*x
					# direction south
					if (board[south] == 1):
						collisions += 1
						occurences.append('south: '+str(i)+' and '+str(south))
					# direction southwest
					if (int((south - x)/n) == int(south/n)):
						southwest = south - x
						if (board[southwest] == 1):
							collisions += 1
							occurences.append('southwest: '+str(i)+' and '+str(southwest))
					# direction southeast
					if (int((south + x)/n) == int(south/n)) and ((south + x) < max_index):
						southeast = south + x
						if (board[southeast] == 1):
							collisions += 1
							occurences.append('southeast: '+str(i)+' and '+str(southeast))
				# direction west (for completeness)
				if (int((i - x)/n) == int(i/n)) and (i - x >= 0):
					west = i - x
					if (board[west] == 1):
						collisions += 1
						occurences.append('west: '+str(i)+' and '+str(west))
				# direction east (for completeness)
				if (int((i + x)/n) == int(i/n)) and (i + x < max_index):
					east = i + x
					if (board[east] == 1):
						collisions += 1
						occurences.append('east: '+str(i)+' and '+str(east))
	return [collisions, occurences]

def determine_h_cost(board, n, verbose=False):
	''' Function to determine heuristic - total collisions on the board '''
	collisions, occurences = find_collisions(board, n)
	if verbose:
		pprint(occurences)
	# return half the collisions, since each colliding position is counted twice from the helper function
	return int(collisions/2)

def find_child(board, n, sideways_move=False):
	''' Function to find the successor from all the children by comparing the heuristic values of moving the queens row-wise '''
	child = []
	current_h_cost = determine_h_cost(board, n)
	same_cost_children = []

	for row in range(n):
		for col in range(n):
			# Build a temporary board which changes the position of the queen in the current board
			temp_board = []
			temp_board.extend(board[:row*n])
			new_row = [0]*n
			new_row[col] = 1
			temp_board.extend(new_row)
			temp_board.extend(board[(row+1)*n:])
			temp_h_cost = determine_h_cost(temp_board, n)
			if (sideways_move):
				# if sideways moves are allowed, and the generated child heuristic cost is less than or equal to the current lowest heuristic cost, save generated child and update current lowest heuristic cost 
				if (temp_board != board):
					if (temp_h_cost < current_h_cost):
						child = temp_board.copy()
						current_h_cost = temp_h_cost
					elif (temp_h_cost == current_h_cost):
						same_cost_children.append(temp_board)
						x = random.randint(0, len(same_cost_children)-1)
						child = same_cost_children[x]
			else:
				# if sideways moves are not allowed, and the generated child heuristic cost is less than the current lowest heuristic cost, save generated child and update current lowest heuristic cost
				if (temp_board != board) and (temp_h_cost < current_h_cost):
					child = temp_board.copy()
					current_h_cost = temp_h_cost
	return child

def steepest_hill_climbing(board, n, max_iterations=200, verbose=False):
	''' Steepest Hill climbing without sideways move, returns the current steps and whether the run succeeded or not '''
	steps = 0
	success = False
	current_board = board.copy()

	if (verbose):
		print_board(current_board, n)
	
	# Until maximum iterations are reached, search for a solution
	for i in range(max_iterations):
		# Get the least heuristic child from the find child helper function
		next_node = find_child(current_board, n).copy()

		if (verbose and len(next_node) != 0):
			print_board(next_node, n)
		
		# Update the steps taken for this run
		steps += 1
		# If we have a child and its heuristic cost is zero, we have a solution
		if (len(next_node) != 0) and (determine_h_cost(next_node, n) == 0):
			success = True
			break
		# If we do not get a child, we cannot get a solution
		if (len(next_node) == 0):
			break
		# Make the current child the next node
		current_board = next_node.copy()
	return steps, success

def steepest_hill_climbing_with_sideways_move(board, n, max_iterations=200, verbose=False):
	''' Steepest Hill climbing with sideways move, returns the current steps and whether the run succeeded or not '''
	steps = 0
	success = False
	current_board = board.copy()
	
	if (verbose):
		print_board(current_board, n)
	
	# Until maximum iterations are reached, search for a solution
	for i in range(max_iterations):
		# Get the least heuristic child from the find child helper function
		next_node = find_child(current_board, n, sideways_move=True).copy()
		
		if (verbose and len(next_node) != 0):
			print_board(next_node, n)
		
		# Update the steps taken for this run
		steps += 1
		# If we have a child and its heuristic cost is zero, we have a solution
		if (len(next_node) != 0) and (determine_h_cost(next_node, n) == 0):
			success = True
			break
		# If we do not get a child, we cannot get a solution
		if (len(next_node) == 0):
			break
		# Make the current child the next node
		current_board = next_node.copy()
	return steps, success

def steepest_hill_climbing_with_random_restart(board, n, max_iterations=200, verbose=False):
	''' Steepest Hill climbing with random restart and without sideways move, returns the current steps and whether the run succeeded or not '''
	steps = 0
	success = False
	rr = 0
	current_board = board.copy()
	
	if (verbose):
		print_board(current_board, n)
	
	# Until maximum iterations are reached, search for a solution
	for i in range(max_iterations):
		# Get the least heuristic child from the find child helper function
		next_node = find_child(current_board, n).copy()
		
		if (verbose and len(next_node) != 0):
			print_board(next_node, n)
		
		# Update the steps taken for this run
		steps += 1
		# If we do not get a child, restart the search by generating another random board
		if (len(next_node) == 0):
			next_node = generate_random_board(n)
			# Maintain count of restarts made
			rr += 1
		# If the current node's heuristic cost is zero, we have a solution
		if (determine_h_cost(next_node, n) == 0):
			success = True
			break
		# Make the current child the next node
		current_board = next_node.copy()
	return steps, success, rr


def steepest_hill_climbing_with_random_restart_and_sideways_move(board, n, max_iterations=200, verbose=False):
	''' Steepest Hill climbing with random restart and sideways move, returns the current steps and whether the run succeeded or not '''
	steps = 0
	success = False
	rr = 0
	current_board = board.copy()
	
	if (verbose):
		print_board(current_board, n)

	# Until maximum iterations are reached, search for a solution
	for i in range(max_iterations):
		# Get the least heuristic child from the find child helper function
		next_node = find_child(current_board, n, sideways_move=True).copy()
		
		if (verbose and len(next_node) != 0):
			print_board(next_node, n)
		
		# Update the steps taken for this run
		steps += 1
		# If we do not get a child, restart the search by generating another random board
		if (len(next_node) == 0):
			next_node = generate_random_board(n)
			# Maintain count of restarts made
			rr += 1
		# If the current node's heuristic cost is zero, we have a solution
		if (determine_h_cost(next_node, n) == 0):
			success = True
			break
		# Make the current child the next node
		current_board = next_node.copy()
	return steps, success, rr

n = input_size_board()
iterations = 200

# Script for running functions
print('Steepest Hill Climbing:')
success_rate_steepest_hill_climbing = False
step_count_rate_steepest_hill_climbing_success = 0
step_count_rate_steepest_hill_climbing_failure = 0
for i in range(3):
	print('Run ' + str(i + 1) + ':')
	step_count, success = steepest_hill_climbing(generate_random_board(n), n, verbose=True)
	if (success):
		print('Success.')
		step_count_rate_steepest_hill_climbing_success += step_count
	else:
		print('Failure.')
		step_count_rate_steepest_hill_climbing_failure += step_count
	success_rate_steepest_hill_climbing += success
for i in range(3, iterations):
	step_count, success = steepest_hill_climbing(generate_random_board(n), n)
	if (success):
		step_count_rate_steepest_hill_climbing_success += step_count
	else:
		step_count_rate_steepest_hill_climbing_failure += step_count
	success_rate_steepest_hill_climbing += success
print('Success rate: ' + str(success_rate_steepest_hill_climbing/iterations))
print('Failure rate: ' + str(1-(success_rate_steepest_hill_climbing/iterations)))
print('Average steps until success: ' + str(step_count_rate_steepest_hill_climbing_success/success_rate_steepest_hill_climbing))
print('Average steps until failure: ' + str(step_count_rate_steepest_hill_climbing_failure/(iterations - success_rate_steepest_hill_climbing)))

print('Steepest Hill Climbing with Sideways Move:')
success_rate_steepest_hill_climbing_sm = False
step_count_rate_steepest_hill_climbing_success_sm = 0
step_count_rate_steepest_hill_climbing_failure_sm = 0
for i in range(3):
	print('Run ' + str(i + 1) + ':')
	step_count, success = steepest_hill_climbing_with_sideways_move(generate_random_board(n), n, verbose=True)
	if (success):
		print('Success.')
		step_count_rate_steepest_hill_climbing_success_sm += step_count
	else:
		print('Failure.')
		step_count_rate_steepest_hill_climbing_failure_sm += step_count
	success_rate_steepest_hill_climbing_sm += success
for i in range(3, iterations):
	step_count, success = steepest_hill_climbing_with_sideways_move(generate_random_board(n), n)
	if (success):
		step_count_rate_steepest_hill_climbing_success_sm += step_count
	else:
		step_count_rate_steepest_hill_climbing_failure_sm += step_count
	success_rate_steepest_hill_climbing_sm += success
print('Success rate: ' + str(success_rate_steepest_hill_climbing_sm/iterations))
print('Failure rate: ' + str(1-(success_rate_steepest_hill_climbing_sm/iterations)))
print('Average steps until success: ' + str(step_count_rate_steepest_hill_climbing_success_sm/success_rate_steepest_hill_climbing_sm))
print('Average steps until failure: ' + str(step_count_rate_steepest_hill_climbing_failure_sm/(iterations - success_rate_steepest_hill_climbing_sm)))

print('Steepest Hill Climbing with Random Restart:')
success_rate_steepest_hill_climbing_rr = False
step_count_rate_steepest_hill_climbing_success_rr = 0
step_count_rate_steepest_hill_climbing_failure_rr = 0
random_restarts = 0
for i in range(iterations):
	step_count, success, rr = steepest_hill_climbing_with_random_restart(generate_random_board(n), n)
	random_restarts += rr
	if (success):
		print('Success.')
		step_count_rate_steepest_hill_climbing_success_rr += step_count
	else:
		print('Failure.')
		step_count_rate_steepest_hill_climbing_failure_rr += step_count
	success_rate_steepest_hill_climbing_rr += success
print('Success rate: ' + str(success_rate_steepest_hill_climbing_rr/iterations))
print('Average steps taken: ' + str(step_count_rate_steepest_hill_climbing_success_rr/success_rate_steepest_hill_climbing_rr))
print('Random restarts required: ' + str(random_restarts))

print('Steepest Hill Climbing with Random Restart and Sideways Move:')
success_rate_steepest_hill_climbing_rrsm = False
step_count_rate_steepest_hill_climbing_success_rrsm = 0
step_count_rate_steepest_hill_climbing_failure_rrsm = 0
random_restarts_sm = 0
for i in range(iterations):
	step_count, success, rr_sm = steepest_hill_climbing_with_random_restart_and_sideways_move(generate_random_board(n), n)
	random_restarts_sm += rr_sm
	if (success):
		print('Success.')
		step_count_rate_steepest_hill_climbing_success_rrsm += step_count
	else:
		print('Failure.')
		step_count_rate_steepest_hill_climbing_failure_rrsm += step_count
	success_rate_steepest_hill_climbing_rrsm += success
print('Success rate: ' + str(success_rate_steepest_hill_climbing_rrsm/iterations))
print('Average steps taken: ' + str(step_count_rate_steepest_hill_climbing_success_rrsm/success_rate_steepest_hill_climbing_rrsm))
print('Random restarts required with sideways move: ' + str(random_restarts_sm))