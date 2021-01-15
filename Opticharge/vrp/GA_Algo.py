import os
import io
import random
from csv import DictWriter
from deap import base, creator, tools
from Opticharge.settings import BASE_DIR
from .GA_utils import make_dirs_for_file, exist, load_instance

def ind2route(individual, instanceC,instanceV):
    route = []
    totalroutes = [0]*101
    # Initialize a sub-route
    sub_route = []
    vehicle_load = [0]*101
    vehicle_used=[False]*101
    updated_vehicle_load =[0]*101
    done =[False]*101
    last_customer_id = 0
    for customer_id in individual:
        # Update vehicle load
        demand = instanceC[f'customer_{customer_id}']['demand']
        typevehicle = instanceC[f'customer_{customer_id}']['type_vehicle']
        for vehicle_id in range(0,100):
            if (typevehicle == instanceV[f'vehicle_{vehicle_id}']['type_vehicle']):
                updated_vehicle_load[vehicle_id]=vehicle_load[vehicle_id]+demand
                if (updated_vehicle_load[vehicle_id] <= instanceV[f'vehicle_{vehicle_id}']['capacity']) and (done[customer_id]==False):
                    # Add to current sub-route
                    if(vehicle_used[vehicle_id]==False):
                        sub_route=[]
                        route.append(sub_route)
                        vehicle_used[vehicle_id]=True
                        totalroutes[vehicle_id]=sub_route
                        sub_route.append(vehicle_id)
                    vehicle_load[vehicle_id] = updated_vehicle_load[vehicle_id]
                    vehicle_used[vehicle_id]=True
                    done[customer_id]=True
                    sub_route=totalroutes[vehicle_id]
                    sub_route.append(customer_id)
            #update last cusomer id
        last_customer_id=customer_id
    return route

def print_route(route, merge=False):
    route_str = '0'
    sub_route_count = 0
    for sub_route in route:
        sub_route_count += 1
        sub_route_str = '0'
        for customer_id in sub_route:
            sub_route_str = f'{sub_route_str} - {customer_id}'
            route_str = f'{route_str} - {customer_id}'
            sub_route_str = f'{sub_route_str}'
        if not merge:
            print(f' Route: {sub_route_str}')
        route_str = f'{route_str}'
    if merge:
        print(route_str)

def eval_vrp(individual, instanceC,instanceV):
    total_distance=0
    route = ind2route(individual, instanceC,instanceV)
    for sub_route in route:
        sub_route_distance = 0
        last_customer_id = 0
        for customer_id in sub_route:
            # Calculate section distance
            distance = instanceC['distance_matrix'][last_customer_id][customer_id]
            # Update sub-route distance
            sub_route_distance = sub_route_distance + distance
            # Update last customer ID
            last_customer_id = customer_id
        total_distance = total_distance + sub_route_distance
    fitness = 1.0 / total_distance
    return (fitness, )

def cx_partialy_matched(ind1, ind2):
    '''use the partial mapped crosseover '''
    #use the maping relation map to legalize offspring
    size = min(len(ind1), len(ind2))
    cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    temp1 = ind1[cxpoint1:cxpoint2+1] + ind2
    temp2 = ind1[cxpoint1:cxpoint2+1] + ind1
    ind1 = []
    for gene in temp1:
        if gene not in ind1:
            ind1.append(gene)
    ind2 = []
    for gene in temp2:
        if gene not in ind2:
            ind2.append(gene)
    return ind1, ind2

def mut_reverse_indexes(individual):
    ''' select 2 random points from the individual and reverse what is in the middle of this 2 points'''
    start, stop = sorted(random.sample(range(len(individual)), 2))
    individual = individual[:start] + individual[stop:start-1:-1] + individual[stop+1:]
    return (individual, )

def run_gavrp(instanceC_name,instanceV_name, ind_size, pop_size, \
                cx_pb, mut_pb, n_gen, export_csv=False, customizeC_data=False,customizeV_data=False ):
    if customizeC_data and customizeV_data:
        json_data_dirC = os.path.join(BASE_DIR, 'dataC', 'json_customizeC')
        json_data_dirV = os.path.join(BASE_DIR, 'dataV', 'json_customizeV')

    else:
        json_data_dirC = os.path.join(BASE_DIR, 'dataC', 'json')
        json_data_dirV = os.path.join(BASE_DIR, 'dataV', 'json')

    json_fileC = os.path.join(json_data_dirC, f'{instanceC_name}')
    instanceC = load_instance(json_file=json_fileC)

    json_fileV = os.path.join(json_data_dirV, f'{instanceV_name}')
    instanceV = load_instance(json_file=json_fileV)

    if instanceC and instanceV is None:
        return
    creator.create('FitnessMax', base.Fitness, weights=(1.0, ))
    creator.create('Individual', list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()

    # Attribute generator
    toolbox.register('indexes', random.sample, range(1, int(ind_size) + 1), ind_size)

    # Structure initializers
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    # Operator registering
    toolbox.register('evaluate', eval_vrp, instanceC=instanceC,instanceV=instanceV)
    toolbox.register('select', tools.selRoulette)
    toolbox.register('mate', cx_partialy_matched)
    toolbox.register('mutate', mut_reverse_indexes)

    pop = toolbox.population(n=int(pop_size))

    # Results holders for exporting results to CSV file
    csv_data = []
    tour_data =[]
    print('Start of evolution')
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    print(fitnesses)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    print(f'  Evaluated {len(pop)} individuals')
    # Begin the evolution
    for gen in range(int(n_gen)):
        print(f'-- Generation {gen} --')
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < float(cx_pb):
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if random.random() < float(mut_pb):
                toolbox.mutate(mutant)
                del mutant.fitness.values
                # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
        print(f'  Evaluated {len(invalid_ind)} individuals')
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum([x**2 for x in fits])
        std = abs(sum2 / length - mean**2)**0.5
        print(f'  Min {min(fits)}')
        print(f'  Max {max(fits)}')
        print(f'  Avg {mean}')
        print(f'  Std {std}')
        best_ind = tools.selBest(pop, 1)[0]

        # Write data to holders for exporting results to CSV file
        if export_csv:
            csv_row = {
                'generation': gen,
                'evaluated_individuals': len(invalid_ind),
                'min_fitness': min(fits),
                'max_fitness': max(fits),
                'avg_fitness': mean,
                'std_fitness': std,
                'Best individual':best_ind,
                'Best fitness':best_ind.fitness.values[0],
                'Total distance':1 / best_ind.fitness.values[0],
            }
            csv_data.append(csv_row)
            tour_row={
                'Route':ind2route(best_ind, instanceC,instanceV),
            }
            tour_data.append(tour_row)

    print('-- End of (successful) evolution --')
    print(f'Best individual: {best_ind}')
    print(f'Fitness: {best_ind.fitness.values[0]}')
    print_route(ind2route(best_ind, instanceC,instanceV))
    print(f'Total distance: {1 / best_ind.fitness.values[0]}')

    if export_csv:
        csv_file_name = f'{instanceC_name}_iS{ind_size}_pS{pop_size}_cP{cx_pb}_mP{mut_pb}_nG{n_gen}.csv'
        tour_file_name=f'{instanceC_name}_{instanceV_name}.csv'

        csv_file = os.path.join(BASE_DIR, 'results', csv_file_name)
        tour_file= os.path.join(BASE_DIR,'results',tour_file_name)

        print(f'Write to file: {csv_file}')
        make_dirs_for_file(path=csv_file)
        make_dirs_for_file(path=tour_file)

        if not exist(path=csv_file, overwrite=True):
            with io.open(csv_file, 'wt', newline='') as file_object:
                fieldnames = [
                    'generation',
                    'evaluated_individuals',
                    'min_fitness',
                    'max_fitness',
                    'avg_fitness',
                    'std_fitness',
                    'Best individual',
                    'Best fitness',
                    'Total distance',
                ]
                writer = DictWriter(file_object, fieldnames=fieldnames, dialect='excel')
                writer.writeheader()
                for csv_row in csv_data:
                    writer.writerow(csv_row)
        if not exist(path=tour_file,overwrite=True):
            with io.open(tour_file,'wt',newline='') as file_object:
                fieldnames=[
                    'Route',
                ]
                writer = DictWriter(file_object, fieldnames=fieldnames, dialect='excel')
                writer.writeheader()
                writer.writerow(tour_row)


