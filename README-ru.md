# Pygame entities
**Pygame entities** - библиотека для игрового движка [Pygame](https://www.pygame.org/) на языке [python](https://www.python.org/)

Является надстройкой над библиотекой pygame, добавляет систему сущностей.

# Установка pygame entities

Установить библиотеку можно такой командой:  
`pip install git+https://github.com/radyshenkya/pygame_entities`

---
# Начало работы
Каждый проект на **pygame entities** базируется на классе *Game* в модуле *game*.

Программа, которая представляет из себя просто черное окно выглядит вот так:

```py
# Импортируем класс Game
from game import Game

# Получаем инстанс game обьекта, задаем окну 500x500 разрешение
game = Game.get_instance((500, 500))

# Запускаем основной цикл игры
game.run()
```

Здесь мы:
1. Импортируем класс `Game`
2. Получаем объект класса `Game`. Важно получать его именно через `get_instance()`. Этот класс написан по паттерну Singleton, и может быть только 1 во всем проекте. Вызывать конструктор у класса `Game` нельзя.
3. Запускаем основной цикл программы.


У вас должно появиться черное окно 500x500 пикселей.

# Спрайты
Все спрайты в игре представлены классом `BaseSprite`. Этот класс наследуется от `pygame.sprite.Sprite`.

Сам по себе класс `BaseSprite` принимает в свой конструктор объект класса `pygame.Surface` - картинка спрайта, `layer` - слой, на котором находится спрайт (Спрайты с большим значение слоя рендерятся поверх спрайтов с меньшим значением слоя), `start_position` - кортеж с 2 значениями, которые отображают позицию нашего спрайта на экране.

Каждый спрайт в игре должен либо быть объектом класса `BaseSprite`, либо быть объектом дочернего класса от `BaseSprite`.

Давайте создадим в нашей игре новый спрайт:
```py
from pygame_entities.utils.drawable import BaseSprite
from pygame_entities.game import Game

import pygame

game = Game.get_instance((500, 500))

# <-- НОВЫЙ КОД -->
# Создаем новый pygame.Surface.
test_sprite_surface = pygame.Surface((64, 64))
test_sprite_surface.fill((255, 255, 255))

# Создаем новый спрайт в мире.
test_sprite = BaseSprite(test_sprite_surface)
test_sprite.center_position = (250, 250)
# <-- КОНЕЦ НОВОГО КОДА -->

game.run()
```

В модуле `pygame_entities.utils.drawable` есть много других типов спрайтов, например `FontSprite` может отображать текст, а `AnimatedSprite` может менять отображаемые картинки с каким-то промежутком во времени (отображать анимацию из спрайтов).


# Сущности
Сущности - это какие-то объекты в игровом пространстве, обладающие какой-либо функциональностью.

Базовый класс сущности - `Entity`, находится в модуле `pygame_entities.entities.entity`.
Сам по себе он обладает только какой-то позицией и id сущности в игре, поэтому изначально он бесполезен.

Но на основе его мы можем создать свой объект.
Создадим сущность, которая с каждым кадром будет перемещаться на какой-то вектор. Так же добавим ей спрайт (что бы мы могли видеть, что она все таки перемещается)

(класс сущности)
```py
# Нужно добавить импорты
from pygame_entities.utils.math import Vector2
from pygame_entities.entities.entity import Entity

class MovingEntity(Entity):
    def __init__(self, position: Vector2, sprite: BaseSprite, moving_vector: Vector2) -> None:
        super().__init__(position)  # Нужно обязательно, а то не будет работать
        self.sprite = sprite

        # Вектор движения нашей сущности
        self.moving_vector = moving_vector

        # Подписываем нашу функцию на вызов ее каждый кадр
        self.subscribe_on_update(self.move)

    # Эта функия будет вызываться каждый кадр. delta_time - сколько времени в секундах заняло переключение с прошлого кадра
    def move(self, delta_time: float):
        # Добавляем к нашей позиции вектор смещения нашей сущности
        self.position += self.moving_vector

        # Обновляем позицию нашего спрайта. Vector2().get_integer_tuple() возвращает кортеж, с округленными до целого числа значениями x и y
        self.sprite.center_position = self.position.get_integer_tuple()
```

Здесь можно увидеть то, как можно создать функцию, которая будет вызываться каждый кадр от нашей сущности. Для этого используется функция из класса `Entity` - `subscribe_on_update()`, куда передается та функция, которую нам нужно вызывать каждый кадр.

Так же здесь применяется класс `Vector2` из модуля `pygame_entities.utils.math`. По сути этот класс представляет вектор с двумя числами - `x` и `y`, и поддерживает математические операции. Позиция каждой сущности хранится именно в виде объекта класса `Vector2`.


Теперь давайте создадим нашу сущность в игре.
Для этого нужно просто вызвать конструктор класса сущности - `MovingEntity()`:
```py
# ..идет после объявления класса новой сущности

game = Game.get_instance((500, 500))

test_sprite_surface = pygame.Surface((64, 64))
test_sprite_surface.fill((255, 255, 255))
test_sprite = BaseSprite(test_sprite_surface)
test_sprite.center_position = (250, 250)

# <-- НОВЫЙ КОД -->
# Вектор позиции нашей сущности
entity_start_position = Vector2(0, 100)

# Вектор движения нашей сущности
moving_vector = Vector2(1, 0)

# Создаем новую сущность в нашем мире
moving_right_entity = MovingEntity(entity_start_position, test_sprite, moving_vector)
# <-- КОНЕЦ НОВОГО КОДА -->

game.run()
```

# Миксины сущностей
Миксины сущностей - это классы, которые расширяют функционал наших сущностей. Они находятся в модуле `pygame_entities.entities.mixins`.
Добавим нашей сущности пару миксинов - `SpriteMixin` и `CollisionMixin`.

`SpriteMixin` добавляет нашей сущности спрайт, привязанный к позиции нашей сущности. С помощью него нам не придется каждый раз вручную изменять позицию спрайта - за нас это будет делать миксин.
`CollisionMixin` отвечает за столкновения с другими сущностями, которые имеют такой же миксин. Сделаем так, что бы при столкновении с другой сущностью, эти 2 сущности удалялись.

Для начала добавим в наш класс `SpriteMixin`:
```py
# Добавляем импорт миксина
from pygame_entities.entities.mixins import SpriteMixin

class MovingEntity(SpriteMixin):
    def __init__(self, position: Vector2, sprite: BaseSprite, moving_vector: Vector2) -> None:
        super().__init__(position)  # Нужно обязательно, а то не будет работать

        # Инициализируем наш миксин
        self.sprite_init(sprite)

        self.moving_vector = moving_vector
        self.subscribe_on_update(self.move)

    def move(self, delta_time: float):
        self.position += self.moving_vector

        # Теперь эта строчка не нужна, и ее можно просто удалить.
        # self.sprite.center_position = self.position.get_integer_tuple()
```

Каждый миксин - это дочерний класс от класса `Entity`, но он не изменяет его конструктор. Вместо этого он добавляет какой-то метод для инициализации функционала этого миксина. (Например, у `SpriteMixin` метод инициализации назван `sprite_init()`)

Если запустить нашу тестовую игру сейчас, ничего не должно измениться.

Теперь добавим `CollisionMixin`:
```py
# Добавим в импорт миксинов CollisionMixin
from pygame_entities.entities.mixins import SpriteMixin, CollisionMixin

class MovingEntity(SpriteMixin, CollisionMixin):
    def __init__(self, position: Vector2, sprite: BaseSprite, moving_vector: Vector2) -> None:
        super().__init__(position)  # Нужно обязательно, а то не будет работать
        self.sprite_init(sprite)

        # Задаем размер коллайдера нашей сущности. Он задается объектом Vector2. Его размеры в пикселях
        collider_size = Vector2(64, 64)

        # Инициализируем миксин коллизии.
        # is_trigger - является ли этот коллайдер триггером
        # is_check_collision - вызываются ли события у этой сущности, при столкновении с другими сущностями.
        self.collision_init(collider_size, is_trigger=False,
                            is_check_collision=True)

        # Подключаем наш метод на вызов при коллизии с другой сущностью
        self.subscribe_on_collide(self.destroy_on_collide)

        self.moving_vector = moving_vector
        self.subscribe_on_update(self.move)

    # Новый метод, вызывается при столкновении двух сущностей, с коллайдерами не триггерами
    # another_entity - сущность, с которой произошло столкновение
    # self_collider_rect - объект типа pygame.Rect - означает наш коллайдер.
    # other_collider_rect - объект типа pygame.Rect - означает коллайдер сущности, с которой столкнулись
    def destroy_on_collide(self, another_entity: Entity, self_collider_rect, other_collider_rect):
        # Удаляем нашу сущность
        self.destroy()
        # Удаляем сущность с которой столкнулись
        another_entity.destroy()

    def move(self, delta_time: float):
        self.position += self.moving_vector
```
Здесь можно увидеть новый метод у сущности - `entity.destroy()` - этот метод удаляет сущность из игры.

Теперь нужно создать 2 сущности класса `MovingEntity`, что бы посмотреть, что они исчезнут при столкновении:
```py
game = Game.get_instance((500, 500))

test_sprite_surface = pygame.Surface((64, 64))
test_sprite_surface.fill((255, 255, 255))

# Создаем сущность которая движется вправо
moving_right_entity = MovingEntity(
    position=Vector2(0, 100), sprite=BaseSprite(test_sprite_surface), moving_vector=Vector2(1, 0))

# Создаем сущность, которая движется влево
moving_left_entity = MovingEntity(
    position=Vector2(500, 100), sprite=BaseSprite(test_sprite_surface), moving_vector=Vector2(-1, 0))

game.run()
```

При столкновении они должны исчезнуть.


# Pygame события
Для обработки событий `pygame` в классе `Game` имеется метод для подписки на определенные события разных функций.

Подписанные функции будут вызываться именно тогда, когда определенное событие произошло.

При разработке игры с этой библиотекой необходимо использовать именно такой подход к событиям `pygame`, ибо мы должны вызывать в 1 кадр только одну функцию `pygame.events.get()` (Если вызывать ее более чем 1 раз, все события за этот кадр получит только первый вызов этой функции, в других вызовах же будут попадаться пустые списки.)

Давайте создадим функцию для выхода из нашей игры по нажатию на крестик окна. Для этого напишем новую функцию `on_quit()`, и подключим ее через метод `Game.subscribe_for_event()`:
```py
# ..начало файла пропущено, там ничего не изменилось
game = Game.get_instance((500, 500))

# Создаем функцию для выхода из нашей программы.
def on_quit(event: pygame.event.Event):
    # Получаем объект нашей игры и останавливаем ее.
    Game.get_instance().running = False

# Подключаем нашу функцию к событию pygame.QUIT
game.subsribe_for_event(on_quit, pygame.QUIT)

# далее так же нет изменений... 
```

С этого момента окно можно закрыть по клику на крестик

