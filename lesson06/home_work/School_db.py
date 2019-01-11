import sqlite3
import os
import sys
import random


class DBObject:
    def __init__(self, id):
        self.id = id


class Person:
    def __init__(self, last_name, first_name, second_name):
        self.last_name = last_name
        self.first_name = first_name
        self.second_name = second_name

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.second_name}'


def get_element_by_id(collection, id):
    result = [x for x in collection if x.id == id]
    if len(result) == 0:
        return None
    return result[0]


class School:
    def __init__(self, classes, lessons, teachers, students, parents):
        self.classes = classes
        self.lessons = lessons
        self.teachers = teachers
        self.students = students
        self.parents = parents

    def apply_student_parent_relation(self, relations):

        for st_id, m_id, f_id in relations:
            stud = get_element_by_id(self.students, st_id)
            mother = get_element_by_id(self.parents, m_id)
            father = get_element_by_id(self.parents, f_id)

            if stud and mother and father:
                stud.set_parents((mother, father))

    def apply_class_teacher_relation(self, relations):

        for cl_id, t_id, les_id in relations:
            _class = get_element_by_id(self.classes, cl_id)
            teacher = get_element_by_id(self.teachers, t_id)

            if _class and teacher:
                _class.set_teacher(teacher)


class Class(DBObject):
    def __init__(self, id, name):
        super().__init__(id)
        self.name = name
        self.students = []
        self.teachers = []

    def set_teacher(self, teacher):
        teacher.classes.append(self)
        self.teachers.append(teacher)

    def __str__(self):
        return f'{self.name} Students count: {len(self.students)}'


class Lesson(DBObject):
    def __init__(self, id, name):
        super().__init__(id)
        self.name = name


class Teacher(Person, DBObject):
    def __init__(self, id, last_name, first_name, second_name, lesson):
        DBObject.__init__(self, id)
        Person.__init__(self, last_name, first_name, second_name)
        self.lesson = lesson
        self.classes = []

    def __str__(self):
        return f'{super().__str__()} ({self.lesson.name})'


class Parent(Person, DBObject):
    def __init__(self, id, last_name, first_name, second_name):
        DBObject.__init__(self, id)
        Person.__init__(self, last_name, first_name, second_name)
        self.children = []


class Student(Person, DBObject):
    def __init__(self, id, last_name, first_name, second_name, _class):
        DBObject.__init__(self, id)
        Person.__init__(self, last_name, first_name, second_name)
        _class.students.append(self)
        self._class = _class
        self.parents = ()

    def set_parents(self, parents):
        for p in parents:
            p.children.append(self)
        self.parents = parents


class SchoolDB:

    TABLES = ['Classes', 'Lessons', 'Parents', 'Students', 'Teachers']
    TABLES_RELATIONS = ['Classes_Lessons_Teachers', 'Students_Parents']

    def __init__(self, sqlite_file):
        self.__db_file = sqlite_file
        if not os.path.isfile(sqlite_file):
            self.__create_tables()

    def __create_tables(self):

        with open('create_tables.sql') as file:
            for line in file.readlines():
                self.execute_command(line, True)
        pass

    def execute_command(self, command, need_commit):
        connect = sqlite3.connect(self.__db_file)
        answer = []
        command = command.split(';\n')
        for c in command:
            # answer.append(connect.cursor().execute(c))
            answer = list(connect.cursor().execute(c))
        if need_commit:
            connect.commit()
        connect.close()
        return answer

    def get_data(self, table, columns='*'):
        command = f'SELECT {columns} FROM {table}'
        return self.execute_command(command, False)


def load_school(db_file):
    if not db_file:
        db_file = 'School_DB.db'
    db = SchoolDB(db_file)
    data = {}
    relation_data = {}
    for t in SchoolDB.TABLES:
        data[t] = db.get_data(t)
    for t in SchoolDB.TABLES_RELATIONS:
        relation_data[t] = db.get_data(t)

    classes = [Class(id, name) for id, name in data['Classes']]
    lessons = [Lesson(id, name) for id, name in data['Lessons']]
    parents = [Parent(id, ln, fn, sn) for id, ln, fn, sn in data['Parents']]

    students = [Student(id, ln, fn, sn, get_element_by_id(classes, cl_id))
                for id, ln, fn, sn, cl_id in data['Students']]
    teachers = [Teacher(id, ln, fn, sn, get_element_by_id(lessons, les_id))
                for id, ln, fn, sn, les_id in data['Teachers']]

    school = School(classes, lessons, teachers, students, parents)
    school.apply_student_parent_relation(relation_data['Students_Parents'])
    school.apply_class_teacher_relation(relation_data['Classes_Lessons_Teachers'])
    return school


def get_random_item(collection):
    return collection[random.randrange(len(collection))]


def main():

    file = ''
    if len(sys.argv) > 1:
        file = sys.argv[1]
    school = load_school(file)

    print('1. Получить полный список всех классов школы')
    print('Полный список всех классов школы')
    print(', '.join([cl.name for cl in school.classes]))
    print('-' * 50)

    print('2. Получить список всех учеников в указанном классе')
    cl = get_random_item([cl for cl in school.classes if len(cl.students) > 2])
    print(f'Случайный класс - {cl.name}:')
    print('\n'.join(sorted([st.__str__() for st in cl.students])))
    print('-' * 50)

    print('3. Получить список всех предметов указанного ученика')
    st = get_random_item(school.students)
    print(f'Случайный ученик - {st}:')
    print('\n'.join([t.lesson.name for t in st._class.teachers]))
    print('-' * 50)

    print('4. Узнать ФИО родителей указанного ученика')
    st = get_random_item(school.students)
    print(f'Случайный ученик - {st}:')
    print(f'Mother - {st.parents[0]}\nFather - {st.parents[1]}')
    print('-' * 50)

    print('5. Получить список всех Учителей, преподающих в указанном классе')
    cl: Class = get_random_item(school.classes)
    print(f'Случайный класс - {cl.name}:')
    print('\n'.join([t.__str__() for t in cl.teachers]))


if __name__ == '__main__':
    main()
