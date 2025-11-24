package java.ru.alex.mymoves.Status;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.StatusMove;
import ru.ifmo.se.pokemon.Stat;

public class Double_Team extends StatusMove {
    public Double_Team() {
        super(ru.ifmo.se.pokemon.Type.NORMAL, 0, 0); // сила: 0, точность: 0
    }

    @Override
    protected void applyOppEffects(Pokemon user) {
        user.setMod(Stat.EVASION, 1); // увеличивает уклонение на 1 уровень
    }

    @Override
    protected String describe() {
        return "использует Double Team";
    }

}
