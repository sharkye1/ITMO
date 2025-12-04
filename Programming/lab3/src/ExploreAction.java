package Programming.lab3.src;

public class ExploreAction implements Action {
    private final String description;

    public ExploreAction(String description) {
        if (description == null)
            throw new IllegalArgumentException("description is required");
        this.description = description;
    }

    @Override
    public void execute(Character actor) throws WrongActionException {
        if (actor == null)
            throw new IllegalArgumentException("actor is required");
        if (actor.getMood() == Mood.SLEEPY) {
            throw new WrongActionException("Сонный персонаж не может отправиться исследовать");
        }
        actor.setMood(Mood.AWAKE);
        System.out.println(actor.getName() + " исследует местность: " + description);
    }
}
