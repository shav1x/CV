package p02.game;

import static p02.pres.SevenSegmentDigit.reset;

public class MyThread extends Thread {

    private final TickEvent tickEvent = new TickEvent();
    private final StartEvent startEvent = new StartEvent();

    public static boolean running;

    public static long tickRate;


    public MyThread() {

        running = true;

        tickRate = 860;


        tickEvent.addTickEventListener(new TickEvent.TickEventListener() {

            @Override
            public void tickEventOccurred() {

                Game.frame.getContentPane().removeAll();
                Game.table.table.getModel().setValueAt(Game.ones.number, 0, 2);
                Game.table.table.getModel().setValueAt(Game.tens.number, 0, 1);
                Game.table.table.getModel().setValueAt(Game.hundreds.number, 0, 0);

                Game.space = 0;

                if (Game.hundreds.number == 0) {
                    Game.space++;
                    if (Game.tens.number == 0) {
                        Game.space++;
                        if (Game.ones.number == 0) {
                            Game.space++;
                        }
                    }
                }

                Board.move(Game.space);

                int combinedValue = (Board.carPos << 16) | Board.lastObs;

                switch (combinedValue) {
                    case (3 << 16) | 1:
                    case (3 << 16) | 11:
                    case (3 << 16) | 101:
                    case (2 << 16) | 110:
                    case (2 << 16) | 11:
                    case (2 << 16) | 10:
                    case (1 << 16) | 100:
                    case (1 << 16) | 110:
                    case (1 << 16) | 101:
                        Game.ones.resetIt();
                        break;
                    default:
                        Board.lastObs = 0;
                        break;
                }

                Game.table.refresh();

                Game.autoslalom.drawObs();

//                Game.frame.add(Game.table.table);
//                Game.frame.pack();
//                Game.frame = Game.autoslalom.frame;
//                Game.frame.setVisible(true);

                if (tickRate > 400)
                    tickRate -= 4;

            }

        });

    }

    @Override
    public void run() {
        Game.autoslalom.frame.requestFocus();
        startEvent.fireStartEvent();
        while (running && !reset) {
            tickEvent.fireTickEvent();
            try {
                Thread.sleep(tickRate);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

}