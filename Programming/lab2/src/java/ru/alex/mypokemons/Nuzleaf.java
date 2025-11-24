package java.ru.alex.mypokemons;

import mymoves.status.confide;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;
import MyMoves.Status.*;
import MyMoves.Special.Extrasensory;

public class Nuzleaf extends Pokemon {
    public Nuzleaf(String name, int level) {
        super(name, level);
        super.setType(Type.GRASS, Type.DARK);
        super.setStats(70, 70, 40, 60, 40, 60);

        Double_Team doubleTeam = new Double_Team();
        super.setMove(doubleTeam);

        Confide confide = new Confide();
        super.setMove(confide);

        Extrasensory extrasensory = new Extrasensory();
        super.setMove(extrasensory);
    }
}
