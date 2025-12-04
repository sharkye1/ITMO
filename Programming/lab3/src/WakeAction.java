package Programming.lab3.src;

public class WakeAction implements Action {
    @Override
    public void execute(Character actor) throws CharacterNotInCabinException {
        if (actor.getLocation().equals(World.get())) {
            throw new CharacterNotInCabinException(actor.getName());
        }
        actor.setMood(Mood.AWAKE);
        System.out.println(actor.getName() + " проснулся после сна.");
    }
}
