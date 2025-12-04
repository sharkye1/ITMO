package Programming.lab3.src;

public class PaintingAction implements Action {
    private final String theme;

    public PaintingAction(String theme) {
        if (theme == null)
            throw new IllegalArgumentException("theme is required");
        this.theme = theme;
    }

    @Override
    public void execute(Character actor) throws WrongActionException {
        if (actor == null)
            throw new IllegalArgumentException("actor is required");
        if (actor.getMood() == Mood.SLEEPY) {
            throw new WrongActionException("Нельзя рисовать, пока спишь");
        }
        actor.setMood(Mood.CREATIVE);
        System.out.println(actor.getName() + " рисует тему: '" + theme + "'. Настроение: " + actor.getMood());
    }
}
