package Programming.lab3.src;

import java.util.ArrayList;
import java.util.List;

public class Location {
    private final String name;

    public Location(String name) {
        if (name == null)
            throw new IllegalArgumentException("name is required");
        this.name = name;
    }

    public String getName() {
        return name;
    }

    // Динамически находит всех персонажей с location == this
    public List<Character> getOccupants(List<Character> allCharacters) {
        List<Character> result = new ArrayList<>();
        for (Character c : allCharacters) {
            if (this.equals(c.getLocation())) {
                result.add(c);
            }
        }
        return result;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || getClass() != o.getClass())
            return false;
        Location location = (Location) o;
        return name.equals(location.name);
    }

    @Override
    public int hashCode() {
        return name.hashCode();
    }

    @Override
    public String toString() {
        return "Location{name='" + name + "'}";
    }
}
