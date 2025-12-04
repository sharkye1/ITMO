package Programming.lab3.src;

public class World {
    private static final Location INSTANCE = new Location("Мир");

    public static Location get() {
        return INSTANCE;
    }

    private World() {
    }
}
