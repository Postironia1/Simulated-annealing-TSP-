import numpy as np
import matplotlib.pyplot as plt

# Функция для вычисления расстояния между двумя точками
def distance(city1, city2):
    return np.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

# Функция для вычисления общего расстояния в маршруте
def total_distance(route, cities):
    total = 0
    for i in range(len(route) - 1):
        total += distance(cities[route[i]], cities[route[i+1]])
    total += distance(cities[route[-1]], cities[route[0]])  # добавляем расстояние до начального города
    return total

# Функция для создания нового состояния путем инвертирования маршрута между двумя случайными городами
def generate_new_state(route):
    i, j = np.random.choice(len(route), 2, replace=False)
    route[i], route[j] = route[j], route[i]
    return route

# Функция изменения температуры
def temperature(iteration, tmax):
    return tmax / (1 + iteration / tmax)

def main():
    # Начальные параметры
    N = 20  # количество городов
    tmax = 100  # начальная температура
    tmin = 0.1  # минимальная температура
    s0 = np.array([16, 19,  0, 15, 13,  4, 14,  5,  7, 17,  6,  8, 18,  9, 11,  3, 10,  2,  1, 12])  # начальное состояние: случайный маршрут (был)
    #print(s0)
    cities = np.array([ [5.84416615, 1.31443578],
                        [8.12971868, 4.03540677],
                        [3.42769052, 4.76945743],
                        [0.33313853, 0.78164357],
                        [9.57605275, 0.72691155],
                        [9.25608887, 6.35967251],
                        [8.41600209, 7.67402688],
                        [2.23242117, 7.17441935],
                        [8.10773496, 5.77685203],
                        [2.64495234, 3.71224116],
                        [4.05942125, 3.65176267],
                        [5.41829775, 5.9049512 ],
                        [0.64710723, 5.13774428],
                        [8.97409289, 4.32026637],
                        [3.04700924, 8.8500869 ],
                        [7.47619875, 4.01047506],
                        [7.33340155, 1.24542913],
                        [5.81429966, 5.80082348],
                        [8.41998652, 8.78820659],
                        [6.2887951,  6.46743834]])  # генерация случайных координат для городов (была)
    
    for _ in range(10):
        # Имитация отжига
        current_state = s0
        current_energy = total_distance(current_state, cities)
        best_state = current_state
        best_energy = current_energy
        energies = [current_energy]
    
        iteration = 0
        while temperature(iteration, tmax) > tmin:
            new_state = generate_new_state(current_state)
            new_energy = total_distance(new_state, cities)
            #print(f'iteration: {iteration}, new route: {new_state}, new energy: {new_energy} ')
            if new_energy < current_energy or np.random.rand() < np.exp((current_energy - new_energy) / temperature(iteration, tmax)):
                current_state = new_state
                current_energy = new_energy
                if current_energy < best_energy:
                    best_state = current_state
                    best_energy = current_energy
            energies.append(current_energy)
            iteration += 1
    
        print(f'best route: {best_state}, best energy: {best_energy} ')
    
    # Построение графика начального расположения точек-городов и маршрута
    plt.figure(figsize=(12, 6))
    
    # Начальное расположение городов
    plt.subplot(1, 2, 1)
    plt.scatter(cities[:, 0], cities[:, 1])
    for i in range(len(cities)):
        plt.text(cities[i, 0], cities[i, 1], str(i))
    plt.title('Начальное расположение городов')
    
    # Конечный маршрут с использованием стрелок для обозначения направления
    plt.subplot(1, 2, 2)
    plt.scatter(cities[:, 0], cities[:, 1])
    for i in range(len(best_state) - 1):
        plt.arrow(cities[best_state[i], 0], cities[best_state[i], 1],
                  cities[best_state[i+1], 0] - cities[best_state[i], 0],
                  cities[best_state[i+1], 1] - cities[best_state[i], 1],
                  head_width=0.2, head_length=0.3, fc='b', ec='b')
    plt.arrow(cities[best_state[-1], 0], cities[best_state[-1], 1],
              cities[best_state[0], 0] - cities[best_state[-1], 0],
              cities[best_state[0], 1] - cities[best_state[-1], 1],
              head_width=0.2, head_length=0.3, fc='b', ec='b')
    for i in range(len(cities)):
        plt.text(cities[i, 0], cities[i, 1], str(i))
    plt.title('Конечный маршрут')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
