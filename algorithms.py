import copy


class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass



def check_word(word, curr_var, fields, width):
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



def write_word(word, curr_var, fields, width, control):

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
        if check_word(word, curr_var, fields, width):

            solution.append([curr_var, domains[curr_var].index(word), domains])
            write_word(word, curr_var, fields, width, control)

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



def find_field(variables, num):
    for var in variables:
        num_s = var.replace('h', '')
        num_s = num_s.replace('v', '')
        num_p = int(num_s)
        if num_p == num:
            return var



def get_index_from_dif(ind1s, ind2s, ind1e, ind2e):
    if ind1e != ind1s:
        return abs(ind1e - ind1s)
    else:
        return abs(ind2e - ind2s)



def forward_check_function(level, variables, domains, fields, width, solution, control):

    if level == len(variables):
        return True

    curr_var = variable_from_lvl(variables, level)

    for word in domains[curr_var]:
        if check_word(word, curr_var, fields, width):

            solution.append([curr_var, domains[curr_var].index(word), domains])
            write_word(word, curr_var, fields, width, control)

            new_domain = copy.deepcopy(domains)
            new_domain[curr_var] = [word]

            empty_domain = domain_pruning(new_domain, curr_var, word, width)

            if empty_domain:
                if forward_check_function(level + 1, variables, new_domain, fields, width, solution, control):
                    return True

                solution.append([variable_from_lvl(variables, level + 1), None, domains])
                delete_word(curr_var, fields, width, variables, control)

            else:
                delete_word(curr_var, fields, width, variables, control)

    return False



def domain_pruning(domains, curr_var, word, width):

    ind1_start = int(curr_var[:-1:]) // width
    ind2_start = int(curr_var[:-1:]) % width
    ind1_end = ind1_start
    ind2_end = ind2_start
    if curr_var[-1] == 'v':
        ind1_end += len(word) - 1
    else:
        ind2_end += len(word) - 1

    for variable in domains:
        if variable != curr_var and len(domains[variable]) > 0:

            c_ind1_start = int(variable[:-1:]) // width
            c_ind2_start = int(variable[:-1:]) % width
            c_ind1_end = c_ind1_start
            c_ind2_end = c_ind2_start
            if variable[-1] == 'v':
                c_ind1_end += len(domains[variable][0]) - 1
            else:
                c_ind2_end += len(domains[variable][0]) - 1

            indexes = cross(ind1_start, ind2_start, ind1_end, ind2_end, curr_var[-1],c_ind1_start,
                        c_ind2_start, c_ind1_end, c_ind2_end, variable[-1])

            if indexes != []:
                ind2 = indexes[0]
                ind1 = indexes[1]

                ind = 0
                while ind < len(domains[variable]):

                    if word[ind2] != domains[variable][ind][ind1]:
                        domains[variable].remove(domains[variable][ind])
                    else:
                        ind += 1

                if len(domains[variable]) == 0:
                    return False

    return True


def cross(ind1_start, ind2_start, ind1_end, ind2_end, dir1, c_ind1_start, c_ind2_start, c_ind1_end, c_ind2_end, dir2):
    if dir1 == dir2:
        return []

    if dir2 != 'h' and dir1 != 'v':
        if c_ind2_start in range(ind2_start, ind2_end + 1):
            if ind1_start in range(c_ind1_start, c_ind1_end + 1):
                return [c_ind2_start - ind2_start, ind1_start - c_ind1_start]
    else:
        if c_ind1_start in range(ind1_start, ind1_end + 1):
            if ind2_start in range(c_ind2_start, c_ind2_end + 1):
                return [c_ind1_start - ind1_start, ind2_start - c_ind2_start]

    return []



class ForwardChecking(Algorithm):

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

        forward_check_function(0, variables, domains, fields, width, solution, control)

        return solution
