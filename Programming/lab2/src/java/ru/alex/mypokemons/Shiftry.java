package java.ru.alex.mypokemons;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;
import MyMoves.Status.*;
import MyMoves.Special.Extrasensory;

public class Shiftry extends Pokemon {
    public Shiftry(String name, int level) {
        super(name, level);
        super.setType(Type.GRASS, Type.DARK);
        super.setStats(90, 100, 60, 90, 60, 80);

        Double_Team doubleTeam = new Double_Team();
        super.setMove(doubleTeam);

        Confide confide = new Confide();
        super.setMove(confide);

        Extrasensory extrasensory = new Extrasensory();
        super.setMove(extrasensory);
    }
}
