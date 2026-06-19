import os

# Suffix avtomatının vəziyyətlərini təmsil edən sinif
# State class for the suffix automaton representation


class State:
    def __init__(self, length=0, link=-1):
        self.length = length
        self.link = link
        self.next = {}


# Suffix avtomatı (Suffix Automaton) alqoritmi ilə unikal alt sətirləri sayırıq
# Suffix Automaton to count distinct substrings efficiently


class SuffixAutomaton:
    def __init__(self):
        self.states = [State(0, -1)]
        self.last = 0

    def extend(self, c):
        cur = len(self.states)
        self.states.append(State(self.states[self.last].length + 1))

        p = self.last
        while p != -1 and c not in self.states[p].next:
            self.states[p].next[c] = cur
            p = self.states[p].link

        if p == -1:
            self.states[cur].link = 0
        else:
            q = self.states[p].next[c]
            if self.states[p].length + 1 == self.states[q].length:
                self.states[cur].link = q
            else:
                clone = len(self.states)
                clone_state = State(
                    self.states[p].length + 1, self.states[q].link
                )
                clone_state.next = self.states[q].next.copy()
                self.states.append(clone_state)

                while p != -1 and self.states[p].next.get(c) == q:
                    self.states[p].next[c] = clone
                    p = self.states[p].link

                self.states[q].link = self.states[cur].link = clone

        self.last = cur

    def count_distinct_substrings(self):
        # Unikal alt sətirlərin sayını hesablayırıq
        # Count total distinct substrings using states
        ans = 0
        for i in range(1, len(self.states)):
            ans += (
                self.states[i].length - self.states[self.states[i].link].length
            )
        return ans


def m(a, n):
    # Maksimal mümkün alt sətir sayını hesablayan riyazi köməkçi funksiya
    # Compute the maximum possible number of substrings mathematically
    total = 0
    ak = 1
    for k in range(1, n + 1):
        if ak <= n:
            ak *= a
        if ak > n:
            L = n - k + 1
            total += L * (L + 1) // 2
            break
        else:
            total += min(ak, n - k + 1)
    return total


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, "rosalind_ling.txt")
    output_path = os.path.join(current_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    sequence_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            continue
        sequence_lines.append(line)

    s = "".join(sequence_lines).upper()

    sam = SuffixAutomaton()
    for char in s:
        sam.extend(char)

    sub_s = sam.count_distinct_substrings()
    m_val = m(4, len(s))
    lc = sub_s / m_val

    print(f"Linguistic Complexity: {lc}")

    with open(output_path, "w") as f:
        f.write(f"{lc}\n")


if __name__ == "__main__":
    main()
