package Programming.lab3.src;


import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Random;

// Художник Тюбик
public class Tyubik extends Person {
    private static final Random random = new Random();
    private EquipmentStatus equipment = EquipmentStatus.SPACESUIT_ON;
    private final List<String> paintings = new ArrayList<>();

    public Tyubik(String name, int energy, Mood mood, Location location) {
        super(name, energy, mood, location);
    }

    public void removeSpacesuit() {
        if (equipment == EquipmentStatus.SPACESUIT_OFF) {
            System.out.println(name + " уже без скафандра.");
            return;
        }
        equipment = EquipmentStatus.SPACESUIT_OFF;
        System.out.println(name + " сбросил скафандр, чтобы скорее запечатлеть увиденное на Луне.");
        decreaseEnergy(5);
    }

    public void paint(String subject) throws TooTiredException {
        if (energy < 15) {
            throw new TooTiredException(name + " слишком устал, чтобы рисовать!");
        }
        if (equipment == EquipmentStatus.SPACESUIT_ON) {
            // unchecked exception: нельзя рисовать в скафандре
            throw new InvalidActionException(name + " не может рисовать в скафандре!");
        }
        paintings.add(subject);
        System.out.println(name + " принялся рисовать: " + subject + ".");
        decreaseEnergy(10);

        // Случайность: иногда вдохновение приходит
        if (random.nextInt(100) < 30) {
            System.out.println(name + " вдохновлён и рисует с удвоенной энергией!");
            mood = Mood.INSPIRED;
        }
    }

    @Override
    public void act() throws TooTiredException {
        if (energy < 15) {
            throw new TooTiredException(name + " слишком устал для творчества!");
        }
        if (equipment == EquipmentStatus.SPACESUIT_OFF) {
            System.out.println(name + " рисует очередной лунный пейзаж.");
            paintings.add("Случайный лунный пейзаж");
            decreaseEnergy(10);
        } else {
            System.out.println(name + " думает о том, что нарисовать.");
        }
    }

    public List<String> getPaintings() {
        return new ArrayList<>(paintings);
    }

    @Override
    public boolean equals(Object o) {
        if (!super.equals(o))
            return false;
        Tyubik tyubik = (Tyubik) o;
        return equipment == tyubik.equipment &&
                Objects.equals(paintings, tyubik.paintings);
    }

    @Override
    public int hashCode() {
        return Objects.hash(super.hashCode(), equipment, paintings);
    }

    @Override
    public String toString() {
        return "Tyubik{" +
                "name='" + name + '\'' +
                ", energy=" + energy +
                ", equipment=" + equipment +
                ", paintings=" + paintings.size() +
                '}';
    }
}
