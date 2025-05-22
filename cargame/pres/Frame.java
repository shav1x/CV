package p02.pres;

import p02.game.Board;
import p02.game.Game;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class Frame {

    public JFrame frame;
    public JTable table;
    public ImagePanel background;

    public BufferedImage obstacle1_1;
    public BufferedImage obstacle1_2;
    public BufferedImage obstacle1_3;
    public BufferedImage obstacle1_4;
    public BufferedImage obstacle1_5;
    public BufferedImage obstacle1_6;
    public BufferedImage obstacle1_7;

    public BufferedImage car;
    public ImageIcon carImage;

    public SevenSegmentDigit ones;
    public SevenSegmentDigit tens;
    public SevenSegmentDigit hundreds;

    public ImageIcon[] obstacles;

    public int[][][] coordinates;

    public ImageIcon[] prevs;

    {
        try {
            obstacle1_1 = ImageIO.read(new File("assets/obstacleMain.png"));
            car = ImageIO.read(new File("assets/car.jpg"));

            Image tmp = obstacle1_1.getScaledInstance(27, 27, Image.SCALE_SMOOTH);
            obstacle1_2 = new BufferedImage(27, 27, BufferedImage.TYPE_INT_ARGB);
            Graphics2D g2d = obstacle1_2.createGraphics();
            g2d.drawImage(tmp, 0, 0, null);
            g2d.dispose();

            tmp = obstacle1_1.getScaledInstance(54, 54, Image.SCALE_SMOOTH);
            obstacle1_3 = new BufferedImage(54, 54, BufferedImage.TYPE_INT_ARGB);
            g2d = obstacle1_3.createGraphics();
            g2d.drawImage(tmp, 0, 0, null);
            g2d.dispose();

            tmp = obstacle1_1.getScaledInstance(62, 62, Image.SCALE_SMOOTH);
            obstacle1_4 = new BufferedImage(62, 62, BufferedImage.TYPE_INT_ARGB);
            g2d = obstacle1_4.createGraphics();
            g2d.drawImage(tmp, 0, 0, null);
            g2d.dispose();

            tmp = obstacle1_1.getScaledInstance(70, 70, Image.SCALE_SMOOTH);
            obstacle1_5 = new BufferedImage(70, 70, BufferedImage.TYPE_INT_ARGB);
            g2d = obstacle1_5.createGraphics();
            g2d.drawImage(tmp, 0, 0, null);
            g2d.dispose();

            tmp = obstacle1_1.getScaledInstance(85, 85, Image.SCALE_SMOOTH);
            obstacle1_6 = new BufferedImage(85, 85, BufferedImage.TYPE_INT_ARGB);
            g2d = obstacle1_6.createGraphics();
            g2d.drawImage(tmp, 0, 0, null);
            g2d.dispose();

            tmp = obstacle1_1.getScaledInstance(103, 103, Image.SCALE_SMOOTH);
            obstacle1_7 = new BufferedImage(103, 103, BufferedImage.TYPE_INT_ARGB);
            g2d = obstacle1_7.createGraphics();
            g2d.drawImage(tmp, 0, 0, null);
            g2d.dispose();

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public Frame() {

        table = Game.table.table;
        background = new ImagePanel("assets/autoslalom board.jpg");
        background.setPreferredSize(new Dimension(1090, 654));
        background.setLayout(null);

        prevs = new ImageIcon[]{null, null, null};

        hundreds = new SevenSegmentDigit();
        ones = new SevenSegmentDigit();
        tens = new SevenSegmentDigit();

        Game.hundreds.setBounds(10, 10, 90, 60);
        Game.tens.setBounds(120, 10, 90, 60);
        Game.ones.setBounds(230, 10, 90, 60);

        carImage = new ImageIcon(car);

        obstacles = new ImageIcon[]{
                new ImageIcon(obstacle1_1),
                new ImageIcon(obstacle1_2),
                new ImageIcon(obstacle1_3),
                new ImageIcon(obstacle1_4),
                new ImageIcon(obstacle1_5),
                new ImageIcon(obstacle1_6),
                new ImageIcon(obstacle1_7)
        };

        coordinates = new int[][][]{
                {{917, 17}, {968, 18}, {1019, 18}},
                {{857, 53}, {928, 53}, {999, 53}},
                {{765, 109}, {859, 109}, {953, 109}},
                {{632, 191}, {776, 191}, {920, 191}},
                {{451, 302}, {666, 302}, {881, 302}},
                {{288, 405}, {562, 405}, {836, 405}},
                {{52, 547}, {413, 547}, {774, 547}}

        };

        createFrame();

    }

    public void createFrame() {

        frame = new JFrame("Autoslalom");
        frame.setSize(new Dimension(1090, 694));
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);

        Game.hundreds.setBounds(80, 30, 50, 100);
        Game.tens.setBounds(140, 30, 50, 100);
        Game.ones.setBounds(200, 30, 50, 100);

        frame.add(background);

    }

    public void drawObs() {

        SwingUtilities.invokeLater(() -> {

            table = Game.table.table;

            background.removeAll();
            background.revalidate();
            background.repaint();

            JLabel l;

            for (int i = 0; i < 6; i++) {
                for (int j = 4; j < 7; j++) {

                    Object valueAt = table.getModel().getValueAt(i, j);

                    if (valueAt == null) {
                        continue;
                    }

                    String val = valueAt.toString();

                    if (val.equals("1")) {
                        l = new JLabel(obstacles[i]);
                        l.setBounds(coordinates[i][j - 4][0], coordinates[i][j - 4][1], l.getIcon().getIconWidth(), l.getIcon().getIconHeight());
                        background.add(l);
                        prevs[j - 4] = obstacles[i];
                    }
                }
            }

            if (Board.rows[6] == 1) {
                l = new JLabel(carImage);
                l.setBounds(673, 547, l.getIcon().getIconWidth(), l.getIcon().getIconHeight());
                background.add(l);
            }
            if (Board.rows[6] == 10) {
                l = new JLabel(carImage);
                l.setBounds(360, 547, l.getIcon().getIconWidth(), l.getIcon().getIconHeight());
                background.add(l);
            }
            if (Board.rows[6] == 100) {
                l = new JLabel(carImage);
                l.setBounds(62, 547, l.getIcon().getIconWidth(), l.getIcon().getIconHeight());
                background.add(l);
            }

            background.add(Game.hundreds);
            background.add(Game.tens);
            background.add(Game.ones);

            background.revalidate();
            background.repaint();

            frame.add(background);
            frame.setVisible(true);
        });
    }

}
