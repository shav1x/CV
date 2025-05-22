package p02.pres;

import p02.game.*;

import javax.swing.*;
import javax.swing.table.TableCellRenderer;
import java.awt.*;
import java.awt.geom.RoundRectangle2D;

public class SevenSegmentDigit extends JPanel implements TableCellRenderer {

    public int number;

    public double scale;

    private StartEvent startEvent = new StartEvent();
    private ResetEvent resetEvent = new ResetEvent();
    private PlusOneEvent plusOneEvent = new PlusOneEvent();

    private final int segment[][] = {
            {1, 1, 1, 1, 1, 1, 0},  // For 0
            {0, 1, 1, 0, 0, 0, 0},  // For 1
            {1, 1, 0, 1, 1, 0, 1},  // For 2
            {1, 1, 1, 1, 0, 0, 1},  // For 3
            {0, 1, 1, 0, 0, 1, 1},  // For 4
            {1, 0, 1, 1, 0, 1, 1},  // For 5
            {1, 0, 1, 1, 1, 1, 1},  // For 6
            {1, 1, 1, 0, 0, 0, 0},  // For 7
            {1, 1, 1, 1, 1, 1, 1},  // For 8
            {1, 1, 1, 1, 0, 1, 1}   // For 9
    };

    public static boolean reset;

    public SevenSegmentDigit() {

        scale = 0.3;

        reset = false;

        startEvent.addStartEventListener(new StartEvent.StartEventListener() {

            @Override
            public void startEventOccurred() {
                Game.hundreds.number = 0;
                Game.tens.number = 0;
                Game.ones.number = 0;
            }

        });

        resetEvent.addResetEventListener(new ResetEvent.ResetEventListener() {

            @Override
            public void resetEventOccured() {
                reset = true;
                Board.started = false;
            }

        });

        plusOneEvent.addPlusOneEventListener(new PlusOneEvent.PlusOneEventListener() {

            @Override
            public void plusOneEventOccurred() {
                Game.ones.number = (Game.ones.number + 1) % 10;
                if (Game.ones.number == 0) {
                    Game.tens.number = (Game.tens.number + 1) % 10;
                    if (Game.tens.number == 0) {
                        Game.hundreds.number = (Game.hundreds.number + 1) % 10;
                        if (Game.hundreds.number == 0) {
                            MyThread.running = false;
                        }
                    }
                }
            }

        });

    }

    public void resetIt() {
        resetEvent.fireResetEvent();
    }

    public void plusIt(){
        plusOneEvent.firePlusOneEvent();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        Graphics2D g2d = (Graphics2D) g;
        g2d.setStroke(new BasicStroke(5));

        g2d.setColor(Color.RED);

        if (reset) {
            g2d.setColor(getBackground());
            g2d.fillRect(0, 0, getWidth(), getHeight());
            return;
        }

        // Calibrate
        double adjust = 30 * scale;

        // Draw the individual segments
        double thickness = 20*scale;
        double length = 100*scale;
        double gap = 20*scale;

        if (segment[number][0] == 1) g2d.draw(new RoundRectangle2D.Double(adjust , adjust , length , thickness , thickness, thickness));
        if (segment[number][1] == 1) g2d.draw(new RoundRectangle2D.Double(adjust + length , adjust + gap , thickness , length , thickness, thickness));
        if (segment[number][2] == 1) g2d.draw(new RoundRectangle2D.Double(adjust + length , adjust + length + 2*gap , thickness , length , thickness, thickness));
        if (segment[number][3] == 1) g2d.draw(new RoundRectangle2D.Double(adjust , adjust + 2*(length +gap) , length , thickness , thickness, thickness));
        if (segment[number][4] == 1) g2d.draw(new RoundRectangle2D.Double(adjust-gap , adjust + length + 2*gap , thickness , length , thickness, thickness));
        if (segment[number][5] == 1) g2d.draw(new RoundRectangle2D.Double(adjust-gap , adjust + gap , thickness , length , thickness, thickness));
        if (segment[number][6] == 1) g2d.draw(new RoundRectangle2D.Double(adjust , adjust + length +gap , length , thickness , thickness, thickness));
    }

    @Override
    public Component getTableCellRendererComponent(JTable table, Object value,
                                                   boolean isSelected, boolean hasFocus, int row, int column) {
        if (value instanceof Integer) {
            number = (Integer) value;
        } else {
            number = 0;
        }

        return this;
    }

    @Override
    public Dimension getPreferredSize() {
        return new Dimension((int) (150 * scale), (int) (300 * scale));
    }

}
