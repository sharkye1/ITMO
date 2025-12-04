package Programming.lab3.src;

public abstract class Character {
    private final String name;
    private Mood mood;
    private Location location;

    protected Character(String name, Mood mood, Location initialLocation) {
        if (name == null)
            throw new IllegalArgumentException("name is required");
        if (mood == null)
            throw new IllegalArgumentException("mood is required");
        this.name = name;
        this.mood = mood;
        this.location = (initialLocation != null) ? initialLocation : World.get();
    }

    public String getName() {
        return name;
    }

    public Mood getMood() {
        return mood;
    }

    public void setMood(Mood mood) {
        if (mood == null)
            throw new IllegalArgumentException("mood is required");
        this.mood = mood;
    }

    public Location getLocation() {
        return location;
    }

    public void moveTo(Location newLocation) {
        Location target = (newLocation != null) ? newLocation : World.get();
        this.location = target;
        System.out.println(name + " переместился в '" + target.getName() + "'.");
    }

    public void performAction(Action action) {
        try {
            action.execute(this);
        } catch (CharacterNotInCabinException | WrongActionException e) {
            System.out.println("[Предупреждение] " + e.getMessage());
        } catch (RuntimeException re) {
            System.out.println("[Неожиданное исключение] " + re.getMessage());
        }
    }

    public abstract String describeState();

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || getClass() != o.getClass())
            return false;
        Character character = (Character) o;
        return name.equals(character.name);
    }

    @Override
    public int hashCode() {
        return name.hashCode();
    }

    @Override
    public String toString() {
        return getClass().getSimpleName() + "{" +
                "name='" + name + '\'' +
                ", mood=" + mood +
                ", location=" + location.getName() +
                '}';
    }
}
