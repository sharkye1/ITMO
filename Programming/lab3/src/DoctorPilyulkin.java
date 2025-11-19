package Programming.lab3.src;

import java.util.Objects;
import java.util.Random;

// Доктор Пилюлькин
public class DoctorPilyulkin extends Person {
    private static final Random random = new Random();
    private Cabin assignedCabin;

    public DoctorPilyulkin(String name, int energy, Mood mood, Location location, Cabin cabin) {
        super(name, energy, mood, location);
        this.assignedCabin = cabin;
    }

    public void warn(String message) {
        System.out.println(message);
        decreaseEnergy(2);
    }

    public void goToCabin(Cabin cabin) {
        this.assignedCabin = cabin;
        setLocation(new Location(cabin.getName()));
        System.out.println(name + " забрался в " + cabin.getName() + ".");
        decreaseEnergy(5);
    }

    public void sleepDeeply(int hours) throws TooTiredException {
        if (energy < 10) {
            throw new TooTiredException(name + " слишком устал, чтобы нормально заснуть!");
        }
        sleepStatus = SleepStatus.ASLEEP;
        energy = Math.min(100, energy + hours * 12);
        System.out.println(name + " заснул крепко на " + hours + " часов и ни разу не проснулся.");

        // Случайность: иногда храпит громче
        if (random.nextBoolean()) {
            System.out.println("Из каюты слышен БОГАТЫРСКИЙ храп...");
        } else {
            System.out.println("Из каюты доносится тихое сопение.");
        }
    }

    @Override
    public void act() throws TooTiredException {
        if (energy < 20) {
            throw new TooTiredException(name + " слишком устал для действий!");
        }
        System.out.println(name + " проверяет здоровье остальных.");
        decreaseEnergy(10);
    }

    @Override
    public boolean equals(Object o) {
        if (!super.equals(o))
            return false;
        DoctorPilyulkin that = (DoctorPilyulkin) o;
        return Objects.equals(assignedCabin, that.assignedCabin);
    }

    @Override
    public int hashCode() {
        return Objects.hash(super.hashCode(), assignedCabin);
    }

    @Override
    public String toString() {
        return "DoctorPilyulkin{" +
                "name='" + name + '\'' +
                ", energy=" + energy +
                ", cabin=" + (assignedCabin != null ? assignedCabin.getName() : "none") +
                '}';
    }
}
