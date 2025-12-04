package Programming.lab3.src;

import java.util.ArrayList;
import java.util.List;

public class Scenario {
    private final List<Action> actions = new ArrayList<>();
    private final List<Character> characters = new ArrayList<>();

    public void addAction(Action a) {
        if (a != null)
            actions.add(a);
    }

    public void addCharacter(Character c) {
        if (c != null)
            characters.add(c);
    }

    // Выполнить сценарий строго по порядку добавленных действий
    public void run() {
        if (characters.isEmpty() || actions.isEmpty()) {
            try {
                throw new MyUncheckedScenarioException("Сценарий некорректен: нет персонажей или действий");
            } catch (MyUncheckedScenarioException e) {
                System.out.println("[Сценарий] " + e.getMessage());
                return;
            }
        }

        System.out.println("[Сценарий] Последовательное исполнение действий.");

        // По тексту: Пилюлькин предупреждает, уходит в каюту и спит 8 часов.
        Character pilulkin = findByNamePrefix("Доктор Пилюлькин");

        // Предполагаем, что действия добавлены в следующем порядке в Main:
        // 0 = SleepingAction, 1 = PaintingAction, 2 = ExploreAction, 3 = WakeAction
        Action sleep = actions.size() > 0 ? actions.get(0) : null;
        Action paint = actions.size() > 1 ? actions.get(1) : null;
        Action explore = actions.size() > 2 ? actions.get(2) : null;
        Action wake = actions.size() > 3 ? actions.get(3) : null;

        if (pilulkin != null && sleep != null) {
            pilulkin.performAction(sleep);
        }

        // Коротышки вылезли из постелей и занялись делами (пусть исследуют)
        for (Character c : characters) {
            if (c != pilulkin && explore != null) {
                c.performAction(explore);
            }
        }

        // Тюбик рисует лунные пейзажи
        Character tyubik = findByNamePrefix("Тюбик");
        if (tyubik != null && paint != null) {
            tyubik.performAction(paint);
        }

        // В конце сценария: попытаться разбудить Пилюлькина (если есть действие
        // пробуждения)
        if (pilulkin != null && wake != null) {
            pilulkin.performAction(wake);
        }

        // Итоговое описание состояний
        for (Character c : characters) {
            c.describeState();
        }
    }

    private Character findByNamePrefix(String prefix) {
        for (Character c : characters) {
            if (c.getName().startsWith(prefix))
                return c;
        }
        return null;
    }

}
