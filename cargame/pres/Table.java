package p02.pres;

import p02.game.Board;
import p02.game.Game;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableCellRenderer;
import javax.swing.table.TableColumn;
import java.awt.*;

public class Table {

    public JTable table;
    public Board board;

    public Table() {
        board = new Board();
        createTable();
    }

    public void createTable() {

        JFrame frame = new JFrame("JTable Example");

        DefaultTableModel model = new DefaultTableModel(7, 11);

        JTable table = new JTable(model) {

            @Override
            public Component prepareRenderer(TableCellRenderer renderer, int row, int column) {

                Component c = super.prepareRenderer(renderer, row, column);

                if ((column <= 2 && row >= 1) || (column >= 8)) {
                    c.setBackground(Color.GREEN);
                } else c.setBackground(Color.GRAY);

                if (column == 3 || column == 7) {
                    c.setBackground(Color.BLACK);
                }

                return c;
            }
        };

        table.setDefaultRenderer(Integer.class, new TableRenderer());

        for (int i = 0; i < 7; i++) {
            String tmp = String.valueOf(Board.rows[i]);
            switch (tmp) {
                case "0" -> {
                    model.setValueAt(0, i, 4);
                    model.setValueAt(0, i, 5);
                    model.setValueAt(0, i, 6);
                }
                case "11" -> {
                    model.setValueAt(0, i, 4);
                    model.setValueAt(1, i, 5);
                    model.setValueAt(1, i, 6);
                }
                case "101" -> {
                    model.setValueAt(1, i, 4);
                    model.setValueAt(0, i, 5);
                    model.setValueAt(1, i, 6);
                }
                case "1" -> {
                    model.setValueAt(0, i, 4);
                    model.setValueAt(0, i, 5);
                    model.setValueAt(1, i, 6);
                }
                case "110" -> {
                    model.setValueAt(1, i, 4);
                    model.setValueAt(1, i, 5);
                    model.setValueAt(0, i, 6);
                }
                case "10" -> {
                    model.setValueAt(0, i, 4);
                    model.setValueAt(1, i, 5);
                    model.setValueAt(0, i, 6);
                }
                case "100" -> {
                    model.setValueAt(1, i, 4);
                    model.setValueAt(0, i, 5);
                    model.setValueAt(0, i, 6);
                }
                case "20" -> {
                    model.setValueAt(0, i, 4);
                    model.setValueAt(2, i, 5);
                    model.setValueAt(0, i, 6);
                }
                case "200" -> {
                    model.setValueAt(2, i, 4);
                    model.setValueAt(0, i, 5);
                    model.setValueAt(0, i, 6);
                }
                case "2" -> {
                    model.setValueAt(0, i, 4);
                    model.setValueAt(0, i, 5);
                    model.setValueAt(2, i, 6);
                }
            }
        }

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        table.setShowGrid(true);
        table.setGridColor(Color.LIGHT_GRAY);
        table.setRowHeight(120);

        // Set column width
        for (int columnIndex = 0; columnIndex < table.getColumnCount(); columnIndex++) {
            TableColumn column = table.getColumnModel().getColumn(columnIndex);
            column.setPreferredWidth(1000);
        }

        for (int i = 1; i < 7; i++) {
            table.getColumnModel().getColumn(i);
        }

        this.table = table;

    }

    public void refresh() {
        for (int i = 0; i < 7; i++) {
            String tmp = String.valueOf(Board.rows[i]);
            switch (tmp) {
                case "0" -> {
                    table.setValueAt(0, i, 4);
                    table.setValueAt(0, i, 5);
                    table.setValueAt(0, i, 6);
                }
                case "11" -> {
                    table.setValueAt(0, i, 4);
                    table.setValueAt(1, i, 5);
                    table.setValueAt(1, i, 6);
                }
                case "101" -> {
                    table.setValueAt(1, i, 4);
                    table.setValueAt(0, i, 5);
                    table.setValueAt(1, i, 6);
                }
                case "1" -> {
                    table.setValueAt(0, i, 4);
                    table.setValueAt(0, i, 5);
                    table.setValueAt(1, i, 6);
                }
                case "110" -> {
                    table.setValueAt(1, i, 4);
                    table.setValueAt(1, i, 5);
                    table.setValueAt(0, i, 6);
                }
                case "10" -> {
                    table.setValueAt(0, i, 4);
                    table.setValueAt(1, i, 5);
                    table.setValueAt(0, i, 6);
                }
                case "100" -> {
                    table.setValueAt(1, i, 4);
                    table.setValueAt(0, i, 5);
                    table.setValueAt(0, i, 6);
                }
                case "20" -> {
                    table.setValueAt(0, i, 4);
                    table.setValueAt(2, i, 5);
                    table.setValueAt(0, i, 6);
                }
                case "200" -> {
                    table.setValueAt(2, i, 4);
                    table.setValueAt(0, i, 5);
                    table.setValueAt(0, i, 6);
                }
                case "2" -> {
                    table.setValueAt(0, i, 4);
                    table.setValueAt(0, i, 5);
                    table.setValueAt(2, i, 6);
                }
            }
        }
        table.setValueAt(Game.hundreds.number, 0, 0);
        table.setValueAt(Game.tens.number, 0, 1);
        table.setValueAt(Game.ones.number, 0, 2);
    }

}
