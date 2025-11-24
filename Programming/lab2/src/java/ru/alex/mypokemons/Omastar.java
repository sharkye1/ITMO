package java.ru.alex.mypokemons;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;
import MyMoves.Physical.Spike_Cannon;
import MyMoves.Physical.Water_Fall;
import MyMoves.Physical.Rock_Slide;
import MyMoves.Special.Hydro_Pump;

public class Omastar extends Pokemon {
    public Omastar(String name, int level) {
        super(name, level);

        super.setType(Type.ROCK, Type.WATER);
        super.setStats(70, 60, 125, 115, 70, 55);

        Rock_Slide rock_slide = new Rock_Slide();
        super.setMove(rock_slide);

        Hydro_Pump hydro_pump = new Hydro_Pump();
        super.setMove(hydro_pump);

        Water_Fall water_fall = new Water_Fall();
        super.setMove(water_fall);

        Spike_Cannon spike_cannon = new Spike_Cannon();
        super.setMove(spike_cannon);
    }
}