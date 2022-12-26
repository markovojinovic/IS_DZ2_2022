import copy


class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass



class ExampleAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
                 ['2h', None], ['1v', None], ['0v', 3], ['1v', 1], ['2h', 1],
                 ['4h', 4], ['5v', 5]]
        domains = {var: [word for word in words] for var in variables}
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution



def find_field(variables, num):
    for var in variables:
        num_s = var.replace('h', '')
        num_s = num_s.replace('v', '')
        num_p = int(num_s)
        if num_p == num:
            return var



def check_word(word, curr_var, fields, width, variables):
    num_p = 0

    for i in range(len(word)):
        nums = curr_var
        nums = nums.replace('h', '')
        nums = nums.replace('v', '')
        num = int(nums)
        if curr_var[-1] == 'v':
            num += i * width
        else:
            num += i

        fil = find_field(variables, num)
        if fil is None:
            num_p += 1
            continue
        if fields[fil] == '' or fields[fil] == word[i]:
            num_p += 1
    return num_p == len(word)



def write_word(word, curr_var, fields, width, variables, control):

    for i in range(len(word)):
        nums = curr_var
        nums = nums.replace('h', '')
        nums = nums.replace('v', '')
        num = int(nums)
        if curr_var[-1] == 'v':
            num += i * width
        else:
            num += i

        fil = find_field(variables, num)

        ind1 = int(num / width)
        ind2 = int(num % width)
        if control[ind1][ind2] != -1:
            control[ind1][ind2] += 1

        if fil is None:
            continue
        fields[fil] = word[i]
    return



def delete_word(curr_var, fields, width, variables, control):

    for i in range(variables[curr_var]):
        nums = curr_var
        nums = nums.replace('h', '')
        nums = nums.replace('v', '')
        num = int(nums)
        if curr_var[-1] == 'v':
            num += i * width
        else:
            num += i

        fil = find_field(variables, num)

        ind1 = int(num / width)
        ind2 = int(num % width)
        if control[ind1][ind2] != -1:
            if control[ind1][ind2] == 1:
                control[ind1][ind2] = 0
                if fil is None:
                    continue
                fields[fil] = ''
            else:
                control[ind1][ind2] -= 1

    return



def rec_deg_function(solutions):
    num = 0
    for i in range(1, len(solutions)):
        if solutions[-i][1] is None:
            num += 1
        else:
            break
    return num * 2



def backtrack_function(variables, domains, solutions, fields, tiles, width, forward, deleted_domains, control):

    rec_deg = rec_deg_function(solutions)       # vraca duplu vrednost stepena rekurzije
    curr_var = solutions[-rec_deg][0]
    if rec_deg > 2:
        delete_word(curr_var, fields, width, variables, control)
    ind = solutions[-rec_deg][1]
    con = True
    new_ind = -1
    new_word = ""

    for word in domains[curr_var]:
        if domains[curr_var].index(word) != ind and check_word(word, curr_var, fields, width, variables):
            con = False
            new_ind = domains[curr_var].index(word)
            new_word = word
            break

    if con:
        solutions.append([curr_var, None, domains])
        if forward:
            retreve_words(curr_var, domains, deleted_domains)
        backtrack_function(variables, domains, solutions, fields, tiles, width, forward, deleted_domains, control)

        problem = False
        for word in domains[curr_var]:
            if check_word(word, curr_var, fields, width, variables):
                solutions.append([curr_var, domains[curr_var].index(word), domains])
                write_word(word, curr_var, fields, width, variables, control)
                problem = True
                break

        if problem:
            return False

    else:
        solutions.append([curr_var, new_ind, domains])
        write_word(new_word, curr_var, fields, width, variables, control)

    return True



class Backtracking(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):

        solution = []
        domains = {}
        fields = {}
        width = len(tiles[0])
        control = copy.deepcopy(tiles)
        for var in variables:
            fields[var] = ''
            domains[var] = []
            for word in words:
                if len(word) == variables[var]:
                    domains[var].append(word)

        for i in range(len(tiles)):
            for j in range(width):
                if not tiles[i][j]:
                    control[i][j] = 0
                else:
                    control[i][j] = -1

        for curr_var in variables:
            backtrack = True

            for word in domains[curr_var]:
                if check_word(word, curr_var, fields, width, variables):
                    write_word(word, curr_var, fields, width, variables, control)
                    solution.append([curr_var, domains[curr_var].index(word), domains])
                    backtrack = False
                    break

            if backtrack:
                solution.append([curr_var, None, domains])
                backtrack_function(variables, domains, solution, fields, tiles, width, False, [], control)

                for word in domains[curr_var]:
                    if check_word(word, curr_var, fields, width, variables):
                        write_word(word, curr_var, fields, width, variables, control)
                        solution.append([curr_var, domains[curr_var].index(word), domains])
                        break

        return solution



def forward_checking_function(fields, curr_var, variables, domains, width):

    kicked = {}

    for i in range(1, variables[curr_var]):
        kick = []

        nums = curr_var
        nums = nums.replace('h', '')
        nums = nums.replace('v', '')
        num = int(nums)
        if curr_var[-1] == 'v':
            num += i * width
        else:
            num += i

        fil = find_field(variables, num)
        if fil is None:
            continue

        kicked[fil] = []
        for word in domains[fil]:       # TODO: zapamti sta se brisalo iz domena i od strane koje promenljive
            if word[0] != fields[fil]:
                kick.append(domains[fil].index(word))
                kicked[fil].append(word)

        for ind in kick:
            domains[fil].pop(ind)

    return kicked



def retreve_words(curr_var, domains, deleted_domains):
    arr = deleted_domains[curr_var][-1]

    for field in arr:
        for word in arr[field]:
            domains[field].append(word)
    deleted_domains[curr_var].pop(-1)

    return



class ForwardChecking(Algorithm):                                       # TODO: proveriti da li treba da se prave duboke kopije domena
                                                                        # koji se dodaju u solutions, kad se prepravljaju domeni
    def get_algorithm_steps(self, tiles, variables, words):
        # ===========================================================================================
        # TODO: Obavezno prepraviti prema gore prepravljenim f-jama
        solution = []
        domains = {}
        fields = {}
        deleted_domains = {}
        width = len(tiles[0])
        control = copy.deepcopy(tiles)
        for var in variables:
            fields[var] = ''
            deleted_domains[var] = []
            domains[var] = []
            for word in words:
                if len(word) == variables[var]:
                    domains[var].append(word)

        for i in range(len(tiles)):
            for j in range(width):
                if not tiles[i][j]:
                    control[i][j] = 0
                else:
                    control[i][j] = -1

        for curr_var in variables:
            backtrack = True

            for word in domains[curr_var]:
                if check_word(word, curr_var, fields, width, variables):
                    write_word(word, curr_var, fields, width, variables, control)
                    kicked = forward_checking_function(fields, curr_var, variables, domains, width)
                    deleted_domains[curr_var].append(kicked)
                    solution.append([curr_var, domains[curr_var].index(word), domains])
                    backtrack = False
                    break

            if backtrack:
                retreve_words(curr_var, domains, deleted_domains)
                delete_word(curr_var, fields, width, variables, control)
                solution.append([curr_var, None, domains])
                backtrack_function(variables, domains, solution, fields, tiles, width, True, deleted_domains, control)
                for word in domains[curr_var]:
                    if check_word(word, curr_var, fields, width, variables):
                        write_word(word, curr_var, fields, width, variables, control)
                        kicked = forward_checking_function(fields, curr_var, variables, domains, width)
                        deleted_domains[curr_var].append(kicked)
                        solution.append([curr_var, domains[curr_var].index(word), domains])
                        break

        return solution



class ArcConsistency(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
                 ['2h', None], ['1v', None], ['0v', 3], ['1v', 1], ['2h', 1],
                 ['4h', 4], ['5v', 5]]
        domains = {var: [word for word in words] for var in variables}
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution
