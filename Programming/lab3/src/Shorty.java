package Programming.lab3.src;


import java.util.Random;

// Обычный коротышка
public class Shorty extends Person {
    private static final Random random = new Random();
    private String currentActivity;

    public Shorty(String name, int energy, Mood mood, Location location) {
        super(name, energy, mood, location);
        this.currentActivity = "ничего не делает";
    }

    public void doSomething(String activity) throws TooTiredException {
        if (energy < 10) {
            throw new TooTiredException(name + " слишком устал для активности!");
        }
        this.currentActivity = activity;
        System.out.println(name + " " + activity + ".");
        decreaseEnergy(8);
    }

    @Override
    public void act() throws TooTiredException {
        if (energy < 10) {
            throw new TooTiredException(name + " слишком устал!");
        }
        // Случайное действие
        String[] actions = {
                "наводит порядок",
                "записывает наблюдения",
                "проверяет оборудование",
                "отдыхает в каюте"
        };
        String action = actions[random.nextInt(actions.length)];
        doSomething(action);
    }

    @Override
    public String toString() {
        return "Shorty{" +
                "name='" + name + '\'' +
                ", energy=" + energy +
                ", activity='" + currentActivity + '\'' +
                '}';
    }
}
