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



def cross(x11, y11, x21, y21, dir_first, x12, y12, x22, y22, dir_second):       # TODO: prepraviti na svoje

    if dir_first == dir_second:
        return []

    if dir_first == 'h' and dir_second == 'v':
        if x11 in range(x12, x22 + 1) and y12 in range(y11, y21 + 1):
            return [y12 - y11, x11 - x12]
    else:
        if y11 in range(y12, y22 + 1) and x12 in range(x11, x21 + 1):
            return [x12 - x11, y11 - y12]
    return []



def get_index_from_dif(ind1s, ind2s, ind1e, ind2e):
    if ind1e != ind1s:
        return abs(ind1e - ind1s)
    else:
        return abs(ind2e - ind2s)

def forward_check_function(level, variables, domains, fields, width, solution, control, tiles):

    if level == len(variables):
        return True

    curr_var = variable_from_lvl(variables, level)

    for word in domains[curr_var]:
        if check_word(word, curr_var, fields, width):

            solution.append([curr_var, domains[curr_var].index(word), domains])
            write_word(word, curr_var, fields, width, control)

            new_domain = copy.deepcopy(domains)
            new_domain[curr_var] = [word]
            ret = domain_narrowing(new_domain, curr_var, word, tiles)

            if not ret:
                delete_word(curr_var, fields, width, variables, control)
                continue

            if forward_check_function(level + 1, variables, new_domain, fields, width, solution, control, tiles):
                return True

            solution.append([variable_from_lvl(variables, level + 1), None, domains])
            delete_word(curr_var, fields, width, variables, control)

    return False



def domain_narrowing(domains, variable, value, tiles):
    row_index = int(variable[:-1:]) // len(tiles[0])
    column_index = int(variable[:-1:]) % len(tiles[0])
    row_index_end = row_index
    column_index_end = column_index
    if variable[-1] == 'h':
        column_index_end += len(value) - 1
    else:
        row_index_end += len(value) - 1
    for var in domains:
        if var != variable and len(domains[var]) > 0:
            domain = domains[var]
            value_row_index = int(var[:-1:]) // len(tiles[0])
            value_column_index = int(var[:-1:]) % len(tiles[0])
            value_row_index_end = value_row_index
            value_column_index_end = value_column_index
            if var[-1] == 'h':
                value_column_index_end += len(domain[0]) - 1
            else:
                value_row_index_end += len(domain[0]) - 1

            # info_list contains, in order: row_index and column_index of intersection,
            # indices of chars in both words
            info_list = words_intersecting(variable[-1], var[-1],
                                           [row_index, column_index, row_index_end, column_index_end],
                                           [value_row_index, value_column_index, value_row_index_end,
                                            value_column_index_end])
            if len(info_list) == 0:
                continue
            variable_index, var_index = info_list[2], info_list[3]
            ind = 0
            while ind < len(domain):
                val = domain[ind]
                if value[variable_index] != val[var_index]:
                    domain.remove(val)
                else:
                    ind += 1
            if len(domain) == 0:
                return False

    return True


def words_intersecting(var1_orientation: str, var2_orientation: str, coordinates1: list, coordinates2: list):
    if var1_orientation == var2_orientation:
        return []
    x11, y11, x21, y21 = coordinates1
    x12, y12, x22, y22 = coordinates2
    if var1_orientation == 'h' and var2_orientation == 'v':
        if x11 in range(x12, x22 + 1) and y12 in range(y11, y21 + 1):
            return [x11, y12, y12 - y11, x11 - x12]
    else:
        if y11 in range(y12, y22 + 1) and x12 in range(x11, x21 + 1):
            return [x12, y11, x12 - x11, y11 - y12]
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

        forward_check_function(0, variables, domains, fields, width, solution, control, tiles)

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
