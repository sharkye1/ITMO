package java.ru.alex.mymoves.Physical;

import ru.ifmo.se.pokemon.PhysicalMove;

public class Spike_Cannon extends PhysicalMove {
    public Spike_Cannon() {
        super(ru.ifmo.se.pokemon.Type.ROCK, 20, 100); // сила: 20, точность: 100
    }

    @Override
    protected String describe() {
        return "использует Spike Cannon";
    }
}