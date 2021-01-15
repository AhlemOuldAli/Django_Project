import random
from Opticharge.vrp.GA_Algo import run_gavrp
import time

def main():
    '''main()'''
    start_time = time.time()
    random.seed(64)

    instanceC_name = 'RC108'
    instanceV_name = 'V11'

    ind_size = 100
    pop_size = 100
    cx_pb = 0.85
    mut_pb = 0.02
    n_gen = 100

    export_csv = True

    run_gavrp(instanceC_name=instanceC_name,instanceV_name=instanceV_name, ind_size=ind_size, pop_size=pop_size,cx_pb=cx_pb, mut_pb=mut_pb, n_gen=n_gen, export_csv=export_csv)
    print("--- %s seconds ---" % (time.time() - start_time))
if __name__ == '__main__':
    main()
