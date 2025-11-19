package Programming.lab3.src;


// Проверяемое (checked) исключение: персонаж слишком устал
public class TooTiredException extends Exception {
    public TooTiredException(String message) {
        super(message);
    }

    @Override
    public String getMessage() {
        return "⚠️ УСТАЛОСТЬ: " + super.getMessage();
    }
}
