package Programming.lab3.src;

public class Shorty extends Character {
    public Shorty(String name, Mood mood, Location location) {
        super(name, mood, location);
    }

    @Override
    public String describeState() {
        String desc = "Коротышка " + getName() + ": настроение=" + getMood() + ", локация=" + getLocation().getName();
        System.out.println(desc);
        return desc;
    }
}
