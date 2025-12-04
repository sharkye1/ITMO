package Programming.lab3.src;

import java.util.ArrayList;
import java.util.List;

public class Cabin {
    private final String name;
    private final List<Character> occupants = new ArrayList<>();

    public Cabin(String name) {
        if (name == null)
            throw new IllegalArgumentException("name is required");
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void addCharacter(Character c) {
        if (c == null)
            return;
        if (!occupants.contains(c)) {
            occupants.add(c);
        }
    }

    public void removeCharacter(Character c) {
        occupants.remove(c);
    }

    public boolean hasCharacter(Character c) {
        return occupants.contains(c);
    }

    public List<Character> getOccupants() {
        return List.copyOf(occupants);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || getClass() != o.getClass())
            return false;
        Cabin cabin = (Cabin) o;
        return name.equals(cabin.name);
    }

    @Override
    public int hashCode() {
        return name.hashCode();
    }

    @Override
    public String toString() {
        return "Cabin{" +
                "name='" + name + '\'' +
                ", occupants=" + occupants.size() +
                '}';
    }
}
