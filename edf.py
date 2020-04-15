

class EarliestDeadlineFirst:

    def __init__(self):
        self.__number_of_tasks = None
        self.__tasks_parameters = dict()
        self.__sorted_tasks_parameters = dict()
        self.__tasks_results = dict()
        self.__overall_computation_time = 0
        self.__max_lateness = dict()
        self.__is_feasible = True
        self.__max_deadline = 0

    def set_tasks(self):
        self.__number_of_tasks = int(input('\n(EDF) Enter number of tasks: '))

        for x in range(self.__number_of_tasks):
            arrival_time = int(input('(EDF) Enter arrival time for task {x}: '.format(x=x+1)))
            worst_case_computation = int(input('(EDF) Enter worst-case computation for task {x}: '.format(x=x+1)))
            deadline = int(input('(EDF) Enter deadline for task {x}: '.format(x=x+1)))
            # task array = [arrival, worst case computation, deadline, move that each task will make --> initial to 0]
            self.__tasks_parameters[x + 1] = [arrival_time, worst_case_computation, deadline, 0]

        # sort based on arrival time and then deadline
        self.__sorted_tasks_parameters = {k: v for k, v in sorted(
            self.__tasks_parameters.items(), key=lambda item: (item[1][0], item[1][2]))}

    def calculate_lateness(self):
        done_tasks = 0
        max_lateness = 0
        first_task = list(self.__sorted_tasks_parameters.items())[0]
        current_task = first_task[0]
        current_deadline = first_task[1][2]
        # set overall computation to first arrival in case the first tasks comes after t=0
        self.__overall_computation_time = first_task[1][0]

        while True:
            for task, parameters in self.__sorted_tasks_parameters.items():
                # if task needs to move, has smaller or equal arrival time in compare to overall, has smaller deadline
                if parameters[1] != parameters[3] and parameters[0] <= self.__overall_computation_time and \
                        (not current_deadline or parameters[2] < current_deadline):
                    current_task = task
                    current_deadline = parameters[2]
            # move 1 for the overall time
            self.__overall_computation_time += 1
            # move 1 forward for the current task
            self.__sorted_tasks_parameters[current_task][3] += 1
            if current_task not in self.__tasks_results:
                self.__tasks_results[current_task] = dict()
                self.__tasks_results[current_task]['moves'] = list()
            self.__tasks_results[current_task]['moves'].append(self.__overall_computation_time)

            if self.__sorted_tasks_parameters[current_task][3] == self.__sorted_tasks_parameters[current_task][1]:
                done_tasks += 1
                # set the current deadline to null so the next task can be picked up
                current_deadline = None
                self.__tasks_results[current_task]['lateness'] = self.__overall_computation_time - \
                    self.__sorted_tasks_parameters[current_task][2]
                # check to see if current task makes the schedule not feasible
                if self.__tasks_results[current_task]['lateness'] > 0:
                    self.__is_feasible = False
                if self.__tasks_results[current_task]['lateness'] > max_lateness:
                    max_lateness = self.__tasks_results[current_task]['lateness']
                # check the max deadline
                if self.__sorted_tasks_parameters[current_task][2] > self.__max_deadline:
                    self.__max_deadline = self.__sorted_tasks_parameters[current_task][2]

            if done_tasks == self.__number_of_tasks:
                # check to find tasks with max lateness
                for task, parameters in self.__tasks_results.items():
                    if parameters['lateness'] == max_lateness:
                        self.__max_lateness[task] = parameters['lateness']
                break

    def get_task_parameters(self):
        return self.__sorted_tasks_parameters

    def get_task_results(self):
        return self.__tasks_results

    def get_overall_computation_time(self):
        return self.__overall_computation_time

    def get_max_deadline(self):
        return self.__max_deadline

    def get_max_lateness(self):
        return self.__max_lateness

    def is_feasible(self):
        return self.__is_feasible

    def print_chart(self):
        axis = ''
        for j in range(6 * (self.get_max_deadline() + (list(
                self.__max_lateness.values())[0] if list(self.__max_lateness.values())[0] > 0 else 0))):
            axis += '-'

        sorted_task_results = {k: v for k, v in sorted(self.__tasks_results.items(), key=lambda item: item[0])}
        print('\n^ = arrival - v = deadline')
        for task, result in sorted_task_results.items():
            previous_move = 0
            print('\n')
            print('{:>{d}}'.format('^', d=5 * (self.__sorted_tasks_parameters[task][0] + 1)), end='')
            print('{:>{d}}'.format('v', d=5 * (self.__sorted_tasks_parameters[task][2] -
                                               self.__sorted_tasks_parameters[task][0])))
            if task == 1 and result['moves'][0] == 1:
                print('J' + str(task), end='  ')
            else:
                print('J' + str(task), end='   ')
            for move in result['moves']:
                if task == 1 and result['moves'].index(move) == 0:
                    print('{:>{d}}'.format('|', d=5 * (move - 1)), end='')
                elif previous_move != move - 1:
                    print('{:>{d}}'.format('|', d=5 * (move - previous_move - 1)), end='')
                print('____|', end='')
                previous_move = move

        print('\n' + axis + '>')

        for x in range(0, self.get_max_deadline() + (list(
                self.__max_lateness.values())[0] if list(self.__max_lateness.values())[0] > 0 else 0) + 1):
            print(f'{x:5d}', end='')
        print()


def run_edf():
    lateness_message = ''
    edf = EarliestDeadlineFirst()
    edf.set_tasks()
    edf.calculate_lateness()
    print()
    for task, result in edf.get_task_results().items():
        print('L ({task}) = {lateness}'.format(task=task, lateness=result['lateness']))
    for task, lateness in edf.get_max_lateness().items():
        lateness_message += 'L ({task}) = '.format(task=task)
    lateness_message += '{max_lateness}'.format(max_lateness=list(edf.get_max_lateness().values())[0])
    print('{feasible} - L max = {lateness}'.format(
        feasible='feasible' if edf.is_feasible() else 'NOT feasible', lateness=lateness_message))
    if edf.is_feasible():
        edf.print_chart()
