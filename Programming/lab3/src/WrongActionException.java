package Programming.lab3.src;

public class WrongActionException extends Exception {
    private final String reason;

    public WrongActionException(String reason) {
        this.reason = reason;
    }

    @Override
    public String getMessage() {
        return "Действие невозможно: " + reason;
    }
}
