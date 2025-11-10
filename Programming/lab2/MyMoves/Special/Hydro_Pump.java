package MyMoves.Special;

import ru.ifmo.se.pokemon.*;

public class Hydro_Pump extends SpecialMove {
    public Hydro_Pump() {
        super(Type.WATER, 110, 80); // сила: 110, точность: 80
    }
    
    @Override
    protected void applyOppEffects(Pokemon p) {
        // если цель имеет тип GRASS — удваиваем её текущие хп, но не выше максимума
        if (p.hasType(Type.GRASS)) {
            double currentHp = p.getHP();
            double maxHp = p.getStat(Stat.HP);
            double newHp = Math.min(maxHp, currentHp * 2.0);
            double healAmount = newHp - currentHp;
            if (healAmount > 0) {
                // applyOppDamage принимает положительное число урона, поэтому передаём отрицательное
                applyOppDamage(p, -healAmount);
                // добавляем к строке вывода сообщение о восстановлении хп
                out = "использует Hydro Pump и восстанавливает " + (int)healAmount + " HP у " + p.getName();
            }
        }
    }

    @Override
    protected String describe() {
        return out;
    }

}