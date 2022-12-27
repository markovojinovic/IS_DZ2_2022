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

        ind1 = int(num / width)
        ind2 = int(num % width)

        if fields[ind1][ind2] == '' or fields[ind1][ind2] == word[i]:
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

        ind1 = int(num / width)
        ind2 = int(num % width)

        if control[ind1][ind2] != -1:
            control[ind1][ind2] += 1

        fields[ind1][ind2] = word[i]

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

        ind1 = int(num / width)
        ind2 = int(num % width)
        if control[ind1][ind2] != -1:
            if control[ind1][ind2] == 1:
                control[ind1][ind2] = 0
                fields[ind1][ind2] = ''
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



def variable_from_lvl(variables, lvl):
    num = 0
    for var in variables:
        if num == lvl:
            return var
        num += 1



def bactrack_search(level, variables, domains, fields, width, solution, control):

    if level == len(variables):
        return True

    curr_var = variable_from_lvl(variables, level)

    for word in domains[curr_var]:
        if check_word(word, curr_var, fields, width, variables):

            solution.append([curr_var, domains[curr_var].index(word), domains])
            write_word(word, curr_var, fields, width, variables, control)

            new_domain = copy.deepcopy(domains)
            new_domain[curr_var] = [word]

            if bactrack_search(level + 1, variables, new_domain, fields, width, solution, control):
                return True

            solution.append([variable_from_lvl(variables, level + 1), None, domains])
            delete_word(curr_var, fields, width, variables, control)

    return False


class Backtracking(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):

        solution = []
        domains = {}
        width = len(tiles[0])
        control = copy.deepcopy(tiles)
        fields = copy.deepcopy(tiles)

        for var in variables:
            domains[var] = []
            for word in words:
                if len(word) == variables[var]:
                    domains[var].append(word)

        for i in range(len(tiles)):
            for j in range(width):
                if not tiles[i][j]:
                    control[i][j] = 0
                    fields[i][j] = ''
                else:
                    control[i][j] = -1
                    fields[i][j] = -1

        bactrack_search(0, variables, domains, fields, width, solution, control)

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



class ForwardChecking(Algorithm):

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

        # TODO: prepraviti i poziv i f-ju
        bactrack_search(0, variables, domains, fields, width, solution, control)

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
