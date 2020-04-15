

class EarliestDueDate:

    def __init__(self):
        self.__number_of_tasks = None
        self.__tasks_parameters = dict()
        self.__sorted_tasks_parameters = dict()
        self.__tasks_lateness = dict()
        self.__overall_computation_time = 0
        self.__max_lateness = None

    def set_tasks(self):
        self.__number_of_tasks = int(input('\n(EDD) Enter number of tasks: '))

        for x in range(self.__number_of_tasks):
            worst_case_computation = int(input('(EDD) Enter worst-case computation for task {x}: '.format(x=x+1)))
            deadline = int(input('(EDD) Enter deadline for task {x}: '.format(x=x+1)))
            self.__tasks_parameters[x + 1] = [worst_case_computation, deadline]

        # sort based on deadline
        self.__sorted_tasks_parameters = {k: v for k, v in sorted(
            self.__tasks_parameters.items(), key=lambda item: item[1][1])}

    def calculate_lateness(self):
        # calculate lateness of each task
        for task, parameters in self.__sorted_tasks_parameters.items():
            self.__overall_computation_time += parameters[0]
            self.__tasks_lateness[task] = self.__overall_computation_time - parameters[1]

        self.__max_lateness = list({k: v for k, v in sorted(
            self.__tasks_lateness.items(), key=lambda item: item[1])}.items())[-1]

    def get_task_parameters(self):
        return self.__sorted_tasks_parameters

    def get_task_lateness(self):
        return self.__tasks_lateness

    def get_overall_computation_time(self):
        return self.__overall_computation_time

    def get_max_deadline(self):
        return (list(self.__sorted_tasks_parameters.items())[-1][1])[1]

    def get_max_lateness(self):
        return self.__max_lateness

    def is_feasible(self):
        return True if self.__max_lateness[1] <= 0 else False

    def print_chart(self):
        axis = ''
        for j in range(6 * self.get_max_deadline()):
            axis += '-'
        print('\nd = deadline')

        print(' ', end='')
        previous_deadline = 0
        for t, p in self.__sorted_tasks_parameters.items():
            print('{:>{d}}'.format('d' + str(t), d=5 * (p[1] - previous_deadline)), end='')
            previous_deadline = p[1]
        print()

        print(' ', end='')
        previous_deadline = 0
        for t, p in self.__sorted_tasks_parameters.items():
            print('{:>{d}}'.format('v', d=5 * (p[1] - previous_deadline)), end='')
            previous_deadline = p[1]
        print('\n' + axis)

        print('|', end='')
        for t, p in self.__sorted_tasks_parameters.items():
            print('{:^{d}}'.format('J' + str(t), d=(5 * p[0]) - 1), end='')
            print('|', end='')

        print('\n' + axis + '>')

        print(0, end='')
        for x in range(1, self.get_max_deadline() + 1):
            print(f'{x:5d}', end='')
        print()


def run_edd():
    edd = EarliestDueDate()
    edd.set_tasks()
    edd.calculate_lateness()
    print()
    for task, lateness in edd.get_task_lateness().items():
        print('L ({task}) = {lateness}'.format(task=task, lateness=lateness))
    print('{feasible} - L max = L ({task}) = {lateness}'.format(
        feasible='feasible' if edd.is_feasible() else 'NOT feasible', task=edd.get_max_lateness()[0],
        lateness=edd.get_max_lateness()[1]))
    if edd.is_feasible():
        edd.print_chart()
