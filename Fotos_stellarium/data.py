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

    target = pointsList[0]
    theta = np.arctan(target[1] / target[0])
    if target[0] < 0:
        theta = theta + np.pi
    phi = np.arctan(target[2] / (target[0]**2 + target[1]**2)**0.5)

    rotation1 = np.zeros([3, 3])
    rotation1[0,0] = rotation1[1,1] = np.cos(theta)
    rotation1[1,0] = -np.sin(theta)
    rotation1[0,1] = np.sin(theta)
    rotation1[2,2] = 1

    for i in range(0, len(pointsList)):
        pointsList[i] = rotation1@pointsList[i]
    
    rotation2 = np.zeros([3, 3])
    rotation2[0,0] = rotation2[2,2] = np.cos(phi)
    rotation2[2,0] = -np.sin(phi)
    rotation2[0,2] = np.sin(phi)
    rotation2[1,1] = 1

    for i in range(0, len(pointsList)):
        pointsList[i] = rotation2@pointsList[i]

    # faz a figura
    fig, ax = plt.subplots()

    i = 0
    for point in pointsList:
        ax.scatter(point[0], point[1], c='black', s= 40 / lista[i]['mag']**2)
        i = i + 1

    plt.savefig('database/' + str(lista[0]['con']) + '.png', dpi=500, format='png')
    plt.close()




constelationList = {}

path = os.getcwd()
csvfile = open(path + '/hyg_v37.csv', 'r', newline='')

# le do csv para a memoria, definindo constelacao como chave
reader = csv.DictReader(csvfile, delimiter=',')
for row in reader:
    if(float(row['mag']) < 5 and float(row['mag']) > 0): # exclui estrelas de baixa luminosidade e o sol
        lista = constelationList.get(row['con'])
        newrow = {'con' : row['con'], 'mag' : float(row['mag']), 'x' : float(row['x']), 'y' : float(row['y']), 'z' : float(row['z'])}
        if(lista == None):
            constelationList.update({newrow['con'] : [newrow]})
        else:
            lista.append(newrow)

# armazena dados em um json
keylist = constelationList.keys()
for key in keylist:
    lista = constelationList.get(key)
    lista.sort(key=sortfunc)
    writefile(lista)

# cria figuras
for key in keylist:
    lista = constelationList.get(key)
    printFig(lista)


