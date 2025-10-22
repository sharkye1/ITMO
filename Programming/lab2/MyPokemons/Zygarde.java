package MyPokemons;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;
import MyMoves.Special.Draco_Meteor;
import MyMoves.Special.Focus_Blast;
import MyMoves.Status.Glare;

public class Zygarde extends Pokemon {
    public Zygarde(String name, int level) {
        super(name, level);

        super.setType(Type.DRAGON, Type.GROUND);
        super.setStats(108, 100, 121, 81, 95, 95);

        Glare glare = new Glare();
        super.setMove(glare);

        Focus_Blast focus_blast = new Focus_Blast();
        super.setMove(focus_blast);

        Draco_Meteor draco_meteor = new Draco_Meteor();
        super.setMove(draco_meteor);
    }
}