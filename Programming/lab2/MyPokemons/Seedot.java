package MyPokemons;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;
import MyMoves.Status.Confide;
import MyMoves.Status.Double_Team;

public class Seedot extends Pokemon {
    public Seedot(String name, int level) {
        super(name, level);
        super.setType(Type.GRASS);
        super.setStats(40, 40, 50, 30, 30, 30);

        Double_Team doubleTeam = new Double_Team();
        super.setMove(doubleTeam);

        Confide confide = new Confide();
        super.setMove(confide);
    }
}
