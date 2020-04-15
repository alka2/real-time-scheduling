
"""
W.I.P. for partial move
"""


class RateMonotonic:

    def __init__(self):
        self.__number_of_tasks = None
        self.__tasks_parameters = dict()
        self.__sorted_tasks_parameters = dict()
        self.__tasks_moves = dict()
        self.__overall_computation_time = 0
        self.__max_task_period = 0
        self.__smallest_worst_execution = None
        self.__smallest_task_period = None

    def set_tasks(self):
        self.__number_of_tasks = int(input('\n(RM) Enter number of tasks: '))

        for x in range(self.__number_of_tasks):
            worst_case_computation = int(input('(RM) Enter worst-case computation for task {x}: '.format(x=x+1)))
            task_period = int(input('(RM) Enter task period for task {x}: '.format(x=x+1)))
            # task array = [worst case computation, task period, Ui --> Ci/Ti]
            self.__tasks_parameters[x + 1] = [worst_case_computation, task_period, worst_case_computation/task_period]

        # sort based on task period
        self.__sorted_tasks_parameters = {k: v for k, v in sorted(
            self.__tasks_parameters.items(), key=lambda item: item[1][1])}

        # set max task period
        self.__max_task_period = (list(self.__sorted_tasks_parameters.items())[-1][1])[1]

        self.__smallest_task_period = (list(self.__sorted_tasks_parameters.items())[0][1])[1]

        # sort based on worst computation time to find the smallest worst execution time
        sorted_worst_execution = {k: v for k, v in sorted(
            self.__tasks_parameters.items(), key=lambda item: item[1][0])}

        self.__smallest_worst_execution = (list(sorted_worst_execution.items())[0][1])[0]

    def calculate_upper_bound(self):
        return self.__number_of_tasks * (2**(1/self.__number_of_tasks) - 1)

    def is_feasible(self):
        ui_sum = 0
        for task, parameters in self.__sorted_tasks_parameters.items():
            ui_sum += parameters[2]
        return True if ui_sum <= self.calculate_upper_bound() else False

    def schedule_tasks(self):
        # incomplete_task = None
        while True:
            temp_overall_time = self.__overall_computation_time
            for task, parameter in self.__sorted_tasks_parameters.items():
                # temp_overall_time_internal = self.__overall_computation_time
                # nearest_task_distance = 0
                if task not in self.__tasks_moves:
                    self.__tasks_moves[task] = dict()
                    self.__tasks_moves[task]['moves'] = []
                self.__tasks_moves[task]['period'] = int(self.__overall_computation_time / parameter[1]) + 1
                if parameter[1] * self.__tasks_moves[task]['period'] - self.__overall_computation_time < parameter[0]:
                    self.__overall_computation_time = parameter[1] * self.__tasks_moves[task]['period']
                if len(self.__tasks_moves[task]['moves']) < self.__tasks_moves[task]['period']:
                    task_move = list()
                    task_move.append(self.__overall_computation_time)
                    self.__overall_computation_time = self.__overall_computation_time + parameter[0]
                    task_move.append(self.__overall_computation_time)
                    self.__tasks_moves[task]['moves'].append(task_move)

                # # try for partial move
                # if temp_overall_time_internal == self.__overall_computation_time:
                #     if not incomplete_task:
                #         incomplete_task = dict()
                #         incomplete_task['task'] = task
                #         incomplete_task['moves'] = list()
                #         incomplete_task['partialMove'] = 0
                #     if incomplete_task['task'] == task:
                #         for t, p in self.__sorted_tasks_parameters.items():
                #             if 0 < p[1] - self.__overall_computation_time < parameter[1]:
                #                 incomplete_task['moves'].append(self.__overall_computation_time)
                #                 partial_move = p[1] - self.__overall_computation_time
                #                 incomplete_task['partialMove'] += partial_move
                #                 self.__overall_computation_time += partial_move
                #                 incomplete_task['moves'].append(self.__overall_computation_time)
                #                 if incomplete_task['partialMove'] == parameter[0]:
                #                     for m in incomplete_task['moves']:
                #                         self.__tasks_moves[task]['moves'].append(m)
                #                     incomplete_task = None
                #                 break
            # if there is no move left in the current period, jump to next period
            if temp_overall_time == self.__overall_computation_time:
                self.__overall_computation_time += self.__smallest_worst_execution
            # stop the loop after 2 max period cycle
            if self.__overall_computation_time > 2 * self.__max_task_period:
                break

    def get_task_parameters(self):
        return self.__sorted_tasks_parameters

    def get_task_moves(self):
        return self.__tasks_moves

    def get_max_task_period(self):
        return self.__max_task_period

    def print_chart(self):
        sorted_task_moves = {k: v for k, v in sorted(self.__tasks_moves.items(), key=lambda item: item[0])}
        axis = ''
        for j in range(6 * (self.__max_task_period + 1) * 2 + self.__smallest_task_period):
            axis += '-'

        for task, result in sorted_task_moves.items():
            previous_move = 0
            print('J' + str(task), end='    ')
            for move in result['moves']:
                temp_move = ''
                print('{:>{d}}'.format('|', d=6 * (move[0] - previous_move)), end='')
                for _ in range(6 * (move[1] - move[0]) - 2):
                    temp_move += '_'
                temp_move += '|'
                print(temp_move, end='')
                previous_move = move[1]
            print('\n')
        print(axis + '>')

        print('   ', end='')
        for x in range(0, (int(self.__max_task_period / self.__smallest_task_period) + 1) * 2):
            print('{:<{d}}'.format(x * self.__smallest_task_period, d=6 * self.__smallest_task_period), end='')
        print()


def run_rm():
    rm = RateMonotonic()
    rm.set_tasks()
    print('\nUpper bound: {0:.4f}'.format(rm.calculate_upper_bound()))
    print('{feasible}\n'.format(feasible='feasible' if rm.is_feasible() else 'NOT feasible'))
    rm.schedule_tasks()
    rm.print_chart()
