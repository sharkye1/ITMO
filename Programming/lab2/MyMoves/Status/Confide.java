package MyMoves.Status;

import ru.ifmo.se.pokemon.StatusMove;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Stat;

public class Confide extends StatusMove {
    public Confide() {
        super(ru.ifmo.se.pokemon.Type.NORMAL, 0, 0); // атака не наносит урон и не промахивается
    }

    @Override
    protected void applyOppEffects(Pokemon target) {
        target.setMod(Stat.SPECIAL_ATTACK, -1); // понижение специальной атаки на 1 уровень
    }

    @Override
    protected String describe() {
        return "использует Confide";
    }

}
