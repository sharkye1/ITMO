package Programming.lab3.src;

public interface Action {
    void execute(Character actor) throws CharacterNotInCabinException, WrongActionException;
}
