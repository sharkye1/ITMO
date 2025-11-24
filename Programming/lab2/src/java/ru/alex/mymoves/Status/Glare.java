package java.ru.alex.mymoves.Status;

import ru.ifmo.se.pokemon.*;

public class Glare extends StatusMove {
    public Glare() {
        super(Type.NORMAL, 0, 100); // сила 0, точность 100%
    }

    @Override
    protected void applyOppEffects(Pokemon target) {
        if (!target.hasType(Type.ELECTRIC)) { // не действует на Electric-type
            Effect.paralyze(target); // стандартный эффект паралича
        }
    }

    @Override
    protected String describe() {
        return "использует Glare"; // сообщение при использовании
    }
}