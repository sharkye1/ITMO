package MyMoves.Physical;

import ru.ifmo.se.pokemon.PhysicalMove;

public class Rock_Slide extends PhysicalMove {
    public Rock_Slide() {
        super(ru.ifmo.se.pokemon.Type.ROCK, 75, 90); // сила: 75, точность: 90
    }

    @Override
    protected String describe() {
        return "использует Rock Slide";
    }
}
