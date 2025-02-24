import random

class PageAccess:
    def __init__(self, page, time, is_write):
        self.page = page
        self.time = time
        self.is_write = is_write

class Frame:
    def __init__(self, page, time=None):
        self.page = page
        self.referenced = False
        self.modified = False
        self.last_used_time = time

class AlgorithmClock:
    @staticmethod
    def execute(p, m, accesses):
        frames = []
        page_faults = 0
        pointer = 0

        for access in accesses:
            page_found = False

            for frame in frames:
                if frame.page == access.page:
                    frame.referenced = True  # Referência
                    page_found = True
                    break

            if not page_found:
                page_faults += 1

                if len(frames) < m:
                    frames.append(Frame(access.page))
                else:
                    while True:
                        frame = frames[pointer]
                        if not frame.referenced:
                            frames[pointer] = Frame(access.page)
                            break
                        else:
                            frame.referenced = False  # Reset
                            pointer = (pointer + 1) % m  # Move

                pointer = (pointer + 1) % m  # Circular

        return page_faults

class AlgorithmNRU:
    @staticmethod
    def execute(p, m, accesses):
        frames = {}
        page_faults = 0

        for access in accesses:
            current_page = frames.get(access.page)

            if current_page is None:
                if len(frames) == m:
                    page_to_replace = AlgorithmNRU.select_page_to_replace(frames)
                    del frames[page_to_replace]
                current_page = Frame(access.page)
                frames[access.page] = current_page
                page_faults += 1

            current_page.referenced = True
            if access.is_write:
                current_page.modified = True

            if access.time % p == 0:
                for frame in frames.values():
                    frame.referenced = False

        return page_faults

    @staticmethod
    def select_page_to_replace(frames):
        class_0, class_1, class_2, class_3 = [], [], [], []

        for page, frame in frames.items():
            if not frame.referenced and not frame.modified:
                class_0.append(page)
            elif not frame.referenced:
                class_1.append(page)
            elif not frame.modified:
                class_2.append(page)
            else:
                class_3.append(page)

        if class_0:
            return random.choice(class_0)
        if class_1:
            return random.choice(class_1)
        if class_2:
            return random.choice(class_2)
        return random.choice(class_3)

    @staticmethod
    def select_page_to_replace(frames):
        class_0, class_1, class_2, class_3 = [], [], [], []

        for page, frame in frames.items():
            if not frame.referenced and not frame.modified:
                class_0.append(page)
            elif not frame.referenced:
                class_1.append(page)
            elif not frame.modified:
                class_2.append(page)
            else:
                class_3.append(page)

        if class_0:
            return random.choice(class_0)
        if class_1:
            return random.choice(class_1)
        if class_2:
            return random.choice(class_2)
        return random.choice(class_3)

class AlgorithmOptimal:
    @staticmethod
    def execute(p, m, accesses):
        frames = set()
        page_faults = 0

        for i in range(len(accesses)):
            current_page = accesses[i].page
            if current_page not in frames:
                if len(frames) == m:
                    page_to_replace = AlgorithmOptimal.find_optimal_page_to_replace(frames, accesses, i)
                    frames.remove(page_to_replace)
                frames.add(current_page)
                page_faults += 1
        return page_faults

    @staticmethod
    def find_optimal_page_to_replace(frames, accesses, current_index):
        future_uses = {}
        for i in range(current_index + 1, len(accesses)):
            page = accesses[i].page
            if page in frames and page not in future_uses:
                future_uses[page] = i

        farthest = current_index
        page_to_replace = None
        for page in frames:
            use = future_uses.get(page, float('inf'))
            if use > farthest:
                farthest = use
                page_to_replace = page
        return page_to_replace

class AlgorithmWSClock:
    @staticmethod
    def execute(p, m, accesses, c):
        frames = []
        page_faults = 0
        pointer = 0

        for access in accesses:
            page_found = False
            for frame in frames:
                if frame.page == access.page:
                    frame.referenced = True
                    frame.last_used_time = access.time
                    if access.is_write:
                        frame.modified = True
                    page_found = True
                    break

            if not page_found:
                if len(frames) < m:
                    frames.append(Frame(access.page, access.time))
                else:
                    while True:
                        frame = frames[pointer]
                        if not frame.referenced and (access.time - frame.last_used_time) >= c:
                            frames[pointer] = Frame(access.page, access.time)
                            break
                        else:
                            frame.referenced = False
                            pointer = (pointer + 1) % m
                pointer = (pointer + 1) % m
                page_faults += 1
        return page_faults

def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.readlines()

def parse_page_accesses(lines):
    accesses = []
    for line in lines:
        parts = line.split()
        page = int(parts[0])
        time = int(parts[1])
        is_write = parts[2] == 'W'
        accesses.append(PageAccess(page, time, is_write))
    return accesses

def write_file(file_name, *faults):
    with open(file_name, 'w') as f:
        for fault in faults:
            f.write(f"{fault}\n")

def main():
    for i in range(1, 11):
        input_file_name = f"C:\\Users\\Migue\\OneDrive\\Documentos\\testes\\TESTE-{i:02d}.txt"
        output_file_name = f"C:\\Users\\Migue\\OneDrive\\Documentos\\testes\\TESTE-{i:02d}-RESULTADO.txt"
        
        try:
            lines = read_file(input_file_name)
            p = int(lines[0].strip())  # Total de páginas
            m = int(lines[1].strip())  # Total de molduras
            c = int(lines[2].strip())  # Ciclo do bit R
            accesses = parse_page_accesses(lines[3:])

            optimal_faults = AlgorithmOptimal.execute(p, m, accesses)
            nru_faults = AlgorithmNRU.execute(p, m, accesses)
            clock_faults = AlgorithmClock.execute(p, m, accesses)
            wsclock_faults = AlgorithmWSClock.execute(p, m, accesses, c)

            write_file(output_file_name, optimal_faults, nru_faults, clock_faults, wsclock_faults)
        except Exception as e:
            print(f"Erro ao processar o arquivo {input_file_name}: {e}")

if __name__ == '__main__':
    main()
