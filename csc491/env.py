def load(filename='.env'):
    env = {}

    with open(filename, 'r') as envfile:
        line_index = 1
        for line in envfile:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                line_index += 1
                continue
            pair = line.split('=', maxsplit=1)
            if len(pair) == 1:
                raise SyntaxError(f'{filename}:{line_index}: expected \'=\'')
            key = pair[0]
            val = pair[1]
            if len(key) == 0:
                raise SyntaxError(f'{filename}:{line_index}: empty key not permitted')
            env[key] = val
            line_index += 1

    return env