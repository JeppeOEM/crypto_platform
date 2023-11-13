from loke.trading_engine.Optimizer import Nsga2
from loke.trading_engine.process_conds import create_conds


def call_optimizer(df, pop_size, generations, id):
    conditions, params_data = create_conds(id)
    print(conditions, params_data)
    generations = int(generations)
    nsga2 = Nsga2(df, pop_size, id, params_data)
    p_population = nsga2.create_initial_population()
    p_population = nsga2.evaluate_population(p_population, conditions)
    p_population = nsga2.crowding_distance(p_population)
    g = 0
    while g < generations:
        q_population = nsga2.create_offspring_population(p_population)
        q_population = nsga2.evaluate_population(q_population, conditions)
        r_population = p_population + q_population
        nsga2.population_params.clear()
        i = 0
        population = dict()
        for bt in r_population:
            bt.reset_results()
            nsga2.population_params.append(bt.parameters)
            population[i] = bt
            i += 1

        fronts = nsga2.non_dominated_sorting(population)
        for j in range(len(fronts)):
            fronts[j] = nsga2.crowding_distance(fronts[j])

        p_population = nsga2.create_new_population(fronts)

        print(f"\r{int((g + 1) / generations * 100)}%", end='')

        g += 1

    print("\n")

    for individual in p_population:
        print(individual)
