import pickle
from JsonIO import JsonIO
from genAlgorithm import *

area, rooms = JsonIO.read("input_data/curr.json")
fitCls = FitnessClass(area, rooms)
genAlg = GeneticAlgorithm(800, 0.3, 0.1, fitCls)
genAlg.repeat(3000)
bestSpecimen = max(genAlg.generation, key=lambda x: x.fitness)
print(bestSpecimen.fitness)
pickle.dump(bestSpecimen, open("output_data/out.bin", "wb+"))
