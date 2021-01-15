import random
from Opticharge.vrp.GA_Algo import run_gavrp

def main():
    '''main()'''
    random.seed(64)

    instanceC_name = 'C1'
    instanceV_name = 'V1'

    ind_size = 25
    pop_size = 100
    cx_pb = 0.85
    mut_pb = 0.02
    n_gen = 100

    export_csv = True

    run_gavrp(instanceC_name=instanceC_name,instanceV_name=instanceV_name, ind_size=ind_size, pop_size=pop_size,cx_pb=cx_pb, mut_pb=mut_pb, n_gen=n_gen, export_csv=export_csv)
if __name__ == '__main__':
    main()
