package java.ru.alex.mypokemons;

import MyMoves.Physical.Rock_Slide;
import MyMoves.Special.Hydro_Pump;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;

public class Omanyte extends Pokemon {
    public Omanyte(String name, int level) {
        super(name, level);

        super.setType(Type.ROCK, Type.WATER);
        super.setStats(35, 40, 100, 90, 55, 70);

        Rock_Slide rock_slide = new Rock_Slide();
        super.setMove(rock_slide);

        Hydro_Pump hydro_pump = new Hydro_Pump();
        super.setMove(hydro_pump);
    }

}
