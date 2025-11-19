package Programming.lab3.src;


// Непроверяемое (unchecked) исключение: недопустимое действие
public class InvalidActionException extends RuntimeException {
    public InvalidActionException(String message) {
        super(message);
    }

    @Override
    public String getMessage() {
        return "❌ ОШИБКА ДЕЙСТВИЯ: " + super.getMessage();
    }
}
