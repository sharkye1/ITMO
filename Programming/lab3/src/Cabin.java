package Programming.lab3.src;

import java.util.Objects;

// Каюта на корабле/станции
public class Cabin {
    private final String name;
    private final int capacity;

    public Cabin(String name, int capacity) {
        this.name = name;
        this.capacity = capacity;
    }

    public String getName() {
        return name;
    }

    public int getCapacity() {
        return capacity;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || getClass() != o.getClass())
            return false;
        Cabin cabin = (Cabin) o;
        return capacity == cabin.capacity && Objects.equals(name, cabin.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, capacity);
    }

    @Override
    public String toString() {
        return "Cabin{" +
                "name='" + name + '\'' +
                ", capacity=" + capacity +
                '}';
    }
}
