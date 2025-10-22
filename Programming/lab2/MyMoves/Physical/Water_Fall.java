package MyMoves.Physical;

import ru.ifmo.se.pokemon.PhysicalMove;

public class Water_Fall extends PhysicalMove {
    public Water_Fall() {
        super(ru.ifmo.se.pokemon.Type.WATER, 80, 100); // сила: 80, точность: 100
    }

    @Override
    protected String describe() {
        return "использует Water Fall";
    }
}
