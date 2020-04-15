
from math import gcd


class CyclicExecutive:

    def __init__(self):
        self.__number_of_tasks = None
        self.__tasks_parameters = dict()
        self.__sorted_tasks_parameters = dict()
        self.__tasks_moves = list()
        self.__overall_computation_time = 0
        self.__max_task_period = 0
        self.__greatest_common_divisor = None
        self.__least_common_multiple = None

    def set_tasks(self):
        self.__number_of_tasks = int(input('\n(CE) Enter number of tasks: '))

        for x in range(self.__number_of_tasks):
            worst_case_computation = int(input('(CE) Enter worst-case computation for task {x}: '.format(x=x+1)))
            task_period = int(input('(CE) Enter task period for task {x}: '.format(x=x+1)))
            # task array = [worst case computation, task period]
            self.__tasks_parameters[x + 1] = [worst_case_computation, task_period]

        # sort based on task period
        self.__sorted_tasks_parameters = {k: v for k, v in sorted(
            self.__tasks_parameters.items(), key=lambda item: item[1][1])}

        # set max task period
        self.__max_task_period = (list(self.__sorted_tasks_parameters.items())[-1][1])[1]

    def calculate_greatest_common_divisor(self):
        # default to first task period
        self.__greatest_common_divisor = (list(self.__sorted_tasks_parameters.items())[0][1])[1]
        for task, parameters in self.__sorted_tasks_parameters.items():
            self.__greatest_common_divisor = gcd(self.__greatest_common_divisor, parameters[1])
        return self.__greatest_common_divisor

    def calculate_least_common_multiple(self):
        # default to first task period
        self.__least_common_multiple = (list(self.__sorted_tasks_parameters.items())[0][1])[1]
        for task, parameters in self.__sorted_tasks_parameters.items():
            self.__least_common_multiple = (self.__least_common_multiple * parameters[1]) // gcd(
                self.__least_common_multiple, parameters[1])
        return self.__least_common_multiple

    def is_feasible(self):
        first_worst_computations = (list(self.__sorted_tasks_parameters.items())[0][1])[0]
        for task, parameters in self.__sorted_tasks_parameters.items():
            if (parameters[0] >= self.__greatest_common_divisor) or (first_worst_computations + parameters[0] >
                                                                     self.__greatest_common_divisor):
                return False

        return True

    def schedule_tasks(self):
        task_tracker = dict()
        while True:
            temp_overall_time = self.__overall_computation_time
            for task, parameter in self.__sorted_tasks_parameters.items():
                if task not in task_tracker:
                    task_tracker[task] = dict()
                    task_tracker[task]['track'] = 0
                task_tracker[task]['period'] = int(self.__overall_computation_time / parameter[1]) + 1
                if parameter[1] * task_tracker[task]['period'] - self.__overall_computation_time < parameter[0]:
                    self.__overall_computation_time = parameter[1] * task_tracker[task]['period']
                if task_tracker[task]['track'] < task_tracker[task]['period']:
                    task_move = list()
                    task_move.append(task)
                    task_move.append(self.__overall_computation_time)
                    self.__overall_computation_time = self.__overall_computation_time + parameter[0]
                    task_move.append(self.__overall_computation_time)
                    self.__tasks_moves.append(task_move)
                    task_tracker[task]['track'] += 1
            # if there is no move left in the current period, jump to next period
            if temp_overall_time == self.__overall_computation_time:
                self.__overall_computation_time = self.__greatest_common_divisor * task_tracker[1]['period']
            # stop the loop after 2 major cycle
            if self.__overall_computation_time > 2 * self.__least_common_multiple:
                break

    def get_task_parameters(self):
        return self.__sorted_tasks_parameters

    def get_task_moves(self):
        return self.__tasks_moves

    def get_max_task_period(self):
        return self.__max_task_period

    def print_chart(self):
        axis = ''
        for j in range(2 * (self.__tasks_moves[-1][2] + 2)):
            axis += '-'
        print('\nm = minor cycle - M = Major cycle')
        print('\n{:<{d}}'.format('|', d=2 * self.__least_common_multiple), end='')
        for x in range(1, 3):
            print('{:<{d}}'.format('M', d=2 * self.__least_common_multiple), end='')

        print('\n{:<{d}}'.format('|', d=2 * self.__greatest_common_divisor), end='')
        for x in range(1, self.__least_common_multiple//self.__greatest_common_divisor * 2 + 1):
            print('{:<{d}}'.format('m', d=2 * self.__greatest_common_divisor), end='')

        print('\n\n', end='')
        previous_move_end = 0
        for move in self.__tasks_moves:
            if move[1] % self.__least_common_multiple == 0:
                print('{:>{d}}'.format('|', d=2 * (move[1] - previous_move_end) + 1), end='')
            elif previous_move_end != move[1]:
                print('{:>{d}}'.format('|', d=2 * (move[1] - previous_move_end + 1)), end='')

            print('{:^{d}}'.format('J' + str(move[0]), d=2 * (move[2] - move[1] - 1)), end='')
            print('|', end='')
            previous_move_end = move[2]

        print('\n' + axis + '>')

        for x in range(0, self.__least_common_multiple//self.__greatest_common_divisor * 2 + 1):
            print('{:<{d}}'.format(x * self.__greatest_common_divisor, d=2 * self.__greatest_common_divisor), end='')
        print()


def run_ce():
    ce = CyclicExecutive()
    ce.set_tasks()
    print('\nMinor Cycle: {}'.format(ce.calculate_greatest_common_divisor()))
    print('Major Cycle: {}'.format(ce.calculate_least_common_multiple()))
    print('Duration of tasks will {feasible} into the Minor Cycle.'.format(
        feasible='fit' if ce.is_feasible() else 'NOT fit'))
    ce.schedule_tasks()
    if ce.is_feasible():
        ce.print_chart()
