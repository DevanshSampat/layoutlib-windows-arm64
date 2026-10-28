import java.lang.reflect.Method;
import java.lang.reflect.Field;
import java.util.HashMap;

public class TestBridgeInit {
    public static void main(String[] args) {
        try {
            System.out.println("Java os.arch: " + System.getProperty("os.arch"));
            String libDir = "C:\\Users\\ASUS\\.gemini\\antigravity\\scratch\\android-studio-dist\\android-studio\\plugins\\design-tools\\resources\\layoutlib\\data\\win\\lib64";
            
            Class<?> bridgeClass = Class.forName("com.android.layoutlib.bridge.Bridge");
            System.out.println("Bridge class found: " + bridgeClass);
            
            // Set sPlatformProperties, sKeyboardPaths, sHyphenDataDir
            for (Field f : bridgeClass.getDeclaredFields()) {
                f.setAccessible(true);
                if (f.getName().equals("sPlatformProperties")) {
                    f.set(null, new HashMap<String, String>());
                } else if (f.getName().equals("sKeyboardPaths")) {
                    f.set(null, new String[0]);
                } else if (f.getName().equals("sHyphenDataDir")) {
                    f.set(null, "");
                }
            }
            System.out.println("Initialized Bridge static fields");

            Method loadNative = bridgeClass.getDeclaredMethod("loadNativeLibraries", String.class);
            loadNative.setAccessible(true);
            System.out.println("Invoking loadNativeLibraries with: " + libDir);
            loadNative.invoke(null, libDir);
            System.out.println("=================================================================");
            System.out.println(">>> SUCCESS: NATIVE LAYOUTLIB INITIALIZED SUCCESSFULLY IN JAVA! <<<");
            System.out.println("=================================================================");

        } catch (Throwable t) {
            t.printStackTrace();
        }
    }
}
