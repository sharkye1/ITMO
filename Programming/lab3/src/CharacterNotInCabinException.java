package Programming.lab3.src;

public class CharacterNotInCabinException extends Exception {
    private final String characterName;

    public CharacterNotInCabinException(String characterName) {
        this.characterName = characterName;
    }

    @Override
    public String getMessage() {
        return "Персонаж '" + characterName
                + "' находится в открытом мире и не может выполнить это действие (требуется быть в конкретной локации).";
    }
}
