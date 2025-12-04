package Programming.lab3.src;

public class Main {
    public static void main(String[] args) {
        Location pilulkinCabin = new Location("Каюта Пилюлькина");
        Location commonCabin = new Location("Общая каюта");

        Human pilulkin = new Human("Доктор Пилюлькин", Mood.AWAKE, pilulkinCabin);
        Shorty tyubik = new Shorty("Тюбик", Mood.AWAKE, commonCabin);
        Shorty korotysh1 = new Shorty("Коротышка-1", Mood.AWAKE, commonCabin);
        Shorty korotysh2 = new Shorty("Коротышка-2", Mood.AWAKE, commonCabin);

        Scenario scenario = new Scenario();
        scenario.addCharacter(pilulkin);
        scenario.addCharacter(tyubik);
        scenario.addCharacter(korotysh1);
        scenario.addCharacter(korotysh2);

        // Базовые действия
        scenario.addAction(new SleepingAction(8, false)); // Пилюлькин спит 8 часов и не просыпается
        scenario.addAction(new PaintingAction("лунные пейзажи")); // Тюбик рисует лунные пейзажи
        scenario.addAction(new ExploreAction("выход из постелей")); // Коротышки исследуют
        scenario.addAction(new WakeAction()); // действие пробуждения, выполняется в конце сценария

        // Пилюлькин засыпает, коротышки слышат храп и занимаются делами
        System.out.println("— Предупреждение сделано. Все расходятся по делам.\n");

        scenario.run();
    }
}
