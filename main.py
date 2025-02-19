class Animal:
    _my_zoo = []

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Animal._my_zoo.append(self)

    @classmethod
    def fn(cls, name):  # найти тварь по имени
        return next((animal for animal in cls._my_zoo if animal.name == name), None)

    @classmethod
    def view_zoo(cls):
        print(format(" Список животных: ", "-^65"))
        for animal in cls._my_zoo:
            print(f'{animal.name:<23} возраст {animal.age:>4}.\t', end="")
            animal_sounds(animal)
        print(format(len(cls._my_zoo), "-^65"))

    def delete_animal(self):
        if self in Animal._my_zoo:
            print(f'Убит {self.name}')
            Animal._my_zoo.remove(self)
            del self

    def __del__(self):
        if self in Animal._my_zoo:
            Animal._my_zoo.remove(self)

    def make_sound(self):
        print("Говорит не по-русски!")

    def eat(self):
        print("Ест!")


class Persons:
    def __init__(self, name):
        self.name = name


class ZooKeeper(Persons):
    def feed_animal(self, animal_name):
        animal = Animal.fn(animal_name.strip())
        if animal:
            print(f"{self.name} кормит {animal.name} ", end="")
            animal.eat()


class Veterinarian(Persons):
    def heal_animal(self, animal_name):
        animal = Animal.fn(animal_name.strip())
        if animal:
            print(f"{self.name} лечит {animal.name} ")


class Hanter(Persons):
    def slaughter_animal(self, animal_name):
        animal = Animal.fn(animal_name.strip())
        if animal:
            print(f"{self.name} охотится за {animal_name} ({animal.age} лет) ")
            animal.delete_animal()


class Bird(Animal):
    def make_sound(self):
        print("Говорит на птичьем языке")


class Mammal(Animal):
    def make_sound(self):
        print("Что-то блеет")


class Reptile(Animal):
    def make_sound(self):
        print("Открывает пасть молча")


def animal_sounds(animal):
    animal.make_sound()

# Создаем зоопарк
zoopark = [Animal("Сторож Петрович", 100), Bird("просто Петух", 1), Mammal("Овца Надя", 3),
           Reptile("Аллигатор Геннадий", 20), Bird("Павлин Мавлин", 4), Reptile("Варан Абрам Генрихович", 31)]

print(zoopark[2].name, end=" - ")
zoopark[2].eat()

zoopark.append(Mammal("Баран Людовиг", 4))
print('Добавлен вручную', zoopark[-1].name)

zoopark = None

vt=Veterinarian("Пилюлькин")
hunter = Hanter("Иван Охотник")
hunter.slaughter_animal('Овца Надя')
Animal.view_zoo()
vt.heal_animal('Сторож Петрович')
input("\n😀 Нажмите Enter для выхода")
