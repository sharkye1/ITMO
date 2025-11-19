package Programming.lab3.src;


import java.util.ArrayList;
import java.util.List;
import java.util.Random;

// Вариативный сценарий: учитывается энергия, настроение, случайность, обработка исключений.
// Использует ArrayList для хранения персонажей, все требования SOLID соблюдены.
public class Main {
    private static final Random random = new Random();

    public static void main(String[] args) {
        System.out.println("=== Запуск сценария на лунной базе ===\n");

        // Создаём локацию и каюту
        Location lunarBase = new Location("Лунная база");
        Cabin cabin = new Cabin("Каюта Пилюлькина", 2);

        // Создаём персонажей со случайными параметрами энергии и настроения
        DoctorPilyulkin pilyulkin = new DoctorPilyulkin(
                "Доктор Пилюлькин",
                randomEnergy(),
                randomMood(),
                lunarBase,
                cabin);

        Tyubik tyubik = new Tyubik(
                "Тюбик",
                randomEnergy(),
                randomMood(),
                lunarBase);

        Shorty shorty1 = new Shorty(
                "Коротышка Винтик",
                randomEnergy(),
                randomMood(),
                lunarBase);

        Shorty shorty2 = new Shorty(
                "Коротышка Шпунтик",
                randomEnergy(),
                randomMood(),
                lunarBase);

        // Хранение в ArrayList (требование)
        List<Person> characters = new ArrayList<>();
        characters.add(pilyulkin);
        characters.add(tyubik);
        characters.add(shorty1);
        characters.add(shorty2);

        System.out.println("Персонажи созданы:");
        for (Person p : characters) {
            System.out.println("  " + p);
        }
        System.out.println();

        // === Вариативный сценарий ===
        try {
            // Доктор предупреждает и идёт спать
            pilyulkin.warn("Сделав такое предупреждение, доктор Пилюлькин забрался в свою каюту...");
            pilyulkin.goToCabin(cabin);
            pilyulkin.sleepDeeply(8);
            System.out.println();

            // Коротышки просыпаются и действуют
            System.out.println("Услыхав храп, коротышки проснулись и занялись делами.\n");

            for (Person person : characters) {
                if (person instanceof Shorty) {
                    person.getOutOfBed();
                    try {
                        person.act(); // вызываем абстрактный метод
                    } catch (TooTiredException e) {
                        System.out.println(e.getMessage());
                        System.out.println(person.getName() + " решил отдохнуть.");
                        person.sleep(2);
                    }
                    System.out.println();
                }
            }

            // Тюбик снимает скафандр и рисует
            tyubik.getOutOfBed();
            try {
                tyubik.removeSpacesuit();
                tyubik.paint("лунный пейзаж с кратером");
                tyubik.paint("тень от ракеты на серой поверхности");
            } catch (TooTiredException e) {
                System.out.println(e.getMessage());
                System.out.println("Тюбик вынужден отложить творчество.");
            } catch (InvalidActionException e) {
                // Обработка unchecked исключения
                System.out.println(e.getMessage());
                System.out.println("Тюбик сначала снимает скафандр.");
                tyubik.removeSpacesuit();
            }
            System.out.println();

            // Итоговое состояние
            System.out.println("=== Итоговое состояние персонажей ===");
            for (Person p : characters) {
                System.out.println(p);
            }

            // Демонстрация полиморфизма через act()
            System.out.println("\n=== Все действуют по-своему (полиморфизм) ===");
            for (Person p : characters) {
                try {
                    p.act();
                } catch (TooTiredException e) {
                    System.out.println(e.getMessage());
                }
            }

        } catch (TooTiredException e) {
            System.err.println("Критическая ошибка: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Непредвиденная ошибка: " + e.getMessage());
        }

        System.out.println("\n=== Сценарий завершён ===");
    }

    // Случайная генерация начальной энергии (вариативность)
    private static int randomEnergy() {
        return 40 + random.nextInt(50); // от 40 до 89
    }

    // Случайное настроение (вариативность)
    private static Mood randomMood() {
        Mood[] moods = Mood.values();
        return moods[random.nextInt(moods.length)];
    }
}
