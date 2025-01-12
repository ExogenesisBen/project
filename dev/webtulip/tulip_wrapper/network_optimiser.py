from tulip import tlp

class NetworkOptimiser:

	def nodePruning(network):

		arrayOfNodesNextToPruned = []
		arrayOfNodesToPrune = []

		# find each node with 1 or less edges
		for node in network.getNodes():
			numOfEdges = 0
			for edge in network.getInOutEdges(node):
				numOfEdges+=1
			if numOfEdges <= 1:
				arrayOfNodesToPrune.append(node)

		# for each node to be pruned analyse each edge
		for node in arrayOfNodesToPrune:
			for edge in network.getInOutEdges(node):
				source = network.source(edge)
				target = network.target(edge)
				# if source/target of edge is node to be pruned then check the other end and increment arrayOfNodesNextToPruned

				if target == node:
					valueUpdated = False
					for nodeNumPair in arrayOfNodesNextToPruned:
						if nodeNumPair["node"] == source:
							nodeNumPair["number"] += 1
							valueUpdated = True
							break
					if valueUpdated == False:
						arrayOfNodesNextToPruned.append({"node": source, "number": 1})
					network.delEdge(edge)

				elif source == node:
					valueUpdated = False
					for nodeNumPair in arrayOfNodesNextToPruned:
						if nodeNumPair["node"] == target:
							nodeNumPair["number"] += 1
							valueUpdated = True
							break
					if valueUpdated == False:
						arrayOfNodesNextToPruned.append({"node": target, "number": 1})
					network.delEdge(edge)

		# delete all nodes that are to be pruned
		for node in arrayOfNodesToPrune:
			network.delNode(node)

		return network, arrayOfNodesNextToPruned


	def cliqueBasedNodeBundling(network):

		deletedStats = []

		result = network.getDoubleProperty("clusteringcoef")
		tlp.clusteringCoefficient(network, result)

		clique_like = []

		for node in network.getNodes():
			if result.getNodeValue(node) > 0.8:
				clique_like.append(node)

		for node in clique_like:
			numDeleted = bundleNode(network, node)
			deletedStats.append({"node": node, "numDeleted": numDeleted})


		return network, deletedStats


	def edgeBasedNodeBundling(network):

		deletedStats = []
		numOfEdges = []

		for node in network.getNodes():
			numOfEdges.append(network.deg(node))
		mean = sum(numOfEdges) / float(len(numOfEdges))

		highestDegreeNodes = []
		theirSizes = []

		for node in network.getNodes():
			degree = network.deg(node)
			if degree > (mean*2):
				highestDegreeNodes.append(node)
				theirSizes.append(degree)

		while len(highestDegreeNodes) > 0:
			index = 0
			counter = 0
			largestSize = 0

			for deg in theirSizes:
				if (deg > largestSize):
					largestSize = deg
					index=counter
				counter+=1

			numDeleted = bundleNode(network, highestDegreeNodes[index])
			deletedStats.append({"node": highestDegreeNodes[index], "numDeleted": numDeleted})
			highestDegreeNodes.pop(index)
			theirSizes.pop(index)

		return network, deletedStats

def bundleNode(network, node):

	numDeleted = 0

	neighbours = []

	# get neighbours then their edges
	try:
		for nnode in network.getInOutNodes(node):
			neighbours.append(nnode)
			for edge in network.getInOutEdges(nnode):
				# if edge from neighbour isn't going to middle
				if network.source(edge) != node and network.target(edge) != node:
					# if source/target edge is set to nnode, then set to middle
					if network.source(edge) == nnode:
						network.setSource(edge, node)
					if network.target(edge) == nnode:
						network.setTarget(edge, node)
				else:
					network.delEdge(edge)

		# delete neighbours
		for nnode in neighbours:
			network.delNode(nnode)
			numDeleted+=1
		return numDeleted

	# error if node no longer exists
	except:
		return numDeleted
