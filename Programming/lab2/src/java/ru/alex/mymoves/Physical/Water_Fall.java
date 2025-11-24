package java.ru.alex.mymoves.Physical;

import ru.ifmo.se.pokemon.*;

public class Water_Fall extends PhysicalMove {
    public Water_Fall() {
        super(Type.WATER, 80, 100); // сила: 80, точность: 100
    }

    @Override
    protected void applyOppEffects(Pokemon p) {
        if (p.hasType(Type.GRASS)) {
            double currentHp = p.getHP();
            double maxHp = p.getStat(Stat.HP);
            double newHp = Math.min(maxHp, currentHp * 2.0);
            double healAmount = newHp - currentHp;
            if (healAmount > 0) {
                applyOppDamage(p, -healAmount);
            }
        }
    }

    @Override
    protected String describe() {
        return "использует Water Fall";
    }
}
