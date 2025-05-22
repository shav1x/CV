package p02.game;

import java.util.*;

public class StartEvent {

    public interface StartEventListener {
        void startEventOccurred();
    }

    private List<StartEventListener> listeners = new ArrayList<>();

    public void addStartEventListener(StartEventListener listener) {
        listeners.add(listener);
    }

    public void removeStartEventListener(StartEventListener listener) {
        listeners.remove(listener);
    }

    public void fireStartEvent() {
        for (StartEventListener listener : listeners)
            listener.startEventOccurred();
    }

}
