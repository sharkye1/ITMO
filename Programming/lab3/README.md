# Лабораторная 3 — Объектная модель по отрывку

На основе отрывка (Пилюлькин, Тюбик и коротышки) разработана простая объектная модель и сценарий.

## Запуск

Скомпилировать и запустить `Programming/lab3/src/Main.java` (пакет `Programming.lab3.src`). При запуске выводится рассказ о том, как Пилюлькин заснул, коротышки занялись делами, а Тюбик снял скафандр и начал рисовать.

## UML-диаграмма (Mermaid)

```mermaid
classDiagram
    direction TB

    class Person {
      - String name
      - SleepStatus sleepStatus
      + Person(String)
      + String getName()
      + SleepStatus getSleepStatus()
      + void getOutOfBed()
    }

    class DoctorPilyulkin {
      - Cabin currentCabin
      + DoctorPilyulkin(String)
      + void warn(String)
      + void goToCabin(Cabin)
      + void sleepHours(int)
    }

    class Tyubik {
      - EquipmentStatus equipment
      - List~String~ paintings
      + Tyubik(String)
      + void removeSpacesuit()
      + void paint(String)
      + List~String~ getPaintings()
    }

    class Shorty {
      + Shorty(String)
      + void doSomething(String)
    }

    class Cabin {
      - String name
      + Cabin(String)
      + String getName()
    }

    enum SleepStatus {
      AWAKE
      ASLEEP
    }

    enum EquipmentStatus {
      SPACESUIT_ON
      SPACESUIT_OFF
    }

    Person <|-- DoctorPilyulkin
    Person <|-- Tyubik
    Person <|-- Shorty
    DoctorPilyulkin --> Cabin
```

## Краткий сценарий
- Доктор Пилюлькин предупреждает и уходит спать в свою каюту, спит 8 часов, слышен богатырский храп.
- Коротышки просыпаются, один записывает наблюдения, другой наводит порядок.
- Тюбик сбрасывает скафандр и начинает рисовать лунные пейзажи.

## Примечания
- Текст вывода — на русском, отражает изменения состояний объектов.
- Модель упрощена, при необходимости можно дополнить новыми классами и действиями.
