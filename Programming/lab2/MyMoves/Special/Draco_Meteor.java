package MyMoves.Special;

import ru.ifmo.se.pokemon.*;

public class Draco_Meteor extends SpecialMove {
    public Draco_Meteor() {
        super(Type.DRAGON, 130, 90); // сила: 130, точность: 90
    }

    @Override
    protected void applySelfEffects(Pokemon user) {
        user.setMod(Stat.SPECIAL_ATTACK, -2); // понижает Special Attack на 2 stage
    }

    @Override
    protected String describe() {
        return "использует Draco Meteor";
    }

}
