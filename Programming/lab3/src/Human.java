package Programming.lab3.src;

public class Human extends Character {
    public Human(String name, Mood mood, Location location) {
        super(name, mood, location);
    }

    @Override
    public String describeState() {
        String desc = getName() + " сейчас в настроении: " + getMood() + ", локация: " + getLocation().getName();
        System.out.println(desc);
        return desc;
    }
}
