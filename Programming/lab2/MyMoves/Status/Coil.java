package MyMoves.Status;

import ru.ifmo.se.pokemon.*;

public class Coil extends StatusMove {
    public Coil() {
        super(Type.NORMAL, 0, 100);
    }

    @Override
    protected void applySelfEffects(Pokemon user) {
        user.setMod(Stat.ATTACK, 1);
        user.setMod(Stat.DEFENSE, 1);
    }

    @Override
    protected String describe() {
        return "использует Coil";
    }
}
