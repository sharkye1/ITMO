package MyMoves.Special;

import ru.ifmo.se.pokemon.*;

public class Focus_Blast extends SpecialMove {
    public Focus_Blast() {
        super(Type.FIGHTING, 120, 70); // сила: 120, точность: 70
    }

    @Override
    protected void applyOppEffects(Pokemon target) {
        if (Math.random() < 0.1) { // 10% шанс
            target.setMod(Stat.SPECIAL_DEFENSE, -1); // понижает Special Defense на 1 stage
        }
    }

    @Override
    protected String describe() {
        return "использует Focus Blast";
    }
}