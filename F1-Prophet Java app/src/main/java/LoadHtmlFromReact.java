import org.cef.CefApp;
import org.cef.CefClient;
import org.cef.browser.CefBrowser;
import org.cef.CefSettings;
import me.friwi.jcefmaven.CefAppBuilder;
import me.friwi.jcefmaven.CefInitializationException;
import me.friwi.jcefmaven.UnsupportedPlatformException;

import javax.swing.*;
import java.awt.*;
import java.io.IOException;

public class LoadHtmlFromReact extends JFrame {
    private CefBrowser browser;
    private static CefApp cefApp;

    public LoadHtmlFromReact() {
        setupFrame();
    }

    private void setupFrame() {
        setTitle("F1 Prophet");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        setSize(screenSize.width, screenSize.height);
        setLocation(0, 0);
        setExtendedState(JFrame.MAXIMIZED_BOTH);

        CefClient client = cefApp.createClient();
        browser = client.createBrowser("http://localhost:5173", false, false);

        add(browser.getUIComponent(), BorderLayout.CENTER);
        setVisible(true);
    }

    @Override
    public void dispose() {
        if (browser != null) {
            browser.stopLoad();
        }
        super.dispose();
        if (cefApp != null) {
            cefApp.dispose();
        }
    }

    public static void main(String[] args) {
        try {
            System.out.println("Initializing native Chromium binaries...");
            CefAppBuilder builder = new CefAppBuilder();
            CefSettings settings = builder.getCefSettings();
            settings.windowless_rendering_enabled = false;

            builder.addJcefArgs(
                    "--disable-gpu-sandbox",
                    "--no-sandbox",
                    "--allow-file-access-from-files",
                    "--disable-web-security",
                    "--allow-running-insecure-content",
                    "--enable-gpu",
                    "--allow-file-access-from-files"
            );

            cefApp = builder.build();
            System.out.println("Chromium loaded successfully!");

            SwingUtilities.invokeLater(() -> {
                try {
                    new LoadHtmlFromReact();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });

        } catch (IOException | UnsupportedPlatformException | CefInitializationException | InterruptedException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
