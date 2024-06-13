import physics_parallel as physics
import cupy, copy

def removeNodes(nodeIDs, nodeIDsToRemove, nodeParents):

    filteredNodeIDs = list(set(nodeIDs) - set(nodeIDsToRemove))

    nodeParents = nodeParents.reshape(-1, 1)
    mask = ~cupy.isin(nodeParents.reshape(-1, 1), nodeIDsToRemove)
    lenMask = mask.sum(axis=0)
    filteredElements = nodeParents[mask.flatten()]
    filteredNodeParents = filteredElements.reshape(lenMask.shape).tolist()

    return filteredNodeIDs, filteredNodeParents

def sortNodes(nodeIDs, nodeParents):

    tempNodeIDs = nodeIDs[:]
    tempNodeParents = copy.deepcopy(nodeParents)

    sortedNodeIDs = cupy.array([])

    while len(tempNodeIDs) > 0:

        nodeIDsToProcess = cupy.array([])
        nodeIDsToRemove = cupy.array([])

        mask = cupy.shape(nodeParents)[1] == 0

        sortedNodeIDs.extend(nodeIDs[mask])

        tempNodeIDs, tempNodeParents = removeNodes(tempNodeIDs, nodeIDs[mask], nodeParents)