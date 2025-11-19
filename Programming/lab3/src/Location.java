package Programming.lab3.src;


// Местоположение (record)
public record Location(String place) {
    @Override
    public String toString() {
        return place;
    }
}
