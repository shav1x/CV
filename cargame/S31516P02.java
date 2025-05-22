package p02;

import p02.game.*;
import p02.pres.*;

public class S31516P02 {

    public static void main(String[] args) throws InterruptedException {

        startTheGame();

    }

    public static void startTheGame() throws InterruptedException {
        new Game();
        SevenSegmentDigit.reset = false;
        Game.ones.number = 0;
        Game.tens.number = 0;
        Game.hundreds.number = 0;
        new Board();
        new MyThread().start();
        MyThread.sleep(1);
        Board.started = true;
        MyThread.running = false;
        Game.ones.resetIt();
        Board.rows[0] = 0;
        Game.table.refresh();
        Game.autoslalom.drawObs();
        Board.started = false;
        Game.autoslalom.frame.requestFocus();
    }

}
