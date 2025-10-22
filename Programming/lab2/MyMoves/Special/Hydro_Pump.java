package MyMoves.Special;

import ru.ifmo.se.pokemon.SpecialMove;

public class Hydro_Pump extends SpecialMove {
    public Hydro_Pump() {
        super(ru.ifmo.se.pokemon.Type.WATER, 110, 80); // сила: 110, точность: 80
    }

    @Override
    protected String describe() {
        return "использует Hydro Pump";
    }

}