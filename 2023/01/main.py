import fileinput


lines = [line.strip() for line in f.readlines()]

search_list1 = [*'123456789']
search_list2 = search_list1 + 'one,two,three,four,five,six,seven,eight,nine'.split(
    ',')
word_to_num = {w: str(i + 1) for i, w in enumerate(search_list2[9:])}


def find_index(line, search_list, find_fn, decider_fn):
  res = [(find_fn(line, s), s) for s in search_list if s in line]
  return word_to_num.get(r := decider_fn(res)[1], r)


def task(search_list):
  return sum(
      int(
          find_index(line, search_list, str.index, min) +
          find_index(line, search_list, str.rindex, max)) for line in lines)


print(f'Task 1: {task(search_list1)}')
print(f'Task 2: {task(search_list2)}')
