package p02.game;

import java.util.ArrayList;
import java.util.List;

public class PlusOneEvent {

    public interface PlusOneEventListener {
        void plusOneEventOccurred();
    }

    private List<PlusOneEventListener> listeners = new ArrayList<>();

    public void addPlusOneEventListener(PlusOneEventListener listener) {
        listeners.add(listener);
    }

    public void removePlusOneEventListener(PlusOneEventListener listener) {
        listeners.remove(listener);
    }

    public void firePlusOneEvent() {
        for (PlusOneEventListener listener : listeners)
            listener.plusOneEventOccurred();
    }

}
