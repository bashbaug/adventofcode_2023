import sys

distmax = sys.maxsize

numrows = 0
numcols = 0
numdirs = 4
numpaths = 10 + 1

maxcoord = 0

U = 0
D = 1
L = 2
R = 3

dtos = {U:'UP', D:'DOWN', L:'LEFT', R:'RIGHT'}

def to_coord(r, c, d, s):
    coord = r
    coord = coord * numcols + c
    coord = coord * numdirs + d
    coord = coord * numpaths + s
    return coord

def from_coord(coord):
    s = coord % numpaths
    coord = coord // numpaths
    d = coord % numdirs
    coord = coord // numdirs
    c = coord % numcols
    coord = coord // numcols
    r = coord
    return (r, c, d, s)

def findMinDistance(worklist, distances, visited):
    result = (0, False)
    dist = distmax
    for coord in worklist:
        if not visited[coord]:
            check = distances[coord]
            if check < dist:
                result = (coord, True)
                dist = check
    return result

def djikstra(board, minpath, maxpath):
    worklist = set()

    distances = [distmax for c in range(maxcoord)]

    coord = to_coord(0, 1, R, 1)
    distances[coord] = board[0][1]
    worklist.add(coord)

    coord = to_coord(1, 0, D, 1)
    distances[coord] = board[1][0]
    worklist.add(coord)

    visited = [False for c in range(maxcoord)]

    iteration = 0
    while True:
        (coord, found) = findMinDistance(worklist, distances, visited)
        if found == False:
            break

        (r, c, d, s) = from_coord(coord)
        dist = distances[coord]
        worklist.remove(coord)

        visited[coord] = True
        iteration = iteration + 1
        if iteration % 100000 == 0:
            print('finished iteration {}'.format(iteration))

        if (r > 0 and                   # check UP
            d != D and
            ((d != U and s >= minpath) or (d == U and s < maxpath))):
            newsteps = 1 if d != U else s + 1
            newcoord = to_coord(r-1, c, U, newsteps)
            if not visited[newcoord]:
                newdist = dist + board[r-1][c]
                if distances[newcoord] > newdist:
                    distances[newcoord] = newdist
                    worklist.add(newcoord)
        if (r < numrows - 1 and         # check DOWN
            d != U and
            ((d != D and s >= minpath) or (d == D and s < maxpath))):
            newsteps = 1 if d != D else s + 1
            newcoord = to_coord(r+1, c, D, newsteps)
            if not visited[newcoord]:
                newdist = dist + board[r+1][c]
                if distances[newcoord] > newdist:
                    distances[newcoord] = newdist
                    worklist.add(newcoord)
        if (c > 0 and                   # check LEFT
            d != R and
            ((d != L and s >= minpath) or (d == L and s < maxpath))):
            newsteps = 1 if d != L else s + 1
            newcoord = to_coord(r, c-1, L, newsteps)
            if not visited[newcoord]:
                newdist = dist + board[r][c-1]
                if distances[newcoord] > newdist:
                    distances[newcoord] = newdist
                    worklist.add(newcoord)
        if (c < numcols - 1 and         # check RIGHT
            d != L and
            ((d != R and s >= minpath) or (d == R and s < maxpath))):
            newsteps = 1 if d != R else s + 1
            newcoord = to_coord(r, c+1, R, newsteps)
            if not visited[newcoord]:
                newdist = dist + board[r][c+1]
                if distances[newcoord] > newdist:
                    distances[newcoord] = newdist
                    worklist.add(newcoord)

    distmin = distmax
    for coord in range(maxcoord):
        (r, c, d, s) = from_coord(coord)
        if r == numrows-1 and c == numcols-1 and s >= minpath:
            distmin = min(distmin, distances[coord])

    print('found solution after {} iterations'.format(iteration))
    return distmin

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    board = [[int(v) for v in line.strip()] for line in lines]

    numrows = len(board)
    numcols = len(board[0])
    maxcoord = numrows * numcols * numdirs * numpaths

    loss = djikstra(board, 1, 3)
    print('Part 1: total loss from start to end is {}'.format(loss))

    loss = djikstra(board, 4, 10)
    print('Part 2: total loss from start to end is {}'.format(loss))
