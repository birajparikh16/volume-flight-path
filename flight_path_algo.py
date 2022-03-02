from typing import List

# Find Source and Destination of the routes
def findflightPath(routes: List[List]):
    """
    Args:
        Accept flight routes as a list of list strings
        example: ["ATL", "EWR"], ["SFO", "ATL"]
    Return:
        List: [source, destination]
    
    """
    source = []
    destination = []
    source_airport = ""
    destination_airport = ""
    # append all the source and destination in the respective list
    for i in range(len(routes)):
        source.append(routes[i][0])
        destination.append((routes[i][1]))

    for src in source:
        # If source found in destination list than remove the source from the destination list because
        # source cannot be same as destination
        if src in destination:
            destination.remove(src)
            continue
        else:
            source_airport += str(src,'utf-8')
    # the last remaining value in the destination list would be our destination
    destination_airport += str(destination[-1],'utf-8')
    return [source_airport, destination_airport]