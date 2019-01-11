from School_db import *
import random
import os
import sys

lessons_array = ['Алгебра', 'Геометрия', 'Русский язык', 'Литература', 'География', 'Биология']
names = {
    'f_last_names': [],
    'm_last_names': [],
    'f_first_names': [],
    'm_first_names': [],
    'f_second_names': [],
    'm_second_names': [],
}


def load_names():
    global names
    for name, collection in names.items():
        file = f'.\\names\\{name}.txt'
        if os.path.isfile(file):
            with open(file, 'r', encoding='utf-8') as file:
                names[name] = [line.strip() for line in file.readlines()]


def get_random_item(collection):
    return collection[random.randrange(len(collection))]


def get_person(is_male):
    if len(names['f_last_names']) == 0:
        load_names()
    if is_male:
        ln = get_random_item(names['m_last_names'])
        fn = get_random_item(names['m_first_names'])
        sn = get_random_item(names['m_second_names'])
    else:
        ln = get_random_item(names['f_last_names'])
        fn = get_random_item(names['f_first_names'])
        sn = get_random_item(names['f_second_names'])
    return ln.replace('\ufeff', ''), fn.replace('\ufeff', ''), sn.replace('\ufeff', '')


def gen_classes():
    cl_list = []
    for n in range(1, 12):
        for c in "АБВГД":
            cl_list.append(f'{n}{c}')
    return cl_list


def gen_inserts(st, m, f):
    st = list(st)
    st.append(random.randrange(1,56))
    st = tuple(st)
    command_st = f'insert into Students (last_name,first_name,second_name,class_id) values {st};\n'
    command_m = f'insert into Parents (last_name,first_name,second_name) values {m};\n'
    command_f = f'insert into Parents (last_name,first_name,second_name) values {f};\n'
    return f'{command_st}{command_m}{command_f}'


def gen_relation():
    result = []
    for i in range(1, 51):
        result.append(f'insert into Students_Parents values({i}, {i*2-1}, {i*2});\n')
    return result


def gen_studs(count):
    result = []
    for i in range(count):
        m_last_name = get_random_item(names['m_last_names'])
        f_last_name = [x for x in names['f_last_names'] if str(x).startswith(m_last_name[:-3])]
        if len(f_last_name) == 0:
            f_last_name = get_random_item(names['f_last_names'])
        else:
            f_last_name = f_last_name[0]

        ln, fn, sn = get_person(False)
        m_ln, m_fn, m_sn = f_last_name, fn, sn
        ln, fn, sn = get_person(True)
        f_ln, f_fn, f_sn = m_last_name, fn, sn

        s = random.choice([True, False])
        ln, fn, sn = get_person(s)
        if s:
            ln = m_last_name
        else:
            ln = f_last_name

        result.append(((ln, fn, sn), (m_ln, m_fn, m_sn), (f_ln, f_fn, f_sn)))
    return result


def gen_teacher_inserts(teachers):
    result = []
    for t in teachers:
        result.append(f'insert into Teachers (last_name,first_name,second_name,lesson_id) values {t};\n')
    return result


def gen_teachers(count):
    result = []
    for i in range(count):
        ln, fn, sn = get_person(random.choice([True, False]))
        result.append((ln, fn, sn, random.randrange(1, len(lessons_array)+1)))
    return result


def gen_class_lesson_relation(class_count, teachers):
    result = []
    for i in range(1, class_count+1):
        for les_id in range(1, len(lessons_array)+1):
            indexes = [(teachers.index(t)+1) for t in teachers if t[3] == les_id]
            if not indexes:
                continue
            teacher_index = random.choice(indexes)
            result.append((i, teacher_index, les_id))
    return result


def gen_db_data(db_file):
    if not db_file:
        db_file = 'School_DB.db'
    load_names()
    db = SchoolDB(db_file)
    command = ''
    classes = gen_classes()
    for cl in classes:
        command += f'INSERT INTO Classes (name) VALUES("{cl}");\n'

    for les in lessons_array:
        command += f'INSERT INTO Lessons (name) VALUES("{les}");\n'

    for st, m, f in gen_studs(50):
        command += gen_inserts(st, m, f)
    for r in gen_relation():
        command += r

    teachers = gen_teachers(15)
    for t in gen_teacher_inserts(teachers):
        command += t

    for rel in gen_class_lesson_relation(len(classes), teachers):
        command += f'insert into Classes_Lessons_Teachers values {rel};\n'
    print(command)
    a = input('Execute? [Y/N]')
    if a.upper() == 'Y':
        db.execute_command(command, True)


if __name__ == '__main__':
    file = ''
    if len(sys.argv) > 1:
        file = sys.argv[1]
    gen_db_data(file)
