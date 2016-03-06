#  Junctions             Grid               Directions
#                       
#   0--1--2--3--4        +--+--+--+--+          0
#   |  |  |  |  |        | 0| 1| 2| 3|          |
#   5--6--7--8--9        +--+--+--+--+      3 --+-- 1
#   |  |  |  |  |        | 4| 5| 6| 7|          |
#  10-11-12-13-14        +--+--+--+--+          2
#   |  |  |  |  |        | 8| 9|10|11| 
#  15-16-17-18-19        +--+--+--+--+
#   |  |  |  |  |        |12|13|14|15|
#  20-21-22-23-24        +--+--+--+--+

junction_dir_to_square_offsets = [
    ((-1, -1), ( 0, -1)),
    (( 0, -1), ( 0,  0)),
    (( 0,  0), (-1,  0)),
    ((-1,  0), (-1, -1)),
]

direction_to_offset = [
    ( 0, -1),
    ( 1,  0),
    ( 0,  1),
    (-1,  0),
]

junction_neighbours = [[] for _ in xrange(25)]

for x in xrange(5):
    for y in xrange(5):
        junction = y * 5 + x
        for dir, (ox, oy) in enumerate(direction_to_offset):
            xx, yy = x + ox, y + oy
            if 0 <= xx <= 4 and 0 <= yy <= 4:
                grids = []
                neighbour = (yy * 5 + xx, dir, grids)
                junction_neighbours[junction].append(neighbour)
                for ox, oy in junction_dir_to_square_offsets[dir]:
                    gx, gy = x + ox, y + oy
                    if 0 <= gx <= 3 and 0 <= gy <= 3:
                        grids.append(gy*4+gx)

def solve((start_x, start_y), (end_x, end_y), grid):
    start_junction = start_y * 5 + start_x
    end_junction = end_y * 5 + end_x
    solutions = []
    junctions = [False] * 25
    path = []
    def recurse(pos):
        if pos == end_junction and all(g in (None, 0) for g in grid):
            solutions.append(path[:])
            return
        junctions[pos] = True
        for next_pos, dir, path_grids in junction_neighbours[pos]:
            if junctions[next_pos]:
                continue

            can_pass = True
            for path_grid in path_grids:
                if grid[path_grid] is not None:
                    grid[path_grid] -= 1
                    if grid[path_grid] < 0:
                        can_pass = False

            if can_pass:
                path.append(dir)
                recurse(next_pos)
                path.pop()

            for path_grid in path_grids:
                if grid[path_grid] is not None:
                    grid[path_grid] += 1
        junctions[pos] = False
    recurse(start_junction)
    return sorted(solutions, key=len)

def draw((start_x, start_y), solution):
    grid_w, grid_h = 4, 2
    pixels = [
        [' ' for _ in xrange(grid_w * 4 + 5)]
             for _ in xrange(grid_h * 4 + 5)
    ]

    for y in xrange(5):
        for x in xrange(5):
            pixels[y*(grid_h+1)][x*(grid_w+1)] = '+'

    x, y = start_x * (grid_w+1), start_y * (grid_h+1)

    lines = "|-|-"
    dir_to_steps = [grid_h, grid_w, grid_h, grid_w]

    for dir in solution:
        xstep, ystep = direction_to_offset[dir]
        line = lines[dir]
        steps = dir_to_steps[dir]
        for step in xrange(steps):
            x += xstep
            y += ystep
            pixels[y][x] = line
        x += xstep
        y += ystep

    return '\n'.join(''.join(row) for row in pixels)

_ = None

start = 0, 4
end   = 4, 0

while True:
    # solutions = solve(start, end, [
    #     _, _, 3, 2,
    #     1, _, _, _,
    #     _, 1, _, _,
    #     3, 1, _, _,
    # ])

    solutions = solve(start, end, [{
        '_': None, '1': 1, '2': 2, '3': 3
    }[c] for c in raw_input("puzzle> ")])

    if not solutions:
        print "no solution"
    else:
        print "%d solutions found" % len(solutions)
        print draw(start, solutions[0])
