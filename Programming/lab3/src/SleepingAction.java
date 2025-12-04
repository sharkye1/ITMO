package Programming.lab3.src;

public class SleepingAction implements Action {
    private final int durationHours;
    private final boolean autoWake;

    public SleepingAction(int durationHours) {
        this(durationHours, true);
    }

    public SleepingAction(int durationHours, boolean autoWake) {
        if (durationHours <= 0)
            throw new IllegalArgumentException("Продолжительность сна должна быть положительной");
        this.durationHours = durationHours;
        this.autoWake = autoWake;
    }

    @Override
    public void execute(Character actor) throws CharacterNotInCabinException {
        if (actor == null)
            throw new IllegalArgumentException("actor is required");
        if (actor.getLocation().equals(World.get())) {
            throw new CharacterNotInCabinException(actor.getName());
        }
        actor.setMood(Mood.SLEEPY);
        System.out.println(actor.getName() + " засыпает крепким сном на " + durationHours + " ч.");
        // по завершении сна – просыпается бодрым только если autoWake
        if (autoWake) {
            actor.setMood(Mood.AWAKE);
            System.out.println(actor.getName() + " проснулся бодрым.");
        } else {
            System.out.println(actor.getName() + " спит и не просыпается.");
        }
    }
}
