import os
import csv
import json
import numpy as np
import matplotlib.pyplot as plt

def writefile(lista):
    newfile = open(path + '/database/' + lista[0]['con'] + '.json', 'w')
    json.dump(lista, newfile, indent=4)

def sortfunc(element):
    return element['mag']

def printFig(lista):
    pointsList = []
    # adiciona lista de pontos normalizados
    for item in lista:
        dist = (item['x']**2 + item['y']**2 + item['z']**2)**0.5
        pointsList.append(np.array([item['x'] / dist, item['y'] / dist, item['z'] / dist]))

    # calcula angulos theta e phi em coordenadas esfericas do primeiro ponto
    target = pointsList[0]
    theta = np.arctan(target[1] / target[0])
    if target[0] < 0:
        theta = theta + np.pi
    phi = np.arctan(target[2] / (target[0]**2 + target[1]**2)**0.5)

    # rotaciona pontos para que theta torne-se zero
    yaw = np.zeros([3, 3])
    yaw[0,0] = yaw[1,1] = np.cos(theta)
    yaw[1,0] = -np.sin(theta)
    yaw[0,1] = np.sin(theta)
    yaw[2,2] = 1

    for i in range(0, len(pointsList)):
        pointsList[i] = yaw@pointsList[i]
    
    # rotaciona pontos para que phi torne-se zero
    pitch = np.zeros([3, 3])
    pitch[0,0] = pitch[2,2] = np.cos(phi)
    pitch[2,0] = -np.sin(phi)
    pitch[0,2] = np.sin(phi)
    pitch[1,1] = 1

    for i in range(0, len(pointsList)):
        pointsList[i] = pitch@pointsList[i]

    # desloca origem para 0
    target = np.copy(pointsList[0])
    for i in range(0, len(pointsList)):
        pointsList[i] = pointsList[i] - target

    # rotaciona e normaliza pontos para que a segunda estrela fique em x=1
    target2 = pointsList[1]
    gamma = -np.arctan(target2[2] / target2[1])
    if target2[1] < 0:
        gamma = gamma - np.pi

    normalize = 1 / (target2[1]**2 + target2[2]**2)**(1/2)

    roll = np.zeros([3, 3])
    roll[1,1] = roll[2,2] = np.cos(gamma)
    roll[1,2] = -np.sin(gamma)
    roll[2,1] = np.sin(gamma)
    roll[0,0] = 1

    for i in range(0, len(pointsList)):
        pointsList[i] = roll@pointsList[i] * normalize

    # escreve json
    for i in range(0, len(pointsList)):
        lista[i]['x'] = pointsList[i][0]
        lista[i]['y'] = pointsList[i][1]
        lista[i]['z'] = pointsList[i][2]

    writefile(lista)

    # faz a figura
    fig, ax = plt.subplots()

    i = 0
    for point in pointsList:
        if i > 20:
            break
        ax.scatter(point[1], point[2], c='black', s= 40 / 2**lista[i]['mag'])
        i = i + 1

    ax.axis('equal')
    plt.savefig('database/' + str(lista[0]['con']) + '.png', dpi=500, format='png')
    plt.close()


constelationList = {}

path = os.getcwd()
csvfile = open(path + '/hyg_v37.csv', 'r', newline='')

# le do csv para a memoria, definindo constelacao como chave
reader = csv.DictReader(csvfile, delimiter=',')
for row in reader:
    if(float(row['mag']) < 6 and float(row['mag']) > 0): # exclui estrelas de baixa luminosidade e o sol
        lista = constelationList.get(row['con'])
        newrow = {'con' : row['con'], 'mag' : float(row['mag']), 'x' : float(row['x']), 'y' : float(row['y']), 'z' : float(row['z'])}
        if(lista == None):
            constelationList.update({newrow['con'] : [newrow]})
        else:
            lista.append(newrow)

# ordena dados
keylist = constelationList.keys()
for key in keylist:
    lista = constelationList.get(key)
    lista.sort(key=sortfunc)

# cria figuras
for key in keylist:
    lista = constelationList.get(key)
    printFig(lista)
