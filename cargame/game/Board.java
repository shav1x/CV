package p02.game;

import p02.pres.SevenSegmentDigit;

import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.*;

public class Board implements KeyListener {

    public static int[] rows = new int[7];
    public static int carPos;
    private static int moved;
    public static int max;
    private static boolean flag = false;
    private static StringBuilder prev;
    public static int lastObs;

    public static boolean started;

    public Board() {
        Arrays.fill(rows, 0);
        rows[6] = 10;
        carPos = 2;
        started = false;
        prev = new StringBuilder();
        prev.append("   ");
    }

    @Override
    public void keyReleased(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_S) {
            switch (e.getKeyCode()) {
                case KeyEvent.VK_S -> {
                    if (!started) {
                        SevenSegmentDigit.reset = false;
                        Game.ones.number = 0;
                        Game.tens.number = 0;
                        Game.hundreds.number = 0;
                        new Board();
                        started = true;
                        new MyThread().start();
                    }
                }
            }
            Game.table.refresh();
            Game.autoslalom.drawObs();
        }
    }

    @Override
    public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_A || e.getKeyCode() == KeyEvent.VK_D) {
            switch (e.getKeyCode()) {
                case KeyEvent.VK_A -> {
                    switch (carPos) {
                        case 2 -> {
                            carPos = 1;
                            rows[6] = 100;
                            Game.table.refresh();
                        }
                        case 3 -> {
                            carPos = 2;
                            rows[6] = 10;
                            Game.table.refresh();
                        }
                    }
                }
                case KeyEvent.VK_D -> {
                    switch (carPos) {
                        case 1 -> {
                            carPos = 2;
                            rows[6] = 10;
                            Game.table.refresh();
                        }
                        case 2 -> {
                            carPos = 3;
                            rows[6] = 1;
                            Game.table.refresh();
                        }
                    }
                }
            }
        }
    }

    public static String createObstacle() {
        boolean fl = true;
        StringBuilder nums = new StringBuilder();
        while (fl) {
            for (int i = 0; i < 3; i++) {
                switch ((int) (Math.random() * 2)) {
                    case 0 -> {
                        nums.append("0");
                    }
                    case 1 -> {
                        if (prev.toString().charAt(i) != '1') {
                            nums.append("1");
                        }
                        else {
                            nums.append("0");
                        }
                    }
                }
            }
            if (!nums.toString().equals("000") && !nums.toString().equals("111") && nums.toString().contains("0"))
                fl = false;
            else nums.setLength(0);
        }
        prev = nums;
        return nums.toString();
    }

    public static void move(int s) {
        lastObs = rows[5];
        if (lastObs != 0)
            Game.ones.plusIt();
        for (int j = 5; j > 0; j--) {
            rows[j] = rows[j - 1];
        }
        moved++;
        rows[0] = 0;
        if (moved == max + 1 || !flag) {
            rows[0] = Integer.parseInt(createObstacle());
            moved = 0;
            max = s;
            flag = true;
        }
    }

    @Override
    public void keyTyped(KeyEvent e) {
    }

}
