package p02.game;

import java.util.*;

public class TickEvent {

    public interface TickEventListener {
        void tickEventOccurred();
    }

    private List<TickEventListener> listeners = new ArrayList<>();

    public void addTickEventListener(TickEventListener listener) {
        listeners.add(listener);
    }

    public void removeTickEventListener(TickEventListener listener) {
        listeners.remove(listener);
    }

    public void fireTickEvent() {
        for (TickEventListener listener : listeners)
            listener.tickEventOccurred();
    }

}
