package p02.pres;

import javax.swing.*;
import javax.swing.table.DefaultTableCellRenderer;
import java.awt.*;

public class TableRenderer extends DefaultTableCellRenderer {

    @Override
    public Component getTableCellRendererComponent(JTable table, Object value,
                                                   boolean isSelected, boolean hasFocus,
                                                   int row, int column) {
        Component c = super.getTableCellRendererComponent(table, value, isSelected, hasFocus, row, column);

        if ((column <= 2 && row >= 1) || (column >= 8)) {
            c.setBackground(Color.GREEN);
        } else {
            c.setBackground(Color.GRAY);
        }
        if (column == 3 || column == 7) {
            c.setBackground(Color.BLACK);
        }

        return c;
    }

}
