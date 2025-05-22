package p02.game;

import p02.pres.Frame;
import p02.pres.SevenSegmentDigit;
import p02.pres.Table;

import javax.swing.*;

public class Game {

    public static SevenSegmentDigit ones;
    public static SevenSegmentDigit tens;
    public static SevenSegmentDigit hundreds;
    public static boolean running = true;
    public static Table table;
    public static int space;
    public static Frame autoslalom;

    public static JFrame frame;

    public static JFrame frameFirst;

    public Game() {

        frameFirst = new JFrame();
        frameFirst.setSize(1090, 694);
        frameFirst.setLocationRelativeTo(null);
        frameFirst.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        hundreds = new SevenSegmentDigit();
        tens = new SevenSegmentDigit();
        ones = new SevenSegmentDigit();

        frame = new JFrame("Table test");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        table = new Table();

        autoslalom = new Frame();

        Board.max = space;

        space = 3;

        Game.autoslalom.frame.addKeyListener(table.board);
        Game.autoslalom.frame.requestFocus();

    }

}
