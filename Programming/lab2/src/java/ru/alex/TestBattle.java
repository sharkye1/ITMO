package java.ru.alex;

import java.ru.alex.mypokemons.*;
import ru.ifmo.se.pokemon.*;

public class TestBattle {
    public static void main(String[] args) {
        Battle b = new Battle();
        

        Zygarde p1 = new Zygarde("зигард", 1);
        Omanyte p2 = new Omanyte("оманайт", 1);
        Omastar p3 = new Omastar("омастар", 1);
        Seedot p4 = new Seedot("сидот", 1);
        Nuzleaf p5 = new Nuzleaf("нузлиф", 1);
        Shiftry p6 = new Shiftry("шифтри", 1);

        b.addAlly(p1);
        b.addAlly(p2);
        b.addAlly(p3);

        b.addFoe(p4);
        b.addFoe(p5);
        b.addFoe(p6);
        // когда водяная атака попадет на травяного покемона, у него хп вырастает в два раза
        
        b.go();
    }
}