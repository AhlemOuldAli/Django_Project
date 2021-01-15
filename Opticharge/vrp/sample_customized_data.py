import random
from Opticharge.vrp.GA_Algo import run_gavrp

def main():
    '''main()'''
    random.seed(64)

    instanceC_name = 'CustomizedC_Data'
    instanceV_name = 'CustomizedV_Data'

    ind_size = 100
    pop_size = 400
    cx_pb = 0.85
    mut_pb = 0.02
    n_gen = 10

    export_csv = True
    customizeC_data = True
    customizeV_data = True

    run_gavrp(instanceC_name=instanceC_name,instanceV_name=instanceV_name, ind_size=ind_size, pop_size=pop_size,cx_pb=cx_pb, mut_pb=mut_pb, n_gen=n_gen, export_csv=export_csv, customizeC_data=customizeC_data,customizeV_data=customizeV_data)


if __name__ == '__main__':
    main()
