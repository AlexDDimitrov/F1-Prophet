import javax.swing.*;
import java.awt.*;
import java.awt.geom.Point2D;

public class MainFrame extends JFrame {
    private final Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    private final int WIDTH = screenSize.width;
    private final int HEIGHT = screenSize.height;

    public MainFrame() {
        setFrame();
    }

    void setFrame() {
        this.setTitle("F1 Prophet");
        this.setSize(screenSize);
        this.setLocation(0, 0);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        this.setContentPane(new GradientPanel());

        this.setVisible(true);

        JPanel testPanel = new JPanel();
        String labelText = "<html>"
                + "<div style='width: 900px; background: #0a0a0a; color: #ffffff; text-align: center; padding: 32px; font-family: sans-serif;'>"
                + "<h1 style='margin: 0 0 32px 0;'>"

                + "<span style='font-size: 48px; font-weight: 900; color: #d30700; letter-spacing: 4px;'>"
                + "F1 Prophet"
                + "</span>"
                + "<br>"

                + "<div style='display: inline-block; font-size: 24px; font-weight: 700; color: #ffffff; "
                + "letter-spacing: 6px; border-top: 3px solid #d30700; border-bottom: 3px solid #d30700; "
                + "padding: 16px 0; margin-top: 16px;'>"
                + "Race and Win"
                + "</div>"
                + "</h1>"

                + "<p style='font-size: 16px; color: #cccccc; margin: 0;'>"
                + "Predict results before qualifying and score points."
                + "</p>"
                + "</div>"
                + "</html>";

        JLabel textLabel = new JLabel(labelText);
        testPanel.add(textLabel);
        testPanel.setVisible(true);

        testPanel.setBorder(BorderFactory.createEmptyBorder());
        testPanel.setOpaque(true);
        testPanel.setBackground(Color.decode("#0a0a0a"));

        this.add(testPanel);
    }

    private class GradientPanel extends JPanel {
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2d = (Graphics2D) g;

            g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

            Point2D start = new Point2D.Float(0, 0);
            Point2D end = new Point2D.Float(WIDTH, HEIGHT);

            float[] fractions = {0.0f, 1.0f};
            Color[] colors = {Color.decode("#1a1a1a"), Color.decode("#0a0a0a")};

            LinearGradientPaint paint = new LinearGradientPaint(start, end, fractions, colors);

            g2d.setPaint(paint);
            g2d.fillRect(0, 0, getWidth(), getHeight());
        }
    }
}
