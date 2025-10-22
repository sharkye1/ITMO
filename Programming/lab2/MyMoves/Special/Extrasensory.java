package MyMoves.Special;

import ru.ifmo.se.pokemon.SpecialMove;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Stat;

public class Extrasensory extends SpecialMove {
    public Extrasensory() {
        super(ru.ifmo.se.pokemon.Type.PSYCHIC, 80, 100); // мощность 80, точность 100%
    }

    @Override
    protected void applyOppEffects(Pokemon p) {
        if (Math.random() < 0.1) {
            p.setMod(Stat.ACCURACY, -1); // понижение точности на 1 уровень с вероятностью 10%
        }
    }

    @Override
    protected String describe() {
        return "использует Extrasensory";
    }
}
