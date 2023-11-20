def save(filename, player):
    with open(filename, "w") as file:
        to_write = (f'{player.rect.x} '
                    f'{player.rect.y} '
                    f'{player.speed_x} '
                    f'{player.speed_y}')
        file.write(to_write + "\n")
        file.write(str(player.index))


def read(filename):
    try:
        with open(filename, "r") as file:
            line = file.readline()
            x, y, s_x, s_y = map(int, line.split())

            args = []
            for line in file.readlines():
                data = int(line)
                args.append(data)

        return x, y, s_x, s_y, args
    except Exception as e:
        print(e)
        return 0, 0, 0, 0, [0]


def read_config():
    with open("saves/1.txt", "r") as file:
        for line in file.readlines():
            name, data = line.split()
            if data[0] == 'i':
                data = int(data[1:])
            elif data[0] == 'f':
                data = float(data[1:])
            elif data[0] == 'c':
                data = data[1:]
                r, g, b = map(int, data.split("."))
                data = (r, g, b)

            print(name, data, type(data))
