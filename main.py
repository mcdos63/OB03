import json
import csv

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

    @classmethod
    def save_animals_to_file(cls, file_data='data', file_type='TXT'):
        "Сохраняет список животных в файл указанного типа."
        # Функция для форматирования данных
        def format_animal(animal):
            return {
                "class": animal.__class__.__name__,
                "name": animal.name,
                "age": animal.age
            }

        # Подготовка данных
        data = []
        for animal in cls._my_zoo:
            if isinstance(animal, Animal):
                if hasattr(animal, 'name') and hasattr(animal, 'age'):
                    data.append(format_animal(animal))
                else:
                    print(f"Ошибка: Объект {animal} не имеет необходимых атрибутов.")
            else:
                print(f"Ошибка: Объект {animal} не является экземпляром класса Animal или его подклассов.")

        # Формируем имя файла
        file_path = f"{file_data}.{file_type.lower()}"

        try:
            # Открываем файл в режиме записи с соответствующей кодировкой
            with open(file_path, "w", encoding='utf-8') as file:
                match file_type.upper():
                    case 'TXT':
                        for entry in data:
                            json_str = json.dumps(entry, ensure_ascii=False)
                            file.write(f"{json_str}\n")
                        print(f"Данные успешно сохранены в {file_path} в формате TXT.")

                    case 'JSON':
                        json.dump(data, file, ensure_ascii=False, indent=4)
                        print(f"Данные успешно сохранены в {file_path} в формате JSON.")

                    case 'CSV':
                        writer = csv.DictWriter(file, fieldnames=["class", "name", "age"])
                        writer.writeheader()
                        for entry in data:
                            writer.writerow(entry)
                        print(f"Данные успешно сохранены в {file_path} в формате CSV.")

                    case _:
                        print("Неподдерживаемый тип файла. Доступные типы: TXT, JSON, CSV.")
        except IOError as e:
            print(f"Ошибка ввода-вывода: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


    @classmethod
    def load_animals_from_file(cls, file_data='data', file_type='TXT'):
        """
        Загружает данные из файла и создает объекты указанного класса.

        :param cls: Класс, экземпляры которого нужно создать.
        :param file_data: Имя файла без расширения.
        :param file_type: Тип файла ('TXT', 'JSON', 'CSV').
        :return: Список объектов класса cls.
        """
        # Проверяем, что cls - это класс
        if not isinstance(cls, type):
            print("Первый параметр должен быть классом.")
            return []

        file_path = f"{file_data}.{file_type.lower()}"

        try:
            with open(file_path, "r", encoding='utf-8') as file:
                if file_type.upper() == 'TXT':
                    data = []
                    for line in file:
                        entry = json.loads(line)
                        data.append(entry)
                elif file_type.upper() == 'JSON':
                    data = json.load(file)
                elif file_type.upper() == 'CSV':
                    reader = csv.DictReader(file)
                    data = [row for row in reader]
                else:
                    print("Неподдерживаемый тип файла.")
                    return []

            # Создаем объекты
            for entry in data:
                class_name = entry['class']
                if class_name in globals():
                    obj_class = globals()[class_name]
                    obj = obj_class(name=entry['name'], age=entry['age'])
                    # cls._my_zoo.append(obj)
                else:
                    print(f"Ошибка: Класс {class_name} не найден.")

        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
            return []
        except IOError as e:
            print(f"Ошибка ввода-вывода: {e}")
            return []
        except json.JSONDecodeError:
            print("Ошибка при декодировании JSON.")
            return []
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return []

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

toro = Mammal("Борька", 4)
print(Mammal.__dict__)
print(toro.__dict__, toro.__class__.__name__)

zoopark = None

vt = Veterinarian("Пилюлькин")
hunter = Hanter("Иван Охотник")
hunter.slaughter_animal('Овца Надя')
Animal.view_zoo()
vt.heal_animal('Сторож Петрович')
# Сохраняем данные в TXT файл
Animal.save_animals_to_file()
# # Сохраняем данные в JSON файл
# save_animals_to_file(zoopark, 'animals_data', 'JSON')
# # Сохраняем данные в CSV файл
# save_animals_to_file(zoopark, 'animals_data', 'CSV')
hunter.slaughter_animal("просто Петух")
hunter.slaughter_animal("Павлин Мавлин")
hunter.slaughter_animal("Варан Абрам Генрихович")
hunter.slaughter_animal("Баран Людовиг")
hunter.slaughter_animal("Борька")
Animal.view_zoo()
Animal.load_animals_from_file()
Animal.view_zoo()

input("\n😀 Нажмите Enter для выхода")
