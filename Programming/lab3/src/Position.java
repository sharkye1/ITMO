package Programming.lab3.src;

public record Position(int x, int y) {
    public Position moveBy(int dx, int dy) {
        return new Position(x + dx, y + dy);
    }
}
