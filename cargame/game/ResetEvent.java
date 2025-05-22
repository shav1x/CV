package p02.game;

import java.util.*;

public class ResetEvent  {

    public interface ResetEventListener {
        void resetEventOccured();
    }

    private List<ResetEventListener> listeners = new ArrayList<>();

    public void addResetEventListener(ResetEventListener listener) {
        listeners.add(listener);
    }

    public void removeResetEventListener(ResetEvent listener) {
        listeners.remove(listener);
    }

    public void fireResetEvent() {
        for (ResetEventListener listener : listeners)
            listener.resetEventOccured();
    }

}
