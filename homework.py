from dataclasses import dataclass
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str  # Имя класса тренировки
    duration: float  # Длительность тренировки в часах
    distance: float  # Дистанция
    speed: float  # Средняя скорость
    calories: float  # Колличество килокалорий

    def __str__(self) -> str:
        """Текст информационного сообщения"""

        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )

    def get_message(self) -> str:
        return str(self)


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # Атрибут класса. Расстояние за одно действие/шаг.
    M_IN_KM: int = 1000  # Атрибут класса. Константа.

    def __init__(
        self,
        action: int,  # Колличество совершенных действий.
        duration: float,  # Длительность тренировки.
        weight: float  # Вес спортсмена.
    ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return (
            self.action
            * Training.LEN_STEP
            / Training.M_IN_KM
        )

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (
            self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass  # Рассчитывается в дочерних классах.

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(
            self.__class__.__name__,  # Создаем объекты
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    М_IN_H: int = 60
    CONST_RUNN_1: int = 18
    CONST_RUNN_2: int = 20

    def get_spent_calories(self) -> float:
        """Рассчитываем каллории за тренировку."""

        return ((
            Running.CONST_RUNN_1
            * self.get_mean_speed()
            - Running.CONST_RUNN_2)
            * self.weight / Training.M_IN_KM
            * self.duration
            * Running.М_IN_H
        )  # Рассчитываем калории.


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CONST_WALK_1: float = 0.035
    CONST_WALK_2: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:

        super().__init__(
            action,
            duration,
            weight
        )

        self.height = height  # Принимаем доп. параметр рост спортсмена

    def get_spent_calories(self) -> float:
        """Рассчитываем каллории за тренировку."""

        return ((
            SportsWalking.CONST_WALK_1
            * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * SportsWalking.CONST_WALK_2
            * self.weight)
            * self.duration
            * Running.М_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CONST_SWIMM_1: float = 1.1
    CONST_SWIMM_2: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,  # Новое свойство. Длина бассейна.
        count_pool: float  # Колличество переплытий.
    ) -> None:

        super().__init__(
            action,
            duration,
            weight
        )

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return (
            self.action
            * Swimming.LEN_STEP
            / Training.M_IN_KM
        )  # Рассчитываем дистанцию.

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания"""

        return (
            self.length_pool
            * self.count_pool
            / Training.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        """Рассчитываем расход каллорий при плавании"""

        return ((
            self.get_mean_speed()
            + Swimming.CONST_SWIMM_1)
            * Swimming.CONST_SWIMM_2
            * self.weight
        )


def read_package(
    workout_type: str,
    data: List[int]
) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_type = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking
                     }
    try:
        return training_type[workout_type](*data)
    except KeyError:
        print('Несуществующие данные!')


def main(training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
