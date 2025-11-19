package Programming.lab3.src;


import java.util.Objects;

// Базовый персонаж с абстрактным методом act()
public abstract class Person implements Sleepable {
    protected final String name;
    protected SleepStatus sleepStatus = SleepStatus.AWAKE;
    protected int energy; // 0-100, влияет на поведение
    protected Mood mood;
    protected Location currentLocation;

    public Person(String name, int initialEnergy, Mood mood, Location location) {
        this.name = name;
        this.energy = Math.max(0, Math.min(100, initialEnergy));
        this.mood = mood;
        this.currentLocation = location;
    }

    public String getName() {
        return name;
    }

    public SleepStatus getSleepStatus() {
        return sleepStatus;
    }

    public int getEnergy() {
        return energy;
    }

    public Mood getMood() {
        return mood;
    }

    public Location getCurrentLocation() {
        return currentLocation;
    }

    public void setLocation(Location location) {
        this.currentLocation = location;
    }

    // Абстрактный метод: каждый персонаж действует по-своему
    public abstract void act() throws TooTiredException;

    public void getOutOfBed() {
        if (sleepStatus == SleepStatus.ASLEEP) {
            sleepStatus = SleepStatus.AWAKE;
        }
        System.out.println(name + " вылез из постели.");
    }

    // Реализация интерфейса Sleepable
    @Override
    public void sleep(int hours) {
        sleepStatus = SleepStatus.ASLEEP;
        energy = Math.min(100, energy + hours * 10); // восстанавливаем энергию
        System.out.println(name + " спит " + hours + " часов. Энергия восстановлена до " + energy + ".");
    }

    protected void decreaseEnergy(int amount) {
        energy = Math.max(0, energy - amount);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || getClass() != o.getClass())
            return false;
        Person person = (Person) o;
        return energy == person.energy &&
                Objects.equals(name, person.name) &&
                sleepStatus == person.sleepStatus &&
                mood == person.mood;
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, sleepStatus, energy, mood);
    }

    @Override
    public String toString() {
        return getClass().getSimpleName() + "{" +
                "name='" + name + '\'' +
                ", sleepStatus=" + sleepStatus +
                ", energy=" + energy +
                ", mood=" + mood +
                ", location=" + currentLocation +
                '}';
    }
}
