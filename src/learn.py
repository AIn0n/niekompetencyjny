import pickle
from JsonIO import JsonIO
from genAlgorithm import *

area, rooms = JsonIO.read("input_data/curr.json")
fitCls = FitnessClass(area, rooms)
genAlg = GeneticAlgorithm(500, 0.3, 0.1, fitCls)
genAlg.repeat(1500)
bestSpecimen = max(genAlg.generation, key=lambda x: x.fitness)
print(bestSpecimen.fitness)
pickle.dump(bestSpecimen, open("output_data/out.bin", "wb+"))
