
"""
Written by Seyed Ali Karimi.
April 2020 for Real-Time Systems
Tested in Python 3.7+
To run:
$ python main.py
"""

import edd
import edf
import rm
import ce

if __name__ == '__main__':

    while True:
        algorithm = int(input("\n1- Earliest Due Date (EDD)\n2- Earliest Deadline First (EDF)\n3- Cyclic Executive (CE)" +
                              "\n4- Rate Monotonic (RM)\n0- Exit\nSelect the scheduling algorithm from the above list" +
                              " or 0 to Exit (please enter the number): "))
        if algorithm == 1:
            edd.run_edd()
        elif algorithm == 2:
            edf.run_edf()
        elif algorithm == 3:
            ce.run_ce()
        elif algorithm == 4:
            rm.run_rm()
        elif algorithm == 0:
            break
        else:
            print('Wrong choice. Try again and choose from (0, 1, 2, 3, 4)')
